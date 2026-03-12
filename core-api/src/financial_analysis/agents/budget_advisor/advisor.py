"""AdvisorReasoning — LLM layer for interpreting signals and generating advice.

This is what makes the Budget Advisor an agent rather than a service.
The deterministic layer produces structured signals (numbers, thresholds, flags).
This layer uses an LLM to interpret those signals: explain why they matter,
generate personalized advice, correlate across categories, and decide what's
worth mentioning vs. noise.

The LLM never does the math — it interprets the math.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from .schemas import (
    CategoryStats,
    DataQualityReport,
    NegotiationOption,
    SavingsRecommendation,
    SpendingAnalysisResult,
)

logger = logging.getLogger(__name__)

# System prompt that frames the LLM's role
ADVISOR_SYSTEM_PROMPT = """You are the Budget Advisor for Spearmint Finance. You receive structured spending data (computed deterministically) and your job is to interpret it for the user.

Your responsibilities:
1. For each savings recommendation, write a concise "reasoning" (1-2 sentences) explaining WHY this matters for the user — not just restating the numbers.
2. Generate 1-2 actionable tips per recommendation based on the transaction descriptions provided.
3. Decide which recommendations are actually worth presenting. Some signals are noise (one-time spikes, seasonal patterns that will self-correct). Flag these with low confidence.
4. Write a brief overall summary (2-3 sentences) of the user's financial picture — lead with something positive.

Rules:
- Be supportive, not judgmental. "You could save..." not "You're overspending on..."
- Include positive reinforcement when warranted.
- Be specific — reference actual transaction patterns, not generic advice.
- Keep reasoning to 1-2 sentences. Keep tips actionable and concrete.
- If a spike looks like a one-time event (concert, medical bill, travel), say so.

Respond with valid JSON matching this structure:
{
  "summary": "Overall financial summary (2-3 sentences)",
  "recommendations": [
    {
      "category": "category name",
      "reasoning": "Why this matters",
      "tips": ["Actionable tip 1", "Actionable tip 2"],
      "worth_mentioning": true
    }
  ]
}"""


async def enrich_with_llm(
    analysis: SpendingAnalysisResult,
    recommendations: List[SavingsRecommendation],
    top_transactions: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """Send structured signals to the LLM for interpretation.

    Args:
        analysis: Deterministic spending analysis result.
        recommendations: Deterministic savings recommendations (with empty reasoning).
        top_transactions: Top transactions per flagged category for context.
            Format: {"Dining Out": [{"description": "DOORDASH", "amount": 45.00, "date": "2026-02-15"}, ...]}

    Returns:
        Dict with "summary" and enriched "recommendations" from the LLM.
        Falls back to template-based output if LLM is unavailable.
    """
    try:
        return await _call_llm(analysis, recommendations, top_transactions)
    except Exception as e:
        logger.warning("LLM reasoning unavailable, falling back to templates: %s", e)
        return _template_fallback(analysis, recommendations)


async def generate_negotiation_message(
    quality: DataQualityReport,
    options: List[NegotiationOption],
) -> str:
    """Use LLM to explain data quality issues conversationally.

    Falls back to a template if LLM is unavailable.
    """
    try:
        return await _call_llm_negotiation(quality, options)
    except Exception:
        logger.warning("LLM unavailable for negotiation, using template")
        return _negotiation_template(quality)


# ── LLM calls ───────────────────────────────────────────────────

async def _call_llm(
    analysis: SpendingAnalysisResult,
    recommendations: List[SavingsRecommendation],
    top_transactions: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """Call Claude API with structured spending data."""
    import os
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_KEY")
    client = anthropic.AsyncAnthropic(api_key=api_key)

    # Build the user message with structured data
    user_message = _build_analysis_prompt(analysis, recommendations, top_transactions)

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=ADVISOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    # Parse JSON from response
    text = response.content[0].text
    # Handle potential markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    return json.loads(text.strip())


async def _call_llm_negotiation(
    quality: DataQualityReport,
    options: List[NegotiationOption],
) -> str:
    """Call Claude to generate a conversational negotiation message."""
    import os
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_KEY")
    client = anthropic.AsyncAnthropic(api_key=api_key)

    prompt = (
        f"The user asked for spending analysis but data quality is limited:\n"
        f"- Available months: {quality.available_months}\n"
        f"- Uncategorized transactions: {quality.uncategorized_pct:.0%}\n"
        f"- Total transactions: {quality.total_transactions}\n\n"
        f"Options available:\n"
    )
    for opt in options:
        prompt += f"- {opt.id}: {opt.description}"
        if opt.confidence:
            prompt += f" (confidence: {opt.confidence:.0%})"
        prompt += "\n"

    prompt += (
        "\nWrite a brief, friendly message (2-3 sentences) explaining the situation "
        "and what the options mean. Don't list the options — just explain the trade-off."
    )

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


# ── prompt building ──────────────────────────────────────────────

def _build_analysis_prompt(
    analysis: SpendingAnalysisResult,
    recommendations: List[SavingsRecommendation],
    top_transactions: Dict[str, List[Dict[str, Any]]],
) -> str:
    """Build a structured prompt for the LLM."""
    parts = [
        "Here is the user's spending analysis (computed deterministically):\n",
        f"Period: {analysis.analysis_period.get('start')} to {analysis.analysis_period.get('end')}",
        f"Monthly income avg: ${analysis.monthly_income_avg:,.2f}",
        f"Monthly expense avg: ${analysis.monthly_expense_avg:,.2f}",
        f"Savings rate: {analysis.savings_rate:.1%}\n",
    ]

    if recommendations:
        parts.append("Savings signals detected (ranked by annual impact):\n")
        for rec in recommendations:
            parts.append(
                f"- {rec.category}: signal={rec.signal}, severity={rec.severity}, "
                f"current=${rec.current_monthly:,.2f}/mo, "
                f"target=${rec.suggested_target:,.2f}/mo, "
                f"saves=${rec.annual_impact:,.2f}/year"
            )

    if top_transactions:
        parts.append("\nRecent transactions in flagged categories:\n")
        for cat, txns in top_transactions.items():
            parts.append(f"  {cat}:")
            for t in txns[:5]:
                parts.append(f"    - {t.get('description', 'N/A')} ${t.get('amount', 0):.2f} ({t.get('date', '')})")

    parts.append(
        "\nInterpret these signals. For each recommendation, provide reasoning and tips. "
        "Flag any that look like noise (one-time events). Write an overall summary."
    )

    return "\n".join(parts)


# ── template fallback ────────────────────────────────────────────

def _template_fallback(
    analysis: SpendingAnalysisResult,
    recommendations: List[SavingsRecommendation],
) -> Dict[str, Any]:
    """Generate template-based output when LLM is unavailable."""
    # Summary
    rate_pct = analysis.savings_rate * 100
    if rate_pct >= 20:
        summary = f"Your savings rate of {rate_pct:.0f}% is strong. "
    elif rate_pct >= 10:
        summary = f"Your savings rate of {rate_pct:.0f}% is reasonable, with room to improve. "
    else:
        summary = f"Your savings rate of {rate_pct:.0f}% is below typical targets. "

    summary += (
        f"You earn an average of ${analysis.monthly_income_avg:,.0f}/month "
        f"and spend ${analysis.monthly_expense_avg:,.0f}/month."
    )

    # Per-recommendation reasoning
    enriched = []
    for rec in recommendations:
        reasoning = _SIGNAL_TEMPLATES.get(rec.signal, "").format(
            category=rec.category,
            current=rec.current_monthly,
            target=rec.suggested_target,
            savings=rec.monthly_savings,
            annual=rec.annual_impact,
            trend_pct=getattr(rec, "trend_pct", 0),
        )
        enriched.append({
            "category": rec.category,
            "reasoning": reasoning,
            "tips": [],
            "worth_mentioning": True,
        })

    return {"summary": summary, "recommendations": enriched}


_SIGNAL_TEMPLATES = {
    "upward_trend": (
        "Your {category} spending has been trending upward. "
        "Reducing to ${target:,.0f}/month could save ${annual:,.0f} per year."
    ),
    "high_variance": (
        "Your {category} spending varies significantly month to month. "
        "Targeting the median of ${target:,.0f}/month would save ${annual:,.0f} per year."
    ),
    "income_disproportionate": (
        "{category} is consuming a large share of your income. "
        "Reducing to ${target:,.0f}/month could save ${annual:,.0f} per year."
    ),
    "seasonal_spike": (
        "Your {category} spending spiked recently above your typical average. "
        "If this continues, consider a target of ${target:,.0f}/month."
    ),
}


def _negotiation_template(quality: DataQualityReport) -> str:
    """Template fallback for negotiation messages."""
    parts = []
    if quality.available_months < 3:
        parts.append(
            f"I only have {quality.available_months} month(s) of data, "
            f"which limits the accuracy of trend analysis."
        )
    if quality.uncategorized_pct > 0.2:
        parts.append(
            f"About {quality.uncategorized_pct:.0%} of transactions aren't categorized yet, "
            f"which affects the accuracy of category-level recommendations."
        )
    return " ".join(parts) if parts else "Data quality check passed."
