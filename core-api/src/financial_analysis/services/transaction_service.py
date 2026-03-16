"""Transaction CRUD service."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from ..database.models import (
    Transaction, Category, TransactionClassification,
    Tag, TransactionTag
)
from ..utils.validators import DataValidator, ValidationError
from .classification_service import ClassificationService


class TransactionFilter:
    """Filter criteria for transaction queries."""

    def __init__(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[str] = None,
        category_id: Optional[int] = None,
        classification_id: Optional[int] = None,
        include_in_analysis: Optional[bool] = None,
        is_transfer: Optional[bool] = None,
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None,
        search_text: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        exclude_classification_ids: Optional[List[int]] = None,
        account_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = 'transaction_date',
        sort_order: str = 'desc'
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.transaction_type = transaction_type
        self.category_id = category_id
        self.classification_id = classification_id
        self.include_in_analysis = include_in_analysis
        self.is_transfer = is_transfer
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.search_text = search_text
        self.tag_ids = tag_ids or []
        self.exclude_classification_ids = exclude_classification_ids or []
        self.account_id = account_id
        self.limit = limit
        self.offset = offset
        self.sort_by = sort_by
        self.sort_order = sort_order


class TransactionService:
    """Service for transaction CRUD operations."""

    def __init__(self, db: Session):
        """
        Initialize transaction service.

        Args:
            db: Database session
        """
        self.db = db
        self.validator = DataValidator()

    def create_transaction(
        self,
        transaction_date: date,
        amount: Decimal,
        transaction_type: str,
        category_id: int,
        source: Optional[str] = None,
        description: Optional[str] = None,
        payment_method: Optional[str] = None,
        classification_id: Optional[int] = None,
        include_in_analysis: bool = True,
        is_transfer: bool = False,
        transfer_account_from: Optional[str] = None,
        transfer_account_to: Optional[str] = None,
        notes: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        account_id: Optional[int] = None
    ) -> Transaction:
        """
        Create a new transaction.

        Args:
            transaction_date: Date of transaction
            amount: Transaction amount
            transaction_type: 'Income' or 'Expense'
            category_id: Category ID
            source: Source of transaction
            description: Transaction description
            payment_method: Payment method used
            classification_id: Classification ID
            include_in_analysis: Whether to include in analysis
            is_transfer: Whether this is a transfer
            transfer_account_from: Source account for transfers
            transfer_account_to: Destination account for transfers
            notes: Additional notes
            tag_names: List of tag names to associate

        Returns:
            Transaction: Created transaction

        Raises:
            ValidationError: If validation fails
        """
        # Validate inputs
        transaction_date = self.validator.validate_date(transaction_date)
        amount = self.validator.validate_amount(amount)
        transaction_type = self.validator.validate_transaction_type(transaction_type)

        # Verify category exists
        category = self.db.query(Category).filter(Category.category_id == category_id).first()
        if not category:
            raise ValidationError(f"Category with ID {category_id} not found")

        # Verify classification if provided
        if classification_id:
            classification = self.db.query(TransactionClassification).filter(
                TransactionClassification.classification_id == classification_id
            ).first()
            if not classification:
                raise ValidationError(f"Classification with ID {classification_id} not found")

        # Create transaction
        transaction = Transaction(
            transaction_date=transaction_date,
            amount=amount,
            transaction_type=transaction_type,
            category_id=category_id,
            source=source,
            description=description,
            payment_method=payment_method,
            classification_id=classification_id,
            include_in_analysis=include_in_analysis,
            is_transfer=is_transfer,
            transfer_account_from=transfer_account_from,
            transfer_account_to=transfer_account_to,
            notes=notes,
            account_id=account_id
        )

        self.db.add(transaction)
        self.db.flush()  # Get transaction_id

        # Add tags if provided
        if tag_names:
            self._add_tags(transaction, tag_names)

        self.db.commit()
        self.db.refresh(transaction)

        return transaction

    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        """
        Get transaction by ID.

        Args:
            transaction_id: Transaction ID

        Returns:
            Optional[Transaction]: Transaction if found, None otherwise
        """
        return self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()

    def list_transactions(self, filters: Optional[TransactionFilter] = None) -> List[Transaction]:
        """
        List transactions with optional filters.

        Args:
            filters: Filter criteria

        Returns:
            List[Transaction]: List of transactions
        """
        if filters is None:
            filters = TransactionFilter()

        query = self.db.query(Transaction)

        # Join with Category table if we need to search by category name
        if filters.search_text:
            query = query.join(Category, Transaction.category_id == Category.category_id)

        # Apply filters
        conditions = []

        if filters.start_date:
            conditions.append(Transaction.transaction_date >= filters.start_date)

        if filters.end_date:
            conditions.append(Transaction.transaction_date <= filters.end_date)

        if filters.transaction_type:
            conditions.append(Transaction.transaction_type == filters.transaction_type)

        if filters.category_id:
            conditions.append(Transaction.category_id == filters.category_id)

        if filters.classification_id:
            conditions.append(Transaction.classification_id == filters.classification_id)

        if filters.include_in_analysis is not None:
            conditions.append(Transaction.include_in_analysis == filters.include_in_analysis)

        if filters.is_transfer is not None:
            conditions.append(Transaction.is_transfer == filters.is_transfer)

        if filters.account_id:
            conditions.append(Transaction.account_id == filters.account_id)

        if filters.min_amount:
            conditions.append(Transaction.amount >= filters.min_amount)

        if filters.max_amount:
            conditions.append(Transaction.amount <= filters.max_amount)

        if filters.search_text:
            search_pattern = f"%{filters.search_text}%"
            conditions.append(
                or_(
                    Transaction.description.ilike(search_pattern),
                    Transaction.source.ilike(search_pattern),
                    Transaction.notes.ilike(search_pattern),
                    Category.category_name.ilike(search_pattern)
                )
            )

        if filters.exclude_classification_ids:
            conditions.append(
                or_(
                    Transaction.classification_id.is_(None),
                    Transaction.classification_id.notin_(filters.exclude_classification_ids)
                )
            )

        if conditions:
            query = query.filter(and_(*conditions))

        # Apply sorting (allowlist prevents arbitrary attribute access)
        ALLOWED_SORT_COLUMNS = {
            'transaction_date', 'amount', 'description', 'source',
            'transaction_type', 'created_at', 'updated_at',
        }
        sort_field = filters.sort_by if filters.sort_by in ALLOWED_SORT_COLUMNS else 'transaction_date'
        sort_column = getattr(Transaction, sort_field)
        if filters.sort_order == 'asc':
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        # Apply pagination
        query = query.limit(filters.limit).offset(filters.offset)

        results = query.all()

        # Heuristic: infer transfers for common reinvestment cases (e.g., dividend reinvestments)
        # This improves UI labeling without requiring manual reclassification.
        for tx in results:
            if not getattr(tx, "is_transfer", False) and self._looks_like_reinvestment(tx):
                # Mark as transfer for response purposes; do not persist here
                tx.is_transfer = True
                # Exclude from analysis for transfers by convention
                if getattr(tx, "include_in_analysis", True):
                    tx.include_in_analysis = False

        return results

    def update_transaction(
        self,
        transaction_id: int,
        **updates
    ) -> Optional[Transaction]:
        """
        Update transaction.

        Args:
            transaction_id: Transaction ID
            **updates: Fields to update

        Returns:
            Optional[Transaction]: Updated transaction if found, None otherwise

        Raises:
            ValidationError: If validation fails
        """
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return None

        # Validate updates
        if 'transaction_date' in updates:
            updates['transaction_date'] = self.validator.validate_date(updates['transaction_date'])

        if 'amount' in updates:
            updates['amount'] = self.validator.validate_amount(updates['amount'])

        if 'transaction_type' in updates:
            updates['transaction_type'] = self.validator.validate_transaction_type(updates['transaction_type'])

        if 'category_id' in updates:
            category = self.db.query(Category).filter(Category.category_id == updates['category_id']).first()
            if not category:
                raise ValidationError(f"Category with ID {updates['category_id']} not found")

        if 'classification_id' in updates and updates['classification_id']:
            classification = self.db.query(TransactionClassification).filter(
                TransactionClassification.classification_id == updates['classification_id']
            ).first()
            if not classification:
                raise ValidationError(f"Classification with ID {updates['classification_id']} not found")

        # Handle tags separately
        tag_names = updates.pop('tag_names', None)
        # Optional flag to force re-apply rules
        reapply_rules_flag = bool(updates.pop('reapply_rules', False))

        # Track which fields are changing before applying
        changed_fields = set(updates.keys())

        # Update fields
        for key, value in updates.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)

        # Prefer timezone-aware now to satisfy linters
        try:
            from datetime import timezone as _tz
            transaction.updated_at = datetime.now(_tz.utc)
        except Exception:
            # Fallback to naive UTC; acceptable for SQLite dev env
            transaction.updated_at = datetime.now()

        # Update tags if provided
        if tag_names is not None:
            # Remove existing tags
            self.db.query(TransactionTag).filter(
                TransactionTag.transaction_id == transaction_id
            ).delete()
            # Add new tags
            if tag_names:
                self._add_tags(transaction, tag_names)

        self.db.commit()
        self.db.refresh(transaction)

        # Auto re-apply classification rules if relevant fields changed
        affecting_fields = {"description", "amount", "category_id", "source", "payment_method", "is_transfer"}
        should_reapply = reapply_rules_flag or (bool(changed_fields & affecting_fields) and (transaction.classification_id is None))
        if should_reapply:
            try:
                cls_service = ClassificationService(self.db)
                changed = cls_service.auto_classify_transaction(transaction)
                if changed:
                    # Ensure derived flags are persisted
                    self.db.commit()
                    self.db.refresh(transaction)
            except Exception:
                # Do not fail the update due to classification errors
                pass

        return transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Delete transaction.

        Args:
            transaction_id: Transaction ID

        Returns:
            bool: True if deleted, False if not found
        """
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return False

        # Delete associated tags
        self.db.query(TransactionTag).filter(
            TransactionTag.transaction_id == transaction_id
        ).delete()

        # Delete transaction
        self.db.delete(transaction)
        self.db.commit()

        return True

    def _add_tags(self, transaction: Transaction, tag_names: List[str]):
        """Add tags to transaction."""
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if not tag_name:
                continue

            # Get or create tag
            tag = self.db.query(Tag).filter(Tag.tag_name == tag_name).first()
            if not tag:
                tag = Tag(tag_name=tag_name)
                self.db.add(tag)
                self.db.flush()

            # Create association
            tx_tag = TransactionTag(
                transaction_id=transaction.transaction_id,
                tag_id=tag.tag_id
            )
            self.db.add(tx_tag)

    def _looks_like_reinvestment(self, tx: Transaction) -> bool:
        """Heuristic check for dividend/stock reinvestment transactions that should be treated as transfers.
        This does not persist changes; it only informs response labeling.
        """
        desc = (getattr(tx, "description", None) or "").lower()
        if not desc:
            return False
        keywords = [
            "reinvest",
            "reinvestment",
            "dividend reinvest",
            "reinvested",
            "re-invest",
        ]
        return any(k in desc for k in keywords)
