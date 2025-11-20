"""
API schemas for projection endpoints.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ProjectionMethodEnum(str, Enum):
    """Projection algorithm methods."""
    LINEAR_REGRESSION = "linear_regression"
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    WEIGHTED_AVERAGE = "weighted_average"


class ScenarioTypeEnum(str, Enum):
    """Scenario analysis types."""
    BEST_CASE = "best_case"
    EXPECTED = "expected"
    WORST_CASE = "worst_case"


class ProjectionRequest(BaseModel):
    """Base request for projections."""
    start_date: Optional[date] = Field(None, description="Start of historical period (default: 1 year ago)")
    end_date: Optional[date] = Field(None, description="End of historical period (default: today)")
    projection_days: int = Field(90, ge=1, le=365, description="Number of days to project forward")
    method: ProjectionMethodEnum = Field(
        ProjectionMethodEnum.LINEAR_REGRESSION,
        description="Projection algorithm to use"
    )
    confidence_level: float = Field(0.95, ge=0.5, le=0.99, description="Confidence level for intervals")

    model_config = {
        "json_schema_extra": {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "projection_days": 90,
                "method": "linear_regression",
                "confidence_level": 0.95
            }
        }
    }


class CashflowProjectionRequest(ProjectionRequest):
    """Request for cash flow projections."""
    include_scenarios: bool = Field(True, description="Include best/worst case scenarios")

    model_config = {
        "json_schema_extra": {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "projection_days": 90,
                "method": "linear_regression",
                "confidence_level": 0.95,
                "include_scenarios": True
            }
        }
    }


class HistoricalPeriod(BaseModel):
    """Historical period information."""
    start_date: str = Field(..., description="Start date of historical period")
    end_date: str = Field(..., description="End date of historical period")
    days: int = Field(..., description="Number of days in historical period")
    total_income: Optional[float] = Field(None, description="Total income in period")
    total_expenses: Optional[float] = Field(None, description="Total expenses in period")
    average_daily: float = Field(..., description="Average daily value")


class ProjectionPeriod(BaseModel):
    """Projection period information."""
    start_date: str = Field(..., description="Start date of projection period")
    end_date: str = Field(..., description="End date of projection period")
    days: int = Field(..., description="Number of days in projection period")


class ConfidenceInterval(BaseModel):
    """Confidence interval for projections."""
    lower: float = Field(..., description="Lower bound of confidence interval")
    upper: float = Field(..., description="Upper bound of confidence interval")
    range: float = Field(..., description="Range of confidence interval")


class DailyProjection(BaseModel):
    """Daily projection data point."""
    date: str = Field(..., description="Projection date")
    projected_value: float = Field(..., description="Projected value for the day")
    lower_bound: float = Field(..., description="Lower confidence bound")
    upper_bound: float = Field(..., description="Upper confidence bound")


class ModelMetrics(BaseModel):
    """Model performance metrics."""
    r_squared: Optional[float] = Field(None, description="R-squared value (linear regression)")
    slope: Optional[float] = Field(None, description="Slope (linear regression)")
    intercept: Optional[float] = Field(None, description="Intercept (linear regression)")
    std_error: Optional[float] = Field(None, description="Standard error")
    moving_average: Optional[float] = Field(None, description="Moving average value")
    std_deviation: Optional[float] = Field(None, description="Standard deviation")
    window_size: Optional[int] = Field(None, description="Window size (moving average)")
    smoothed_value: Optional[float] = Field(None, description="Smoothed value (exponential smoothing)")
    alpha: Optional[float] = Field(None, description="Alpha parameter (exponential smoothing)")
    weighted_average: Optional[float] = Field(None, description="Weighted average value")
    weighted_std: Optional[float] = Field(None, description="Weighted standard deviation")
    sample_size: Optional[int] = Field(None, description="Sample size")


class IncomeProjectionResponse(BaseModel):
    """Response for income projections."""
    projection_type: str = Field(..., description="Type of projection")
    historical_period: HistoricalPeriod = Field(..., description="Historical period details")
    projection_period: ProjectionPeriod = Field(..., description="Projection period details")
    method: str = Field(..., description="Projection method used")
    confidence_level: float = Field(..., description="Confidence level")
    projected_total: float = Field(..., description="Total projected income")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")
    daily_projections: List[DailyProjection] = Field(..., description="Daily projection values")
    model_metrics: ModelMetrics = Field(..., description="Model performance metrics")

    model_config = {
        "json_schema_extra": {
            "example": {
                "projection_type": "income",
                "historical_period": {
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "days": 365,
                    "total_income": 75000.00,
                    "average_daily": 205.48
                },
                "projection_period": {
                    "start_date": "2025-01-01",
                    "end_date": "2025-03-31",
                    "days": 90
                },
                "method": "linear_regression",
                "confidence_level": 0.95,
                "projected_total": 18500.00,
                "confidence_interval": {
                    "lower": 17000.00,
                    "upper": 20000.00,
                    "range": 3000.00
                },
                "daily_projections": [],
                "model_metrics": {
                    "r_squared": 0.85,
                    "slope": 0.5,
                    "intercept": 200.0,
                    "std_error": 15.5
                }
            }
        }
    }


class ExpenseProjectionResponse(BaseModel):
    """Response for expense projections."""
    projection_type: str = Field(..., description="Type of projection")
    historical_period: HistoricalPeriod = Field(..., description="Historical period details")
    projection_period: ProjectionPeriod = Field(..., description="Projection period details")
    method: str = Field(..., description="Projection method used")
    confidence_level: float = Field(..., description="Confidence level")
    projected_total: float = Field(..., description="Total projected expenses")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")
    daily_projections: List[DailyProjection] = Field(..., description="Daily projection values")
    model_metrics: ModelMetrics = Field(..., description="Model performance metrics")


class CashflowDailyProjection(BaseModel):
    """Daily cash flow projection data point."""
    date: str = Field(..., description="Projection date")
    projected_income: float = Field(..., description="Projected income for the day")
    projected_expenses: float = Field(..., description="Projected expenses for the day")
    projected_cashflow: float = Field(..., description="Projected net cash flow")
    cashflow_lower: float = Field(..., description="Lower confidence bound for cash flow")
    cashflow_upper: float = Field(..., description="Upper confidence bound for cash flow")


class ScenarioData(BaseModel):
    """Scenario analysis data."""
    income: float = Field(..., description="Projected income in scenario")
    expenses: float = Field(..., description="Projected expenses in scenario")
    cashflow: float = Field(..., description="Projected cash flow in scenario")
    description: str = Field(..., description="Scenario description")


class ScenarioRange(BaseModel):
    """Range across scenarios."""
    cashflow_range: float = Field(..., description="Range of cash flow across scenarios")
    income_range: float = Field(..., description="Range of income across scenarios")
    expense_range: float = Field(..., description="Range of expenses across scenarios")


class Scenarios(BaseModel):
    """Scenario analysis results."""
    expected: ScenarioData = Field(..., description="Expected case scenario")
    best_case: ScenarioData = Field(..., description="Best case scenario")
    worst_case: ScenarioData = Field(..., description="Worst case scenario")
    range: ScenarioRange = Field(..., description="Range across scenarios")


class CashflowProjectionResponse(BaseModel):
    """Response for cash flow projections."""
    projection_type: str = Field(..., description="Type of projection")
    historical_period: HistoricalPeriod = Field(..., description="Historical period details")
    projection_period: ProjectionPeriod = Field(..., description="Projection period details")
    method: str = Field(..., description="Projection method used")
    confidence_level: float = Field(..., description="Confidence level")
    projected_income: float = Field(..., description="Total projected income")
    projected_expenses: float = Field(..., description="Total projected expenses")
    projected_cashflow: float = Field(..., description="Total projected cash flow")
    confidence_interval: ConfidenceInterval = Field(..., description="Cash flow confidence interval")
    daily_projections: List[CashflowDailyProjection] = Field(..., description="Daily cash flow projections")
    scenarios: Optional[Scenarios] = Field(None, description="Scenario analysis")

    model_config = {
        "json_schema_extra": {
            "example": {
                "projection_type": "cashflow",
                "historical_period": {
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "days": 365,
                    "average_daily": 50.00
                },
                "projection_period": {
                    "start_date": "2025-01-01",
                    "end_date": "2025-03-31",
                    "days": 90
                },
                "method": "linear_regression",
                "confidence_level": 0.95,
                "projected_income": 18500.00,
                "projected_expenses": 14000.00,
                "projected_cashflow": 4500.00,
                "confidence_interval": {
                    "lower": 2000.00,
                    "upper": 7000.00,
                    "range": 5000.00
                },
                "daily_projections": [],
                "scenarios": {
                    "expected": {
                        "income": 18500.00,
                        "expenses": 14000.00,
                        "cashflow": 4500.00,
                        "description": "Most likely outcome based on historical trends"
                    },
                    "best_case": {
                        "income": 20000.00,
                        "expenses": 12000.00,
                        "cashflow": 8000.00,
                        "description": "Optimistic scenario with high income and low expenses"
                    },
                    "worst_case": {
                        "income": 17000.00,
                        "expenses": 16000.00,
                        "cashflow": 1000.00,
                        "description": "Conservative scenario with low income and high expenses"
                    },
                    "range": {
                        "cashflow_range": 7000.00,
                        "income_range": 3000.00,
                        "expense_range": 4000.00
                    }
                }
            }
        }
    }


class AccuracyMetrics(BaseModel):
    """Projection accuracy metrics."""
    mape: float = Field(..., description="Mean Absolute Percentage Error")
    rmse: float = Field(..., description="Root Mean Squared Error")
    mae: float = Field(..., description="Mean Absolute Error")
    r_squared: float = Field(..., description="R-squared value")
    sample_size: int = Field(..., description="Number of data points")
    accuracy_grade: str = Field(..., description="Accuracy grade (Excellent/Good/Acceptable/Poor/Very Poor)")


class ValidationRequest(BaseModel):
    """Request for projection validation."""
    actual_values: List[float] = Field(..., description="Actual observed values")
    predicted_values: List[float] = Field(..., description="Predicted values")

    @field_validator('actual_values', 'predicted_values')
    @classmethod
    def check_not_empty(cls, v):
        if not v:
            raise ValueError("Values list cannot be empty")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "actual_values": [100.0, 105.0, 110.0, 108.0, 115.0],
                "predicted_values": [98.0, 107.0, 109.0, 110.0, 113.0]
            }
        }
    }

