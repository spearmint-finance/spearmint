"""Pydantic schemas for Scenario Planning preview."""

from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class ScenarioAdjusterIn(BaseModel):
    """Inline adjuster for preview/simulate."""
    type: str = Field(..., description="Adjuster type: job_loss | income_reduction | expense_change | one_time")
    target_person_id: Optional[int] = Field(None)
    params: Dict[str, Any] = Field(default_factory=dict)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)


class ScenarioPreviewRequest(BaseModel):
    """Scenario preview request body."""
    name: Optional[str] = Field(None, description="Optional scenario name (for preview display only)")
    description: Optional[str] = None
    horizon_months: int = Field(default=12, ge=1, le=60)
    starting_balance: Optional[Decimal] = Field(default=Decimal("0.0"))
    shared_expense_strategy: str = Field(default="equal_split", description="Default split if no explicit splits present")
    adjusters: List[ScenarioAdjusterIn] = Field(default_factory=list)


class SeriesPoint(BaseModel):
    date: date
    income: Decimal
    expenses: Decimal
    net_cf: Decimal
    by_person: Optional[Dict[int, Dict[str, Decimal]]] = None  # {personId: {income, expenses, net_cf}}


class ScenarioKPIs(BaseModel):
    runway_months: Optional[float]
    min_balance: Decimal
    coverage_by_person: Dict[int, float] = Field(default_factory=dict)
    monthly_shortfall_by_person: Optional[Dict[int, Decimal]] = None


class ScenarioPreviewResponse(BaseModel):
    baseline_series: List[SeriesPoint]
    scenario_series: List[SeriesPoint]
    kpis: ScenarioKPIs
    deltas: Dict[str, Decimal]
    generated_at: datetime

