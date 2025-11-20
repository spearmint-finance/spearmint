"""Data import service for Excel files."""

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
import pandas as pd
from sqlalchemy.orm import Session

from ..database.models import (
    Transaction, Category, TransactionClassification,
    Tag, TransactionTag, ImportHistory
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
            'errors': self.errors,
            'warnings': self.warnings,
            'success_rate': (self.successful_rows / self.total_rows * 100) if self.total_rows > 0 else 0
        }


class ImportService:
    """Service for importing transaction data from Excel files."""
    
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
        'classification': ['classification', 'class'],
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
        skip_duplicates: bool = True
    ) -> ImportResult:
        """
        Import transactions from Excel file.
        
        Args:
            file_path: Path to Excel file
            mode: Import mode ('full', 'incremental', 'update')
            skip_duplicates: Whether to skip duplicate transactions
            
        Returns:
            ImportResult: Result of the import operation
        """
        result = ImportResult()
        
        try:
            # Validate import mode
            mode = self.validator.validate_import_mode(mode)
            
            # Read Excel file
            df = self._read_excel_file(file_path)
            result.total_rows = len(df)
            
            # Normalize column names
            df = self._normalize_columns(df)
            
            # Handle import mode
            if mode == 'full':
                self._clear_existing_data()
            
            # Get existing duplicate keys if needed
            existing_keys = set()
            if skip_duplicates:
                existing_keys = self._get_existing_duplicate_keys()
            
            # Get or create categories and classifications
            category_cache = self._build_category_cache()
            classification_cache = self._build_classification_cache()
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
                    if category.is_transfer_category:
                        transaction_data['is_transfer'] = True
                        transaction_data['include_in_analysis'] = False

                    # Get classification if specified
                    classification_code = transaction_data.pop('classification_code', None)
                    if classification_code:
                        classification = classification_cache.get(classification_code)
                        if classification:
                            transaction_data['classification_id'] = classification.classification_id
                            result.classified_rows += 1

                    # Extract tags
                    tags = transaction_data.pop('tags', [])

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
            
        except Exception as e:
            self.db.rollback()
            result.add_error(0, 'file', f"Failed to import file: {str(e)}")
        
        return result
    
    def _read_excel_file(self, file_path: str) -> pd.DataFrame:
        """Read Excel file into DataFrame."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.suffix.lower() in ['.xlsx', '.xls']:
            raise ValueError(f"Invalid file format. Expected .xlsx or .xls, got {path.suffix}")

        # Use context manager to ensure file is properly closed
        with pd.ExcelFile(file_path) as xl_file:
            sheet_names = xl_file.sheet_names
            print(f"DEBUG: Available sheets: {sheet_names}")

            # Try to find 'transactions' or 'import' sheet first
            sheet_to_use = None
            for sheet in sheet_names:
                sheet_lower = sheet.lower().strip()
                if sheet_lower in ['transactions', 'import', 'transaction']:
                    sheet_to_use = sheet
                    print(f"DEBUG: Found data sheet: '{sheet}'")
                    break

            # Default to first sheet if no recognized sheet found
            if sheet_to_use is None:
                sheet_to_use = 0
                print(f"DEBUG: No recognized sheet found, using first sheet")

            print(f"DEBUG: Using sheet: '{sheet_to_use}'")

            # Read the selected sheet
            df = pd.read_excel(xl_file, sheet_name=sheet_to_use)

        # Debug: Print column info (will appear in logs)
        print(f"DEBUG: Read Excel with {len(df)} rows and {len(df.columns)} columns")
        print(f"DEBUG: Columns found: {list(df.columns)}")

        return df
    
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to standard format."""
        column_map = {}
        df_columns_lower = {col.lower().strip(): col for col in df.columns}

        print(f"DEBUG: Lowercase columns: {list(df_columns_lower.keys())}")

        for standard_name, variations in self.COLUMN_MAPPINGS.items():
            for variation in variations:
                if variation in df_columns_lower:
                    column_map[df_columns_lower[variation]] = standard_name
                    print(f"DEBUG: Mapped '{df_columns_lower[variation]}' -> '{standard_name}'")
                    break

        print(f"DEBUG: Final column mapping: {column_map}")
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
            classification_code = self.validator.validate_optional_string(row.get('classification'), 'Classification', 20)
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
                'classification_code': classification_code,
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
    
    def _build_classification_cache(self) -> Dict[str, TransactionClassification]:
        """Build cache of existing classifications."""
        classifications = self.db.query(TransactionClassification).all()
        return {cls.classification_code: cls for cls in classifications}
    
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
            if is_transfer and not category.is_transfer_category:
                category.is_transfer_category = True
                self.db.flush()
            return category

        # Create new category
        category = Category(
            category_name=category_name,
            category_type=transaction_type,
            is_transfer_category=is_transfer
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

