"""Pydantic schemas for Transaction Splits."""

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class TransactionSplitCreate(BaseModel):
    """Create a split for a transaction."""
    person_id: int = Field(..., description="Person ID for this split")
    amount: Decimal = Field(..., description="Split amount (positive for income shares, negative for expense shares)")


class TransactionSplitRead(BaseModel):
    """Read model for a transaction split."""
    split_id: int
    transaction_id: int
    person_id: int
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True

