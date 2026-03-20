"""SpendingAnalyzer — computes category-level spending statistics."""

from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ...database.models import Category, Transaction, TransactionClassification
from .schemas import CategoryStats, DataQualityReport, SpendingAnalysisResult


class SpendingAnalyzer:
    """Pulls transaction data and computes per-category monthly statistics."""

    def __init__(self, db: Session):
        self.db = db

    # ── public ───────────────────────────────────────────────────

    def get_data_quality(self, months_back: int) -> DataQualityReport:
        """Check data coverage and categorization quality."""
        end_date = date.today()
        requested_start = _months_ago(end_date, months_back)

        # Earliest / latest transaction in analysis view
        row = (
            self.db.query(
                func.min(Transaction.transaction_date),
                func.max(Transaction.transaction_date),
                func.count(Transaction.transaction_id),
            )
            .filter(Transaction.include_in_analysis == True)  # noqa: E712
            # Transfers excluded via include_in_analysis=False
            .first()
        )
        earliest, latest, total = row if row else (None, None, 0)

        if not earliest or total == 0:
            return DataQualityReport(
                available_months=0,
                uncategorized_pct=1.0,
                total_transactions=0,
            )

        # Available months within the requested window
        effective_start = max(earliest, requested_start)
        available_months = _month_diff(effective_start, latest)

        # Uncategorized percentage
        uncat_count = (
            self.db.query(func.count(Transaction.transaction_id))
            .outerjoin(Category, Transaction.category_id == Category.category_id)
            .filter(Transaction.include_in_analysis == True)  # noqa: E712
            # Transfers excluded via include_in_analysis=False
            .filter(Transaction.transaction_date >= effective_start)
            .filter(
                or_(
                    Transaction.category_id == None,  # noqa: E711
                    Category.category_name == "Uncategorized",
                )
            )
            .scalar()
        ) or 0

        total_in_window = (
            self.db.query(func.count(Transaction.transaction_id))
            .filter(Transaction.include_in_analysis == True)  # noqa: E712
            # Transfers excluded via include_in_analysis=False
            .filter(Transaction.transaction_date >= effective_start)
            .scalar()
        ) or 0

        return DataQualityReport(
            available_months=max(available_months, 0),
            uncategorized_pct=uncat_count / total_in_window if total_in_window else 1.0,
            total_transactions=total_in_window,
            earliest_date=earliest,
            latest_date=latest,
        )

    def analyze(self, months_back: int = 6) -> SpendingAnalysisResult:
        """Run full spending analysis and return category stats."""
        end_date = date.today()
        start_date = _months_ago(end_date, months_back)

        # Pull all analysis-eligible transactions in the window
        txns = self._query_transactions(start_date, end_date)

        if not txns:
            return SpendingAnalysisResult(
                analysis_period={"start": str(start_date), "end": str(end_date)},
                monthly_income_avg=0,
                monthly_expense_avg=0,
                savings_rate=0,
                category_breakdown=[],
                recommendations=[],
                confidence=0,
            )

        df = pd.DataFrame(
            [
                {
                    "date": t.transaction_date,
                    "amount": float(t.amount),
                    "type": t.transaction_type,
                    "category_id": t.category_id,
                    "category_name": t.category.category_name if t.category else "Uncategorized",
                    "is_fixed": t.category.is_fixed_obligation if t.category else False,
                }
                for t in txns
            ]
        )
        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")

        # All months in the window (for zero-filling)
        all_months = pd.period_range(start=start_date, end=end_date, freq="M")
        n_months = len(all_months)

        # Income / expense totals
        total_income = float(df.loc[df["type"] == "Income", "amount"].sum())
        total_expenses = float(df.loc[df["type"] == "Expense", "amount"].sum())
        monthly_income_avg = total_income / n_months if n_months else 0
        monthly_expense_avg = total_expenses / n_months if n_months else 0
        savings_rate = (
            (monthly_income_avg - monthly_expense_avg) / monthly_income_avg
            if monthly_income_avg > 0
            else 0
        )

        # Per-category stats (expenses only for recommendations)
        expense_df = df[df["type"] == "Expense"]
        category_stats = self._compute_category_stats(
            expense_df, all_months, monthly_income_avg, monthly_expense_avg
        )

        # Determine confidence based on data quality
        quality = self.get_data_quality(months_back)
        confidence = self._compute_confidence(quality, months_back)

        return SpendingAnalysisResult(
            analysis_period={"start": str(start_date), "end": str(end_date)},
            monthly_income_avg=round(monthly_income_avg, 2),
            monthly_expense_avg=round(monthly_expense_avg, 2),
            savings_rate=round(savings_rate, 4),
            category_breakdown=category_stats,
            recommendations=[],  # filled in by agent after recommender runs
            confidence=round(confidence, 2),
        )

    # ── private ──────────────────────────────────────────────────

    def _query_transactions(self, start_date: date, end_date: date) -> list:
        """Query analysis-eligible transactions, joining category."""
        query = (
            self.db.query(Transaction)
            .outerjoin(Category, Transaction.category_id == Category.category_id)
            .outerjoin(
                TransactionClassification,
                Transaction.classification_id == TransactionClassification.classification_id,
            )
            .filter(Transaction.include_in_analysis == True)  # noqa: E712
            # Transfers excluded via include_in_analysis=False
            .filter(Transaction.transaction_date >= start_date)
            .filter(Transaction.transaction_date <= end_date)
            .filter(
                or_(
                    TransactionClassification.exclude_from_expense_calc == 0,
                    TransactionClassification.exclude_from_expense_calc == None,  # noqa: E711
                    # Also include income transactions (not excluded by expense filter)
                    Transaction.transaction_type == "Income",
                )
            )
        )
        return query.all()

    def _compute_category_stats(
        self,
        expense_df: pd.DataFrame,
        all_months: pd.PeriodIndex,
        monthly_income_avg: float,
        monthly_expense_avg: float,
    ) -> List[CategoryStats]:
        """Compute per-category monthly stats."""
        if expense_df.empty:
            return []

        stats: List[CategoryStats] = []
        grouped = expense_df.groupby(["category_id", "category_name", "is_fixed"])

        for (cat_id, cat_name, is_fixed), grp in grouped:
            monthly = grp.groupby("month")["amount"].sum()
            # Zero-fill missing months
            monthly = monthly.reindex(all_months, fill_value=0.0)
            values = monthly.values.astype(float).tolist()

            monthly_avg = float(np.mean(values))
            if monthly_avg < 0.01:
                continue  # skip negligible categories

            trend, trend_pct = _compute_trend(values)
            variance = _compute_variance(values)

            pct_of_income = (monthly_avg / monthly_income_avg * 100) if monthly_income_avg > 0 else 0
            pct_of_expenses = (monthly_avg / monthly_expense_avg * 100) if monthly_expense_avg > 0 else 0

            stats.append(
                CategoryStats(
                    category=cat_name,
                    category_id=int(cat_id),
                    monthly_avg=round(monthly_avg, 2),
                    trend=trend,
                    trend_pct=round(trend_pct, 1),
                    pct_of_income=round(pct_of_income, 1),
                    pct_of_expenses=round(pct_of_expenses, 1),
                    variance=variance,
                    months=[round(v, 2) for v in values],
                    is_fixed=bool(is_fixed),
                )
            )

        # Sort by monthly_avg descending
        stats.sort(key=lambda s: s.monthly_avg, reverse=True)
        return stats

    def _compute_confidence(self, quality: DataQualityReport, requested_months: int) -> float:
        """Heuristic confidence score 0-1."""
        month_factor = min(quality.available_months / max(requested_months, 1), 1.0)
        cat_factor = 1.0 - quality.uncategorized_pct
        return round(month_factor * 0.6 + cat_factor * 0.4, 2)


# ── helpers ──────────────────────────────────────────────────────

def _months_ago(ref: date, n: int) -> date:
    """Return the first of the month, n months before ref."""
    month = ref.month - n
    year = ref.year
    while month <= 0:
        month += 12
        year -= 1
    return date(year, month, 1)


def _month_diff(start: date, end: date) -> int:
    """Number of calendar months between two dates (inclusive)."""
    return (end.year - start.year) * 12 + (end.month - start.month) + 1


def _compute_trend(values: list) -> Tuple[str, float]:
    """Linear regression slope → trend classification and percentage."""
    if len(values) < 2:
        return "stable", 0.0
    mean = np.mean(values)
    if mean < 0.01:
        return "stable", 0.0
    x = np.arange(len(values), dtype=float)
    coeffs = np.polyfit(x, values, 1)
    slope = coeffs[0]
    trend_pct = (slope * len(values)) / mean * 100
    if trend_pct > 5:
        return "increasing", trend_pct
    elif trend_pct < -5:
        return "decreasing", trend_pct
    return "stable", trend_pct


def _compute_variance(values: list) -> str:
    """Coefficient of variation → variance classification."""
    if len(values) < 2:
        return "low"
    mean = np.mean(values)
    if mean < 0.01:
        return "low"
    cv = float(np.std(values) / mean)
    if cv >= 0.30:
        return "high"
    elif cv >= 0.15:
        return "moderate"
    return "low"
