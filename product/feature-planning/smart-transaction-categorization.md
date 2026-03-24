# Product Requirements Document: Smart Transaction Categorization

**Product:** Spearmint Personal Finance Engine
**Feature:** LLM-Powered Transaction Auto-Categorization
**Owner:** Accounts Team
**Status:** Draft
**Last Updated:** 2026-03-24

---

## Executive Summary

Spearmint users import thousands of transactions from banks and brokerages, but the raw descriptions are cryptic merchant codes that don't map to human-readable categories. Today, users must manually categorize each transaction or create pattern-matching rules one at a time. With 6,700+ uncategorized transactions in a typical account, this is untenable.

This PRD defines **Smart Transaction Categorization** — a system that uses an LLM combined with web search to automatically identify merchants, infer transaction categories, and propose categorization rules. The goal: reduce uncategorized transactions from thousands to near-zero with minimal user effort.

**Expected Impact:**
- Auto-categorize 80%+ of imported transactions without user intervention
- Generate reusable rules from LLM classifications so future imports are instant
- Surface merchant identification (e.g., "ACME.COM #0294 VENTNOR CITY NJ" = ShopRite grocery store)
- Learn from user corrections to improve accuracy over time

---

## Problem Statement

### The User Problem

Bank transaction descriptions are designed for bank systems, not humans:

| Raw Description | What It Actually Is |
|----------------|-------------------|
| `ACME.COM #0294 VENTNOR CITY NJ` | ShopRite grocery store purchase |
| `AplPay ACTBLUE* EARLBOSTON MA` | ActBlue political donation |
| `OPENAI SAN FRANCISCO CA` | OpenAI API subscription |
| `FEE CHARGED Fidelity Basket Portfolios` | Brokerage management fee |
| `FIDELITY GOVERNMENT MONEY MARKET - PURCHASE INTO CORE ACCOUNT` | Internal cash sweep (transfer) |

Users face three problems:

1. **Volume:** Importing a year of transactions from multiple accounts yields thousands of uncategorized entries. Manual categorization is not feasible.

2. **Ambiguity:** Many descriptions are truncated, abbreviated, or use internal merchant codes that humans can't identify without searching.

3. **Repetition:** The same merchant appears hundreds of times. Users shouldn't have to categorize "ACME.COM" once — they should categorize it zero times.

### Current State

Spearmint has a **transaction rules** system that matches description patterns and assigns categories/entities. This works well for known patterns but requires users to manually create each rule. The system has no way to:
- Identify what a merchant is from its cryptic bank description
- Suggest which category a transaction belongs to
- Auto-generate rules from classifications
- Learn from user corrections

### Scale of the Problem

In the current dataset:
- **9,027** total transactions
- **6,706** categorized as "nan" (uncategorized) — 74%
- **10** categories exist (most user-created during manual categorization)
- **5** transaction rules exist (manually created)

---

## Solution Overview

### Architecture

```
┌─────────────────────────────────────────────────┐
│                User Triggers                      │
│  (Import, Bulk categorize, "Categorize All")      │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           Categorization Pipeline                 │
│                                                   │
│  1. Rule Matching (fast, deterministic)           │
│     → Apply existing rules first                  │
│                                                   │
│  2. LLM Classification (smart, batch)             │
│     → Group by unique description                 │
│     → Send batch to LLM with category list        │
│     → LLM returns category + confidence           │
│                                                   │
│  3. Web Search Enrichment (when needed)           │
│     → For low-confidence or unknown merchants     │
│     → Search "[description] + merchant"           │
│     → Feed search results to LLM for reclassify   │
│                                                   │
│  4. Rule Generation                               │
│     → High-confidence matches → auto-create rule  │
│     → Medium-confidence → propose rule to user    │
│     → Low-confidence → flag for manual review     │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              User Review                          │
│                                                   │
│  - Review proposed categories (approve/reject)    │
│  - Correct misclassifications                     │
│  - Corrections fed back as training signal        │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions

**1. Deduplicate before classifying.** Don't send 9,000 transactions to the LLM — group by unique description first. The 6,706 uncategorized transactions likely have ~500-1,000 unique descriptions. Classify each unique description once, then apply to all matching transactions.

**2. Rules are the durable artifact.** The LLM classifies; the output is a transaction rule. Once created, the rule handles all future imports of that merchant without calling the LLM again. This keeps ongoing costs near-zero.

**3. Confidence tiers drive automation level.**
- **High confidence (>0.9):** Auto-apply category, auto-create rule, no user review needed
- **Medium confidence (0.7-0.9):** Apply category, propose rule for user confirmation
- **Low confidence (<0.7):** Flag for manual review, don't create rule

**4. Web search is a fallback, not default.** Most merchant descriptions can be classified by the LLM alone using its training data. Web search is only triggered for unknown or ambiguous merchants to avoid unnecessary latency and cost.

**5. Batch processing for cost efficiency.** Send multiple descriptions in a single LLM call (up to 50 per batch). This reduces API costs by ~10x compared to one-call-per-transaction.

---

## Detailed Requirements

### Phase 1: Core Categorization Engine

#### P1.1: Batch LLM Classification Endpoint

**Backend:** `POST /api/transactions/auto-categorize`

Request:
```json
{
  "mode": "preview",           // "preview" (dry-run) or "apply"
  "scope": "uncategorized",    // "uncategorized", "all", or specific IDs
  "transaction_ids": [],       // optional: specific transactions
  "confidence_threshold": 0.7, // minimum confidence to auto-apply
  "create_rules": true,        // auto-create rules for high-confidence
  "web_search_fallback": true  // enable web search for low-confidence
}
```

Response:
```json
{
  "total_processed": 6706,
  "unique_descriptions": 847,
  "categorized": {
    "high_confidence": 523,
    "medium_confidence": 198,
    "low_confidence": 126
  },
  "categories_created": 12,
  "rules_created": 523,
  "results": [
    {
      "description": "ACME.COM #0294 VENTNOR CITY NJ",
      "merchant_name": "ShopRite",
      "merchant_type": "Grocery Store",
      "suggested_category": "Groceries",
      "category_id": 6,
      "confidence": 0.95,
      "reasoning": "ACME Markets/ShopRite grocery chain, location in Ventnor City NJ",
      "transaction_count": 47,
      "action": "auto_applied"
    }
  ]
}
```

#### P1.2: LLM Classification Logic

The classification prompt should include:
- The transaction description
- The existing category list (so the LLM maps to existing categories)
- The transaction amount and type (Income/Expense) for context
- The account name (for institution-specific patterns like brokerage sweeps)
- Instructions to identify the merchant name, merchant type, and best category

**Prompt structure:**
```
You are a financial transaction categorizer. Given bank transaction
descriptions, identify the merchant and assign the best category.

Existing categories:
{category_list}

For each transaction, return:
- merchant_name: The real business name
- merchant_type: What kind of business (grocery, restaurant, utility, etc.)
- category: Best matching category from the list, or suggest a new one
- confidence: 0.0-1.0 how confident you are
- reasoning: Brief explanation

Transactions to categorize:
{batch_of_descriptions}
```

#### P1.3: Web Search Enrichment

For descriptions where the LLM confidence is below 0.7:
1. Search the web for: `"{description}" merchant` or `"{description}" what is`
2. Feed the top 3 search results back to the LLM
3. Re-classify with the additional context

This handles cases like:
- Regional businesses the LLM hasn't seen
- Merchant codes that are abbreviations (e.g., "WAWA XXX 870" = Wawa convenience store)
- Payment processor prefixes (e.g., "AplPay", "SQ *", "ZELLE")

#### P1.4: Rule Auto-Generation

After classification, for each unique description with confidence > threshold:
1. Extract a generalized pattern (strip location-specific suffixes, store numbers)
2. Create a transaction rule with the pattern and assigned category
3. Mark the rule as "auto-generated" for audit trail

**Pattern generalization examples:**
| Raw Description | Generated Pattern | Category |
|----------------|------------------|----------|
| `ACME.COM #0294 VENTNOR CITY NJ` | `ACME.COM` | Groceries |
| `AplPay WAWA XXX 870 BEAR DE` | `WAWA` | Gas Station / Convenience |
| `AMAZON MKTPL*BD5Y44LM0` | `AMAZON MKTPL` | Shopping |
| `OPENAI SAN FRANCISCO CA` | `OPENAI` | Software / Subscriptions |

### Phase 2: User Interface

#### P2.1: Entry Points

**Transaction List Toolbar:**
A "Smart Categorize" button in the transaction list toolbar (alongside "Detect Relationships" and "Export CSV"). Clicking it launches the categorization pipeline on all uncategorized transactions and opens a review dialog with results.

**Post-Import Flow (Phase 3):**
After importing transactions, auto-run the pipeline on uncategorized imports. Show notification: "42 imported, 38 auto-categorized, 4 need review" with a link to the review dialog.

#### P2.2: Smart Categorize Review Dialog

A full-screen dialog showing results in three sections:

```
Smart Categorization Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Processing: 847 unique descriptions from 6,706 transactions

✅ Auto-Applied (523 descriptions, 4,102 transactions)
These were high-confidence matches. Rules have been created.

  ACME.COM → Groceries (47 txns)                    [Undo]
  OPENAI → Software Subscriptions (12 txns)          [Undo]
  AMAZON MKTPL → Shopping (89 txns)                  [Undo]
  WAWA → Gas & Convenience (23 txns)                 [Undo]
  ...show more

⚠️ Needs Review (198 descriptions, 1,847 transactions)
These need your confirmation. Click to approve or change the category.

  AplPay ACTBLUE* → Political Donation? (3 txns)    [✓ Accept] [Change ▾]
  FEE CHARGED Fidelity → Bank Fees? (8 txns)        [✓ Accept] [Change ▾]
  Check Paid # → ??? (15 txns)                       [Assign ▾]
  ...

❓ Unclassified (126 descriptions, 757 transactions)
Could not determine category. Assign manually or skip.

  PLVCC6H2K3 → Unknown (2 txns)                     [Assign ▾] [Skip]
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Accept All Reviewed]  [Close]
```

**Key interactions:**
- Each row represents a unique description, not individual transactions
- "Change" opens a category dropdown (with inline create, reusing existing pattern)
- "Accept" creates the rule and applies to all matching transactions
- "Accept All Reviewed" bulk-applies all medium-confidence suggestions
- "Undo" on auto-applied items removes the category and deletes the rule
- Progress bar during processing with live updates

#### P2.3: Correction Feedback Loop

When a user corrects a categorization:
1. Update the transaction's category
2. Update or create the corresponding rule
3. Store the correction as a "training signal" for future batches
4. Re-categorize other transactions with the same description

### Phase 3: Continuous Categorization

#### P3.1: Auto-Categorize on Import

When new transactions are imported:
1. Run existing rules first (instant, free)
2. For remaining uncategorized, batch-classify with LLM
3. Apply high-confidence results automatically
4. Queue medium/low-confidence for user review
5. Show notification: "12 new transactions imported. 10 auto-categorized, 2 need review."

#### P3.2: Category Suggestion on Manual Entry

When a user creates a transaction manually:
- After typing the description, suggest a category based on LLM classification
- Show as an autocomplete suggestion, not a forced selection

---

## Technical Considerations

### LLM Provider

- **Primary:** Claude API (Anthropic) — best at structured extraction and following category schemas
- **Fallback:** OpenAI GPT-4o — widely available, good at merchant identification
- **Configuration:** Provider and model should be configurable via environment variables
- **Cost estimate:** ~$0.02 per batch of 50 descriptions with Claude Haiku, ~$0.50 for full initial categorization of 1,000 unique descriptions

### Web Search Provider

- **Primary:** Brave Search API or SerpAPI — structured results, reasonable pricing
- **Fallback:** DuckDuckGo instant answers (free, limited)
- **Rate limiting:** Max 10 searches per categorization batch to control costs

### Performance

- **Batch size:** 50 descriptions per LLM call (balances latency vs. cost)
- **Parallelism:** Up to 5 concurrent LLM calls for large batches
- **Caching:** Cache LLM responses by description hash for 30 days
- **Total time for initial categorization:** ~2-5 minutes for 1,000 unique descriptions

### Data Privacy

- Transaction descriptions are sent to external LLM APIs
- No account numbers, balances, or PII are included in classification requests
- Users should be informed and consent before first use
- Option to use local/self-hosted models for privacy-sensitive users

---

## Category Taxonomy

The auto-categorizer should be able to suggest new categories beyond the existing set. Recommended starter taxonomy:

**Income:** Salary, Dividend Income, Interest, Rental Income, Capital Gains, Refunds
**Housing:** Mortgage, Rent, Property Tax, Home Insurance, HOA, Maintenance
**Transportation:** Gas, Auto Insurance, Auto Maintenance, Parking, Public Transit, Rideshare
**Food:** Groceries, Restaurants, Coffee Shops, Food Delivery
**Utilities:** Electric, Gas (Utility), Water, Internet, Phone, Streaming
**Shopping:** Amazon, Clothing, Electronics, Home Goods, General Retail
**Health:** Health Insurance, Medical, Dental, Pharmacy, Gym
**Financial:** Bank Fees, Credit Card Fees, Investment Fees, Tax Payment
**Personal:** Education, Childcare, Pet, Subscriptions, Donations
**Transfer:** Internal Transfer, Account Transfer, Loan Payment

---

## Acceptance Criteria

### Phase 1 (MVP)
- [ ] `POST /api/transactions/auto-categorize` endpoint works in preview and apply modes
- [ ] LLM correctly identifies merchant names for 80%+ of common transaction descriptions
- [ ] Categories are assigned with confidence scores
- [ ] High-confidence results auto-create transaction rules
- [ ] Web search fallback improves classification for unknown merchants
- [ ] Batch processing handles 1,000+ unique descriptions without timeout
- [ ] Existing categories are used when appropriate; new categories suggested when needed

### Phase 2
- [ ] Review UI shows proposed categorizations grouped by confidence
- [ ] Users can approve/reject/modify in bulk
- [ ] Corrections update rules and re-categorize matching transactions

### Phase 3
- [ ] New imports auto-categorize without user action
- [ ] Manual transaction entry suggests categories from description

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Auto-categorization accuracy | >80% correct on first pass | User correction rate after auto-categorization |
| Uncategorized transaction rate | <5% after initial run | Count of "nan" category transactions / total |
| Rule generation | >500 rules from initial run | Count of auto-generated rules |
| User effort reduction | 90% fewer manual categorizations | Manual category changes per import batch |
| Processing time | <5 minutes for initial batch | Wall clock time for full categorization |
| Cost per categorization | <$1.00 for initial batch | LLM API costs for full run |

---

## Open Questions

1. **Should we support local LLMs?** Self-hosted models (Llama, Mistral) would eliminate privacy concerns but require infrastructure. Could be Phase 4.

2. **How should we handle multi-entity transactions?** If a transaction could belong to multiple entities (e.g., shared household expense), should the auto-categorizer also suggest entity assignment?

3. **Should categories be hierarchical?** A deep taxonomy (Food > Groceries > Organic) provides more insight but increases classification complexity. Start flat, add hierarchy later?

4. **Merchant database vs. LLM?** Should we build a local merchant lookup database over time (from LLM responses + user corrections) to reduce API calls? The rules system partially serves this purpose already.
