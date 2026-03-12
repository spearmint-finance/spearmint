"""Pydantic schemas for the Budget Advisor A2A agent."""

from datetime import date
from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


# ── Request schemas ──────────────────────────────────────────────

class NegotiationChoice(BaseModel):
    chosen_option: str


class A2ARequest(BaseModel):
    """Generic A2A invocation envelope."""
    skill: str
    params: Dict[str, Any] = Field(default_factory=dict)
    negotiation: Optional[NegotiationChoice] = None


class AnalyzeSpendingParams(BaseModel):
    months_back: int = Field(default=6, ge=1, le=24)
    goal: Optional[str] = Field(default="reduce_spending")


# ── Response schemas ─────────────────────────────────────────────

class NegotiationOption(BaseModel):
    id: str
    description: str
    confidence: Optional[float] = None
    prerequisite: Optional[str] = None


class CategoryStats(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    category: str
    category_id: int
    monthly_avg: float
    trend: Literal["increasing", "decreasing", "stable"]
    trend_pct: float
    pct_of_income: float
    pct_of_expenses: float
    variance: Literal["low", "moderate", "high"]
    months: List[float]
    is_fixed: bool


class SavingsRecommendation(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    category: str
    signal: str
    severity: Literal["low", "moderate", "high"]
    current_monthly: float
    suggested_target: float
    monthly_savings: float
    annual_impact: float
    confidence: float
    reasoning: str


class SpendingAnalysisResult(BaseModel):
    model_config = ConfigDict(json_encoders={Decimal: float})

    analysis_period: Dict[str, str]
    monthly_income_avg: float
    monthly_expense_avg: float
    savings_rate: float
    category_breakdown: List[CategoryStats]
    recommendations: List[SavingsRecommendation]
    confidence: float


class DataQualityReport(BaseModel):
    available_months: int
    uncategorized_pct: float
    total_transactions: int
    earliest_date: Optional[date] = None
    latest_date: Optional[date] = None


class A2AResponse(BaseModel):
    """Generic A2A response envelope."""
    agent: str = "budget-advisor"
    skill: str
    status: Literal["completed", "needs_input", "error"]
    duration_ms: Optional[int] = None
    result: Optional[SpendingAnalysisResult] = None
    issue: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    options: Optional[List[NegotiationOption]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
