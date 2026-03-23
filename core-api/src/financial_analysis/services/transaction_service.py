"""Transaction CRUD service."""

import logging
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, case, exists

logger = logging.getLogger(__name__)

from ..database.models import (
    Transaction, Category,
    Tag, TransactionTag, Account
)
from ..utils.validators import DataValidator, ValidationError


class TransactionFilter:
    """Filter criteria for transaction queries."""

    def __init__(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[str] = None,
        category_id: Optional[int] = None,
        include_in_analysis: Optional[bool] = None,
        is_transfer: Optional[bool] = None,  # deprecated: kept for API compat, uses category join
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None,
        search_text: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        account_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = 'transaction_date',
        sort_order: str = 'desc'
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.transaction_type = transaction_type
        self.category_id = category_id
        self.include_in_analysis = include_in_analysis
        self.is_transfer = is_transfer
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.search_text = search_text
        self.tag_ids = tag_ids or []
        self.account_id = account_id
        self.entity_id = entity_id
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
        include_in_analysis: bool = True,
        transfer_account_from: Optional[str] = None,
        transfer_account_to: Optional[str] = None,
        notes: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        account_id: Optional[int] = None,
        entity_id: Optional[int] = None,
        is_capital_expense: bool = False,
        is_tax_deductible: bool = False,
        is_recurring: bool = False,
        is_reimbursable: bool = False,
        exclude_from_income: bool = False,
        exclude_from_expenses: bool = False,
        splits: Optional[List] = None,
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
            include_in_analysis: Whether to include in analysis
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

        # Auto-inherit entity from account if not explicitly set
        resolved_entity_id = entity_id
        if resolved_entity_id is None and account_id is not None:
            from .account_service import AccountService
            account_svc = AccountService(self.db)
            acct = account_svc.get_account(account_id)
            if acct and len(acct.entities) == 1:
                resolved_entity_id = acct.entities[0].entity_id

        # Create transaction
        transaction = Transaction(
            transaction_date=transaction_date,
            amount=amount,
            transaction_type=transaction_type,
            category_id=category_id,
            source=source,
            description=description,
            payment_method=payment_method,
            include_in_analysis=include_in_analysis,
            transfer_account_from=transfer_account_from,
            transfer_account_to=transfer_account_to,
            notes=notes,
            account_id=account_id,
            entity_id=resolved_entity_id,
            is_capital_expense=is_capital_expense,
            is_tax_deductible=is_tax_deductible,
            is_recurring=is_recurring,
            is_reimbursable=is_reimbursable,
            exclude_from_income=exclude_from_income,
            exclude_from_expenses=exclude_from_expenses,
        )

        self.db.add(transaction)
        self.db.flush()  # Get transaction_id

        # Add splits if provided
        if splits:
            self._validate_split_amounts(splits, amount)
            for s in splits:
                from ..database.models import TransactionSplit
                split = TransactionSplit(
                    transaction_id=transaction.transaction_id,
                    amount=s.amount if hasattr(s, 'amount') else s['amount'],
                    category_id=s.category_id if hasattr(s, 'category_id') else s['category_id'],
                    entity_id=s.entity_id if hasattr(s, 'entity_id') else s.get('entity_id'),
                    description=s.description if hasattr(s, 'description') else s.get('description'),
                    notes=s.notes if hasattr(s, 'notes') else s.get('notes'),
                )
                self.db.add(split)

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

        if filters.include_in_analysis is not None:
            conditions.append(Transaction.include_in_analysis == filters.include_in_analysis)

        if filters.is_transfer is not None:
            # Join Category to filter by category_type
            query = query.join(Category, Transaction.category_id == Category.category_id, isouter=True)
            if filters.is_transfer:
                conditions.append(Category.category_type == 'Transfer')
            else:
                conditions.append(Category.category_type != 'Transfer')

        if filters.account_id:
            conditions.append(Transaction.account_id == filters.account_id)

        if filters.entity_id:
            # Show transactions explicitly assigned to this entity,
            # OR inherited from account (entity_id IS NULL and account belongs to entity),
            # OR that have splits assigned to this entity.
            from ..database.models import account_entities, TransactionSplit
            account_has_entity = exists().where(
                and_(
                    account_entities.c.account_id == Transaction.account_id,
                    account_entities.c.entity_id == filters.entity_id
                )
            )
            split_has_entity = exists().where(
                and_(
                    TransactionSplit.transaction_id == Transaction.transaction_id,
                    TransactionSplit.entity_id == filters.entity_id
                )
            )
            conditions.append(
                or_(
                    Transaction.entity_id == filters.entity_id,
                    and_(
                        Transaction.entity_id.is_(None),
                        account_has_entity
                    ),
                    split_has_entity
                )
            )

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

        if filters.tag_ids:
            query = query.join(
                TransactionTag,
                Transaction.transaction_id == TransactionTag.transaction_id
            ).filter(TransactionTag.tag_id.in_(filters.tag_ids))

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

        return results

    def count_and_summarize(self, filters: Optional[TransactionFilter] = None) -> Dict[str, Any]:
        """
        Get total count and summary stats using SQL aggregation (no row fetching).

        Returns dict with: total, total_income, total_expenses, net_income.
        """
        if filters is None:
            filters = TransactionFilter()

        query = self.db.query(
            func.count(Transaction.transaction_id).label('total'),
            func.coalesce(
                func.sum(case(
                    (Transaction.transaction_type == 'Income', Transaction.amount),
                    else_=0
                )), 0
            ).label('total_income'),
            func.coalesce(
                func.sum(case(
                    (Transaction.transaction_type == 'Expense', func.abs(Transaction.amount)),
                    else_=0
                )), 0
            ).label('total_expenses'),
        )

        if filters.search_text:
            query = query.join(Category, Transaction.category_id == Category.category_id)

        if filters.tag_ids:
            query = query.join(
                TransactionTag,
                Transaction.transaction_id == TransactionTag.transaction_id
            ).filter(TransactionTag.tag_id.in_(filters.tag_ids))

        conditions = []
        if filters.start_date:
            conditions.append(Transaction.transaction_date >= filters.start_date)
        if filters.end_date:
            conditions.append(Transaction.transaction_date <= filters.end_date)
        if filters.transaction_type:
            conditions.append(Transaction.transaction_type == filters.transaction_type)
        if filters.category_id:
            conditions.append(Transaction.category_id == filters.category_id)
        if filters.include_in_analysis is not None:
            conditions.append(Transaction.include_in_analysis == filters.include_in_analysis)
        if filters.is_transfer is not None:
            query = query.join(Category, Transaction.category_id == Category.category_id, isouter=True)
            if filters.is_transfer:
                conditions.append(Category.category_type == 'Transfer')
            else:
                conditions.append(Category.category_type != 'Transfer')
        if filters.account_id:
            conditions.append(Transaction.account_id == filters.account_id)
        if filters.entity_id:
            from ..database.models import account_entities, TransactionSplit
            account_has_entity = exists().where(
                and_(
                    account_entities.c.account_id == Transaction.account_id,
                    account_entities.c.entity_id == filters.entity_id
                )
            )
            split_has_entity = exists().where(
                and_(
                    TransactionSplit.transaction_id == Transaction.transaction_id,
                    TransactionSplit.entity_id == filters.entity_id
                )
            )
            conditions.append(
                or_(
                    Transaction.entity_id == filters.entity_id,
                    and_(
                        Transaction.entity_id.is_(None),
                        account_has_entity
                    ),
                    split_has_entity
                )
            )
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
        if conditions:
            query = query.filter(and_(*conditions))

        result = query.one()
        total_income = float(result.total_income)
        total_expenses = float(result.total_expenses)

        return {
            'total': result.total,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses,
        }

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

        # Handle tags separately
        tag_names = updates.pop('tag_names', None)
        # Handle splits separately
        splits = updates.pop('splits', None)
        # Remove deprecated reapply_rules flag (classification auto-apply removed in Phase 2)
        updates.pop('reapply_rules', None)

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

        # Replace splits if provided (None = no change, [] = remove all)
        if splits is not None:
            if splits:
                # Use updated amount if provided, otherwise use existing
                tx_amount = Decimal(str(updates.get('amount', transaction.amount)))
                self._validate_split_amounts(splits, tx_amount)
            from ..database.models import TransactionSplit
            self.db.query(TransactionSplit).filter(
                TransactionSplit.transaction_id == transaction_id
            ).delete()
            for s in splits:
                split = TransactionSplit(
                    transaction_id=transaction_id,
                    amount=s.amount if hasattr(s, 'amount') else s['amount'],
                    category_id=s.category_id if hasattr(s, 'category_id') else s['category_id'],
                    entity_id=s.entity_id if hasattr(s, 'entity_id') else s.get('entity_id'),
                    description=s.description if hasattr(s, 'description') else s.get('description'),
                    notes=s.notes if hasattr(s, 'notes') else s.get('notes'),
                )
                self.db.add(split)

        self.db.commit()
        self.db.refresh(transaction)

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

    @staticmethod
    def _validate_split_amounts(splits, transaction_amount: Decimal):
        """Validate that split amounts sum to the transaction amount."""
        split_sum = sum(
            Decimal(str(s.amount if hasattr(s, 'amount') else s['amount']))
            for s in splits
        )
        tx_amount = Decimal(str(transaction_amount))
        if abs(split_sum - tx_amount) > Decimal('0.01'):
            raise ValidationError(
                f"Split amounts sum to {split_sum} but transaction amount is {tx_amount}"
            )

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
