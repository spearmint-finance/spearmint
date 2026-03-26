"""Analysis API endpoints.

Provides endpoints for income, expense, cash flow, and financial health analysis.  

"""

from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas.analysis import (
    DateRangeRequest,
    IncomeAnalysisResponse,
    ExpenseAnalysisResponse,
    CashFlowResponse,
    TrendsResponse,
    CashFlowTrendsResponse,
    FinancialHealthResponse,
    PeriodComparisonResponse,
    TimePeriodEnum,
    AnalysisModeEnum,
    CategoryBreakdown,
    TopCategory,
    TrendDataPoint,
    CashFlowTrendPoint,
    FinancialSummaryResponse,
    RecentTransaction,
    IncomeExpenseComparisonResponse,
    CategoryBreakdownResponse,
    CategoryBreakdownItem
)
from ...services.analysis_service import (
    AnalysisService,
    DateRange,
    AnalysisMode,
    TimePeriod
)

router = APIRouter()


def _convert_mode(mode: AnalysisModeEnum) -> AnalysisMode:
    """Convert API mode enum to service mode enum."""
    if mode == AnalysisModeEnum.ANALYSIS:
        return AnalysisMode.ANALYSIS
    elif mode == AnalysisModeEnum.WITH_CAPITAL:
        return AnalysisMode.WITH_CAPITAL
    else:
        return AnalysisMode.COMPLETE


def _convert_period(period: TimePeriodEnum) -> TimePeriod:
    """Convert API period enum to service period enum."""
    return TimePeriod(period.value)


@router.get("/analysis/income", response_model=IncomeAnalysisResponse)
def get_income_analysis(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get income analysis for a period.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        IncomeAnalysisResponse: Income analysis results
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.analyze_income(date_range=date_range, mode=_convert_mode(mode), entity_id=entity_id)
    
    # Convert breakdown to Pydantic models
    breakdown = {
        cat: CategoryBreakdown(**data)
        for cat, data in result.breakdown_by_category.items()
    }
    
    return IncomeAnalysisResponse(
        total_income=result.total_income,
        transaction_count=result.transaction_count,
        average_transaction=result.average_transaction,
        breakdown_by_category=breakdown,
        period_start=result.period_start,
        period_end=result.period_end,
        mode=AnalysisModeEnum(result.mode.value)
    )


@router.get("/analysis/income/trends", response_model=TrendsResponse)
def get_income_trends(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    period: TimePeriodEnum = Query(TimePeriodEnum.MONTHLY, description="Period granularity"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get income trends over time.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        period: Period granularity (daily, weekly, monthly, etc.)
        mode: Analysis mode
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        TrendsResponse: Income trend data
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    trends = service.get_income_trends(
        date_range=date_range,
        period=_convert_period(period),
        mode=_convert_mode(mode),
        entity_id=entity_id
    )
    
    return TrendsResponse(
        trends=[TrendDataPoint(period=t.period, value=t.value, count=t.count) for t in trends],
        period_type=period,
        mode=mode
    )


@router.get("/analysis/expenses", response_model=ExpenseAnalysisResponse)
def get_expense_analysis(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    top_n: int = Query(10, ge=1, le=50, description="Number of top categories to return"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get expense analysis for a period.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        top_n: Number of top categories to return
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        ExpenseAnalysisResponse: Expense analysis results
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.analyze_expenses(date_range=date_range, mode=_convert_mode(mode), top_n=top_n, entity_id=entity_id)
    
    # Convert breakdown to Pydantic models
    breakdown = {
        cat: CategoryBreakdown(**data)
        for cat, data in result.breakdown_by_category.items()
    }
    
    # Convert top categories
    top_categories = [TopCategory(**cat) for cat in result.top_categories]
    
    return ExpenseAnalysisResponse(
        total_expenses=result.total_expenses,
        transaction_count=result.transaction_count,
        average_transaction=result.average_transaction,
        breakdown_by_category=breakdown,
        top_categories=top_categories,
        period_start=result.period_start,
        period_end=result.period_end,
        mode=AnalysisModeEnum(result.mode.value)
    )


@router.get("/analysis/expenses/trends", response_model=TrendsResponse)
def get_expense_trends(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    period: TimePeriodEnum = Query(TimePeriodEnum.MONTHLY, description="Period granularity"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get expense trends over time.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        period: Period granularity (daily, weekly, monthly, etc.)
        mode: Analysis mode
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        TrendsResponse: Expense trend data
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    trends = service.get_expense_trends(
        date_range=date_range,
        period=_convert_period(period),
        mode=_convert_mode(mode),
        entity_id=entity_id
    )
    
    return TrendsResponse(
        trends=[TrendDataPoint(period=t.period, value=t.value, count=t.count) for t in trends],
        period_type=period,
        mode=mode
    )


@router.get("/analysis/cashflow", response_model=CashFlowResponse)
def get_cash_flow_analysis(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get cash flow analysis for a period.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        CashFlowResponse: Cash flow analysis results
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.analyze_cash_flow(date_range=date_range, mode=_convert_mode(mode), entity_id=entity_id)
    
    return CashFlowResponse(
        net_cash_flow=result.net_cash_flow,
        total_income=result.total_income,
        total_expenses=result.total_expenses,
        income_count=result.income_count,
        expense_count=result.expense_count,
        period_start=result.period_start,
        period_end=result.period_end,
        mode=AnalysisModeEnum(result.mode.value)
    )


@router.get("/analysis/cashflow/trends", response_model=CashFlowTrendsResponse)
def get_cash_flow_trends(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    period: TimePeriodEnum = Query(TimePeriodEnum.MONTHLY, description="Period granularity"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get cash flow trends over time.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        period: Period granularity (daily, weekly, monthly, etc.)
        mode: Analysis mode
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        CashFlowTrendsResponse: Cash flow trend data
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    trends = service.get_cash_flow_trends(
        date_range=date_range,
        period=_convert_period(period),
        mode=_convert_mode(mode),
        entity_id=entity_id
    )
    
    return CashFlowTrendsResponse(
        trends=[CashFlowTrendPoint(**t) for t in trends],
        period_type=period,
        mode=mode
    )


@router.get("/analysis/health", response_model=FinancialHealthResponse)
def get_financial_health(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get financial health indicators.

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis, with_capital, or complete)
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        FinancialHealthResponse: Financial health indicators
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.get_financial_health_indicators(date_range=date_range, mode=_convert_mode(mode), entity_id=entity_id)

    return FinancialHealthResponse(
        income_to_expense_ratio=result.income_to_expense_ratio,
        savings_rate=result.savings_rate,
        average_daily_income=result.average_daily_income,
        average_daily_expense=result.average_daily_expense,
        net_daily_cash_flow=result.net_daily_cash_flow,
        period_start=result.period_start,
        period_end=result.period_end
    )

@router.get("/analysis/summary", response_model=FinancialSummaryResponse)
def get_financial_summary(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    top_n: int = Query(5, ge=1, le=20, description="Number of top categories to return"),
    recent_count: int = Query(10, ge=1, le=50, description="Number of recent transactions to return"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive financial summary.

    This endpoint provides a complete financial overview including:
    - Total income, expenses, and net cash flow
    - Top income and expense categories
    - Recent transactions
    - Financial health indicators

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        top_n: Number of top categories to return
        recent_count: Number of recent transactions to return
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        FinancialSummaryResponse: Comprehensive financial summary
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.get_financial_summary(
        date_range=date_range,
        mode=_convert_mode(mode),
        top_n=top_n,
        recent_count=recent_count,
        entity_id=entity_id
    )

    # Convert to response model
    return FinancialSummaryResponse(
        total_income=result['total_income'],
        total_expenses=result['total_expenses'],
        net_cash_flow=result['net_cash_flow'],
        income_count=result['income_count'],
        expense_count=result['expense_count'],
        top_income_categories=[TopCategory(**cat) for cat in result['top_income_categories']],
        top_expense_categories=[TopCategory(**cat) for cat in result['top_expense_categories']],
        recent_transactions=[RecentTransaction(**txn) for txn in result['recent_transactions']],
        financial_health=FinancialHealthResponse(**result['financial_health']),
        period_start=result['period_start'],
        period_end=result['period_end'],
        mode=AnalysisModeEnum(result['mode'].value)
    )


@router.get("/analysis/income-expense", response_model=IncomeExpenseComparisonResponse)
def get_income_expense_comparison(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    top_n: int = Query(10, ge=1, le=50, description="Number of top categories to return"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get combined income and expense comparison.

    This endpoint provides a side-by-side comparison of income and expenses including:
    - Detailed income analysis
    - Detailed expense analysis
    - Cash flow summary
    - Comparison metrics (ratios, percentages)

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        top_n: Number of top categories to return
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        IncomeExpenseComparisonResponse: Income vs expense comparison
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.get_income_expense_comparison(
        date_range=date_range,
        mode=_convert_mode(mode),
        top_n=top_n,
        entity_id=entity_id
    )

    # Convert breakdown to Pydantic models for income
    income_breakdown = {
        cat: CategoryBreakdown(**data)
        for cat, data in result['income_analysis'].breakdown_by_category.items()
    }

    # Convert breakdown to Pydantic models for expenses
    expense_breakdown = {
        cat: CategoryBreakdown(**data)
        for cat, data in result['expense_analysis'].breakdown_by_category.items()
    }

    return IncomeExpenseComparisonResponse(
        income_analysis=IncomeAnalysisResponse(
            total_income=result['income_analysis'].total_income,
            transaction_count=result['income_analysis'].transaction_count,
            average_transaction=result['income_analysis'].average_transaction,
            breakdown_by_category=income_breakdown,
            period_start=result['income_analysis'].period_start,
            period_end=result['income_analysis'].period_end,
            mode=AnalysisModeEnum(result['income_analysis'].mode.value)
        ),
        expense_analysis=ExpenseAnalysisResponse(
            total_expenses=result['expense_analysis'].total_expenses,
            transaction_count=result['expense_analysis'].transaction_count,
            average_transaction=result['expense_analysis'].average_transaction,
            breakdown_by_category=expense_breakdown,
            top_categories=[TopCategory(**cat) for cat in result['expense_analysis'].top_categories],
            period_start=result['expense_analysis'].period_start,
            period_end=result['expense_analysis'].period_end,
            mode=AnalysisModeEnum(result['expense_analysis'].mode.value)
        ),
        cash_flow=CashFlowResponse(
            net_cash_flow=result['cash_flow'].net_cash_flow,
            total_income=result['cash_flow'].total_income,
            total_expenses=result['cash_flow'].total_expenses,
            income_count=result['cash_flow'].income_count,
            expense_count=result['cash_flow'].expense_count,
            period_start=result['cash_flow'].period_start,
            period_end=result['cash_flow'].period_end,
            mode=AnalysisModeEnum(result['cash_flow'].mode.value)
        ),
        comparison_metrics=result['comparison_metrics']
    )


@router.get("/analysis/category-breakdown", response_model=CategoryBreakdownResponse)
def get_category_breakdown(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get detailed category breakdown for income and expenses.

    This endpoint provides a comprehensive breakdown of all categories including:
    - Income categories with totals, counts, and percentages
    - Expense categories with totals, counts, and percentages
    - Percentage of total for each category type
    - Percentage of all transactions

    Args:
        start_date: Start date for analysis
        end_date: End date for analysis
        mode: Analysis mode (analysis or complete)
        entity_id: Entity ID to filter by
        db: Database session

    Returns:
        CategoryBreakdownResponse: Detailed category breakdown
    """
    service = AnalysisService(db)

    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None
    result = service.get_category_breakdown(
        date_range=date_range,
        mode=_convert_mode(mode),
        entity_id=entity_id
    )

    return CategoryBreakdownResponse(
        income_categories=[CategoryBreakdownItem(**cat) for cat in result['income_categories']],
        expense_categories=[CategoryBreakdownItem(**cat) for cat in result['expense_categories']],
        total_income=result['total_income'],
        total_expenses=result['total_expenses'],
        period_start=result['period_start'],
        period_end=result['period_end'],
        mode=AnalysisModeEnum(result['mode'].value)
    )


@router.get("/analysis/expenses/category-trends")
def get_expense_category_trends(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    period: TimePeriodEnum = Query(TimePeriodEnum.MONTHLY, description="Period granularity"),
    mode: AnalysisModeEnum = Query(AnalysisModeEnum.ANALYSIS, description="Analysis mode"),
    top_n: int = Query(8, description="Number of top categories to include"),
    entity_id: Optional[int] = Query(None, description="Entity ID to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get expense trends broken down by category for stacked charts.

    Returns expense amounts for each category for each time period,
    allowing for accurate stacked bar charts that show actual expenses
    per period rather than proportional distributions.
    """
    service = AnalysisService(db)
    date_range = DateRange(start_date=start_date, end_date=end_date) if start_date or end_date else None

    result = service.get_expense_category_trends(
        period=_convert_period(period),
        date_range=date_range,
        mode=_convert_mode(mode),
        top_n=top_n,
        entity_id=entity_id
    )

    return result


