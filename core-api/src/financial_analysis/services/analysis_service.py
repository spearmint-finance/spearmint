"""
Analysis service for financial data.

Provides income, expense, cash flow, and financial health analysis
with classification-aware calculations.
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import numpy as np
from sqlalchemy import func, and_, or_, text
from sqlalchemy.orm import Session

from ..database.models import (
    Transaction, Category, TransactionClassification
)


class TimePeriod(str, Enum):
    """Time period granularity for analysis."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class AnalysisMode(str, Enum):
    """Analysis mode for transaction filtering."""
    ANALYSIS = "analysis"  # Excludes transfers and capital expenses (operating only)
    WITH_CAPITAL = "with_capital"  # Excludes transfers but includes capital expenses
    COMPLETE = "complete"  # Includes all transactions


@dataclass
class DateRange:
    """Date range for analysis."""
    start_date: Optional[date] = None
    end_date: Optional[date] = None


@dataclass
class IncomeAnalysisResult:
    """Result of income analysis."""
    total_income: Decimal
    transaction_count: int
    average_transaction: Decimal
    breakdown_by_category: Dict[str, Dict[str, Any]]
    period_start: Optional[date]
    period_end: Optional[date]
    mode: AnalysisMode


@dataclass
class ExpenseAnalysisResult:
    """Result of expense analysis."""
    total_expenses: Decimal
    transaction_count: int
    average_transaction: Decimal
    breakdown_by_category: Dict[str, Dict[str, Any]]
    top_categories: List[Dict[str, Any]]
    period_start: Optional[date]
    period_end: Optional[date]
    mode: AnalysisMode


@dataclass
class CashFlowResult:
    """Result of cash flow analysis."""
    net_cash_flow: Decimal
    total_income: Decimal
    total_expenses: Decimal
    income_count: int
    expense_count: int
    period_start: Optional[date]
    period_end: Optional[date]
    mode: AnalysisMode


@dataclass
class FinancialHealthIndicators:
    """Financial health indicators."""
    income_to_expense_ratio: Optional[float]
    savings_rate: Optional[float]
    average_daily_income: Decimal
    average_daily_expense: Decimal
    net_daily_cash_flow: Decimal
    period_start: Optional[date]
    period_end: Optional[date]


@dataclass
class TrendDataPoint:
    """Single data point in a trend."""
    period: str
    value: Decimal
    count: int


class AnalysisService:
    """Service for financial analysis operations."""
    
    def __init__(self, db: Session):
        """
        Initialize analysis service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    # ==================== Income Analysis ====================
    
    def analyze_income(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> IncomeAnalysisResult:
        """
        Analyze income for a given period.
        
        Args:
            date_range: Date range for analysis
            mode: Analysis mode (analysis or complete)
            
        Returns:
            IncomeAnalysisResult: Income analysis results
        """
        # Build base query
        query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Income'
        )
        
        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS or mode == AnalysisMode.WITH_CAPITAL:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)  # Always exclude transfers

            # For both ANALYSIS and WITH_CAPITAL modes: exclude non-operating income
            # (e.g., credit card receipts, loan disbursements, reimbursements)
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )
            query = query.filter(
                or_(
                    TransactionClassification.exclude_from_income_calc == 0,
                    TransactionClassification.exclude_from_income_calc == None
                )
            )
        
        # Apply date range
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)
        
        # Get transactions
        transactions = query.all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions)
        transaction_count = len(transactions)
        average_transaction = total_income / transaction_count if transaction_count > 0 else Decimal(0)
        
        # Breakdown by category
        breakdown = self._breakdown_by_category(transactions)
        
        return IncomeAnalysisResult(
            total_income=total_income,
            transaction_count=transaction_count,
            average_transaction=average_transaction,
            breakdown_by_category=breakdown,
            period_start=date_range.start_date if date_range else None,
            period_end=date_range.end_date if date_range else None,
            mode=mode
        )
    
    def get_income_trends(
        self,
        date_range: Optional[DateRange] = None,
        period: TimePeriod = TimePeriod.MONTHLY,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> List[TrendDataPoint]:
        """
        Get income trends over time.
        
        Args:
            date_range: Date range for analysis
            period: Time period granularity
            mode: Analysis mode
            
        Returns:
            List[TrendDataPoint]: Trend data points
        """
        # Build query
        query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Income'
        )
        
        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS or mode == AnalysisMode.WITH_CAPITAL:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)  # Exclude transfers
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )
            query = query.filter(
                or_(
                    TransactionClassification.exclude_from_income_calc == 0,
                    TransactionClassification.exclude_from_income_calc == None
                )
            )

        # Apply date range
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)
        
        # Get transactions
        transactions = query.all()

        # Convert to DataFrame for easier grouping
        if not transactions:
            return []

        df = pd.DataFrame([
            {
                'date': t.transaction_date,
                'amount': float(t.amount)
            }
            for t in transactions
        ])

        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Group by period
        df['period'] = self._get_period_key(df['date'], period)
        grouped = df.groupby('period').agg({
            'amount': 'sum',
            'date': 'count'
        }).reset_index()
        
        # Convert to TrendDataPoint
        trends = [
            TrendDataPoint(
                period=row['period'],
                value=Decimal(str(row['amount'])),
                count=int(row['date'])
            )
            for _, row in grouped.iterrows()
        ]
        
        return sorted(trends, key=lambda x: x.period)

    # ==================== Expense Analysis ====================

    def analyze_expenses(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS,
        top_n: int = 10
    ) -> ExpenseAnalysisResult:
        """
        Analyze expenses for a given period.

        Args:
            date_range: Date range for analysis
            mode: Analysis mode (analysis or complete)
            top_n: Number of top categories to return

        Returns:
            ExpenseAnalysisResult: Expense analysis results
        """
        # Build base query
        query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Expense'
        )

        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS or mode == AnalysisMode.WITH_CAPITAL:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)  # Always exclude transfers

            # Join with classifications for filtering
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )

            if mode == AnalysisMode.ANALYSIS:
                # ANALYSIS mode: exclude ALL non-operating expenses (capital, CC payments, refunds, etc.)
                query = query.filter(
                    or_(
                        TransactionClassification.exclude_from_expense_calc == 0,
                        TransactionClassification.exclude_from_expense_calc == None
                    )
                )
            elif mode == AnalysisMode.WITH_CAPITAL:
                # WITH_CAPITAL mode: exclude non-operating expenses EXCEPT capital expenses
                # Include if: no classification, OR exclude_from_expense_calc=False, OR is Capital Expense
                query = query.filter(
                    or_(
                        TransactionClassification.exclude_from_expense_calc == 0,
                        TransactionClassification.exclude_from_expense_calc == None,
                        TransactionClassification.classification_name == 'Capital Expense'
                    )
                )

        # Apply date range
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)

        # Get transactions
        transactions = query.all()

        # Calculate totals
        total_expenses = sum(t.amount for t in transactions)
        transaction_count = len(transactions)
        average_transaction = total_expenses / transaction_count if transaction_count > 0 else Decimal(0)

        # Breakdown by category
        breakdown = self._breakdown_by_category(transactions)

        # Get top categories
        top_categories = sorted(
            [
                {
                    'category': cat,
                    'amount': data['total'],
                    'count': data['count'],
                    'percentage': data['percentage']
                }
                for cat, data in breakdown.items()
            ],
            key=lambda x: x['amount'],
            reverse=True
        )[:top_n]

        return ExpenseAnalysisResult(
            total_expenses=total_expenses,
            transaction_count=transaction_count,
            average_transaction=average_transaction,
            breakdown_by_category=breakdown,
            top_categories=top_categories,
            period_start=date_range.start_date if date_range else None,
            period_end=date_range.end_date if date_range else None,
            mode=mode
        )

    def get_expense_trends(
        self,
        date_range: Optional[DateRange] = None,
        period: TimePeriod = TimePeriod.MONTHLY,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> List[TrendDataPoint]:
        """
        Get expense trends over time.

        Args:
            date_range: Date range for analysis
            period: Time period granularity
            mode: Analysis mode

        Returns:
            List[TrendDataPoint]: Trend data points
        """
        # Build query
        query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Expense'
        )

        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS or mode == AnalysisMode.WITH_CAPITAL:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)  # Exclude transfers
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )

            if mode == AnalysisMode.ANALYSIS:
                # ANALYSIS mode: exclude ALL non-operating expenses
                query = query.filter(
                    or_(
                        TransactionClassification.exclude_from_expense_calc == False,
                        TransactionClassification.exclude_from_expense_calc == None
                    )
                )
            elif mode == AnalysisMode.WITH_CAPITAL:
                # WITH_CAPITAL mode: exclude non-operating expenses EXCEPT capital expenses
                query = query.filter(
                    or_(
                        TransactionClassification.exclude_from_expense_calc == 0,
                        TransactionClassification.exclude_from_expense_calc == None,
                        TransactionClassification.classification_name == 'Capital Expense'
                    )
                )

        # Apply date range
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)

        # Get transactions
        transactions = query.all()

        # Convert to DataFrame for easier grouping
        if not transactions:
            return []

        df = pd.DataFrame([
            {
                'date': t.transaction_date,
                'amount': float(t.amount)
            }
            for t in transactions
        ])

        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Group by period
        df['period'] = self._get_period_key(df['date'], period)
        grouped = df.groupby('period').agg({
            'amount': 'sum',
            'date': 'count'
        }).reset_index()

        # Convert to TrendDataPoint
        trends = [
            TrendDataPoint(
                period=row['period'],
                value=Decimal(str(row['amount'])),
                count=int(row['date'])
            )
            for _, row in grouped.iterrows()
        ]

        return sorted(trends, key=lambda x: x.period)

    # ==================== Cash Flow Analysis ====================

    def analyze_cash_flow(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> CashFlowResult:
        """
        Analyze cash flow (income - expenses).

        Args:
            date_range: Date range for analysis
            mode: Analysis mode

        Returns:
            CashFlowResult: Cash flow analysis results
        """
        # Get income analysis
        income_result = self.analyze_income(date_range, mode)

        # Get expense analysis
        expense_result = self.analyze_expenses(date_range, mode)

        # Calculate net cash flow
        # Note: expenses are stored as positive values, so we subtract them
        net_cash_flow = income_result.total_income - expense_result.total_expenses

        return CashFlowResult(
            net_cash_flow=net_cash_flow,
            total_income=income_result.total_income,
            total_expenses=expense_result.total_expenses,
            income_count=income_result.transaction_count,
            expense_count=expense_result.transaction_count,
            period_start=date_range.start_date if date_range else None,
            period_end=date_range.end_date if date_range else None,
            mode=mode
        )

    def get_cash_flow_trends(
        self,
        date_range: Optional[DateRange] = None,
        period: TimePeriod = TimePeriod.MONTHLY,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> List[Dict[str, Any]]:
        """
        Get cash flow trends over time.

        Args:
            date_range: Date range for analysis
            period: Time period granularity
            mode: Analysis mode

        Returns:
            List[Dict]: Cash flow trend data with income, expenses, and net
        """
        # Get income and expense trends
        income_trends = self.get_income_trends(date_range, period, mode)
        expense_trends = self.get_expense_trends(date_range, period, mode)

        # Create a dictionary for easy lookup
        income_dict = {t.period: t for t in income_trends}
        expense_dict = {t.period: t for t in expense_trends}

        # Get all unique periods
        all_periods = sorted(set(income_dict.keys()) | set(expense_dict.keys()))

        # Combine into cash flow trends
        trends = []
        for period_key in all_periods:
            income_val = income_dict.get(period_key, TrendDataPoint(period_key, Decimal(0), 0))
            expense_val = expense_dict.get(period_key, TrendDataPoint(period_key, Decimal(0), 0))

            trends.append({
                'period': period_key,
                'income': income_val.value,
                'expenses': expense_val.value,
                # Expenses are stored as positive values, so we subtract them
                'net_cash_flow': income_val.value - expense_val.value,
                'income_count': income_val.count,
                'expense_count': expense_val.count
            })

        return trends

    # ==================== Financial Health Indicators ====================

    def get_financial_health_indicators(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> FinancialHealthIndicators:
        """
        Calculate financial health indicators.

        Args:
            date_range: Date range for analysis
            mode: Analysis mode (ANALYSIS, WITH_CAPITAL, or COMPLETE)

        Returns:
            FinancialHealthIndicators: Financial health metrics
        """
        # Get cash flow analysis using the specified mode
        cash_flow = self.analyze_cash_flow(date_range, mode)

        # Calculate number of days in period
        if date_range and date_range.start_date and date_range.end_date:
            days = (date_range.end_date - date_range.start_date).days + 1
        else:
            # If no date range, use all transactions to estimate
            first_tx = self.db.query(Transaction).order_by(Transaction.transaction_date).first()
            last_tx = self.db.query(Transaction).order_by(Transaction.transaction_date.desc()).first()
            if first_tx and last_tx:
                days = (last_tx.transaction_date - first_tx.transaction_date).days + 1
            else:
                days = 1

        # Calculate daily averages
        average_daily_income = cash_flow.total_income / days if days > 0 else Decimal(0)
        average_daily_expense = cash_flow.total_expenses / days if days > 0 else Decimal(0)
        net_daily_cash_flow = cash_flow.net_cash_flow / days if days > 0 else Decimal(0)

        # Calculate ratios
        income_to_expense_ratio = None
        if cash_flow.total_expenses != 0:
            # Expenses are stored as positive values
            income_to_expense_ratio = float(cash_flow.total_income / cash_flow.total_expenses)

        savings_rate = None
        if cash_flow.total_income > 0:
            savings_rate = float(cash_flow.net_cash_flow / cash_flow.total_income)

        return FinancialHealthIndicators(
            income_to_expense_ratio=income_to_expense_ratio,
            savings_rate=savings_rate,
            average_daily_income=average_daily_income,
            average_daily_expense=average_daily_expense,
            net_daily_cash_flow=net_daily_cash_flow,
            period_start=date_range.start_date if date_range else None,
            period_end=date_range.end_date if date_range else None
        )

    # ==================== Helper Methods ====================

    def _breakdown_by_category(self, transactions: List[Transaction]) -> Dict[str, Dict[str, Any]]:
        """
        Break down transactions by category.

        Args:
            transactions: List of transactions

        Returns:
            Dict: Category breakdown with totals and percentages
        """
        if not transactions:
            return {}

        # Group by category
        category_totals = {}
        for tx in transactions:
            category_name = tx.category.category_name if tx.category else "Uncategorized"

            if category_name not in category_totals:
                category_totals[category_name] = {
                    'total': Decimal(0),
                    'count': 0,
                    'average': Decimal(0)
                }

            category_totals[category_name]['total'] += tx.amount
            category_totals[category_name]['count'] += 1

        # Calculate averages and percentages
        grand_total = sum(t.amount for t in transactions)

        for data in category_totals.values():
            data['average'] = data['total'] / data['count'] if data['count'] > 0 else Decimal(0)
            # Use absolute value for percentage calculation since expenses are negative
            data['percentage'] = float(abs(data['total']) / abs(grand_total) * 100) if grand_total != 0 else 0.0

        return category_totals

    def _get_period_key(self, dates: pd.Series, period: TimePeriod) -> pd.Series:
        """
        Get period key for grouping.

        Args:
            dates: Series of dates
            period: Time period granularity

        Returns:
            Series: Period keys
        """
        if period == TimePeriod.DAILY:
            return dates.dt.strftime('%Y-%m-%d')
        elif period == TimePeriod.WEEKLY:
            return dates.dt.strftime('%Y-W%U')
        elif period == TimePeriod.MONTHLY:
            return dates.dt.strftime('%Y-%m')
        elif period == TimePeriod.QUARTERLY:
            return dates.dt.to_period('Q').astype(str)
        elif period == TimePeriod.YEARLY:
            return dates.dt.strftime('%Y')
        else:
            return dates.dt.strftime('%Y-%m')

    # ==================== Comparison Methods ====================

    def compare_periods(
        self,
        period1: DateRange,
        period2: DateRange,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> Dict[str, Any]:
        """
        Compare two time periods.

        Args:
            period1: First period
            period2: Second period
            mode: Analysis mode

        Returns:
            Dict: Comparison results
        """
        # Get cash flow for both periods
        cf1 = self.analyze_cash_flow(period1, mode)
        cf2 = self.analyze_cash_flow(period2, mode)

        # Calculate differences
        income_diff = cf1.total_income - cf2.total_income
        expense_diff = cf1.total_expenses - cf2.total_expenses
        net_diff = cf1.net_cash_flow - cf2.net_cash_flow

        # Calculate percentage changes
        income_pct = float(income_diff / cf2.total_income * 100) if cf2.total_income > 0 else None
        expense_pct = float(expense_diff / cf2.total_expenses * 100) if cf2.total_expenses > 0 else None
        net_pct = float(net_diff / cf2.net_cash_flow * 100) if cf2.net_cash_flow != 0 else None

        return {
            'period1': {
                'start': period1.start_date,
                'end': period1.end_date,
                'income': cf1.total_income,
                'expenses': cf1.total_expenses,
                'net_cash_flow': cf1.net_cash_flow
            },
            'period2': {
                'start': period2.start_date,
                'end': period2.end_date,
                'income': cf2.total_income,
                'expenses': cf2.total_expenses,
                'net_cash_flow': cf2.net_cash_flow
            },
            'differences': {
                'income': income_diff,
                'expenses': expense_diff,
                'net_cash_flow': net_diff
            },
            'percentage_changes': {
                'income': income_pct,
                'expenses': expense_pct,
                'net_cash_flow': net_pct
            }
        }

    def get_financial_summary(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS,
        top_n: int = 5,
        recent_count: int = 10
    ) -> Dict[str, Any]:
        """
        Get comprehensive financial summary.

        Args:
            date_range: Date range for analysis
            mode: Analysis mode (analysis or complete)
            top_n: Number of top categories to return
            recent_count: Number of recent transactions to return

        Returns:
            Dictionary with comprehensive financial summary
        """
        # Get income, expense, and cash flow analysis
        income_result = self.analyze_income(date_range=date_range, mode=mode)
        expense_result = self.analyze_expenses(date_range=date_range, mode=mode, top_n=top_n)
        cash_flow_result = self.analyze_cash_flow(date_range=date_range, mode=mode)
        health_result = self.get_financial_health_indicators(date_range=date_range)

        # Get top income categories
        top_income = sorted(
            [
                {
                    'category': cat,
                    'amount': data['total'],
                    'count': data['count'],
                    'percentage': data['percentage']
                }
                for cat, data in income_result.breakdown_by_category.items()
            ],
            key=lambda x: x['amount'],
            reverse=True
        )[:top_n]

        # Get recent transactions
        query = self.db.query(Transaction).join(Category)

        # Apply date range filter
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)

        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS:
            query = query.filter(Transaction.include_in_analysis == True)

        recent_transactions = query.order_by(Transaction.transaction_date.desc()).limit(recent_count).all()

        recent_txns = [
            {
                'transaction_id': txn.transaction_id,
                'transaction_date': txn.transaction_date,
                'amount': txn.amount,
                'transaction_type': txn.transaction_type,
                'category': txn.category.category_name,
                'description': txn.description
            }
            for txn in recent_transactions
        ]

        return {
            'total_income': income_result.total_income,
            'total_expenses': expense_result.total_expenses,
            'net_cash_flow': cash_flow_result.net_cash_flow,
            'income_count': income_result.transaction_count,
            'expense_count': expense_result.transaction_count,
            'top_income_categories': top_income,
            'top_expense_categories': expense_result.top_categories,
            'recent_transactions': recent_txns,
            'financial_health': {
                'income_to_expense_ratio': health_result.income_to_expense_ratio,
                'savings_rate': health_result.savings_rate,
                'average_daily_income': health_result.average_daily_income,
                'average_daily_expense': health_result.average_daily_expense,
                'net_daily_cash_flow': health_result.net_daily_cash_flow,
                'period_start': health_result.period_start,
                'period_end': health_result.period_end
            },
            'period_start': income_result.period_start,
            'period_end': income_result.period_end,
            'mode': mode
        }

    def get_income_expense_comparison(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Get combined income and expense comparison.

        Args:
            date_range: Date range for analysis
            mode: Analysis mode (analysis or complete)
            top_n: Number of top categories to return

        Returns:
            Dictionary with income/expense comparison
        """
        income_result = self.analyze_income(date_range=date_range, mode=mode)
        expense_result = self.analyze_expenses(date_range=date_range, mode=mode, top_n=top_n)
        cash_flow_result = self.analyze_cash_flow(date_range=date_range, mode=mode)

        # Calculate comparison metrics
        income_to_expense_ratio = None
        expense_to_income_pct = None

        if expense_result.total_expenses != 0:
            # Expenses are stored as positive values
            income_to_expense_ratio = float(income_result.total_income / expense_result.total_expenses)

        if income_result.total_income > 0:
            # Use absolute value of expenses for percentage calculation
            expense_to_income_pct = float(abs(expense_result.total_expenses) / income_result.total_income * 100)

        return {
            'income_analysis': income_result,
            'expense_analysis': expense_result,
            'cash_flow': cash_flow_result,
            'comparison_metrics': {
                'income_to_expense_ratio': income_to_expense_ratio,
                'expense_to_income_percentage': expense_to_income_pct
            }
        }

    def get_category_breakdown(
        self,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS
    ) -> Dict[str, Any]:
        """
        Get detailed category breakdown for income and expenses.

        Args:
            date_range: Date range for analysis
            mode: Analysis mode (analysis or complete)

        Returns:
            Dictionary with category breakdown
        """
        # Build base query
        query = self.db.query(
            Category.category_id,
            Category.category_name,
            Category.category_type,
            func.sum(Transaction.amount).label('total_amount'),
            func.count(Transaction.transaction_id).label('transaction_count'),
            func.avg(Transaction.amount).label('average_amount')
        ).join(Transaction)

        # Apply date range filter
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)

        # Apply mode filter
        if mode == AnalysisMode.ANALYSIS or mode == AnalysisMode.WITH_CAPITAL:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)

            # Join with classifications to apply exclusion rules
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )

            # For income transactions: exclude if exclude_from_income_calc is True
            # For expense transactions: exclude if exclude_from_expense_calc is True
            # (unless it's a capital expense in WITH_CAPITAL mode)
            if mode == AnalysisMode.WITH_CAPITAL:
                # WITH_CAPITAL: include capital expenses, exclude other non-operating transactions
                query = query.filter(
                    or_(
                        # Income: not excluded from income calc
                        and_(
                            Category.category_type == 'Income',
                            or_(
                                TransactionClassification.exclude_from_income_calc == 0,
                                TransactionClassification.exclude_from_income_calc == None
                            )
                        ),
                        # Expense: not excluded OR is capital expense
                        and_(
                            Category.category_type == 'Expense',
                            or_(
                                TransactionClassification.exclude_from_expense_calc == 0,
                                TransactionClassification.exclude_from_expense_calc == None,
                                TransactionClassification.classification_name == 'Capital Expense'
                            )
                        )
                    )
                )
            else:  # ANALYSIS mode
                # ANALYSIS: exclude all non-operating transactions
                query = query.filter(
                    or_(
                        # Income: not excluded from income calc
                        and_(
                            Category.category_type == 'Income',
                            or_(
                                TransactionClassification.exclude_from_income_calc == 0,
                                TransactionClassification.exclude_from_income_calc == None
                            )
                        ),
                        # Expense: not excluded from expense calc
                        and_(
                            Category.category_type == 'Expense',
                            or_(
                                TransactionClassification.exclude_from_expense_calc == 0,
                                TransactionClassification.exclude_from_expense_calc == None
                            )
                        )
                    )
                )

        # Group by category
        query = query.group_by(
            Category.category_id,
            Category.category_name,
            Category.category_type
        )

        results = query.all()

        # Calculate totals
        total_income = Decimal('0')
        total_expenses = Decimal('0')
        total_all = Decimal('0')

        for row in results:
            total_all += row.total_amount
            if row.category_type == 'Income':
                total_income += row.total_amount
            else:
                total_expenses += row.total_amount

        # Build category lists
        income_categories = []
        expense_categories = []

        for row in results:
            category_item = {
                'category_id': row.category_id,
                'category_name': row.category_name,
                'category_type': row.category_type,
                'total_amount': row.total_amount,
                'transaction_count': row.transaction_count,
                'average_amount': row.average_amount,
                'percentage_of_total': 0.0,
                'percentage_of_all': float(row.total_amount / total_all * 100) if total_all > 0 else 0.0
            }

            if row.category_type == 'Income':
                category_item['percentage_of_total'] = float(row.total_amount / total_income * 100) if total_income > 0 else 0.0
                income_categories.append(category_item)
            else:
                category_item['percentage_of_total'] = float(row.total_amount / total_expenses * 100) if total_expenses > 0 else 0.0
                expense_categories.append(category_item)

        # Sort by total amount descending
        income_categories.sort(key=lambda x: x['total_amount'], reverse=True)
        expense_categories.sort(key=lambda x: x['total_amount'], reverse=True)

        # Get period dates
        period_start, period_end = self._get_period_dates(date_range)

        return {
            'income_categories': income_categories,
            'expense_categories': expense_categories,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'period_start': period_start,
            'period_end': period_end,
            'mode': mode
        }

    def get_expense_category_trends(
        self,
        period: TimePeriod,
        date_range: Optional[DateRange] = None,
        mode: AnalysisMode = AnalysisMode.ANALYSIS,
        top_n: int = 8
    ) -> Dict[str, Any]:
        """
        Get expense trends broken down by category for each time period.

        This method returns the actual expense amounts for each category
        in each time period, enabling accurate stacked bar charts.

        Args:
            period: Time period for grouping (daily, weekly, monthly, etc.)
            date_range: Optional date range for filtering
            mode: Analysis mode
            top_n: Number of top categories to include

        Returns:
            Dictionary with:
            - periods: List of period labels
            - categories: List of top N category names
            - data: List of dictionaries with period and category amounts
        """
        from collections import defaultdict
        import pandas as pd

        # Build base query for expenses
        query = self.db.query(Transaction).filter(
            Transaction.transaction_type == 'Expense'
        )

        # Apply mode filtering
        if mode == AnalysisMode.ANALYSIS:
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )
            query = query.filter(
                or_(
                    TransactionClassification.exclude_from_expense_calc == False,
                    TransactionClassification.exclude_from_expense_calc == None
                )
            )
        elif mode == AnalysisMode.WITH_CAPITAL:
            # WITH_CAPITAL mode: exclude non-operating expenses EXCEPT capital expenses
            query = query.filter(Transaction.include_in_analysis == True)
            query = query.filter(Transaction.is_transfer == False)
            query = query.outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id
            )
            query = query.filter(
                or_(
                    TransactionClassification.exclude_from_expense_calc == 0,
                    TransactionClassification.exclude_from_expense_calc == None,
                    TransactionClassification.classification_name == 'Capital Expense'
                )
            )

        # Apply date range filter
        if date_range:
            if date_range.start_date:
                query = query.filter(Transaction.transaction_date >= date_range.start_date)
            if date_range.end_date:
                query = query.filter(Transaction.transaction_date <= date_range.end_date)

        # Join with Category to get category names
        query = query.join(Category, Transaction.category_id == Category.category_id)

        # Get all transactions with category info
        transactions = query.add_columns(
            Category.category_name,
            Transaction.transaction_date,
            Transaction.amount
        ).all()

        if not transactions:
            return {
                'periods': [],
                'categories': [],
                'data': []
            }

        # Create DataFrame for easier processing
        df = pd.DataFrame([
            {
                'date': t.transaction_date,
                'category': t.category_name,
                'amount': float(abs(t.amount))  # Convert to positive for display
            }
            for t in transactions
        ])

        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Add period column based on grouping
        df['period'] = self._get_period_key(df['date'], period)

        # Group by period and category
        period_category_totals = df.groupby(['period', 'category'])['amount'].sum().reset_index()

        # Get top N categories by total amount
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        top_categories = category_totals.head(top_n).index.tolist()

        # Filter to only include top categories
        period_category_totals = period_category_totals[
            period_category_totals['category'].isin(top_categories)
        ]

        # Get unique periods (sorted)
        periods = sorted(period_category_totals['period'].unique())

        # Create data structure for stacked bar chart
        data = []
        for period_label in periods:
            period_data = {'period': period_label}

            # Get data for this period
            period_df = period_category_totals[period_category_totals['period'] == period_label]

            # Add amount for each category (0 if no data)
            for category in top_categories:
                category_data = period_df[period_df['category'] == category]
                if not category_data.empty:
                    period_data[category] = float(category_data['amount'].iloc[0])
                else:
                    period_data[category] = 0.0

            data.append(period_data)

        return {
            'periods': periods,
            'categories': top_categories,
            'data': data,
            'period_type': period.value,
            'mode': mode.value
        }


