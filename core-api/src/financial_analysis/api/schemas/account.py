"""
Pydantic schemas for account-related API endpoints.

These schemas define the request/response models for account management,
balance tracking, holdings, and reconciliation endpoints.
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict


# ==================== Account Schemas ====================

class AccountBase(BaseModel):
    """Base account schema with common fields."""
    account_name: str = Field(..., min_length=1, max_length=100)
    account_type: Literal[
        'checking', 'savings', 'brokerage', 'investment',
        'credit_card', 'loan', '401k', 'ira', 'other'
    ]
    account_subtype: Optional[str] = Field(None, max_length=50)
    institution_name: Optional[str] = Field(None, max_length=100)
    account_number_last4: Optional[str] = Field(None, pattern=r'^\d{4}$')
    currency: str = Field(default='USD', pattern=r'^[A-Z]{3}$')
    notes: Optional[str] = None


class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    opening_balance: Decimal = Field(default=Decimal('0'))
    opening_balance_date: Optional[date] = None
    entity_id: Optional[int] = Field(None, gt=0, description="Entity this account belongs to")


class AccountUpdate(BaseModel):
    """Schema for updating an account."""
    account_name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_subtype: Optional[str] = Field(None, max_length=50)
    institution_name: Optional[str] = Field(None, max_length=100)
    account_number_last4: Optional[str] = Field(None, pattern=r'^\d{4}$')
    is_active: Optional[bool] = None
    entity_id: Optional[int] = Field(None, gt=0, description="Entity this account belongs to")
    notes: Optional[str] = None


class AccountResponse(AccountBase):
    """Schema for account responses."""
    model_config = ConfigDict(from_attributes=True)

    account_id: int
    is_active: bool
    has_cash_component: bool
    has_investment_component: bool
    opening_balance: Decimal
    opening_balance_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    # Include current balance if available
    current_balance: Optional[Decimal] = None
    current_balance_date: Optional[date] = None
    cash_balance: Optional[Decimal] = None
    investment_value: Optional[Decimal] = None

    # Entity assignment
    entity_id: Optional[int] = None

    # Linked provider info
    link_type: str = 'manual'
    linked_provider_id: Optional[int] = None


class AccountSummary(BaseModel):
    """Schema for account summary with balance."""
    account_id: int
    account_name: str
    account_type: str
    institution: Optional[str]
    current_balance: Decimal
    balance_date: Optional[date]
    has_cash: bool
    has_investments: bool
    cash_balance: Optional[Decimal] = None
    investment_value: Optional[Decimal] = None


# ==================== Balance Schemas ====================

class BalanceCreate(BaseModel):
    """Schema for creating a balance snapshot."""
    balance_date: date
    total_balance: Decimal
    balance_type: Literal['statement', 'calculated', 'reconciled'] = 'statement'
    cash_balance: Optional[Decimal] = None
    investment_value: Optional[Decimal] = None
    notes: Optional[str] = None


class BalanceResponse(BaseModel):
    """Schema for balance responses."""
    model_config = ConfigDict(from_attributes=True)

    balance_id: int
    account_id: int
    balance_date: date
    total_balance: Decimal
    balance_type: str
    cash_balance: Optional[Decimal]
    investment_value: Optional[Decimal]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class BalanceHistory(BaseModel):
    """Schema for balance history response."""
    account_id: int
    account_name: str
    balances: List[BalanceResponse]
    start_date: Optional[date]
    end_date: Optional[date]


# ==================== Investment Holding Schemas ====================

class HoldingCreate(BaseModel):
    """Schema for creating/updating a holding."""
    symbol: str = Field(..., min_length=1, max_length=20)
    quantity: Decimal = Field(..., gt=0)
    as_of_date: date
    description: Optional[str] = Field(None, max_length=200)
    cost_basis: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    asset_class: Optional[str] = Field(None, max_length=50)
    sector: Optional[str] = Field(None, max_length=50)


class HoldingResponse(BaseModel):
    """Schema for holding responses."""
    model_config = ConfigDict(from_attributes=True)

    holding_id: int
    account_id: int
    symbol: str
    description: Optional[str]
    quantity: Decimal
    cost_basis: Optional[Decimal]
    current_value: Optional[Decimal]
    as_of_date: date
    asset_class: Optional[str]
    sector: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Calculated fields
    gain_loss: Optional[Decimal] = None
    gain_loss_percent: Optional[float] = None


class PortfolioSummary(BaseModel):
    """Schema for portfolio summary."""
    account_id: int
    account_name: str
    total_value: Decimal
    total_cost_basis: Optional[Decimal]
    total_gain_loss: Optional[Decimal]
    holdings: List[HoldingResponse]
    as_of_date: date


# ==================== Reconciliation Schemas ====================

class ReconciliationCreate(BaseModel):
    """Schema for creating a reconciliation."""
    statement_date: date
    statement_balance: Decimal
    statement_cash_balance: Optional[Decimal] = None
    statement_investment_value: Optional[Decimal] = None
    notes: Optional[str] = None


class ReconciliationComplete(BaseModel):
    """Schema for completing a reconciliation."""
    reconciled_by: Optional[str] = Field(None, max_length=100)
    cleared_transaction_ids: Optional[List[int]] = None


class ReconciliationResponse(BaseModel):
    """Schema for reconciliation responses."""
    model_config = ConfigDict(from_attributes=True)

    reconciliation_id: int
    account_id: int
    statement_date: date
    statement_balance: Decimal
    calculated_balance: Decimal
    statement_cash_balance: Optional[Decimal]
    calculated_cash_balance: Optional[Decimal]
    statement_investment_value: Optional[Decimal]
    calculated_investment_value: Optional[Decimal]
    discrepancy_amount: Optional[Decimal]
    is_reconciled: bool
    reconciled_at: Optional[datetime]
    reconciled_by: Optional[str]
    transactions_cleared_count: int
    transactions_pending_count: int
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


# ==================== Net Worth & Analytics Schemas ====================

class NetWorthResponse(BaseModel):
    """Schema for net worth response."""
    assets: Decimal
    liabilities: Decimal
    net_worth: Decimal
    liquid_assets: Decimal
    investments: Decimal
    as_of_date: date

    # Breakdown by account type
    account_breakdown: Optional[dict] = None


class AccountFilterParams(BaseModel):
    """Schema for account filtering parameters."""
    is_active: Optional[bool] = None
    account_type: Optional[str] = None
    institution: Optional[str] = None
    has_cash: Optional[bool] = None
    has_investments: Optional[bool] = None


class TransactionClearRequest(BaseModel):
    """Schema for clearing transactions."""
    transaction_ids: List[int]
    cleared_date: Optional[date] = None


class CalculatedBalance(BaseModel):
    """Schema for calculated balance response."""
    account_id: int
    as_of_date: date
    total: Decimal
    cash: Optional[Decimal] = None
    investments: Optional[Decimal] = None
    based_on_transactions: int