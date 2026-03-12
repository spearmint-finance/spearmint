"""BudgetAdvisorAgent — orchestrates the hybrid deterministic + LLM pipeline."""

import logging
import time
from typing import Any, Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from ...database.models import Category, Transaction
from ..base import A2AAgent
from .advisor import enrich_with_llm, generate_negotiation_message, _template_fallback
from .analyzer import SpendingAnalyzer
from .recommender import SavingsRecommender
from .schemas import (
    A2AResponse,
    AnalyzeSpendingParams,
    DataQualityReport,
    NegotiationOption,
    SavingsRecommendation,
    SpendingAnalysisResult,
)

logger = logging.getLogger(__name__)


class BudgetAdvisorAgent(A2AAgent):
    """Hybrid agent: deterministic analysis + LLM interpretation.

    Flow:
        1. SpendingAnalyzer (deterministic) → structured stats
        2. SavingsRecommender (deterministic) → ranked signals
        3. AdvisorReasoning (LLM) → personalized interpretation & advice
    """

    AGENT_CARD = {
        "name": "budget-advisor",
        "description": (
            "Hybrid financial advisor that uses deterministic analysis for "
            "calculations and LLM reasoning for personalized interpretation "
            "and advice"
        ),
        "version": "1.0.0",
        "capabilities": {
            "input": ["spending-analysis-request"],
            "output": ["budget-recommendation", "savings-opportunities", "spending-alerts"],
            "proactive": True,
            "stateful": True,
            "orchestrator": True,
            "hybrid": True,
        },
        "endpoint": "/a2a/budget-advisor",
        "authentication": "bearer",
        "skills": [
            {
                "id": "analyze-spending",
                "description": (
                    "Evaluate spending with deterministic analysis, then use LLM "
                    "to interpret signals and generate personalized recommendations"
                ),
            },
        ],
    }

    def get_agent_card(self) -> Dict[str, Any]:
        return self.AGENT_CARD

    async def invoke(
        self,
        skill: str,
        params: Dict[str, Any],
        negotiation: Optional[Dict[str, Any]],
        db: Session,
    ) -> Dict[str, Any]:
        if skill == "analyze-spending":
            return await self._analyze_spending(params, negotiation, db)

        return A2AResponse(
            skill=skill,
            status="error",
            error=f"Unknown skill: {skill}",
        ).model_dump()

    async def _analyze_spending(
        self,
        params: Dict[str, Any],
        negotiation: Optional[Dict[str, Any]],
        db: Session,
    ) -> Dict[str, Any]:
        start_time = time.time()
        parsed = AnalyzeSpendingParams(**params)
        analyzer = SpendingAnalyzer(db)

        # ── Step 1: Check data quality (deterministic) ───────────
        quality = analyzer.get_data_quality(parsed.months_back)

        if not negotiation:
            if quality.available_months < 3 or quality.uncategorized_pct > 0.20:
                return await self._build_negotiation_response(
                    quality, parsed.months_back, start_time
                )

        # Handle negotiation choices
        effective_months = parsed.months_back
        if negotiation:
            chosen = negotiation.get("chosen_option", "")
            if chosen == "proceed_low_confidence":
                pass  # proceed as-is
            elif chosen == "reduce_scope":
                effective_months = min(quality.available_months, parsed.months_back)
            # "wait_for_categorization" would not result in a re-invocation

        # ── Step 2: Deterministic analysis ───────────────────────
        analysis = analyzer.analyze(months_back=effective_months)

        # ── Step 3: Deterministic signal detection ───────────────
        recommender = SavingsRecommender()
        recommendations = recommender.recommend(
            analysis.category_breakdown,
            analysis.monthly_income_avg,
        )

        # ── Step 4: Get top transactions for LLM context ────────
        flagged_categories = [r.category for r in recommendations]
        top_transactions = _get_top_transactions(db, flagged_categories)

        # ── Step 5: LLM interpretation ───────────────────────────
        llm_output = await enrich_with_llm(analysis, recommendations, top_transactions)

        # Merge LLM reasoning into deterministic recommendations
        enriched_recs = _merge_llm_into_recs(recommendations, llm_output)
        analysis.recommendations = enriched_recs

        duration_ms = int((time.time() - start_time) * 1000)

        return A2AResponse(
            skill="analyze-spending",
            status="completed",
            duration_ms=duration_ms,
            result=analysis,
            metadata={
                "data_period": analysis.analysis_period,
                "transaction_count": quality.total_transactions,
                "confidence": analysis.confidence,
                "llm_summary": llm_output.get("summary", ""),
            },
        ).model_dump()

    async def _build_negotiation_response(
        self,
        quality: DataQualityReport,
        requested_months: int,
        start_time: float,
    ) -> Dict[str, Any]:
        """Build a needs_input response with LLM-generated explanation."""
        options = []

        if quality.available_months >= 1:
            options.append(NegotiationOption(
                id="proceed_low_confidence",
                description=(
                    f"Proceed with {quality.available_months} month(s) of data "
                    f"(lower accuracy)"
                ),
                confidence=round(quality.available_months / max(requested_months, 1) * 0.7, 2),
            ))

        if quality.uncategorized_pct > 0.20:
            uncat_count = int(quality.total_transactions * quality.uncategorized_pct)
            options.append(NegotiationOption(
                id="wait_for_categorization",
                description="Categorize transactions first for higher accuracy",
                prerequisite=f"Classify the {uncat_count} uncategorized transactions",
            ))

        if quality.available_months >= 1:
            options.append(NegotiationOption(
                id="reduce_scope",
                description=(
                    f"Analyze only the {quality.available_months} month(s) available"
                ),
                confidence=round(min(quality.available_months / 3, 1.0) * 0.8, 2),
            ))

        # LLM generates a conversational explanation (with template fallback)
        message = await generate_negotiation_message(quality, options)

        duration_ms = int((time.time() - start_time) * 1000)

        return A2AResponse(
            skill="analyze-spending",
            status="needs_input",
            duration_ms=duration_ms,
            issue="insufficient_data",
            details={
                "requested_months": requested_months,
                "available_months": quality.available_months,
                "uncategorized_pct": quality.uncategorized_pct,
                "message": message,
            },
            options=options,
        ).model_dump()


# ── helpers ──────────────────────────────────────────────────────

def _get_top_transactions(
    db: Session,
    categories: List[str],
    limit_per_category: int = 5,
) -> Dict[str, List[Dict[str, Any]]]:
    """Pull recent transactions for flagged categories (for LLM context)."""
    result = {}
    for cat_name in categories:
        txns = (
            db.query(Transaction)
            .join(Category, Transaction.category_id == Category.category_id)
            .filter(Category.category_name == cat_name)
            .filter(Transaction.transaction_type == "Expense")
            .order_by(desc(Transaction.transaction_date))
            .limit(limit_per_category)
            .all()
        )
        result[cat_name] = [
            {
                "description": t.description or "",
                "amount": float(t.amount),
                "date": str(t.transaction_date),
            }
            for t in txns
        ]
    return result


def _merge_llm_into_recs(
    deterministic_recs: List[SavingsRecommendation],
    llm_output: Dict[str, Any],
) -> List[SavingsRecommendation]:
    """Merge LLM reasoning and tips into deterministic recommendations."""
    llm_recs = {
        r["category"]: r
        for r in llm_output.get("recommendations", [])
    }

    enriched = []
    for rec in deterministic_recs:
        llm_rec = llm_recs.get(rec.category, {})

        # LLM can filter noise by setting worth_mentioning=False
        if llm_rec.get("worth_mentioning") is False:
            rec.confidence = min(rec.confidence, 0.3)

        # Merge reasoning (LLM overrides empty template)
        if llm_rec.get("reasoning"):
            rec.reasoning = llm_rec["reasoning"]

        enriched.append(rec)

    return enriched
