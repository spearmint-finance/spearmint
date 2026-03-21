"""
Database models for financial analysis tool.

Implements the database schema as defined in PRD Section 3.2.
"""

from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    Column, Integer, String, Numeric, Date, DateTime, Boolean, Text,
    ForeignKey, CheckConstraint, UniqueConstraint, Index, func, JSON
)
from sqlalchemy.orm import relationship
from .base import Base


def utc_now():
    """Get current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


class Category(Base):
    """
    Categories table (PRD Section 3.2.3).

    Hierarchical categorization of transactions.
    """
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False, unique=True)
    category_type = Column(String(10), nullable=False)
    parent_category_id = Column(Integer, ForeignKey('categories.category_id'))
    description = Column(Text)
    is_fixed_obligation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    parent_category = relationship("Category", remote_side=[category_id], backref="subcategories")
    transactions = relationship("Transaction", back_populates="category")

    # Constraints
    __table_args__ = (
        CheckConstraint("category_type IN ('Income', 'Expense', 'Transfer', 'Both')", name='check_category_type'),
    )

    def __repr__(self):
        return f"<Category(id={self.category_id}, name='{self.category_name}', type='{self.category_type}')>"


class Transaction(Base):
    """
    Transactions table (PRD Section 3.2.1).

    Core table storing all financial transactions.
    """
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    source = Column(String(255))
    description = Column(Text)
    payment_method = Column(String(50))
    include_in_analysis = Column(Boolean, default=True)
    related_transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'))
    transfer_account_from = Column(String(100))
    transfer_account_to = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Account tracking fields
    account_id = Column(Integer, ForeignKey('accounts.account_id'))
    is_cleared = Column(Boolean, default=False)
    cleared_date = Column(Date)

    # External provider dedup field (Plaid transaction_id or Akoya transaction ID)
    external_transaction_id = Column(String(100), unique=True)

    # Investment transaction fields
    affects_cash_balance = Column(Boolean, default=True)
    affects_investment_value = Column(Boolean, default=False)
    security_symbol = Column(String(20))
    security_quantity = Column(Numeric(15, 6))

    # Relationships
    category = relationship("Category", back_populates="transactions")
    related_transaction = relationship("Transaction", remote_side=[transaction_id], backref="related_transactions")
    tags = relationship("Tag", secondary="transaction_tags", back_populates="transactions")
    splits = relationship("TransactionSplit", back_populates="transaction", cascade="all, delete-orphan")
    account = relationship("Account", back_populates="transactions")

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("transaction_type IN ('Income', 'Expense')", name='check_transaction_type'),
        Index('idx_transaction_date', 'transaction_date'),
        Index('idx_transaction_type', 'transaction_type'),
        Index('idx_category_id', 'category_id'),
        Index('idx_include_in_analysis', 'include_in_analysis'),
        Index('idx_related_transaction', 'related_transaction_id'),
        Index('idx_account_id', 'account_id'),
        Index('idx_is_cleared', 'is_cleared'),
        Index('idx_security_symbol', 'security_symbol'),
    )

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, date={self.transaction_date}, amount={self.amount}, type='{self.transaction_type}')>"


class TransactionRelationship(Base):
    """
    Transaction relationships table (PRD Section 3.2.4).

    Links related transactions (e.g., transfer pairs, credit card payment/receipt).
    """
    __tablename__ = "transaction_relationships"

    relationship_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id_1 = Column(Integer, ForeignKey('transactions.transaction_id', ondelete='CASCADE'), nullable=False)
    transaction_id_2 = Column(Integer, ForeignKey('transactions.transaction_id', ondelete='CASCADE'), nullable=False)
    relationship_type = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=utc_now)

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint('transaction_id_1 != transaction_id_2', name='check_different_transactions'),
        UniqueConstraint('transaction_id_1', 'transaction_id_2', 'relationship_type', name='uq_transaction_relationship'),
        Index('idx_relationship_tx1', 'transaction_id_1'),
        Index('idx_relationship_tx2', 'transaction_id_2'),
        Index('idx_relationship_type', 'relationship_type'),
    )

    def __repr__(self):
        return f"<TransactionRelationship(id={self.relationship_id}, type='{self.relationship_type}')>"


class CategoryRule(Base):
    """
    Category rules table.

    Pattern-based rules for automatic transaction categorization.
    """
    __tablename__ = "category_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(100), nullable=False)
    rule_priority = Column(Integer, default=100)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    is_active = Column(Boolean, default=True)

    # Pattern matching criteria
    description_pattern = Column(String(255))
    source_pattern = Column(String(255))
    amount_min = Column(Numeric(10, 2))
    amount_max = Column(Numeric(10, 2))
    payment_method_pattern = Column(String(50))
    transaction_type_pattern = Column(String(10))  # 'Income', 'Expense', or None for both

    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    category = relationship("Category", backref="category_rules")

    # Indexes
    __table_args__ = (
        Index('idx_category_rule_priority', 'rule_priority'),
        Index('idx_category_rule_active', 'is_active'),
        Index('idx_category_rule_category', 'category_id'),
    )

    def __repr__(self):
        return f"<CategoryRule(id={self.rule_id}, name='{self.rule_name}', priority={self.rule_priority})>"


class Tag(Base):
    """
    Tags table (PRD Section 3.2.6).

    Flexible tagging system for transactions.
    """
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    transactions = relationship("Transaction", secondary="transaction_tags", back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.tag_id}, name='{self.tag_name}')>"


class TransactionTag(Base):
    """
    Transaction-Tag association table (PRD Section 3.2.6).

    Many-to-many relationship between transactions and tags.
    """
    __tablename__ = "transaction_tags"

    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id', ondelete='CASCADE'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<TransactionTag(transaction_id={self.transaction_id}, tag_id={self.tag_id})>"


class ImportHistory(Base):
    """
    Import history table (PRD Section 3.2.7).

    Tracks data import operations.
    """
    __tablename__ = "import_history"

    import_id = Column(Integer, primary_key=True, autoincrement=True)
    import_date = Column(DateTime, default=utc_now)
    file_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    total_rows = Column(Integer, nullable=False)
    successful_rows = Column(Integer, nullable=False)
    failed_rows = Column(Integer, nullable=False)
    classified_rows = Column(Integer, default=0)
    import_mode = Column(String(20), nullable=False)
    error_log = Column(Text)

    def __repr__(self):
        return f"<ImportHistory(id={self.import_id}, file='{self.file_name}', date={self.import_date})>"


class ImportProfile(Base):
    """
    Import mapping profiles table.

    Stores column mappings for different bank/institution export formats
    to enable reusable import configurations.
    """
    __tablename__ = "import_profiles"

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # e.g., "Chase Credit Card"
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=True)
    column_mappings = Column(JSON, nullable=False)  # {"Posting Date": "date", "Description": "description", ...}
    date_format = Column(String(50))  # e.g., "%m/%d/%Y"
    skip_rows = Column(Integer, default=0)  # Number of header rows to skip
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    account = relationship("Account", backref="import_profiles")

    # Indexes
    __table_args__ = (
        Index('idx_import_profile_name', 'name'),
        Index('idx_import_profile_account', 'account_id'),
        Index('idx_import_profile_active', 'is_active'),
    )

    def __repr__(self):
        return f"<ImportProfile(id={self.profile_id}, name='{self.name}')>"


class Budget(Base):
    """
    Budgets table (PRD Section 3.2.8).

    Budget tracking by category (future enhancement).
    """
    __tablename__ = "budgets"

    budget_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    budget_amount = Column(Numeric(10, 2), nullable=False)
    period_type = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    created_at = Column(DateTime, default=utc_now)

    # Constraints
    __table_args__ = (
        CheckConstraint("period_type IN ('Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly')", name='check_period_type'),
    )

    def __repr__(self):
        return f"<Budget(id={self.budget_id}, category_id={self.category_id}, amount={self.budget_amount})>"




class Person(Base):
    """
    Persons table for person-aware attribution.
    """
    __tablename__ = "persons"

    person_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    splits = relationship("TransactionSplit", back_populates="person")

    def __repr__(self):
        return f"<Person(id={self.person_id}, name='{self.name}')>"


class TransactionSplit(Base):
    """
    Transaction splits for shared costs and per-person attribution.
    """
    __tablename__ = "transaction_splits"

    split_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id', ondelete='CASCADE'), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    transaction = relationship("Transaction", back_populates="splits")
    person = relationship("Person", back_populates="splits")

    __table_args__ = (
        UniqueConstraint('transaction_id', 'person_id', name='uq_transaction_person_split'),
        Index('idx_split_transaction', 'transaction_id'),
        Index('idx_split_person', 'person_id'),
    )

    def __repr__(self):
        return f"<TransactionSplit(id={self.split_id}, tx_id={self.transaction_id}, person_id={self.person_id}, amount={self.amount})>"


class Scenario(Base):
    """
    Saved scenario definitions (Phase 2 will use persist). Phase 1 uses preview only.
    """
    __tablename__ = "scenarios"

    scenario_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    horizon_months = Column(Integer, nullable=False, default=12)
    created_by = Column(String(100))
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    adjusters = relationship("ScenarioAdjuster", back_populates="scenario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Scenario(id={self.scenario_id}, name='{self.name}', horizon={self.horizon_months})>"


class ScenarioAdjuster(Base):
    """
    Adjusters linked to a saved scenario. For previews, adjusters are provided inline via API.
    """
    __tablename__ = "scenario_adjusters"

    adjuster_id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_id = Column(Integer, ForeignKey('scenarios.scenario_id', ondelete='CASCADE'))
    type = Column(String(50), nullable=False)  # e.g., 'job_loss', 'income_reduction', 'expense_change', 'one_time'
    target_person_id = Column(Integer, ForeignKey('persons.person_id'), nullable=True)
    params_json = Column(Text)  # JSON-encoded parameters
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime, default=utc_now)

    # Relationships
    scenario = relationship("Scenario", back_populates="adjusters")

    __table_args__ = (
        Index('idx_adjuster_scenario', 'scenario_id'),
        Index('idx_adjuster_type', 'type'),
    )

    def __repr__(self):
        return f"<ScenarioAdjuster(id={self.adjuster_id}, type='{self.type}', scenario_id={self.scenario_id})>"


class LinkedProvider(Base):
    """
    Linked data providers for bank account aggregation.

    Tracks connections to external data providers (Plaid, Akoya) that
    supply account, transaction, balance, and investment holdings data.
    One LinkedProvider represents one institutional connection (e.g., one
    bank login) which may contain multiple accounts.
    """
    __tablename__ = "linked_providers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_type = Column(String(20), nullable=False)  # 'plaid' or 'akoya'
    provider_item_id = Column(String(200), nullable=False, unique=True)  # Plaid item_id or Akoya grant ID
    access_token_encrypted = Column(Text, nullable=False)
    refresh_token_encrypted = Column(Text)  # Used by Akoya for token rotation
    institution_id = Column(String(50))
    institution_name = Column(String(200))
    status = Column(String(50), default='active')  # active, login_required, error
    error_code = Column(String(100))
    error_message = Column(Text)
    sync_cursor = Column(Text)  # Plaid transaction cursor for incremental sync
    last_synced_at = Column(DateTime)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    accounts = relationship("Account", back_populates="linked_provider")

    __table_args__ = (
        CheckConstraint("provider_type IN ('plaid', 'akoya')", name='check_provider_type'),
        CheckConstraint("status IN ('active', 'login_required', 'error', 'revoked')", name='check_provider_status'),
        Index('idx_provider_item_id', 'provider_item_id'),
        Index('idx_provider_status', 'status'),
    )

    def __repr__(self):
        return f"<LinkedProvider(id={self.id}, type='{self.provider_type}', institution='{self.institution_name}', status='{self.status}')>"


class Entity(Base):
    """
    Entities table for separating financial books.

    Each entity represents an independent financial context — personal finances,
    a business, a rental property, or a side hustle. Accounts are assigned to
    entities, and transactions are entity-scoped through their accounts.
    """
    __tablename__ = "entities"

    entity_id = Column(Integer, primary_key=True, autoincrement=True)
    entity_name = Column(String(100), nullable=False)
    entity_type = Column(String(20), nullable=False)  # personal, business, rental_property, side_hustle
    tax_id = Column(String(20))  # EIN for businesses
    address = Column(Text)  # For rental properties
    fiscal_year_start_month = Column(Integer, default=1)  # 1=January
    is_default = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    accounts = relationship("Account", back_populates="entity")

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('personal', 'business', 'rental_property', 'side_hustle')",
            name='check_entity_type'
        ),
        Index('idx_entity_type', 'entity_type'),
        Index('idx_entity_default', 'is_default'),
    )

    def __repr__(self):
        return f"<Entity(id={self.entity_id}, name='{self.entity_name}', type='{self.entity_type}')>"


class Account(Base):
    """
    Accounts table for tracking financial accounts.

    Supports various account types including hybrid brokerage accounts
    that contain both cash and investment components.
    """
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    account_name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)  # checking, savings, brokerage, credit_card, etc.
    account_subtype = Column(String(50))  # cash_management, investment_only, hybrid, etc.
    institution_name = Column(String(100))
    account_number_last4 = Column(String(4))
    currency = Column(String(3), default='USD')
    is_active = Column(Boolean, default=True)
    has_cash_component = Column(Boolean, default=False)  # True for brokerage accounts with cash
    has_investment_component = Column(Boolean, default=False)  # True for investment accounts
    opening_balance = Column(Numeric(15, 2), default=0)
    opening_balance_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Entity assignment (NULL = default/personal entity)
    entity_id = Column(Integer, ForeignKey('entities.entity_id'), nullable=True)

    # Linked provider fields (for Plaid/Akoya connected accounts)
    linked_provider_id = Column(Integer, ForeignKey('linked_providers.id'))
    external_account_id = Column(String(100))  # Provider's account ID
    link_type = Column(String(20), default='manual')  # manual, plaid, akoya

    # Relationships
    entity = relationship("Entity", back_populates="accounts")
    linked_provider = relationship("LinkedProvider", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    balances = relationship("AccountBalance", back_populates="account", cascade="all, delete-orphan")
    holdings = relationship("InvestmentHolding", back_populates="account", cascade="all, delete-orphan")
    reconciliations = relationship("Reconciliation", back_populates="account", cascade="all, delete-orphan")

    # Constraints and Indexes
    __table_args__ = (
        CheckConstraint("account_type IN ('checking', 'savings', 'brokerage', 'investment', "
                       "'credit_card', 'loan', '401k', 'ira', 'other')",
                       name='check_account_type'),
        Index('idx_account_type', 'account_type'),
        Index('idx_account_active', 'is_active'),
        Index('idx_account_institution', 'institution_name'),
        Index('idx_account_entity', 'entity_id'),
    )

    def __repr__(self):
        return f"<Account(id={self.account_id}, name='{self.account_name}', type='{self.account_type}')>"


class AccountBalance(Base):
    """
    Account balances table for tracking balance snapshots over time.

    Supports both simple balances and complex brokerage account balances
    with separate cash and investment components.
    """
    __tablename__ = "account_balances"

    balance_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    balance_date = Column(Date, nullable=False)

    # Standard balance fields
    total_balance = Column(Numeric(15, 2), nullable=False)  # Total account value
    balance_type = Column(String(20), default='statement')  # statement, calculated, reconciled

    # Hybrid account fields (nullable for non-brokerage accounts)
    cash_balance = Column(Numeric(15, 2))  # Cash/core position
    investment_value = Column(Numeric(15, 2))  # Securities value

    # Metadata
    notes = Column(Text)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    account = relationship("Account", back_populates="balances")

    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('account_id', 'balance_date', 'balance_type',
                        name='uq_account_balance_date_type'),
        CheckConstraint("balance_type IN ('statement', 'calculated', 'reconciled')",
                       name='check_balance_type'),
        Index('idx_balance_account', 'account_id'),
        Index('idx_balance_date', 'balance_date'),
        Index('idx_balance_type', 'balance_type'),
    )

    def __repr__(self):
        return f"<AccountBalance(id={self.balance_id}, account={self.account_id}, date={self.balance_date}, balance={self.total_balance})>"


class InvestmentHolding(Base):
    """
    Investment holdings table for tracking securities positions.

    Tracks individual investment positions within brokerage and investment accounts.
    """
    __tablename__ = "investment_holdings"

    holding_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    symbol = Column(String(20), nullable=False)
    description = Column(String(200))
    quantity = Column(Numeric(15, 6), nullable=False)
    cost_basis = Column(Numeric(15, 2))
    current_value = Column(Numeric(15, 2))
    as_of_date = Column(Date, nullable=False)

    # Additional fields
    asset_class = Column(String(50))  # stock, etf, mutual_fund, bond, etc.
    sector = Column(String(50))

    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    account = relationship("Account", back_populates="holdings")

    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('account_id', 'symbol', 'as_of_date',
                        name='uq_holding_account_symbol_date'),
        Index('idx_holding_account', 'account_id'),
        Index('idx_holding_symbol', 'symbol'),
        Index('idx_holding_date', 'as_of_date'),
    )

    def __repr__(self):
        return f"<InvestmentHolding(id={self.holding_id}, symbol='{self.symbol}', quantity={self.quantity})>"


class APIKey(Base):
    """
    API keys for MCP server authentication.

    Stores hashed API keys for authenticating external MCP clients
    (Claude Desktop, Gemini CLI, ChatGPT, etc.) to the Spearmint API.
    """
    __tablename__ = "api_keys"

    key_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # e.g., "Claude Desktop"
    key_prefix = Column(String(16), nullable=False)  # "smint_live_" + first 4 chars
    key_hash = Column(String(128), nullable=False)  # SHA-256 hash
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_api_key_hash', 'key_hash'),
        Index('idx_api_key_active', 'is_active'),
    )

    def __repr__(self):
        return f"<APIKey(id={self.key_id}, name='{self.name}', prefix='{self.key_prefix}')>"


class Reconciliation(Base):
    """
    Reconciliations table for tracking account reconciliation history.

    Supports both simple reconciliations and complex brokerage account
    reconciliations with separate cash and investment tracking.
    """
    __tablename__ = "reconciliations"

    reconciliation_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id', ondelete='CASCADE'), nullable=False)
    statement_date = Column(Date, nullable=False)

    # Standard reconciliation fields
    statement_balance = Column(Numeric(15, 2), nullable=False)
    calculated_balance = Column(Numeric(15, 2), nullable=False)

    # Hybrid account reconciliation fields (nullable)
    statement_cash_balance = Column(Numeric(15, 2))
    calculated_cash_balance = Column(Numeric(15, 2))
    statement_investment_value = Column(Numeric(15, 2))
    calculated_investment_value = Column(Numeric(15, 2))

    # Results
    discrepancy_amount = Column(Numeric(15, 2))
    is_reconciled = Column(Boolean, default=False)
    reconciled_at = Column(DateTime)
    reconciled_by = Column(String(100))

    # Transaction tracking
    transactions_cleared_count = Column(Integer, default=0)
    transactions_pending_count = Column(Integer, default=0)

    notes = Column(Text)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    account = relationship("Account", back_populates="reconciliations")

    # Constraints and Indexes
    __table_args__ = (
        UniqueConstraint('account_id', 'statement_date', name='uq_reconciliation_account_date'),
        Index('idx_reconciliation_account', 'account_id'),
        Index('idx_reconciliation_date', 'statement_date'),
        Index('idx_reconciliation_status', 'is_reconciled'),
    )

    def __repr__(self):
        return f"<Reconciliation(id={self.reconciliation_id}, account={self.account_id}, date={self.statement_date}, reconciled={self.is_reconciled})>"
