"""
Account service for managing financial accounts, balances, and reconciliations.

Handles account CRUD operations, balance tracking, investment holdings,
and reconciliation workflows.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from sqlalchemy import func, and_, or_, desc
from sqlalchemy.orm import Session

from ..database.models import (
    Account, AccountBalance, InvestmentHolding, Reconciliation, Transaction
)


class AccountService:
    """Service for managing financial accounts and related operations."""

    def __init__(self, db: Session):
        """Initialize the account service with a database session."""
        self.db = db

    # ==================== Account Management ====================

    def create_account(
        self,
        account_name: str,
        account_type: str,
        institution_name: Optional[str] = None,
        account_number_last4: Optional[str] = None,
        account_subtype: Optional[str] = None,
        currency: str = 'USD',
        opening_balance: Decimal = Decimal('0'),
        opening_balance_date: Optional[date] = None,
        entity_ids: Optional[List[int]] = None,
        notes: Optional[str] = None
    ) -> Account:
        """
        Create a new financial account.

        Args:
            account_name: Name of the account
            account_type: Type of account (checking, savings, brokerage, etc.)
            institution_name: Name of the financial institution
            account_number_last4: Last 4 digits of account number
            account_subtype: Subtype for specialized accounts
            currency: Currency code (default USD)
            opening_balance: Initial balance
            opening_balance_date: Date of opening balance
            entity_ids: Entity IDs this account belongs to
            notes: Optional notes

        Returns:
            Created Account object
        """
        from ..database.models import Entity

        # Determine account capabilities based on type
        has_cash = account_type in ['checking', 'savings', 'brokerage']
        has_investments = account_type in ['brokerage', 'investment', '401k', 'ira']

        account = Account(
            account_name=account_name,
            account_type=account_type,
            account_subtype=account_subtype,
            institution_name=institution_name,
            account_number_last4=account_number_last4,
            currency=currency,
            has_cash_component=has_cash,
            has_investment_component=has_investments,
            opening_balance=opening_balance,
            opening_balance_date=opening_balance_date or date.today(),
            notes=notes
        )

        # Assign entities
        if entity_ids:
            entities = self.db.query(Entity).filter(
                Entity.entity_id.in_(entity_ids)
            ).all()
            account.entities = entities

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        # Create initial balance record if opening balance is provided
        if opening_balance != 0:
            self.add_balance_snapshot(
                account_id=account.account_id,
                balance_date=opening_balance_date or date.today(),
                total_balance=opening_balance,
                balance_type='statement'
            )

        return account

    def get_account(self, account_id: int) -> Optional[Account]:
        """Get an account by ID."""
        return self.db.query(Account).filter(
            Account.account_id == account_id
        ).first()

    def get_accounts(
        self,
        is_active: Optional[bool] = None,
        account_type: Optional[str] = None,
        entity_id: Optional[int] = None
    ) -> List[Account]:
        """
        Get all accounts with optional filtering.

        Args:
            is_active: Filter by active status
            account_type: Filter by account type
            entity_id: Filter by entity ID

        Returns:
            List of Account objects
        """
        query = self.db.query(Account)

        if is_active is not None:
            query = query.filter(Account.is_active == is_active)

        if account_type:
            query = query.filter(Account.account_type == account_type)

        if entity_id is not None:
            from ..database.models import account_entities
            query = query.join(account_entities).filter(
                account_entities.c.entity_id == entity_id
            )

        return query.order_by(Account.account_name).all()

    def update_account(
        self,
        account_id: int,
        **kwargs
    ) -> Optional[Account]:
        """
        Update an account's properties.

        Args:
            account_id: ID of account to update
            **kwargs: Fields to update

        Returns:
            Updated Account object or None if not found
        """
        account = self.get_account(account_id)
        if not account:
            return None

        # Handle entity_ids separately (many-to-many)
        entity_ids = kwargs.pop('entity_ids', None)
        if entity_ids is not None:
            from ..database.models import Entity
            entities = self.db.query(Entity).filter(
                Entity.entity_id.in_(entity_ids)
            ).all() if entity_ids else []
            account.entities = entities

            # Backfill transactions with NULL entity_id when account has exactly one entity
            if len(entities) == 1:
                self.db.query(Transaction).filter(
                    Transaction.account_id == account_id,
                    Transaction.entity_id.is_(None),
                ).update(
                    {Transaction.entity_id: entities[0].entity_id},
                    synchronize_session='fetch',
                )

        for key, value in kwargs.items():
            if hasattr(account, key):
                setattr(account, key, value)

        self.db.commit()
        self.db.refresh(account)
        return account

    def deactivate_account(self, account_id: int) -> bool:
        """
        Deactivate an account (soft delete).

        Args:
            account_id: ID of account to deactivate

        Returns:
            True if successful, False if account not found
        """
        account = self.get_account(account_id)
        if not account:
            return False

        account.is_active = False
        self.db.commit()
        return True

    # ==================== Balance Management ====================

    def add_balance_snapshot(
        self,
        account_id: int,
        balance_date: date,
        total_balance: Decimal,
        balance_type: str = 'statement',
        cash_balance: Optional[Decimal] = None,
        investment_value: Optional[Decimal] = None,
        notes: Optional[str] = None
    ) -> AccountBalance:
        """
        Add a balance snapshot for an account.

        Args:
            account_id: ID of the account
            balance_date: Date of the balance
            total_balance: Total account value
            balance_type: Type of balance (statement, calculated, reconciled)
            cash_balance: Cash position (for brokerage accounts)
            investment_value: Investment value (for brokerage accounts)
            notes: Optional notes

        Returns:
            Created AccountBalance object
        """
        # Check if balance already exists for this date and type
        existing = self.db.query(AccountBalance).filter(
            AccountBalance.account_id == account_id,
            AccountBalance.balance_date == balance_date,
            AccountBalance.balance_type == balance_type
        ).first()

        if existing:
            # Update existing balance
            existing.total_balance = total_balance
            existing.cash_balance = cash_balance
            existing.investment_value = investment_value
            existing.notes = notes
            balance = existing
        else:
            # Create new balance
            balance = AccountBalance(
                account_id=account_id,
                balance_date=balance_date,
                total_balance=total_balance,
                balance_type=balance_type,
                cash_balance=cash_balance,
                investment_value=investment_value,
                notes=notes
            )
            self.db.add(balance)

        self.db.commit()
        self.db.refresh(balance)
        return balance

    def get_current_balance(self, account_id: int) -> Optional[AccountBalance]:
        """
        Get the most recent balance for an account.

        Args:
            account_id: ID of the account

        Returns:
            Most recent AccountBalance or None
        """
        return self.db.query(AccountBalance).filter(
            AccountBalance.account_id == account_id
        ).order_by(desc(AccountBalance.balance_date)).first()

    def get_balance_history(
        self,
        account_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        balance_type: Optional[str] = None
    ) -> List[AccountBalance]:
        """
        Get balance history for an account.

        Args:
            account_id: ID of the account
            start_date: Start of date range
            end_date: End of date range
            balance_type: Filter by balance type

        Returns:
            List of AccountBalance objects
        """
        query = self.db.query(AccountBalance).filter(
            AccountBalance.account_id == account_id
        )

        if start_date:
            query = query.filter(AccountBalance.balance_date >= start_date)

        if end_date:
            query = query.filter(AccountBalance.balance_date <= end_date)

        if balance_type:
            query = query.filter(AccountBalance.balance_type == balance_type)

        return query.order_by(AccountBalance.balance_date).all()

    def calculate_balance_from_transactions(
        self,
        account_id: int,
        as_of_date: date
    ) -> Dict[str, Decimal]:
        """
        Calculate account balance from transactions.

        Args:
            account_id: ID of the account
            as_of_date: Calculate balance as of this date

        Returns:
            Dictionary with calculated balances
        """
        account = self.get_account(account_id)
        if not account:
            return {'total': Decimal('0')}

        # Get opening balance
        opening_balance = account.opening_balance or Decimal('0')

        # Sum all transactions up to the date
        transaction_sum = self.db.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.account_id == account_id,
            Transaction.transaction_date <= as_of_date
        ).scalar() or Decimal('0')

        total_balance = opening_balance + transaction_sum

        result = {'total': total_balance}

        # For brokerage accounts, calculate cash and investment components
        if account.has_cash_component and account.has_investment_component:
            # Cash-affecting transactions
            cash_sum = self.db.query(
                func.sum(Transaction.amount)
            ).filter(
                Transaction.account_id == account_id,
                Transaction.transaction_date <= as_of_date,
                Transaction.affects_cash_balance == True
            ).scalar() or Decimal('0')

            # Investment value from holdings
            investment_value = self.db.query(
                func.sum(InvestmentHolding.current_value)
            ).filter(
                InvestmentHolding.account_id == account_id,
                InvestmentHolding.as_of_date <= as_of_date
            ).scalar() or Decimal('0')

            result['cash'] = opening_balance + cash_sum
            result['investments'] = investment_value

        return result

    # ==================== Investment Holdings ====================

    def add_holding(
        self,
        account_id: int,
        symbol: str,
        quantity: Decimal,
        as_of_date: date,
        description: Optional[str] = None,
        cost_basis: Optional[Decimal] = None,
        current_value: Optional[Decimal] = None,
        asset_class: Optional[str] = None,
        sector: Optional[str] = None
    ) -> InvestmentHolding:
        """
        Add or update an investment holding.

        Args:
            account_id: ID of the account
            symbol: Security symbol
            quantity: Number of shares/units
            as_of_date: Date of the holding
            description: Security description
            cost_basis: Total cost basis
            current_value: Current market value
            asset_class: Asset classification
            sector: Market sector

        Returns:
            Created or updated InvestmentHolding
        """
        # Check if holding exists for this date
        existing = self.db.query(InvestmentHolding).filter(
            InvestmentHolding.account_id == account_id,
            InvestmentHolding.symbol == symbol,
            InvestmentHolding.as_of_date == as_of_date
        ).first()

        if existing:
            # Update existing holding
            existing.quantity = quantity
            existing.description = description or existing.description
            existing.cost_basis = cost_basis
            existing.current_value = current_value
            existing.asset_class = asset_class or existing.asset_class
            existing.sector = sector or existing.sector
            holding = existing
        else:
            # Create new holding
            holding = InvestmentHolding(
                account_id=account_id,
                symbol=symbol,
                quantity=quantity,
                as_of_date=as_of_date,
                description=description,
                cost_basis=cost_basis,
                current_value=current_value,
                asset_class=asset_class,
                sector=sector
            )
            self.db.add(holding)

        self.db.commit()
        self.db.refresh(holding)
        return holding

    def get_current_holdings(self, account_id: int) -> List[InvestmentHolding]:
        """
        Get current investment holdings for an account.

        Args:
            account_id: ID of the account

        Returns:
            List of current InvestmentHolding objects
        """
        # Get the most recent date for each symbol
        subquery = self.db.query(
            InvestmentHolding.symbol,
            func.max(InvestmentHolding.as_of_date).label('max_date')
        ).filter(
            InvestmentHolding.account_id == account_id
        ).group_by(InvestmentHolding.symbol).subquery()

        # Get holdings for the most recent dates
        holdings = self.db.query(InvestmentHolding).join(
            subquery,
            and_(
                InvestmentHolding.symbol == subquery.c.symbol,
                InvestmentHolding.as_of_date == subquery.c.max_date,
                InvestmentHolding.account_id == account_id
            )
        ).filter(
            InvestmentHolding.quantity > 0  # Only non-zero holdings
        ).all()

        return holdings

    def update_holding(self, holding_id: int, updates: dict) -> Optional[InvestmentHolding]:
        """Update an existing investment holding."""
        holding = self.db.query(InvestmentHolding).filter(
            InvestmentHolding.holding_id == holding_id
        ).first()
        if not holding:
            return None
        for key, value in updates.items():
            if value is not None and hasattr(holding, key):
                setattr(holding, key, value)
        self.db.commit()
        self.db.refresh(holding)
        return holding

    def delete_holding(self, holding_id: int) -> bool:
        """Delete an investment holding by ID."""
        holding = self.db.query(InvestmentHolding).filter(
            InvestmentHolding.holding_id == holding_id
        ).first()
        if not holding:
            return False
        self.db.delete(holding)
        self.db.commit()
        return True

    # ==================== Reconciliation ====================

    def create_reconciliation(
        self,
        account_id: int,
        statement_date: date,
        statement_balance: Decimal,
        statement_cash_balance: Optional[Decimal] = None,
        statement_investment_value: Optional[Decimal] = None,
        notes: Optional[str] = None
    ) -> Reconciliation:
        """
        Create a new reconciliation for an account.

        Args:
            account_id: ID of the account
            statement_date: Date of the statement
            statement_balance: Balance from statement
            statement_cash_balance: Cash balance (for brokerage)
            statement_investment_value: Investment value (for brokerage)
            notes: Optional notes

        Returns:
            Created Reconciliation object
        """
        # Calculate current balance from transactions
        calculated = self.calculate_balance_from_transactions(
            account_id, statement_date
        )

        reconciliation = Reconciliation(
            account_id=account_id,
            statement_date=statement_date,
            statement_balance=statement_balance,
            calculated_balance=calculated['total'],
            statement_cash_balance=statement_cash_balance,
            calculated_cash_balance=calculated.get('cash'),
            statement_investment_value=statement_investment_value,
            calculated_investment_value=calculated.get('investments'),
            discrepancy_amount=statement_balance - calculated['total']
        )

        self.db.add(reconciliation)
        self.db.commit()
        self.db.refresh(reconciliation)
        return reconciliation

    def complete_reconciliation(
        self,
        reconciliation_id: int,
        reconciled_by: Optional[str] = None
    ) -> bool:
        """
        Mark a reconciliation as complete.

        Args:
            reconciliation_id: ID of the reconciliation
            reconciled_by: Name of person reconciling

        Returns:
            True if successful
        """
        reconciliation = self.db.query(Reconciliation).filter(
            Reconciliation.reconciliation_id == reconciliation_id
        ).first()

        if not reconciliation:
            return False

        # Count cleared and uncleared transactions
        account_id = reconciliation.account_id
        cleared_count = self.db.query(func.count(Transaction.transaction_id)).filter(
            Transaction.account_id == account_id,
            Transaction.transaction_date <= reconciliation.statement_date,
            Transaction.is_cleared == True
        ).scalar()

        pending_count = self.db.query(func.count(Transaction.transaction_id)).filter(
            Transaction.account_id == account_id,
            Transaction.transaction_date <= reconciliation.statement_date,
            Transaction.is_cleared == False
        ).scalar()

        reconciliation.is_reconciled = True
        reconciliation.reconciled_at = datetime.utcnow()
        reconciliation.reconciled_by = reconciled_by
        reconciliation.transactions_cleared_count = cleared_count
        reconciliation.transactions_pending_count = pending_count

        # Create a reconciled balance record
        self.add_balance_snapshot(
            account_id=account_id,
            balance_date=reconciliation.statement_date,
            total_balance=reconciliation.statement_balance,
            balance_type='reconciled',
            cash_balance=reconciliation.statement_cash_balance,
            investment_value=reconciliation.statement_investment_value
        )

        self.db.commit()
        return True

    def get_reconciliations(
        self,
        account_id: int,
        is_reconciled: Optional[bool] = None
    ) -> List[Reconciliation]:
        """
        Get reconciliations for an account.

        Args:
            account_id: ID of the account
            is_reconciled: Filter by reconciliation status

        Returns:
            List of Reconciliation objects
        """
        query = self.db.query(Reconciliation).filter(
            Reconciliation.account_id == account_id
        )

        if is_reconciled is not None:
            query = query.filter(Reconciliation.is_reconciled == is_reconciled)

        return query.order_by(desc(Reconciliation.statement_date)).all()

    def clear_transaction(
        self,
        transaction_id: int,
        cleared_date: Optional[date] = None
    ) -> bool:
        """
        Mark a transaction as cleared.

        Args:
            transaction_id: ID of the transaction
            cleared_date: Date cleared (defaults to today)

        Returns:
            True if successful
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()

        if not transaction:
            return False

        transaction.is_cleared = True
        transaction.cleared_date = cleared_date or date.today()
        self.db.commit()
        return True

    def clear_transactions_batch(
        self,
        transaction_ids: List[int],
        cleared_date: Optional[date] = None
    ) -> int:
        """
        Mark multiple transactions as cleared.

        Args:
            transaction_ids: List of transaction IDs
            cleared_date: Date cleared (defaults to today)

        Returns:
            Number of transactions cleared
        """
        count = self.db.query(Transaction).filter(
            Transaction.transaction_id.in_(transaction_ids)
        ).update({
            'is_cleared': True,
            'cleared_date': cleared_date or date.today()
        }, synchronize_session=False)

        self.db.commit()
        return count

    # ==================== Net Worth & Analytics ====================

    def get_net_worth(self, as_of_date: Optional[date] = None, entity_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculate total net worth across all accounts.

        Args:
            as_of_date: Calculate as of this date (defaults to today)
            entity_id: Filter to accounts belonging to this entity

        Returns:
            Dictionary with net worth breakdown
        """
        as_of_date = as_of_date or date.today()

        assets = Decimal('0')
        liabilities = Decimal('0')
        liquid_assets = Decimal('0')
        investments = Decimal('0')

        accounts = self.get_accounts(is_active=True, entity_id=entity_id)

        for account in accounts:
            balance = self.get_current_balance(account.account_id)
            if balance and balance.balance_date <= as_of_date:
                amount = balance.total_balance

                # Categorize by account type
                if account.account_type in ['credit_card', 'loan']:
                    # For credit cards/loans: negative or positive balance = amount owed (liability)
                    # But if balance is negative (credit in your favor), it's an asset
                    if amount < 0:
                        # Credit in your favor (overpayment) - treat as asset
                        assets += abs(amount)
                        liquid_assets += abs(amount)
                    else:
                        # Amount owed - treat as liability
                        liabilities += amount
                else:
                    assets += amount

                    # Categorize into liquid assets or investments
                    if account.account_type in ['checking', 'savings', 'money_market']:
                        liquid_assets += amount
                    elif account.account_type in ['brokerage', 'investment', 'retirement', '401k', 'ira', 'roth_ira', 'hsa']:
                        # Investment-type accounts
                        if account.has_investment_component and balance.investment_value:
                            investments += balance.investment_value
                            if balance.cash_balance:
                                liquid_assets += balance.cash_balance
                        else:
                            # No breakdown available, treat full balance as investment
                            investments += amount
                    elif account.has_investment_component:
                        # Other accounts with investment component
                        if balance.investment_value:
                            investments += balance.investment_value
                        if balance.cash_balance:
                            liquid_assets += balance.cash_balance

        return {
            'assets': assets,
            'liabilities': liabilities,
            'net_worth': assets - liabilities,
            'liquid_assets': liquid_assets,
            'investments': investments,
            'as_of_date': as_of_date
        }

    def get_account_summary(self, entity_id: int = None) -> List[Dict[str, Any]]:
        """
        Get a summary of accounts with current balances.

        Args:
            entity_id: If provided, only return accounts linked to this entity.

        Returns:
            List of account summaries
        """
        if entity_id is not None:
            from ..database.models import account_entities
            # Get account IDs linked to this entity
            linked = self.db.query(account_entities.c.account_id).filter(
                account_entities.c.entity_id == entity_id
            ).all()
            linked_ids = {row[0] for row in linked}
            accounts = [a for a in self.get_accounts(is_active=True) if a.account_id in linked_ids]
        else:
            accounts = self.get_accounts(is_active=True)
        summaries = []

        for account in accounts:
            balance = self.get_current_balance(account.account_id)
            summary = {
                'account_id': account.account_id,
                'account_name': account.account_name,
                'account_type': account.account_type,
                'institution': account.institution_name,
                'current_balance': balance.total_balance if balance else Decimal('0'),
                'balance_date': balance.balance_date if balance else None,
                'has_cash': account.has_cash_component,
                'has_investments': account.has_investment_component
            }

            if balance and account.has_cash_component and account.has_investment_component:
                summary['cash_balance'] = balance.cash_balance
                summary['investment_value'] = balance.investment_value

            summaries.append(summary)

        return summaries