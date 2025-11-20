"""
Pydantic schemas for report endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum


class ReportFormatEnum(str, Enum):
    """Report export formats."""
    JSON = "json"
    CSV = "csv"


class ReportTypeEnum(str, Enum):
    """Types of reports available."""
    SUMMARY = "summary"
    INCOME_DETAIL = "income_detail"
    EXPENSE_DETAIL = "expense_detail"
    CASHFLOW = "cashflow"
    CATEGORY_BREAKDOWN = "category_breakdown"
    RECONCILIATION = "reconciliation"
    BALANCE = "balance"


class AnalysisModeEnum(str, Enum):
    """Analysis mode for reports."""
    ANALYSIS = "analysis"
    COMPLETE = "complete"


class ReportRequest(BaseModel):
    """Request parameters for generating a report."""
    start_date: Optional[date] = Field(None, description="Start date for the report period")
    end_date: Optional[date] = Field(None, description="End date for the report period")
    mode: AnalysisModeEnum = Field(
        AnalysisModeEnum.ANALYSIS,
        description="Analysis mode: 'analysis' excludes transfers, 'complete' includes all"
    )
    format: ReportFormatEnum = Field(
        ReportFormatEnum.JSON,
        description="Export format for the report"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
                "mode": "analysis",
                "format": "json"
            }
        }


class ReportPeriod(BaseModel):
    """Report period information."""
    start_date: str = Field(..., description="Start date of the period")
    end_date: str = Field(..., description="End date of the period")
    days: int = Field(..., description="Number of days in the period")


class CategorySummary(BaseModel):
    """Category summary in a report."""
    category: str = Field(..., description="Category name")
    amount: float = Field(..., description="Total amount for the category")
    percentage: float = Field(..., description="Percentage of total")


class CategoryDetail(BaseModel):
    """Detailed category information."""
    category: str = Field(..., description="Category name")
    total: float = Field(..., description="Total amount")
    count: int = Field(..., description="Number of transactions")
    average: float = Field(..., description="Average transaction amount")
    percentage: float = Field(..., description="Percentage of total")


class IncomeSummary(BaseModel):
    """Income summary in a report."""
    total: float = Field(..., description="Total income")
    transaction_count: int = Field(..., description="Number of income transactions")
    average_transaction: float = Field(..., description="Average income transaction")
    top_categories: List[CategorySummary] = Field(..., description="Top 5 income categories")


class ExpenseSummary(BaseModel):
    """Expense summary in a report."""
    total: float = Field(..., description="Total expenses")
    transaction_count: int = Field(..., description="Number of expense transactions")
    average_transaction: float = Field(..., description="Average expense transaction")
    top_categories: List[CategorySummary] = Field(..., description="Top 5 expense categories")


class CashflowSummary(BaseModel):
    """Cash flow summary in a report."""
    net_cashflow: float = Field(..., description="Net cash flow (income - expenses)")
    total_income: float = Field(..., description="Total income")
    total_expenses: float = Field(..., description="Total expenses")


class HealthIndicators(BaseModel):
    """Financial health indicators."""
    income_to_expense_ratio: Optional[float] = Field(None, description="Income to expense ratio")
    savings_rate: Optional[float] = Field(None, description="Savings rate as percentage")
    average_daily_income: float = Field(..., description="Average daily income")
    average_daily_expense: float = Field(..., description="Average daily expense")
    average_daily_cashflow: float = Field(..., description="Average daily cash flow")


class SummaryReportResponse(BaseModel):
    """Response for summary report."""
    report_type: str = Field(..., description="Type of report")
    period: ReportPeriod = Field(..., description="Report period")
    mode: str = Field(..., description="Analysis mode used")
    income: IncomeSummary = Field(..., description="Income summary")
    expenses: ExpenseSummary = Field(..., description="Expense summary")
    cashflow: CashflowSummary = Field(..., description="Cash flow summary")
    health_indicators: HealthIndicators = Field(..., description="Financial health indicators")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_type": "summary",
                "period": {
                    "start_date": "2025-01-01",
                    "end_date": "2025-01-31",
                    "days": 31
                },
                "mode": "analysis",
                "income": {
                    "total": 5000.00,
                    "transaction_count": 10,
                    "average_transaction": 500.00,
                    "top_categories": [
                        {"category": "Salary", "amount": 4500.00, "percentage": 90.0}
                    ]
                },
                "expenses": {
                    "total": 3000.00,
                    "transaction_count": 50,
                    "average_transaction": 60.00,
                    "top_categories": [
                        {"category": "Groceries", "amount": 800.00, "percentage": 26.67}
                    ]
                },
                "cashflow": {
                    "net_cashflow": 2000.00,
                    "total_income": 5000.00,
                    "total_expenses": 3000.00
                },
                "health_indicators": {
                    "income_to_expense_ratio": 1.67,
                    "savings_rate": 40.0,
                    "average_daily_income": 161.29,
                    "average_daily_expense": 96.77,
                    "average_daily_cashflow": 64.52
                }
            }
        }


class IncomeDetailReportResponse(BaseModel):
    """Response for detailed income report."""
    report_type: str = Field(..., description="Type of report")
    period: ReportPeriod = Field(..., description="Report period")
    mode: str = Field(..., description="Analysis mode used")
    total_income: float = Field(..., description="Total income")
    transaction_count: int = Field(..., description="Number of transactions")
    average_transaction: float = Field(..., description="Average transaction amount")
    categories: List[CategoryDetail] = Field(..., description="Income by category")


class ExpenseDetailReportResponse(BaseModel):
    """Response for detailed expense report."""
    report_type: str = Field(..., description="Type of report")
    period: ReportPeriod = Field(..., description="Report period")
    mode: str = Field(..., description="Analysis mode used")
    total_expenses: float = Field(..., description="Total expenses")
    transaction_count: int = Field(..., description="Number of transactions")
    average_transaction: float = Field(..., description="Average transaction amount")
    categories: List[CategoryDetail] = Field(..., description="Expenses by category")


class TransactionDetail(BaseModel):
    """Transaction detail for reconciliation report."""
    date: str = Field(..., description="Transaction date")
    description: str = Field(..., description="Transaction description")
    category: str = Field(..., description="Category name")
    type: str = Field(..., description="Transaction type (Income/Expense)")
    amount: float = Field(..., description="Transaction amount")
    classification: str = Field(..., description="Transaction classification")
    source: str = Field(..., description="Data source")


class ReconciliationSummary(BaseModel):
    """Summary for reconciliation report."""
    total_income: float = Field(..., description="Total income (all transactions)")
    total_expenses: float = Field(..., description="Total expenses (all transactions)")
    net_cashflow: float = Field(..., description="Net cash flow")
    transaction_count: int = Field(..., description="Total number of transactions")


class ReconciliationReportResponse(BaseModel):
    """Response for reconciliation report."""
    report_type: str = Field(..., description="Type of report")
    period: ReportPeriod = Field(..., description="Report period")
    mode: str = Field(..., description="Analysis mode (always 'complete' for reconciliation)")
    summary: ReconciliationSummary = Field(..., description="Summary statistics")
    transactions: List[TransactionDetail] = Field(..., description="All transactions in period")
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_type": "reconciliation",
                "period": {
                    "start_date": "2025-01-01",
                    "end_date": "2025-01-31",
                    "days": 31
                },
                "mode": "complete",
                "summary": {
                    "total_income": 5500.00,
                    "total_expenses": 3200.00,
                    "net_cashflow": 2300.00,
                    "transaction_count": 75
                },
                "transactions": [
                    {
                        "date": "2025-01-31",
                        "description": "Salary",
                        "category": "Income",
                        "type": "Income",
                        "amount": 5000.00,
                        "classification": "Standard Transaction",
                        "source": "Manual Entry"
                    }
                ]
            }
        }


class AccountBalanceDetail(BaseModel):
    """Detail for a single account balance."""
    account_name: str
    account_type: str
    balance: float
    transaction_count: int
    income_sum: float
    expense_sum: float

class BalanceSummary(BaseModel):
    """High-level balance summary."""
    total_assets: float
    total_liabilities: float
    net_worth: float

class BalanceReportResponse(BaseModel):
    """Response for balance report."""
    report_type: str = Field(..., description="Type of report (balance)")
    summary: BalanceSummary
    accounts: List[AccountBalanceDetail]
    potential_issues: List[str]