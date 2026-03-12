"""SavingsRecommender — deterministic detection rules and ranking."""

from typing import List, Optional

import numpy as np

from .schemas import CategoryStats, SavingsRecommendation


class SavingsRecommender:
    """Applies detection rules to category stats and ranks opportunities.

    This is the deterministic layer. It produces structured signals
    (category, signal type, severity, savings numbers) but does NOT
    generate explanations or advice — that is the LLM's job.
    """

    def recommend(
        self,
        category_stats: List[CategoryStats],
        monthly_income_avg: float,
    ) -> List[SavingsRecommendation]:
        """Apply all detection rules and return ranked recommendations."""
        recs: List[SavingsRecommendation] = []

        for stats in category_stats:
            if stats.is_fixed:
                continue  # don't recommend cuts on fixed obligations

            rec = self._best_signal_for_category(stats, monthly_income_avg)
            if rec:
                recs.append(rec)

        # Rank by annual_impact descending, keep top 5
        recs.sort(key=lambda r: r.annual_impact, reverse=True)
        return recs[:5]

    # ── detection rules ──────────────────────────────────────────

    def _best_signal_for_category(
        self,
        stats: CategoryStats,
        monthly_income_avg: float,
    ) -> Optional[SavingsRecommendation]:
        """Run all rules for a category, return the highest-impact signal."""
        candidates: List[SavingsRecommendation] = []

        r = self._detect_upward_trend(stats)
        if r:
            candidates.append(r)

        r = self._detect_high_variance(stats)
        if r:
            candidates.append(r)

        r = self._detect_income_disproportionate(stats, monthly_income_avg)
        if r:
            candidates.append(r)

        r = self._detect_seasonal_spike(stats)
        if r:
            candidates.append(r)

        if not candidates:
            return None

        # Return the one with highest annual impact
        return max(candidates, key=lambda c: c.annual_impact)

    def _detect_upward_trend(self, stats: CategoryStats) -> Optional[SavingsRecommendation]:
        """Flag categories with spending increasing >10%."""
        if stats.trend != "increasing" or stats.trend_pct <= 10:
            return None

        target = min(stats.months) if stats.months else stats.monthly_avg
        target = max(target, stats.monthly_avg * 0.5)  # don't suggest unrealistic cuts
        savings = stats.monthly_avg - target

        if savings < 5:
            return None

        return SavingsRecommendation(
            category=stats.category,
            signal="upward_trend",
            severity=_severity(stats.trend_pct, thresholds=(10, 25)),
            current_monthly=stats.monthly_avg,
            suggested_target=round(target, 2),
            monthly_savings=round(savings, 2),
            annual_impact=round(savings * 12, 2),
            confidence=0.8,
            reasoning="",  # LLM will fill this
        )

    def _detect_high_variance(self, stats: CategoryStats) -> Optional[SavingsRecommendation]:
        """Flag categories with coefficient of variation >30%."""
        if stats.variance != "high":
            return None

        values = stats.months
        if len(values) < 2:
            return None

        target = float(np.median(values))
        savings = stats.monthly_avg - target

        if savings < 5:
            return None

        return SavingsRecommendation(
            category=stats.category,
            signal="high_variance",
            severity="moderate",
            current_monthly=stats.monthly_avg,
            suggested_target=round(target, 2),
            monthly_savings=round(savings, 2),
            annual_impact=round(savings * 12, 2),
            confidence=0.7,
            reasoning="",
        )

    def _detect_income_disproportionate(
        self, stats: CategoryStats, monthly_income_avg: float
    ) -> Optional[SavingsRecommendation]:
        """Flag non-essential categories consuming >15% of income."""
        if stats.pct_of_income <= 15 or monthly_income_avg <= 0:
            return None

        target = monthly_income_avg * 0.12  # suggest reducing to 12%
        savings = stats.monthly_avg - target

        if savings < 5:
            return None

        return SavingsRecommendation(
            category=stats.category,
            signal="income_disproportionate",
            severity=_severity(stats.pct_of_income, thresholds=(15, 25)),
            current_monthly=stats.monthly_avg,
            suggested_target=round(target, 2),
            monthly_savings=round(savings, 2),
            annual_impact=round(savings * 12, 2),
            confidence=0.75,
            reasoning="",
        )

    def _detect_seasonal_spike(self, stats: CategoryStats) -> Optional[SavingsRecommendation]:
        """Flag categories where the last month is >50% above trailing average."""
        if len(stats.months) < 3:
            return None

        last = stats.months[-1]
        trailing_avg = float(np.mean(stats.months[:-1]))

        if trailing_avg < 1 or last <= trailing_avg * 1.5:
            return None

        savings = last - trailing_avg

        return SavingsRecommendation(
            category=stats.category,
            signal="seasonal_spike",
            severity=_severity(last / trailing_avg * 100 - 100, thresholds=(50, 100)),
            current_monthly=round(last, 2),
            suggested_target=round(trailing_avg, 2),
            monthly_savings=round(savings, 2),
            annual_impact=round(savings * 12, 2),
            confidence=0.6,  # lower — could be one-time
            reasoning="",
        )


def _severity(value: float, thresholds: tuple = (10, 25)) -> str:
    """Classify severity based on thresholds."""
    low, high = thresholds
    if value >= high:
        return "high"
    elif value >= low:
        return "moderate"
    return "low"
