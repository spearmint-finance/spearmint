"""
Smart transaction auto-categorization using LLM.

Groups transactions by unique description, classifies each group via
Claude API, and generates transaction rules for high-confidence matches.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database.models import Transaction, Category

logger = logging.getLogger(__name__)


@dataclass
class ClassificationResult:
    """Result of classifying a single unique description."""
    description: str
    merchant_name: str
    merchant_type: str
    suggested_category: str
    category_id: Optional[int]
    confidence: float
    reasoning: str
    transaction_count: int
    action: str  # "auto_applied", "needs_review", "unclassified"
    suggested_pattern: Optional[str] = None


@dataclass
class AutoCategorizeResponse:
    """Response from the auto-categorization pipeline."""
    total_transactions: int
    unique_descriptions: int
    high_confidence: int
    medium_confidence: int
    low_confidence: int
    categories_created: int
    rules_created: int
    results: List[ClassificationResult]


class AutoCategorizeService:
    """Service for LLM-powered transaction auto-categorization."""

    def __init__(self, db: Session):
        self.db = db

    def get_uncategorized_descriptions(self) -> Dict[str, Dict]:
        """
        Get unique descriptions from uncategorized transactions
        with their counts and sample data.
        """
        # Find the "nan" category or transactions with no real category
        nan_cat = self.db.query(Category).filter(
            Category.category_name == "nan"
        ).first()

        conditions = []
        if nan_cat:
            conditions.append(Transaction.category_id == nan_cat.category_id)
        conditions.append(Transaction.category_id.is_(None))

        from sqlalchemy import or_
        transactions = self.db.query(
            Transaction.description,
            func.count(Transaction.transaction_id).label("count"),
            func.min(Transaction.transaction_type).label("transaction_type"),
            func.avg(Transaction.amount).label("avg_amount"),
        ).filter(
            or_(*conditions)
        ).group_by(
            Transaction.description,
        ).all()

        desc_map: Dict[str, Dict] = {}
        for row in transactions:
            desc = row.description or ""
            if not desc.strip():
                continue
            desc_map[desc] = {
                "description": desc,
                "transaction_type": row.transaction_type,
                "sample_amount": float(row.avg_amount) if row.avg_amount else 0,
                "count": row.count,
            }

        return desc_map

    def get_existing_categories(self) -> List[Dict]:
        """Get all categories for the LLM prompt."""
        categories = self.db.query(Category).filter(
            Category.category_name != "nan"
        ).all()
        return [
            {
                "category_id": c.category_id,
                "category_name": c.category_name,
                "category_type": c.category_type,
            }
            for c in categories
        ]

    async def classify_batch(
        self,
        descriptions: List[Dict],
        categories: List[Dict],
    ) -> List[Dict]:
        """
        Classify a batch of descriptions using OpenAI GPT-4o-mini.
        Returns list of classification dicts.
        """
        import openai

        api_key = os.environ.get("OPENAI_KEY_CATEGORIES") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_KEY_CATEGORIES not set. Set it in your environment to use smart categorization."
            )

        client = openai.AsyncOpenAI(api_key=api_key)

        category_list = "\n".join(
            f"- {c['category_name']} (type: {c['category_type']}, id: {c['category_id']})"
            for c in categories
        )

        transaction_list = "\n".join(
            f"- \"{d['description']}\" (type: {d['transaction_type']}, amount: ${abs(d['sample_amount']):.2f}, count: {d['count']})"
            for d in descriptions
        )

        prompt = f"""You are a financial transaction categorizer for a personal finance app. Given bank transaction descriptions, identify the merchant and assign a SPECIFIC category.

Existing categories (use these if they fit well):
{category_list}

IMPORTANT: Do NOT default to generic categories like "Expense" or "Income". If no existing category is a good fit, ALWAYS suggest a new specific category name. Good category names describe what you're spending on:
- "Coffee & Cafes" not "Expense"
- "Restaurants & Dining" not "Food"
- "Gas & Fuel" not "Transportation"
- "Software & Subscriptions" not "Expense"
- "Home Improvement" not "Shopping"
- "Pet Care" not "Expense"
- "Clothing & Apparel" not "Shopping"

For each transaction description, return a JSON array. Each element must have:
- "description": the original description (exact match)
- "merchant_name": the real business name (e.g., "Dunkin' Donuts", "OpenAI", "Wawa")
- "merchant_type": what kind of business (e.g., "Coffee & Donut Shop", "Software Company", "Gas Station & Convenience Store")
- "suggested_category": the best specific category. Use an existing category ONLY if it truly fits. Otherwise suggest a new descriptive name. Never use generic names like "Expense", "Income", "Other", or "Miscellaneous".
- "category_id": the ID of the matching existing category, or null if suggesting a new one
- "confidence": 0.0-1.0 how confident you are
- "reasoning": brief 1-sentence explanation
- "suggested_pattern": a generalized pattern for a transaction rule (strip store numbers, locations — e.g., "DUNKIN #XX6233 VENTNOR NJ" → "DUNKIN")

Other rules:
- Internal bank transfers, sweeps, money movements between accounts → "Transfers"
- Interest or dividend income → use the appropriate existing income category
- Strip payment processor prefixes (AplPay, SQ *, ZELLE) when identifying the merchant
- Be conservative with confidence — only use >0.9 when you're very certain of both the merchant AND the category

Return ONLY a valid JSON array, no other text.

Transactions to categorize:
{transaction_list}"""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=16384,
            messages=[
                {"role": "system", "content": "You are a financial transaction categorizer. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        # Parse the response
        text = response.choices[0].message.content.strip()
        # Handle potential markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            results = json.loads(text)
            if not isinstance(results, list):
                results = [results]
            return results
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}\nResponse: {text[:500]}")
            return []

    async def auto_categorize(
        self,
        mode: str = "preview",
        confidence_threshold: float = 0.7,
        create_rules: bool = True,
        max_descriptions: int = 100,
    ) -> AutoCategorizeResponse:
        """
        Run the full auto-categorization pipeline.

        Args:
            mode: "preview" (dry-run) or "apply"
            confidence_threshold: minimum confidence to auto-apply
            create_rules: whether to auto-create transaction rules
        """
        # Step 1: Get uncategorized descriptions
        desc_map = self.get_uncategorized_descriptions()
        if not desc_map:
            return AutoCategorizeResponse(
                total_transactions=0,
                unique_descriptions=0,
                high_confidence=0,
                medium_confidence=0,
                low_confidence=0,
                categories_created=0,
                rules_created=0,
                results=[],
            )

        categories = self.get_existing_categories()
        all_descriptions = list(desc_map.values())
        total_transactions = sum(d["count"] for d in all_descriptions)

        # Sort by count (most impactful first) and limit
        all_descriptions.sort(key=lambda d: d["count"], reverse=True)
        descriptions = all_descriptions[:max_descriptions]

        # Step 2: Classify in batches of 50
        all_classifications: List[Dict] = []
        batch_size = 20
        for i in range(0, len(descriptions), batch_size):
            batch = descriptions[i : i + batch_size]
            try:
                results = await self.classify_batch(batch, categories)
                all_classifications.extend(results)
            except Exception as e:
                logger.error(f"Batch classification failed: {e}")
                # Mark this batch as unclassified
                for d in batch:
                    all_classifications.append({
                        "description": d["description"],
                        "merchant_name": "Unknown",
                        "merchant_type": "Unknown",
                        "suggested_category": "",
                        "category_id": None,
                        "confidence": 0.0,
                        "reasoning": f"Classification failed: {str(e)}",
                        "suggested_pattern": None,
                    })

        # Step 3: Process results
        results: List[ClassificationResult] = []
        high_count = 0
        medium_count = 0
        low_count = 0
        categories_created = 0
        rules_created = 0

        # Build category name → id lookup
        cat_name_to_id = {c["category_name"].lower(): c["category_id"] for c in categories}

        for classification in all_classifications:
            desc = classification.get("description", "")
            confidence = classification.get("confidence", 0.0)
            suggested_cat = classification.get("suggested_category", "")
            cat_id = classification.get("category_id")
            count = desc_map.get(desc, {}).get("count", 0)

            # Resolve category_id
            if cat_id is None and suggested_cat:
                cat_id = cat_name_to_id.get(suggested_cat.lower())

            # Determine action based on confidence
            if confidence >= 0.9:
                action = "auto_applied"
                high_count += 1
            elif confidence >= confidence_threshold:
                action = "needs_review"
                medium_count += 1
            else:
                action = "unclassified"
                low_count += 1

            result = ClassificationResult(
                description=desc,
                merchant_name=classification.get("merchant_name", "Unknown"),
                merchant_type=classification.get("merchant_type", "Unknown"),
                suggested_category=suggested_cat,
                category_id=cat_id,
                confidence=confidence,
                reasoning=classification.get("reasoning", ""),
                transaction_count=count,
                action=action,
                suggested_pattern=classification.get("suggested_pattern"),
            )
            results.append(result)

            # Step 4: Apply if mode == "apply"
            if mode == "apply" and action == "auto_applied" and cat_id:
                # Create category if it doesn't exist
                if cat_id is None and suggested_cat:
                    new_cat = Category(
                        category_name=suggested_cat,
                        category_type=desc_map.get(desc, {}).get("transaction_type", "Expense"),
                    )
                    self.db.add(new_cat)
                    self.db.flush()
                    cat_id = new_cat.category_id
                    result.category_id = cat_id
                    cat_name_to_id[suggested_cat.lower()] = cat_id
                    categories_created += 1

                # Update transactions
                nan_cat = self.db.query(Category).filter(
                    Category.category_name == "nan"
                ).first()

                from sqlalchemy import or_
                conditions = [Transaction.description == desc]
                cat_conditions = []
                if nan_cat:
                    cat_conditions.append(Transaction.category_id == nan_cat.category_id)
                cat_conditions.append(Transaction.category_id.is_(None))

                self.db.query(Transaction).filter(
                    Transaction.description == desc,
                    or_(*cat_conditions),
                ).update(
                    {Transaction.category_id: cat_id},
                    synchronize_session="fetch",
                )

                # Create transaction rule
                if create_rules and result.suggested_pattern:
                    from ..database.models import CategoryRule
                    existing_rule = self.db.query(CategoryRule).filter(
                        CategoryRule.description_pattern == result.suggested_pattern,
                    ).first()
                    if not existing_rule:
                        rule = CategoryRule(
                            rule_name=f"Auto: {result.merchant_name}",
                            description_pattern=result.suggested_pattern,
                            category_id=cat_id,
                            rule_priority=5,
                            is_active=True,
                        )
                        self.db.add(rule)
                        rules_created += 1

        if mode == "apply":
            self.db.commit()

        return AutoCategorizeResponse(
            total_transactions=total_transactions,
            unique_descriptions=len(desc_map),
            high_confidence=high_count,
            medium_confidence=medium_count,
            low_confidence=low_count,
            categories_created=categories_created,
            rules_created=rules_created,
            results=results,
        )
