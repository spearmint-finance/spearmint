"""Data import service for Excel files."""

import logging
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
import pandas as pd

logger = logging.getLogger(__name__)
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from ..database.models import (
    Transaction, Category,
    Tag, TransactionTag, ImportHistory, ImportProfile, Account, AccountBalance
)
from ..utils.validators import DataValidator, DuplicateDetector, ValidationError


class ImportResult:
    """Result of an import operation."""

    def __init__(self):
        self.total_rows: int = 0
        self.successful_rows: int = 0
        self.failed_rows: int = 0
        self.classified_rows: int = 0
        self.skipped_duplicates: int = 0
        self.accounts_created: int = 0
        self.accounts_skipped: int = 0
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[str] = []

    def add_error(self, row_number: int, field: str, message: str, value: Any = None):
        """Add an error to the result."""
        self.errors.append({
            'row': row_number,
            'field': field,
            'message': message,
            'value': value
        })
        self.failed_rows += 1

    def add_warning(self, message: str):
        """Add a warning to the result."""
        self.warnings.append(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'total_rows': self.total_rows,
            'successful_rows': self.successful_rows,
            'failed_rows': self.failed_rows,
            'classified_rows': self.classified_rows,
            'skipped_duplicates': self.skipped_duplicates,
            'accounts_created': self.accounts_created,
            'accounts_skipped': self.accounts_skipped,
            'errors': self.errors,
            'warnings': self.warnings,
            'success_rate': (self.successful_rows / self.total_rows * 100) if self.total_rows > 0 else 0
        }


class ImportService:
    """Service for importing transaction data from Excel files."""

    # Mapping from Tiller/aggregator account types to Spearmint account types
    TILLER_TYPE_MAP = {
        'credit': 'credit_card',
        'individual': 'brokerage',
        'joint_tenants_with_rights_of_survivorship_jtwros': 'brokerage',
        'uniform_transfer_to_minors_act_utma': 'brokerage',
        'educational_savings_plan_529': 'investment',
        'ira': 'ira',
        'roth_ira': 'ira',
        '401k': '401k',
        '403b': '401k',
        'checking': 'checking',
        'savings': 'savings',
        'money_market': 'savings',
        'cd': 'savings',
        'brokerage': 'brokerage',
    }

    # Expected column mappings (case-insensitive)
    COLUMN_MAPPINGS = {
        'date': ['date', 'transaction date', 'trans_date', 'transaction_date', 'post date', 'posting date', 'posted date', 'date added', 'month'],
        'amount': ['amount', 'value', 'transaction_amount', 'transaction amount'],
        'type': ['type', 'transaction_type', 'trans_type'],  # Optional - will derive from amount if missing
        'category': ['category', 'category_name'],
        'source': ['source', 'account', 'from_account'],
        'description': ['full description', 'description', 'desc', 'memo'],  # Prioritize 'full description'
        'payment_method': ['payment_method', 'payment', 'method', 'institution'],  # Added 'institution'
        'tags': ['tags', 'tag'],
        'include_in_analysis': ['include_in_analysis', 'include', 'analyze'],
        # Additional metadata fields (stored in notes)
        'transaction_id_external': ['transaction id', 'transaction_id', 'trans_id', 'external_id'],
        'account_id_external': ['account id', 'account_id', 'acct_id'],
        'account_number': ['account #', 'account_number', 'acct_number', 'acct_num'],
        'date_added': ['date added', 'date_added', 'added_date'],
        'categorized_date': ['categorized date', 'categorized_date', 'cat_date'],
    }
    
    def __init__(self, db: Session):
        """
        Initialize import service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.validator = DataValidator()
        self.duplicate_detector = DuplicateDetector()
    
    def import_from_excel(
        self,
        file_path: str,
        mode: str = 'incremental',
        skip_duplicates: bool = True,
        profile_id: Optional[int] = None
    ) -> ImportResult:
        """
        Import transactions from Excel file.

        Args:
            file_path: Path to Excel file
            mode: Import mode ('full', 'incremental', 'update')
            skip_duplicates: Whether to skip duplicate transactions
            profile_id: Optional import profile ID to apply saved mappings

        Returns:
            ImportResult: Result of the import operation
        """
        result = ImportResult()

        try:
            # Validate import mode
            mode = self.validator.validate_import_mode(mode)

            # Load import profile if specified
            profile = None
            if profile_id:
                profile = self.get_profile(profile_id)
                if not profile:
                    result.add_warning(f"Import profile {profile_id} not found, using default mappings")

            # Process Accounts sheet if present (auto-create accounts)
            account_name_to_id = self._process_accounts_sheet(file_path, result)

            # Read Excel file (with optional skip_rows from profile)
            skip_rows = profile.skip_rows if profile else 0
            df = self._read_excel_file(file_path, skip_rows=skip_rows)
            result.total_rows = len(df)

            # Normalize column names (use profile mappings if available)
            df = self._normalize_columns(df, profile=profile)

            # Handle import mode
            if mode == 'full':
                self._clear_existing_data()
            
            # Get existing duplicate keys if needed
            existing_keys = set()
            if skip_duplicates:
                existing_keys = self._get_existing_duplicate_keys()
            
            # Get or create categories
            category_cache = self._build_category_cache()
            tag_cache = {}
            
            # Process each row
            for idx, row in df.iterrows():
                row_number = idx + 2  # +2 for header and 0-based index
                
                try:
                    # Validate and parse row
                    transaction_data = self._validate_row(row, row_number, result)
                    if transaction_data is None:
                        continue  # Validation failed, error already logged
                    
                    # Check for duplicates
                    if skip_duplicates:
                        dup_key = self.duplicate_detector.generate_duplicate_key(
                            transaction_data['transaction_date'],
                            transaction_data['amount'],
                            transaction_data.get('description')
                        )
                        if self.duplicate_detector.is_duplicate(dup_key, existing_keys):
                            result.skipped_duplicates += 1
                            result.add_warning(f"Row {row_number}: Skipped duplicate transaction")
                            continue
                        existing_keys.add(dup_key)
                    
                    # Get or create category
                    category_name = transaction_data.pop('category_name')
                    category = self._get_or_create_category(
                        category_name,
                        transaction_data['transaction_type'],
                        category_cache
                    )
                    transaction_data['category_id'] = category.category_id

                    # Check if this is a transfer transaction
                    if category.category_type == 'Transfer':
                        transaction_data['include_in_analysis'] = False

                    # Extract tags
                    tags = transaction_data.pop('tags', [])

                    # Link transaction to account if we have a mapping
                    # Try the raw 'Account' column first (exact account name),
                    # then fall back to the mapped 'source' field
                    if account_name_to_id:
                        acct_name = None
                        raw_acct = row.get('Account') if 'Account' in df.columns else None
                        if raw_acct is None:
                            raw_acct = row.get('account') if 'account' in df.columns else None
                        if raw_acct and not pd.isna(raw_acct):
                            acct_name = str(raw_acct).strip()
                        elif transaction_data.get('source'):
                            acct_name = transaction_data['source']

                        if acct_name and acct_name in account_name_to_id:
                            transaction_data['account_id'] = account_name_to_id[acct_name]

                    # Create transaction
                    transaction = Transaction(**transaction_data)
                    self.db.add(transaction)
                    self.db.flush()  # Get transaction_id
                    
                    # Add tags
                    if tags:
                        self._add_tags_to_transaction(transaction, tags, tag_cache)
                    
                    result.successful_rows += 1
                    
                except ValidationError as e:
                    result.add_error(row_number, 'validation', str(e))
                except Exception as e:
                    result.add_error(row_number, 'unknown', f"Unexpected error: {str(e)}")
            
            # Commit all changes
            self.db.commit()
            
            # Record import history
            self._record_import_history(file_path, mode, result)
            
        except OperationalError as e:
            self.db.rollback()
            logger.error("Database error during import: %s", e)
            result.add_error(0, 'database', "Database is not properly initialized. Please contact support or restart the application.")
        except Exception as e:
            self.db.rollback()
            logger.error("Unexpected error during import: %s", e)
            result.add_error(0, 'file', f"Failed to import file: {str(e)}")

        return result
    
    def _read_excel_file(self, file_path: str, skip_rows: int = 0) -> pd.DataFrame:
        """Read Excel file into DataFrame.

        Args:
            file_path: Path to Excel file
            skip_rows: Number of rows to skip at the beginning (from profile)
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.suffix.lower() in ['.xlsx', '.xls']:
            raise ValueError(f"Invalid file format. Expected .xlsx or .xls, got {path.suffix}")

        # Use context manager to ensure file is properly closed
        with pd.ExcelFile(file_path) as xl_file:
            sheet_names = xl_file.sheet_names
            logger.debug("Available sheets: %s", sheet_names)

            # Try to find 'transactions' or 'import' sheet first
            sheet_to_use = None
            for sheet in sheet_names:
                sheet_lower = sheet.lower().strip()
                if sheet_lower in ['transactions', 'import', 'transaction']:
                    sheet_to_use = sheet
                    logger.debug("Found data sheet: '%s'", sheet)
                    break

            # Default to first sheet if no recognized sheet found
            if sheet_to_use is None:
                sheet_to_use = 0
                logger.debug("No recognized sheet found, using first sheet")

            logger.debug("Using sheet: '%s'", sheet_to_use)

            # Read the selected sheet (with optional row skip)
            df = pd.read_excel(xl_file, sheet_name=sheet_to_use, skiprows=skip_rows if skip_rows > 0 else None)

        # Debug: Print column info (will appear in logs)
        logger.debug("Read Excel with %d rows and %d columns", len(df), len(df.columns))
        logger.debug("Columns found: %s", list(df.columns))

        return df

    def _normalize_columns(self, df: pd.DataFrame, profile: Optional[ImportProfile] = None) -> pd.DataFrame:
        """Normalize column names to standard format.

        Args:
            df: DataFrame with original column names
            profile: Optional import profile with custom column mappings
        """
        column_map = {}
        df_columns_lower = {col.lower().strip(): col for col in df.columns}

        logger.debug("Lowercase columns: %s", list(df_columns_lower.keys()))

        # If profile has custom mappings, apply them first
        if profile and profile.column_mappings:
            logger.debug("Applying profile '%s' mappings", profile.name)
            for source_col, target_field in profile.column_mappings.items():
                source_lower = source_col.lower().strip()
                if source_lower in df_columns_lower:
                    column_map[df_columns_lower[source_lower]] = target_field
                    logger.debug("Profile mapped '%s' -> '%s'", df_columns_lower[source_lower], target_field)

        # Apply default mappings for any unmapped columns
        for standard_name, variations in self.COLUMN_MAPPINGS.items():
            # Skip if already mapped by profile
            if standard_name in column_map.values():
                continue
            for variation in variations:
                if variation in df_columns_lower and df_columns_lower[variation] not in column_map:
                    column_map[df_columns_lower[variation]] = standard_name
                    logger.debug("Default mapped '%s' -> '%s'", df_columns_lower[variation], standard_name)
                    break

        logger.debug("Final column mapping: %s", column_map)
        return df.rename(columns=column_map)
    
    def _validate_row(
        self,
        row: pd.Series,
        row_number: int,
        result: ImportResult
    ) -> Optional[Dict[str, Any]]:
        """Validate a single row and return transaction data."""
        try:
            # Required fields
            transaction_date = self.validator.validate_date(row.get('date'), 'Date')
            amount = self.validator.validate_amount(row.get('amount'), 'Amount')

            # Transaction type - derive from amount if not provided
            type_value = row.get('type')
            if pd.isna(type_value) or type_value is None or str(type_value).strip() == '':
                # Derive from amount: negative = Expense, positive = Income
                transaction_type = 'Expense' if float(amount) < 0 else 'Income'
            else:
                transaction_type = self.validator.validate_transaction_type(type_value, 'Type')

            category_name = self.validator.validate_category(row.get('category'), 'Category')

            # Optional fields
            source = self.validator.validate_optional_string(row.get('source'), 'Source', 255)
            description = self.validator.validate_optional_string(row.get('description'), 'Description')
            payment_method = self.validator.validate_optional_string(row.get('payment_method'), 'Payment Method', 50)
            include_in_analysis = self.validator.validate_boolean(row.get('include_in_analysis'), 'Include in Analysis', True)

            # Parse tags
            tags = self.validator.validate_tags(row.get('tags'))

            # Collect metadata fields for notes
            metadata = {}
            if not pd.isna(row.get('transaction_id_external')):
                metadata['external_transaction_id'] = str(row.get('transaction_id_external'))
            if not pd.isna(row.get('account_id_external')):
                metadata['external_account_id'] = str(row.get('account_id_external'))
            if not pd.isna(row.get('account_number')):
                metadata['account_number'] = str(row.get('account_number'))
            if not pd.isna(row.get('date_added')):
                metadata['date_added'] = str(row.get('date_added'))
            if not pd.isna(row.get('categorized_date')):
                metadata['categorized_date'] = str(row.get('categorized_date'))

            # Build notes field with metadata
            notes_parts = []
            if metadata:
                import json
                notes_parts.append(f"Metadata: {json.dumps(metadata)}")

            notes = '\n'.join(notes_parts) if notes_parts else None

            # Ensure amount sign matches transaction type
            # Expenses should always be negative, Income always positive
            if transaction_type == 'Expense' and float(amount) > 0:
                amount = -abs(float(amount))
            elif transaction_type == 'Income' and float(amount) < 0:
                amount = abs(float(amount))

            return {
                'transaction_date': transaction_date,
                'amount': amount,
                'transaction_type': transaction_type,
                'category_name': category_name,
                'source': source,
                'description': description,
                'payment_method': payment_method,
                'include_in_analysis': include_in_analysis,
                'notes': notes,
                'tags': tags
            }

        except ValidationError as e:
            result.add_error(row_number, 'validation', str(e))
            return None
    
    def _clear_existing_data(self):
        """Clear existing transaction data (for full import mode)."""
        self.db.query(TransactionTag).delete()
        self.db.query(Transaction).delete()
        self.db.commit()
    
    def _get_existing_duplicate_keys(self) -> set[str]:
        """Get duplicate detection keys for existing transactions."""
        transactions = self.db.query(Transaction).all()
        keys = set()
        for tx in transactions:
            key = self.duplicate_detector.generate_duplicate_key(
                tx.transaction_date,
                tx.amount,
                tx.description
            )
            keys.add(key)
        return keys
    
    def _build_category_cache(self) -> Dict[str, Category]:
        """Build cache of existing categories."""
        categories = self.db.query(Category).all()
        return {cat.category_name: cat for cat in categories}
    
    def _get_or_create_category(
        self,
        category_name: str,
        transaction_type: str,
        cache: Dict[str, Category]
    ) -> Category:
        """Get existing category or create new one."""
        # Check if this is a transfer category (case-insensitive)
        is_transfer = category_name.lower() == 'transfer'

        if category_name in cache:
            category = cache[category_name]
            # Update existing category if it's a transfer but not marked as such
            if is_transfer and category.category_type != 'Transfer':
                category.category_type = 'Transfer'
                self.db.flush()
            return category

        # Create new category
        category = Category(
            category_name=category_name,
            category_type='Transfer' if is_transfer else transaction_type,
        )
        self.db.add(category)
        self.db.flush()
        cache[category_name] = category
        return category
    
    def _add_tags_to_transaction(
        self,
        transaction: Transaction,
        tag_names: List[str],
        tag_cache: Dict[str, Tag]
    ):
        """Add tags to transaction."""
        for tag_name in tag_names:
            # Get or create tag
            if tag_name not in tag_cache:
                tag = self.db.query(Tag).filter(Tag.tag_name == tag_name).first()
                if not tag:
                    tag = Tag(tag_name=tag_name)
                    self.db.add(tag)
                    self.db.flush()
                tag_cache[tag_name] = tag
            else:
                tag = tag_cache[tag_name]
            
            # Create association
            tx_tag = TransactionTag(
                transaction_id=transaction.transaction_id,
                tag_id=tag.tag_id
            )
            self.db.add(tx_tag)
    
    def _record_import_history(
        self,
        file_path: str,
        mode: str,
        result: ImportResult
    ):
        """Record import operation in history."""
        import_record = ImportHistory(
            file_name=Path(file_path).name,
            file_path=file_path,
            total_rows=result.total_rows,
            successful_rows=result.successful_rows,
            failed_rows=result.failed_rows,
            classified_rows=result.classified_rows,
            import_mode=mode,
            error_log=str(result.errors) if result.errors else None
        )
        self.db.add(import_record)
        self.db.commit()

    # ==================== Account Import Methods ====================

    def _process_accounts_sheet(
        self,
        file_path: str,
        result: ImportResult
    ) -> Dict[str, int]:
        """Process the Accounts sheet from a Tiller-style XLSX and create Account records.

        Args:
            file_path: Path to Excel file
            result: ImportResult to update with account stats

        Returns:
            Dict mapping account name to account_id for transaction linking
        """
        account_name_to_id: Dict[str, int] = {}

        try:
            with pd.ExcelFile(file_path) as xl_file:
                sheet_names_lower = {s.lower().strip(): s for s in xl_file.sheet_names}

                if 'accounts' not in sheet_names_lower:
                    logger.debug("No 'Accounts' sheet found, skipping account creation")
                    return account_name_to_id

                accounts_sheet = sheet_names_lower['accounts']
                df = pd.read_excel(xl_file, sheet_name=accounts_sheet)

        except Exception as e:
            logger.warning("Failed to read Accounts sheet: %s", e)
            result.add_warning(f"Could not read Accounts sheet: {e}")
            return account_name_to_id

        # Normalize column names for lookup
        col_map = {col.lower().strip(): col for col in df.columns}
        logger.debug("Accounts sheet columns (normalized): %s", list(col_map.keys()))

        # Identify key columns — Tiller uses 'Account.1' for the clean name
        # (the first 'Account' column is for overrides)
        acct_name_col = col_map.get('account.1') or col_map.get('account')
        acct_num_col = col_map.get('account #') or col_map.get('account_number')
        balance_col = col_map.get('last balance') or col_map.get('balance')
        institution_col = col_map.get('institution')
        type_col = col_map.get('type')
        class_col = col_map.get('class')
        acct_id_ext_col = col_map.get('account id') or col_map.get('account_id')

        if not acct_name_col:
            logger.debug("No account name column found in Accounts sheet")
            result.add_warning("Accounts sheet missing account name column")
            return account_name_to_id

        # Build a set of existing account names + last4 for duplicate detection
        existing_accounts = self.db.query(Account).all()
        existing_keys = set()
        for acct in existing_accounts:
            key = (acct.account_name, acct.account_number_last4 or '')
            existing_keys.add(key)
            account_name_to_id[acct.account_name] = acct.account_id

        for idx, row in df.iterrows():
            try:
                name = row.get(acct_name_col)
                if pd.isna(name) or not str(name).strip():
                    continue

                name = str(name).strip()
                last4 = str(row.get(acct_num_col, '')).strip() if acct_num_col and not pd.isna(row.get(acct_num_col)) else ''
                # Clean last4 — keep only last 4 chars if longer
                if len(last4) > 4:
                    last4 = last4[-4:]

                # Skip if already exists
                if (name, last4) in existing_keys:
                    account_name_to_id.setdefault(name, None)
                    # Find the existing account_id
                    for acct in existing_accounts:
                        if acct.account_name == name and (acct.account_number_last4 or '') == last4:
                            account_name_to_id[name] = acct.account_id
                            break
                    result.accounts_skipped += 1
                    continue

                # Determine account type
                tiller_type = str(row.get(type_col, '')).strip().lower() if type_col and not pd.isna(row.get(type_col)) else ''
                acct_class = str(row.get(class_col, '')).strip().lower() if class_col and not pd.isna(row.get(class_col)) else ''
                account_type = self._map_tiller_type(tiller_type, acct_class)

                # Parse balance
                balance = Decimal('0')
                if balance_col and not pd.isna(row.get(balance_col)):
                    try:
                        balance = Decimal(str(row.get(balance_col)))
                    except Exception:
                        pass

                # Institution
                institution = None
                if institution_col and not pd.isna(row.get(institution_col)):
                    institution = str(row.get(institution_col)).strip()

                # Account subtype (preserve original Tiller type)
                subtype = str(row.get(type_col, '')).strip() if type_col and not pd.isna(row.get(type_col)) else None

                # Determine capabilities
                has_cash = account_type in ['checking', 'savings', 'brokerage']
                has_investments = account_type in ['brokerage', 'investment', '401k', 'ira']

                account = Account(
                    account_name=name,
                    account_type=account_type,
                    account_subtype=subtype,
                    institution_name=institution,
                    account_number_last4=last4 if last4 else None,
                    currency='USD',
                    has_cash_component=has_cash,
                    has_investment_component=has_investments,
                    opening_balance=balance,
                    opening_balance_date=datetime.now().date(),
                )
                self.db.add(account)
                self.db.flush()

                account_name_to_id[name] = account.account_id
                existing_keys.add((name, last4))
                result.accounts_created += 1

                # Create balance snapshot
                if balance != 0:
                    bal_snapshot = AccountBalance(
                        account_id=account.account_id,
                        balance_date=datetime.now().date(),
                        total_balance=balance,
                        balance_type='statement',
                    )
                    self.db.add(bal_snapshot)

                logger.debug("Created account: %s (%s) at %s — balance %s",
                             name, account_type, institution, balance)

            except Exception as e:
                logger.warning("Failed to create account from row %d: %s", idx, e)
                result.add_warning(f"Account row {idx}: {e}")

        self.db.flush()
        return account_name_to_id

    def _map_tiller_type(self, tiller_type: str, acct_class: str) -> str:
        """Map a Tiller account type string to a Spearmint account type.

        Args:
            tiller_type: Tiller type (e.g. 'CREDIT', 'INDIVIDUAL')
            acct_class: Tiller class ('asset' or 'liability')

        Returns:
            Spearmint account type string
        """
        # Normalize
        tiller_type = tiller_type.lower().replace(' ', '_')

        if tiller_type in self.TILLER_TYPE_MAP:
            return self.TILLER_TYPE_MAP[tiller_type]

        # Fallback by class
        if acct_class == 'liability':
            return 'credit_card'
        if acct_class == 'asset':
            return 'savings'

        return 'other'

    # ==================== Import Profile Methods ====================

    def get_profiles(self, is_active: Optional[bool] = None) -> List[ImportProfile]:
        """Get all import profiles with optional filtering.

        Args:
            is_active: Filter by active status

        Returns:
            List of import profiles
        """
        query = self.db.query(ImportProfile)
        if is_active is not None:
            query = query.filter(ImportProfile.is_active == is_active)
        return query.order_by(ImportProfile.name).all()

    def get_profile(self, profile_id: int) -> Optional[ImportProfile]:
        """Get a single import profile by ID.

        Args:
            profile_id: Profile ID

        Returns:
            ImportProfile or None if not found
        """
        return self.db.query(ImportProfile).filter(
            ImportProfile.profile_id == profile_id
        ).first()

    def create_profile(
        self,
        name: str,
        column_mappings: Dict[str, str],
        account_id: Optional[int] = None,
        date_format: Optional[str] = None,
        skip_rows: int = 0
    ) -> ImportProfile:
        """Create a new import profile.

        Args:
            name: Profile name
            column_mappings: Dictionary mapping source columns to standard fields
            account_id: Optional associated account ID
            date_format: Optional date format string
            skip_rows: Number of header rows to skip

        Returns:
            Created ImportProfile
        """
        # Validate account exists if specified
        if account_id:
            account = self.db.query(Account).filter(Account.account_id == account_id).first()
            if not account:
                raise ValueError(f"Account {account_id} not found")

        profile = ImportProfile(
            name=name,
            account_id=account_id,
            column_mappings=column_mappings,
            date_format=date_format,
            skip_rows=skip_rows,
            is_active=True
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update_profile(
        self,
        profile_id: int,
        **kwargs
    ) -> Optional[ImportProfile]:
        """Update an import profile.

        Args:
            profile_id: Profile ID
            **kwargs: Fields to update

        Returns:
            Updated ImportProfile or None if not found
        """
        profile = self.get_profile(profile_id)
        if not profile:
            return None

        # Validate account if being updated
        if 'account_id' in kwargs and kwargs['account_id']:
            account = self.db.query(Account).filter(Account.account_id == kwargs['account_id']).first()
            if not account:
                raise ValueError(f"Account {kwargs['account_id']} not found")

        for key, value in kwargs.items():
            if hasattr(profile, key) and value is not None:
                setattr(profile, key, value)

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete_profile(self, profile_id: int) -> bool:
        """Delete an import profile.

        Args:
            profile_id: Profile ID

        Returns:
            True if deleted, False if not found
        """
        profile = self.get_profile(profile_id)
        if not profile:
            return False

        self.db.delete(profile)
        self.db.commit()
        return True

    def suggest_profiles(self, file_columns: List[str]) -> List[Dict[str, Any]]:
        """Suggest matching import profiles based on file columns.

        Args:
            file_columns: List of column names from the file

        Returns:
            List of profile suggestions with match scores
        """
        profiles = self.get_profiles(is_active=True)
        suggestions = []

        file_columns_lower = {col.lower().strip() for col in file_columns}

        for profile in profiles:
            if not profile.column_mappings:
                continue

            # Calculate match score
            profile_columns = {col.lower().strip() for col in profile.column_mappings.keys()}
            matched_columns = profile_columns.intersection(file_columns_lower)

            if matched_columns:
                match_score = (len(matched_columns) / len(profile_columns)) * 100
                suggestions.append({
                    'profile_id': profile.profile_id,
                    'name': profile.name,
                    'match_score': round(match_score, 1),
                    'matched_columns': list(matched_columns)
                })

        # Sort by match score descending
        suggestions.sort(key=lambda x: x['match_score'], reverse=True)
        return suggestions

