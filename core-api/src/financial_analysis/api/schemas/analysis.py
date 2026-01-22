"""Pydantic schemas for analysis API endpoints."""

from datetime import date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class DecimalBaseModel(BaseModel):
    """Base model with Decimal to string conversion for JSON serialization."""
    model_config = ConfigDict(
        json_encoders={Decimal: str}
    )


class TimePeriodEnum(str, Enum):
    """Time period granularity."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class AnalysisModeEnum(str, Enum):
    """Analysis mode."""
    ANALYSIS = "analysis"
    WITH_CAPITAL = "with_capital"
    COMPLETE = "complete"


class DateRangeRequest(BaseModel):
    """Date range for analysis requests."""
    start_date: Optional[date] = Field(None, description="Start date for analysis")
    end_date: Optional[date] = Field(None, description="End date for analysis")


class CategoryBreakdown(DecimalBaseModel):
    """Category breakdown data."""
    total: Decimal = Field(..., description="Total amount for category")
    count: int = Field(..., description="Number of transactions")
    average: Decimal = Field(..., description="Average transaction amount")
    percentage: float = Field(..., description="Percentage of total")


class IncomeAnalysisResponse(DecimalBaseModel):
    """Response for income analysis."""
    total_income: Decimal = Field(..., description="Total income amount")
    transaction_count: int = Field(..., description="Number of income transactions")
    average_transaction: Decimal = Field(..., description="Average transaction amount")
    breakdown_by_category: Dict[str, CategoryBreakdown] = Field(..., description="Breakdown by category")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "total_income": "10000.00",
                "transaction_count": 2,
                "average_transaction": "5000.00",
                "breakdown_by_category": {
                    "Salary": {
                        "total": "10000.00",
                        "count": 2,
                        "average": "5000.00",
                        "percentage": 100.0
                    }
                },
                "period_start": "2025-01-01",
                "period_end": "2025-01-31",
                "mode": "analysis"
            }
        }


class TopCategory(DecimalBaseModel):
    """Top category data."""
    category: str = Field(..., description="Category name")
    amount: Decimal = Field(..., description="Total amount")
    count: int = Field(..., description="Number of transactions")
    percentage: float = Field(..., description="Percentage of total")


class ExpenseAnalysisResponse(DecimalBaseModel):
    """Response for expense analysis."""
    total_expenses: Decimal = Field(..., description="Total expense amount")
    transaction_count: int = Field(..., description="Number of expense transactions")
    average_transaction: Decimal = Field(..., description="Average transaction amount")
    breakdown_by_category: Dict[str, CategoryBreakdown] = Field(..., description="Breakdown by category")
    top_categories: List[TopCategory] = Field(..., description="Top spending categories")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "total_expenses": "1850.00",
                "transaction_count": 3,
                "average_transaction": "616.67",
                "breakdown_by_category": {
                    "Rent": {
                        "total": "1500.00",
                        "count": 1,
                        "average": "1500.00",
                        "percentage": 81.08
                    },
                    "Groceries": {
                        "total": "350.00",
                        "count": 2,
                        "average": "175.00",
                        "percentage": 18.92
                    }
                },
                "top_categories": [
                    {
                        "category": "Rent",
                        "amount": "1500.00",
                        "count": 1,
                        "percentage": 81.08
                    }
                ],
                "period_start": "2025-01-01",
                "period_end": "2025-01-31",
                "mode": "analysis"
            }
        }


class CashFlowResponse(DecimalBaseModel):
    """Response for cash flow analysis."""
    net_cash_flow: Decimal = Field(..., description="Net cash flow (income - expenses)")
    total_income: Decimal = Field(..., description="Total income")
    total_expenses: Decimal = Field(..., description="Total expenses")
    income_count: int = Field(..., description="Number of income transactions")
    expense_count: int = Field(..., description="Number of expense transactions")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "net_cash_flow": "8150.00",
                "total_income": "10000.00",
                "total_expenses": "1850.00",
                "income_count": 2,
                "expense_count": 3,
                "period_start": "2025-01-01",
                "period_end": "2025-01-31",
                "mode": "analysis"
            }
        }


class TrendDataPoint(DecimalBaseModel):
    """Single data point in a trend."""
    period: str = Field(..., description="Period identifier (e.g., '2025-01', '2025-W01')")
    value: Decimal = Field(..., description="Value for the period")
    count: int = Field(..., description="Number of transactions in period")


class TrendsResponse(BaseModel):
    """Response for trend analysis."""
    trends: List[TrendDataPoint] = Field(..., description="Trend data points")
    period_type: TimePeriodEnum = Field(..., description="Period granularity")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "trends": [
                    {
                        "period": "2025-01",
                        "value": "5000.00",
                        "count": 1
                    },
                    {
                        "period": "2025-02",
                        "value": "5000.00",
                        "count": 1
                    }
                ],
                "period_type": "monthly",
                "mode": "analysis"
            }
        }


class CashFlowTrendPoint(DecimalBaseModel):
    """Cash flow trend data point."""
    period: str = Field(..., description="Period identifier")
    income: Decimal = Field(..., description="Income for period")
    expenses: Decimal = Field(..., description="Expenses for period")
    net_cash_flow: Decimal = Field(..., description="Net cash flow for period")
    income_count: int = Field(..., description="Number of income transactions")
    expense_count: int = Field(..., description="Number of expense transactions")


class CashFlowTrendsResponse(BaseModel):
    """Response for cash flow trends."""
    trends: List[CashFlowTrendPoint] = Field(..., description="Cash flow trend data")
    period_type: TimePeriodEnum = Field(..., description="Period granularity")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")


class FinancialHealthResponse(DecimalBaseModel):
    """Response for financial health indicators."""
    income_to_expense_ratio: Optional[float] = Field(None, description="Income to expense ratio")
    savings_rate: Optional[float] = Field(None, description="Savings rate (percentage)")
    average_daily_income: Decimal = Field(..., description="Average daily income")
    average_daily_expense: Decimal = Field(..., description="Average daily expense")
    net_daily_cash_flow: Decimal = Field(..., description="Net daily cash flow")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")

    class Config:
        json_schema_extra = {
            "example": {
                "income_to_expense_ratio": 5.41,
                "savings_rate": 0.815,
                "average_daily_income": "166.67",
                "average_daily_expense": "30.83",
                "net_daily_cash_flow": "135.84",
                "period_start": "2025-01-01",
                "period_end": "2025-01-31"
            }
        }


class PeriodComparisonResponse(DecimalBaseModel):
    """Response for period comparison."""
    period1: Dict[str, Any] = Field(..., description="First period data")
    period2: Dict[str, Any] = Field(..., description="Second period data")
    differences: Dict[str, Decimal] = Field(..., description="Absolute differences")
    percentage_changes: Dict[str, Optional[float]] = Field(..., description="Percentage changes")

    class Config:
        json_schema_extra = {
            "example": {
                "period1": {
                    "start": "2025-02-01",
                    "end": "2025-02-28",
                    "income": "5000.00",
                    "expenses": "1800.00",
                    "net_cash_flow": "3200.00"
                },
                "period2": {
                    "start": "2025-01-01",
                    "end": "2025-01-31",
                    "income": "5000.00",
                    "expenses": "1850.00",
                    "net_cash_flow": "3150.00"
                },
                "differences": {
                    "income": "0.00",
                    "expenses": "-50.00",
                    "net_cash_flow": "50.00"
                },
                "percentage_changes": {
                    "income": 0.0,
                    "expenses": -2.70,
                    "net_cash_flow": 1.59
                }
            }
        }


class RecentTransaction(DecimalBaseModel):
    """Recent transaction summary."""
    transaction_id: int = Field(..., description="Transaction ID")
    transaction_date: date = Field(..., description="Transaction date")
    amount: Decimal = Field(..., description="Transaction amount")
    transaction_type: str = Field(..., description="Transaction type (Income/Expense)")
    category: str = Field(..., description="Category name")
    description: Optional[str] = Field(None, description="Transaction description")


class FinancialSummaryResponse(DecimalBaseModel):
    """Response for comprehensive financial summary."""
    total_income: Decimal = Field(..., description="Total income for period")
    total_expenses: Decimal = Field(..., description="Total expenses for period")
    net_cash_flow: Decimal = Field(..., description="Net cash flow (income - expenses)")
    income_count: int = Field(..., description="Number of income transactions")
    expense_count: int = Field(..., description="Number of expense transactions")
    top_income_categories: List[TopCategory] = Field(..., description="Top income categories")
    top_expense_categories: List[TopCategory] = Field(..., description="Top expense categories")
    recent_transactions: List[RecentTransaction] = Field(..., description="Recent transactions")
    financial_health: FinancialHealthResponse = Field(..., description="Financial health indicators")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "total_income": "10000.00",
                "total_expenses": "1850.00",
                "net_cash_flow": "8150.00",
                "income_count": 2,
                "expense_count": 3,
                "top_income_categories": [
                    {
                        "category": "Salary",
                        "amount": "10000.00",
                        "count": 2,
                        "percentage": 100.0
                    }
                ],
                "top_expense_categories": [
                    {
                        "category": "Rent",
                        "amount": "1500.00",
                        "count": 1,
                        "percentage": 81.08
                    }
                ],
                "recent_transactions": [
                    {
                        "transaction_id": 1,
                        "transaction_date": "2025-01-15",
                        "amount": "5000.00",
                        "transaction_type": "Income",
                        "category": "Salary",
                        "description": "Monthly salary"
                    }
                ],
                "financial_health": {
                    "income_to_expense_ratio": 5.41,
                    "savings_rate": 0.815,
                    "average_daily_income": "166.67",
                    "average_daily_expense": "30.83",
                    "net_daily_cash_flow": "135.84",
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31"
                },
                "period_start": "2025-01-01",
                "period_end": "2025-01-31",
                "mode": "analysis"
            }
        }


class IncomeExpenseComparisonResponse(BaseModel):
    """Response for income vs expense comparison."""
    income_analysis: IncomeAnalysisResponse = Field(..., description="Income analysis")
    expense_analysis: ExpenseAnalysisResponse = Field(..., description="Expense analysis")
    cash_flow: CashFlowResponse = Field(..., description="Cash flow summary")
    comparison_metrics: Dict[str, Any] = Field(..., description="Comparison metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "income_analysis": {
                    "total_income": "10000.00",
                    "transaction_count": 2,
                    "average_transaction": "5000.00",
                    "breakdown_by_category": {},
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "mode": "analysis"
                },
                "expense_analysis": {
                    "total_expenses": "1850.00",
                    "transaction_count": 3,
                    "average_transaction": "616.67",
                    "breakdown_by_category": {},
                    "top_categories": [],
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "mode": "analysis"
                },
                "cash_flow": {
                    "net_cash_flow": "8150.00",
                    "total_income": "10000.00",
                    "total_expenses": "1850.00",
                    "income_count": 2,
                    "expense_count": 3,
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "mode": "analysis"
                },
                "comparison_metrics": {
                    "income_to_expense_ratio": 5.41,
                    "expense_to_income_percentage": 18.5
                }
            }
        }


class CategoryBreakdownItem(DecimalBaseModel):
    """Category breakdown item with details."""
    category_id: int = Field(..., description="Category ID")
    category_name: str = Field(..., description="Category name")
    category_type: str = Field(..., description="Category type (Income/Expense)")
    total_amount: Decimal = Field(..., description="Total amount for category")
    transaction_count: int = Field(..., description="Number of transactions")
    average_amount: Decimal = Field(..., description="Average transaction amount")
    percentage_of_total: float = Field(..., description="Percentage of total income/expenses")
    percentage_of_all: float = Field(..., description="Percentage of all transactions")


class CategoryBreakdownResponse(DecimalBaseModel):
    """Response for category breakdown analysis."""
    income_categories: List[CategoryBreakdownItem] = Field(..., description="Income category breakdown")
    expense_categories: List[CategoryBreakdownItem] = Field(..., description="Expense category breakdown")
    total_income: Decimal = Field(..., description="Total income")
    total_expenses: Decimal = Field(..., description="Total expenses")
    period_start: Optional[date] = Field(None, description="Analysis period start date")
    period_end: Optional[date] = Field(None, description="Analysis period end date")
    mode: AnalysisModeEnum = Field(..., description="Analysis mode used")

    class Config:
        json_schema_extra = {
            "example": {
                "income_categories": [
                    {
                        "category_id": 1,
                        "category_name": "Salary",
                        "category_type": "Income",
                        "total_amount": "10000.00",
                        "transaction_count": 2,
                        "average_amount": "5000.00",
                        "percentage_of_total": 100.0,
                        "percentage_of_all": 84.4
                    }
                ],
                "expense_categories": [
                    {
                        "category_id": 2,
                        "category_name": "Rent",
                        "category_type": "Expense",
                        "total_amount": "1500.00",
                        "transaction_count": 1,
                        "average_amount": "1500.00",
                        "percentage_of_total": 81.08,
                        "percentage_of_all": 12.7
                    }
                ],
                "total_income": "10000.00",
                "total_expenses": "1850.00",
                "period_start": "2025-01-01",
                "period_end": "2025-01-31",
                "mode": "analysis"
            }
        }

