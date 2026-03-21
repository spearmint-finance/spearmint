"""Pydantic schemas for Transaction Splits."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TransactionSplitCreate(BaseModel):
    """Create a category-based split for a transaction."""
    amount: Decimal = Field(..., description="Split amount (positive)")
    category_id: int = Field(..., description="Category for this split")
    entity_id: Optional[int] = Field(None, description="Entity assignment (null = inherit from parent)")
    description: Optional[str] = Field(None, description="Split-specific description")
    notes: Optional[str] = Field(None, description="Notes for this split")


class TransactionSplitResponse(BaseModel):
    """Read model for a transaction split."""
    split_id: int
    transaction_id: int
    amount: Decimal
    category_id: int
    category_name: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
