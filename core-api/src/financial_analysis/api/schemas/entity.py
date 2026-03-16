"""Pydantic schemas for entity-related API endpoints."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict


class EntityCreate(BaseModel):
    """Schema for creating an entity."""
    entity_name: str = Field(..., min_length=1, max_length=100)
    entity_type: Literal['personal', 'business', 'rental_property', 'side_hustle']
    tax_id: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    fiscal_year_start_month: int = Field(default=1, ge=1, le=12)
    is_default: bool = False
    notes: Optional[str] = None


class EntityUpdate(BaseModel):
    """Schema for updating an entity."""
    entity_name: Optional[str] = Field(None, min_length=1, max_length=100)
    entity_type: Optional[Literal['personal', 'business', 'rental_property', 'side_hustle']] = None
    tax_id: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    fiscal_year_start_month: Optional[int] = Field(None, ge=1, le=12)
    notes: Optional[str] = None


class EntityResponse(BaseModel):
    """Schema for entity responses."""
    model_config = ConfigDict(from_attributes=True)

    entity_id: int
    entity_name: str
    entity_type: str
    tax_id: Optional[str] = None
    address: Optional[str] = None
    fiscal_year_start_month: int
    is_default: bool
    notes: Optional[str] = None
    account_count: int = 0
    created_at: datetime
    updated_at: datetime


# ==================== Financial Statement Schemas ====================

class CategoryBreakdown(BaseModel):
    """A single category's contribution to a financial statement."""
    category_name: str
    category_id: int
    amount: float
    tax_line_item: Optional[str] = None


class PnlResponse(BaseModel):
    """Profit & Loss statement response."""
    entity_id: int
    entity_name: str
    period: dict  # { start: str, end: str }
    revenue: dict  # { total: float, by_category: List[CategoryBreakdown] }
    expenses: dict  # { total: float, by_category: List[CategoryBreakdown] }
    net_income: float


class CashFlowItem(BaseModel):
    """A single line item in a cash flow section."""
    description: str
    amount: float
    category_name: Optional[str] = None


class CashFlowResponse(BaseModel):
    """Cash flow statement response."""
    entity_id: int
    entity_name: str
    period: dict  # { start: str, end: str }
    operating: dict  # { net_income: float, items: List[CashFlowItem], total: float }
    investing: dict  # { items: List[CashFlowItem], total: float }
    financing: dict  # { items: List[CashFlowItem], total: float }
    net_change: float
