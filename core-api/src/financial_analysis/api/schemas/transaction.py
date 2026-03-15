"""Transaction Pydantic schemas."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from .analysis import DecimalBaseModel


class TransactionBase(DecimalBaseModel):
    """Base transaction schema with common fields."""

    transaction_date: date = Field(..., description="Transaction date")
    amount: Decimal = Field(..., description="Transaction amount (can be negative for expenses)")
    transaction_type: str = Field(..., pattern="^(Income|Expense)$", description="Transaction type")
    category_id: int = Field(..., gt=0, description="Category ID")
    source: Optional[str] = Field(None, max_length=255, description="Transaction source")
    description: Optional[str] = Field(None, description="Transaction description")
    payment_method: Optional[str] = Field(None, max_length=50, description="Payment method")
    classification_id: Optional[int] = Field(None, gt=0, description="Classification ID")
    include_in_analysis: bool = Field(default=True, description="Include in analysis")
    is_transfer: bool = Field(default=False, description="Is transfer transaction")
    transfer_account_from: Optional[str] = Field(None, max_length=100, description="Transfer from account")
    transfer_account_to: Optional[str] = Field(None, max_length=100, description="Transfer to account")
    notes: Optional[str] = Field(None, description="Additional notes")
    account_id: Optional[int] = Field(None, gt=0, description="Account ID this transaction belongs to")


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    
    tag_names: Optional[List[str]] = Field(default=None, description="List of tag names")


class TransactionUpdate(DecimalBaseModel):
    """Schema for updating a transaction."""

    transaction_date: Optional[date] = Field(None, description="Transaction date")
    amount: Optional[Decimal] = Field(None, description="Transaction amount (can be negative for expenses)")
    transaction_type: Optional[str] = Field(None, pattern="^(Income|Expense)$", description="Transaction type")
    category_id: Optional[int] = Field(None, gt=0, description="Category ID")
    source: Optional[str] = Field(None, max_length=255, description="Transaction source")
    description: Optional[str] = Field(None, description="Transaction description")
    payment_method: Optional[str] = Field(None, max_length=50, description="Payment method")
    classification_id: Optional[int] = Field(None, gt=0, description="Classification ID")
    include_in_analysis: Optional[bool] = Field(None, description="Include in analysis")
    is_transfer: Optional[bool] = Field(None, description="Is transfer transaction")
    transfer_account_from: Optional[str] = Field(None, max_length=100, description="Transfer from account")
    transfer_account_to: Optional[str] = Field(None, max_length=100, description="Transfer to account")
    notes: Optional[str] = Field(None, description="Additional notes")
    account_id: Optional[int] = Field(None, gt=0, description="Account ID this transaction belongs to")
    tag_names: Optional[List[str]] = Field(None, description="List of tag names")
    # Force re-application of classification rules even if a manual classification exists
    reapply_rules: Optional[bool] = Field(None, description="If true, re-apply classification rules on this update")


class CategoryInfo(BaseModel):
    """Category information for transaction response."""
    
    category_id: int
    category_name: str
    category_type: str
    
    model_config = ConfigDict(from_attributes=True)


class ClassificationInfo(BaseModel):
    """Classification information for transaction response."""
    
    classification_id: int
    classification_name: str
    classification_code: str
    
    model_config = ConfigDict(from_attributes=True)


class TagInfo(BaseModel):
    """Tag information for transaction response."""
    
    tag_id: int
    tag_name: str
    
    model_config = ConfigDict(from_attributes=True)


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""

    transaction_id: int = Field(..., description="Transaction ID")
    # Convenience field used by the UI to display/link paired transactions
    related_transaction_id: Optional[int] = Field(
        None,
        description="If present, the ID of a related transaction (e.g., transfer pair, dividend reinvestment pair)"
    )
    category: Optional[CategoryInfo] = Field(None, description="Category information")
    classification: Optional[ClassificationInfo] = Field(None, description="Classification information")
    tags: List[TagInfo] = Field(default_factory=list, description="Associated tags")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class TransactionListResponse(BaseModel):
    """Schema for transaction list response."""

    transactions: List[TransactionResponse] = Field(..., description="List of transactions")
    total: int = Field(..., description="Total number of transactions")
    limit: int = Field(..., description="Limit used")
    offset: int = Field(..., description="Offset used")
    summary: Optional[dict] = Field(None, description="Summary statistics for all filtered transactions")

