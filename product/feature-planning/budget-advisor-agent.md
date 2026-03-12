# Product Requirements Document: Budget Advisor Agent

**Product:** Spearmint Personal Finance Engine
**Feature:** Budget Advisor Agent (A2A)
**Owner:** Product Team
**Status:** Draft
**Last Updated:** 2026-03-12

---

## Executive Summary

Users have rich transaction history in Spearmint but lack actionable guidance on how to optimize their spending. They want to know: *"Where am I overspending?"* and *"What can I realistically cut back on?"* — and they want that guidance to be continuous, not a one-time report.

This PRD defines the **Budget Advisor Agent** — an autonomous A2A (Agent-to-Agent) agent that continuously monitors spending patterns, proactively surfaces alerts, generates personalized budgets, and orchestrates specialized sub-agents to deliver comprehensive financial advice. Unlike a passive MCP tool that only responds when called, the Budget Advisor is a peer in a multi-agent ecosystem: it initiates conversations, delegates work to other agents, maintains state across interactions, negotiates with callers about data quality trade-offs, and can be deployed independently by third parties.

**Expected Impact:**
- Surface spending reduction opportunities users wouldn't find on their own
- Provide personalized, data-driven budget recommendations (not generic rules of thumb)
- Proactively alert users to spending anomalies without requiring them to ask
- Enable a multi-agent financial advisory ecosystem through A2A orchestration
- Bridge the gap between Spearmint's analytical depth and actionable financial guidance

---

## Why A2A (Not MCP)

A simple spending analysis tool could be implemented as an MCP tool — the LLM calls it, gets results, done. The Budget Advisor is designed as an A2A agent because it requires five capabilities that MCP tools cannot provide:

| Capability | MCP Tool | A2A Agent | Budget Advisor Needs |
|------------|----------|-----------|---------------------|
| **Autonomous initiative** | Passive — only responds when called | Active — can initiate conversations | Monitors spending continuously and pushes alerts to Minty when anomalies are detected |
| **Agent orchestration** | Tools don't call other tools | Agents delegate to and coordinate with other agents | Orchestrates Subscription Auditor, Bill Negotiator, and Tax Optimizer agents |
| **Stateful interactions** | Stateless request/response | Maintains state, memory, and ongoing goals | Tracks budget adherence month-over-month, follows up on previous recommendations |
| **Negotiation** | Succeeds or fails | Agents negotiate approach and trade-offs | Communicates data quality issues and confidence levels; proposes alternatives when data is insufficient |
| **Independent deployment** | Bundled with the server | Independently deployed service with runtime discovery | Third-party advisors can build and deploy their own Budget Advisor implementations |

---

## Problem Statement

### The User Problem

Spearmint shows users *what* they spent, but not *what they should do about it*:

1. **No spending benchmarks:** Users see category totals but have no sense of whether $400/month on dining is reasonable for their income level.

2. **No prioritized recommendations:** Even users who know they overspend don't know *where* cutting back would have the most impact relative to the effort required.

3. **No budget generation:** Users must manually set budgets category-by-category. Most never do, losing the value of forward-looking financial planning.

4. **No trend-aware advice:** Static budgets ignore that spending patterns change seasonally, after life events, or as habits shift.

5. **No proactive monitoring:** Users must remember to check their spending. Nobody tells them "hey, your dining spending just spiked 40% this week" unless they go look.

6. **Fragmented analysis:** Getting a holistic "financial health checkup" requires visiting multiple pages (Analysis, Expenses, Cash Flow, Projections) and synthesizing the data yourself. No single agent coordinates across these domains.

### Evidence

- The AI Assistant PRD (User Story #8) identifies "How can I reduce my expenses?" as a top post-MVP request
- Users with 6+ months of transaction history have sufficient data for meaningful analysis but no automated way to leverage it
- Competitor apps (Monarch, YNAB, Copilot Money) are adding AI-driven budget suggestions
- Users report wanting Spearmint to "tell me when something looks wrong" rather than having to check manually

---

## Goals & Success Metrics

### Goals

1. **Identify actionable savings:** Surface the top 3-5 categories where the user can realistically reduce spending
2. **Generate personalized budgets:** Produce a monthly budget based on actual spending patterns, not arbitrary targets
3. **Explain the "why":** Every recommendation includes context (trend data, benchmarks, impact estimate)
4. **Proactively monitor and alert:** Detect spending anomalies and push alerts without user prompting
5. **Orchestrate specialized agents:** Coordinate sub-agents for subscription auditing, bill negotiation, and tax optimization
6. **Maintain continuity:** Track recommendations over time and follow up on budget adherence

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Users who receive budget advice and reduce spending in recommended categories | 30% | 3 months post-launch |
| Avg. number of actionable recommendations per analysis | 3-5 | Launch |
| Agent invocation success rate (A2A calls) | 99% | Launch |
| User satisfaction with recommendation relevance | 4.2/5 | 2 months post-launch |
| Proactive alerts acted upon (user clicks through or adjusts spending) | 40% | 3 months post-launch |
| Sub-agent orchestration success rate | 95% | Phase 3 launch |
| Adoption by other agents (Minty, MCP, third-party) | 3+ callers | 3 months post-launch |

---

## A2A Agent Design

### Agent Card

The Budget Advisor registers itself as an A2A-compliant agent with the following Agent Card:

```json
{
  "name": "budget-advisor",
  "description": "Autonomous financial advisor that monitors spending, generates budgets, orchestrates sub-agents, and proactively surfaces savings opportunities",
  "version": "1.0.0",
  "capabilities": {
    "input": ["spending-analysis-request"],
    "output": ["budget-recommendation", "savings-opportunities", "spending-alerts"],
    "proactive": true,
    "stateful": true,
    "orchestrator": true
  },
  "endpoint": "/a2a/budget-advisor",
  "authentication": "bearer",
  "skills": [
    {
      "id": "analyze-spending",
      "description": "Evaluate current spending across all categories and identify optimization opportunities"
    },
    {
      "id": "generate-budget",
      "description": "Create a personalized monthly budget based on income, spending history, and goals"
    },
    {
      "id": "compare-periods",
      "description": "Compare spending between two time periods and explain significant changes"
    },
    {
      "id": "monitor",
      "description": "Continuously monitor spending and emit alerts when anomalies are detected"
    },
    {
      "id": "follow-up",
      "description": "Review adherence to a previously generated budget and adjust recommendations"
    }
  ]
}
```

### A2A Interaction Patterns

#### Pattern 1: Request/Response (Agent Called)

The standard pattern — another agent invokes the Budget Advisor.

```
Calling Agent (Minty / MCP / External)
    │
    ├─► POST /a2a/budget-advisor
    │   {
    │     "skill": "analyze-spending",
    │     "params": {
    │       "person_id": 1,
    │       "months_back": 6,
    │       "goal": "reduce_spending"
    │     }
    │   }
    │
    ◄── Response
        {
          "status": "completed",
          "result": {
            "summary": "...",
            "recommendations": [...],
            "proposed_budget": {...},
            "confidence": 0.85
          }
        }
```

#### Pattern 2: Proactive Initiative (Agent Initiates)

The Budget Advisor monitors spending and pushes alerts to other agents when it detects anomalies. This is the key differentiator from an MCP tool — the agent acts on its own.

```
Budget Advisor (background monitor)
    │
    │   [Detects: dining spend 40% above trailing average]
    │
    ├─► POST /a2a/minty  (pushes alert to Minty)
    │   {
    │     "type": "spending-alert",
    │     "priority": "medium",
    │     "alert": {
    │       "category": "Dining Out",
    │       "signal": "spike",
    │       "current_week": 180.00,
    │       "typical_week": 105.00,
    │       "message": "Dining spending is 71% above your weekly average this week"
    │     },
    │     "suggested_action": "Present alert to user with option to see details"
    │   }
    │
    Minty decides when/how to surface this to the user
```

**Monitor Triggers:**
| Trigger | Threshold | Alert Priority |
|---------|-----------|----------------|
| Weekly spending spike in any category | >50% above trailing 4-week avg | Medium |
| New recurring charge detected | 2+ identical charges in 60 days | Low |
| Monthly budget exceeded (if budget active) | >100% of budgeted amount with >7 days remaining | High |
| Income drop detected | Monthly income >20% below trailing avg | High |
| Savings rate decline | Savings rate dropped >5 percentage points month-over-month | Medium |

#### Pattern 3: Agent Orchestration (Agent Delegates)

The Budget Advisor orchestrates specialized sub-agents to build comprehensive recommendations. It delegates, collects results, and synthesizes.

```
Budget Advisor
    │
    ├─► POST /a2a/subscription-auditor
    │   { "skill": "audit", "params": { "months_back": 3 } }
    │   ◄── { "duplicates": [...], "unused": [...], "annual_waste": 340.00 }
    │
    ├─► POST /a2a/bill-negotiator
    │   { "skill": "find-opportunities", "params": { "categories": ["Insurance", "Internet", "Phone"] } }
    │   ◄── { "negotiable": [...], "estimated_savings": 600.00 }
    │
    ├─► POST /a2a/tax-optimizer
    │   { "skill": "scan-deductions", "params": { "year": 2026 } }
    │   ◄── { "missed_deductions": [...], "potential_savings": 1200.00 }
    │
    └─► Synthesizes all results into unified recommendation set
        {
          "spending_cuts": [...],           // from own analysis
          "subscription_savings": [...],    // from subscription-auditor
          "bill_negotiation": [...],        // from bill-negotiator
          "tax_opportunities": [...],       // from tax-optimizer
          "total_annual_savings": 4100.00
        }
```

**Sub-Agent Registry:**
| Agent | Purpose | Status |
|-------|---------|--------|
| `subscription-auditor` | Detect duplicate, unused, or overpriced subscriptions | Future (Phase 3) |
| `bill-negotiator` | Identify bills that could be reduced by switching providers or negotiating | Future (Phase 4) |
| `tax-optimizer` | Scan for missed deductions and tax-efficient categorization | Future (Phase 4) |

The Budget Advisor gracefully degrades when sub-agents are unavailable — it returns its own analysis and notes which sub-agents could not be reached.

#### Pattern 4: Negotiation (Agent Discusses Trade-offs)

When data quality is insufficient or the request is ambiguous, the Budget Advisor negotiates with the calling agent rather than silently returning low-quality results.

```
Minty
    │
    ├─► POST /a2a/budget-advisor
    │   { "skill": "generate-budget", "params": { "months_back": 6 } }
    │
    ◄── Response (status: "needs_input")
        {
          "status": "needs_input",
          "issue": "insufficient_data",
          "details": {
            "requested_months": 6,
            "available_months": 2,
            "uncategorized_pct": 0.35,
            "message": "Only 2 months of data available and 35% of transactions are uncategorized."
          },
          "options": [
            {
              "id": "proceed_low_confidence",
              "description": "Generate budget with low confidence (data covers 2 months only)",
              "confidence": 0.45
            },
            {
              "id": "wait_for_categorization",
              "description": "Categorize transactions first, then re-run for higher accuracy",
              "prerequisite": "Classify the 147 uncategorized transactions"
            },
            {
              "id": "reduce_scope",
              "description": "Analyze only the 3 categories with enough data (Housing, Groceries, Dining)",
              "confidence": 0.72
            }
          ]
        }

Minty presents options to user, user chooses, Minty re-invokes:

    ├─► POST /a2a/budget-advisor
    │   {
    │     "skill": "generate-budget",
    │     "params": { "months_back": 6 },
    │     "negotiation": { "chosen_option": "reduce_scope" }
    │   }
    │
    ◄── Response (status: "completed", scoped to 3 categories)
```

**Negotiation Triggers:**
| Condition | Agent Response |
|-----------|---------------|
| <3 months of transaction history | Offer: proceed with low confidence, or wait for more data |
| >20% uncategorized transactions | Offer: proceed anyway, categorize first, or analyze only categorized |
| Conflicting goals (e.g., "save aggressively" + "don't cut dining") | Offer: ranked trade-offs showing impact of each constraint |
| Multiple persons with no split data | Offer: household-level analysis, or prompt for split configuration |

#### Pattern 5: Stateful Follow-Up (Agent Remembers)

The Budget Advisor maintains state across interactions. When it generates a budget, it remembers the targets and can follow up in subsequent months.

```
Month 1: Budget Created
    Minty ──► budget-advisor.generate-budget
    ◄── Budget with targets: Dining $350, Shopping $200, Entertainment $150

Month 2: Follow-Up Review
    Budget Advisor (scheduled or on-demand)
    │
    ├─► Pulls actual spending for Month 1
    ├─► Compares against budget targets
    ├─► Generates adherence report
    │
    ├─► POST /a2a/minty  (pushes follow-up)
    │   {
    │     "type": "budget-followup",
    │     "period": "2026-02",
    │     "adherence": {
    │       "on_track": ["Housing", "Groceries", "Entertainment"],
    │       "over_budget": [
    │         {
    │           "category": "Dining Out",
    │           "budgeted": 350.00,
    │           "actual": 410.00,
    │           "overage": 60.00,
    │           "suggestion": "You were on track through the 20th — the overage came from 3 delivery orders in the last week. Consider setting a weekly sub-target of $87."
    │         }
    │       ],
    │       "under_budget": [
    │         {
    │           "category": "Shopping",
    │           "budgeted": 200.00,
    │           "actual": 120.00,
    │           "saved": 80.00
    │         }
    │       ],
    │       "overall_savings_vs_plan": -20.00,
    │       "adjusted_recommendation": "You're close to target overall. Shifting $50 from Shopping to Dining would match your actual behavior without increasing total spend."
    │     }
    │   }
```

**State Model:**

The agent persists the following state per user:

```json
{
  "user_id": 1,
  "active_budget": {
    "created_at": "2026-02-01",
    "strategy": "optimize",
    "targets": { "Dining Out": 350, "Shopping": 200 },
    "horizon_months": 3
  },
  "recommendation_history": [
    {
      "date": "2026-02-01",
      "recommendations": ["reduce_dining", "cancel_duplicate_streaming"],
      "outcome": { "reduce_dining": "partial", "cancel_duplicate_streaming": "completed" }
    }
  ],
  "alert_preferences": {
    "frequency": "weekly",
    "min_priority": "medium"
  }
}
```

---

### Caller Examples

**Minty (AI Assistant) — Reactive:**
> User: "How can I save more money?"
> Minty invokes `budget-advisor.analyze-spending` → receives recommendations → presents conversationally

**Minty (AI Assistant) — Proactive Alert:**
> Budget Advisor pushes spending-alert to Minty → Minty decides timing → Minty tells user: "Heads up — your dining spending is running 40% above average this week"

**MCP Server (Claude Desktop):**
> User: "Create a budget for me based on my spending"
> MCP tool calls `budget-advisor.generate-budget` → returns structured budget → Claude formats for user

**Scheduled Follow-Up:**
> First of each month, Budget Advisor reviews last month's adherence → pushes follow-up to Minty → Minty presents: "Here's how you did against your budget last month"

**Third-Party Advisor Agent:**
> A financial planning company deploys their own Budget Advisor implementation → user connects it to their Spearmint instance → it discovers available data via A2A discovery → provides advice using the company's proprietary methodology

---

## Core Capabilities

### 1. Spending Analysis

**Input:** User's transaction history (configurable lookback window, default 6 months)

**Process:**
- Pull all non-transfer transactions from the Analysis view (respecting classification exclusions)
- Group by category, compute monthly averages, trends, and variance
- Identify categories with high variance (inconsistent spending)
- Identify categories with upward trends (growing spending)
- Identify categories consuming disproportionate share of income

**Output:**
```json
{
  "analysis_period": { "start": "2025-09-01", "end": "2026-03-01" },
  "monthly_income_avg": 8500.00,
  "monthly_expense_avg": 6200.00,
  "savings_rate": 0.27,
  "category_breakdown": [
    {
      "category": "Dining Out",
      "monthly_avg": 420.00,
      "trend": "increasing",
      "trend_pct": 12.5,
      "pct_of_income": 4.9,
      "pct_of_expenses": 6.8,
      "variance": "high",
      "months": [380, 400, 410, 450, 460, 420]
    }
  ]
}
```

### 2. Savings Opportunity Detection

Identifies specific areas where the user can cut back, ranked by impact and feasibility:

**Detection Rules:**
| Rule | Signal | Example |
|------|--------|---------|
| Upward trend | Category spending increasing >10% over analysis window | "Dining Out spending has grown 12.5% over 6 months" |
| High variance | Monthly std dev >30% of mean | "Entertainment spending swings from $50 to $300/month" |
| Income disproportionate | Category >15% of income (excluding housing/essentials) | "Shopping is consuming 18% of your income" |
| Duplicate subscriptions | Multiple recurring charges in same category | "You have 3 separate streaming service charges" |
| Seasonal spike | Current month >50% above trailing average | "Your travel spending this month is 2x your average" |
| Peer comparison (future) | Spending significantly above anonymized cohort averages | "Your dining spending is in the top 20% for your income bracket" |

**Output per opportunity:**
```json
{
  "category": "Dining Out",
  "signal": "upward_trend",
  "severity": "moderate",
  "current_monthly": 460.00,
  "suggested_target": 380.00,
  "monthly_savings": 80.00,
  "annual_impact": 960.00,
  "confidence": 0.82,
  "reasoning": "Your dining spending has increased 12.5% over the last 6 months, from $380 to $460/month. Reducing to your 6-month floor of $380 would save $960/year.",
  "actionable_tips": [
    "Your highest dining charges are on weekends — consider meal prepping for Saturday lunches",
    "3 of your top 5 dining transactions are delivery services, which typically cost 30% more than dining in"
  ]
}
```

### 3. Budget Generation

Creates a personalized monthly budget based on actual spending patterns:

**Budget Strategies:**
| Strategy | Description | Use Case |
|----------|-------------|----------|
| `maintain` | Budget at current averages | "I want to stay where I am" |
| `optimize` | Reduce discretionary by 10-15% | "I want to save a bit more" |
| `aggressive` | Cut to minimums observed in history | "I need to seriously cut back" |
| `goal_based` | Work backward from a savings target | "I want to save $500/month more" |

**Output:**
```json
{
  "strategy": "optimize",
  "monthly_income": 8500.00,
  "budget_lines": [
    {
      "category": "Housing",
      "type": "fixed",
      "budgeted": 2200.00,
      "current_avg": 2200.00,
      "change": 0,
      "note": "Fixed cost — no adjustment recommended"
    },
    {
      "category": "Dining Out",
      "type": "discretionary",
      "budgeted": 350.00,
      "current_avg": 420.00,
      "change": -70.00,
      "note": "Trending up; target set to 6-month median"
    }
  ],
  "total_budgeted": 5800.00,
  "projected_savings": 2700.00,
  "savings_rate": 0.318,
  "improvement_vs_current": 450.00
}
```

### 4. Period Comparison

Compares two time periods and explains what changed:

**Input:** Two date ranges (e.g., this month vs. last month, this quarter vs. same quarter last year)

**Output:** Category-level deltas with explanations, flagging significant changes and likely causes based on transaction descriptions.

### 5. Continuous Monitoring

Runs on a configurable schedule (default: daily) to detect spending anomalies and budget deviations:

**Process:**
- Pull recent transactions since last check
- Compare rolling weekly/monthly totals against baselines
- Check active budget adherence
- Detect new recurring charges
- If any trigger fires, push alert to registered listener agents (e.g., Minty)

**Configuration:**
```json
{
  "monitor_frequency": "daily",
  "alert_targets": ["/a2a/minty"],
  "min_alert_priority": "medium",
  "active_budget_id": "budget-2026-03"
}
```

### 6. Budget Follow-Up

Triggered monthly (or on-demand) to review adherence to an active budget:

**Process:**
- Compare actual spending against budget targets for the completed period
- Categorize each line as on-track, over-budget, or under-budget
- Generate natural-language explanations for deviations
- Suggest budget adjustments for the next period based on actuals
- Push follow-up report to listener agents

---

## Data Requirements

The agent reads from the existing Spearmint data layer. Stateful features (active budgets, recommendation history) require new storage.

| Data Source | Used For | Access Via | New? |
|-------------|----------|------------|------|
| Transactions (analysis view) | Spending patterns, trends | `AnalysisService` | No |
| Categories | Grouping, fixed vs. discretionary classification | `Category` model | No |
| Classifications | Exclude transfers, CC payments | `TransactionClassification` model | No |
| Transaction Splits | Per-person spending | `TransactionSplit` model | No |
| Persons | Multi-person household analysis | `Person` model | No |
| Agent State | Active budgets, recommendation history, alert prefs | `AgentState` model | **Yes** |
| Monitor Checkpoints | Last-checked timestamp, rolling baselines | `MonitorCheckpoint` model | **Yes** |

### New Data Models

**AgentState** — Persists the agent's memory across interactions:
```python
class AgentState(Base):
    id: int
    user_id: int
    agent_name: str              # "budget-advisor"
    state_key: str               # "active_budget", "recommendation_history", "alert_preferences"
    state_value: JSON            # Flexible JSON payload
    created_at: datetime
    updated_at: datetime
```

**MonitorCheckpoint** — Tracks monitoring state:
```python
class MonitorCheckpoint(Base):
    id: int
    user_id: int
    agent_name: str
    last_checked_at: datetime
    rolling_baselines: JSON      # Category-level weekly/monthly averages
    pending_alerts: JSON         # Alerts not yet pushed
```

### Category Classification

The agent must distinguish between spending types to make appropriate recommendations:

| Type | Examples | Budget Treatment |
|------|----------|-----------------|
| **Fixed essential** | Housing, insurance, loan payments | Report but don't suggest cuts |
| **Variable essential** | Groceries, utilities, gas | Suggest optimization, not elimination |
| **Discretionary** | Dining, entertainment, shopping | Primary target for savings recommendations |
| **Periodic** | Travel, gifts, medical | Normalize across months; flag spikes |

This classification can be derived from existing category metadata (`category_type`) or extended with a new `budget_category_type` field if needed.

---

## Hybrid Architecture: Determinism + LLM

The Budget Advisor uses a **hybrid architecture** where deterministic computation and LLM reasoning each handle what they're best at. The rubric is simple: **if you can write an if/else for it, use determinism. If the answer requires interpretation, use the LLM.**

### Decision Rubric

| Use determinism when... | Use the LLM when... |
|---|---|
| The logic is a formula or threshold | The answer requires interpretation |
| The inputs are structured (numbers, categories) | The inputs are unstructured (descriptions, cross-category patterns) |
| The output is a known shape (alert/no-alert, number) | The output is open-ended (explanation, novel insight, advice) |
| Being wrong is costly (financial calculations) | Being approximate is fine (tone, framing, creative connections) |
| The rules are stable and domain-standard | The rules would require infinite branching to cover all cases |

### What Each Layer Does

**Deterministic layer** (SpendingAnalyzer, SavingsRecommender):
- Calculate monthly averages, trends, variance (math)
- Detect if a category exceeds a threshold (if/else)
- Generate budget numbers (arithmetic)
- Classify categories as fixed/variable/discretionary (lookup)
- Detect duplicate recurring charges (pattern match on amount + frequency)
- Rank opportunities by annual impact (sort)

**LLM layer** (Advisor reasoning):
- Explain *why* spending changed ("You started ordering delivery after you moved")
- Prioritize recommendations *for this specific person* ("Cutting dining won't work for you — you eat out for work. Focus on subscriptions instead")
- Correlate across categories ("Your gas spending dropped when your gym membership started")
- Generate advice that accounts for context ("You mentioned expecting a baby — here's how to adjust")
- Decide what's worth mentioning vs. noise ("Entertainment spiked, but it was a one-time concert — not actionable")
- Negotiate in natural language when data quality is poor

### Data Flow

```
Transactions
    │
    ▼
[Deterministic: SpendingAnalyzer]
    │  Monthly averages, trends, variance, category stats
    ▼
[Deterministic: SavingsRecommender]
    │  Structured signals: "dining +12%", "variance: high", "3 streaming subs"
    ▼
[LLM: Advisor Reasoning]
    │  Receives structured signals + transaction descriptions as context
    │  Reasons about what matters, what to say, how to prioritize
    ▼
Personalized advice
    "You're spending more on delivery since February.
     Cooking 2 more meals/week would save ~$80/month."
```

The LLM never does the math — it interprets the math. The deterministic layer never generates prose — it produces structured data for the LLM to reason about.

### Agent Implementation

```
core-api/
├── src/financial_analysis/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py              # A2A base agent class (discovery, negotiation, state)
│   │   ├── budget_advisor/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py         # BudgetAdvisorAgent (orchestrator — routes to deterministic or LLM)
│   │   │   ├── analyzer.py      # SpendingAnalyzer (deterministic: data crunching)
│   │   │   ├── recommender.py   # SavingsRecommender (deterministic: detection rules, ranking)
│   │   │   ├── advisor.py       # AdvisorReasoning (LLM: interpretation, personalization, advice)
│   │   │   ├── budget_builder.py # BudgetBuilder (deterministic: budget generation)
│   │   │   ├── monitor.py       # SpendingMonitor (deterministic: anomaly detection)
│   │   │   ├── orchestrator.py  # SubAgentOrchestrator (delegates to sub-agents)
│   │   │   ├── state.py         # State persistence (budgets, history, prefs)
│   │   │   └── schemas.py       # Request/response Pydantic models
│   │   └── registry.py          # Agent registry for A2A discovery
│   ├── api/
│   │   └── routes/
│   │       └── agents.py        # A2A endpoint handler
```

### A2A Protocol

The agent follows the A2A (Agent-to-Agent) protocol:

1. **Discovery:** `GET /a2a/agents` returns registered agent cards
2. **Invocation:** `POST /a2a/{agent-name}` with skill ID and parameters
3. **Negotiation:** Response with `status: "needs_input"` and options array when data is insufficient or request is ambiguous
4. **Push:** Agent initiates `POST /a2a/{target-agent}` to push alerts and follow-ups
5. **Streaming (future):** SSE stream for long-running analyses with progress updates

### API Endpoints

```
GET  /a2a/agents                    # List all registered agents
GET  /a2a/agents/budget-advisor     # Get Budget Advisor agent card
POST /a2a/budget-advisor            # Invoke the Budget Advisor
POST /a2a/budget-advisor/subscribe  # Register as alert listener
GET  /a2a/budget-advisor/state      # Get current agent state (active budget, etc.)
```

### Independent Deployment

The Budget Advisor is designed to be deployable as a standalone service, separate from the core Spearmint API:

```
┌──────────────────────┐     ┌──────────────────────┐
│   Spearmint Core     │     │  Budget Advisor       │
│   (REST API + MCP)   │◄───►│  (A2A Agent)          │
│                      │     │                       │
│  /api/*              │     │  /a2a/budget-advisor  │
│  /a2a/agents         │     │  Own database/state   │
│  /a2a/minty          │     │  Own release cycle    │
└──────────────────────┘     └──────────────────────┘
         ▲                            ▲
         │                            │
    ┌────┴────┐                  ┌────┴────┐
    │  Minty  │                  │ 3rd Party│
    │  (MCP)  │                  │ Advisor  │
    └─────────┘                  └──────────┘
```

A third party can implement the Budget Advisor agent card interface, deploy their own instance, and users connect it to Spearmint via A2A discovery. The third-party agent:
- Discovers Spearmint's data capabilities via `GET /a2a/agents`
- Requests spending data through Spearmint's A2A data-access skills
- Applies its own proprietary analysis methodology
- Returns recommendations in the standard schema

---

## Implementation Phases

### Phase 1: Hybrid Spending Analysis & Recommendations (MVP)

**Scope:**
- `SpendingAnalyzer` (deterministic): Pull transaction data, compute category-level stats (averages, trends, variance)
- `SavingsRecommender` (deterministic): Apply detection rules, rank opportunities by annual impact
- `AdvisorReasoning` (LLM): Interpret structured signals, generate personalized explanations and actionable tips, decide what's worth mentioning vs. noise
- A2A endpoint: `POST /a2a/budget-advisor` with `analyze-spending` skill
- Agent card registration and discovery endpoint
- Negotiation: LLM explains data quality trade-offs conversationally when data is insufficient (<3 months or >20% uncategorized)

**Hybrid split in Phase 1:**
| Component | Layer | What it does |
|-----------|-------|-------------|
| Monthly averages, trends, variance | Deterministic | Math on transaction data |
| Detection rules (upward trend, high variance, etc.) | Deterministic | Threshold-based signal detection |
| Ranking by annual impact | Deterministic | Sort by savings potential |
| Reasoning text ("why this matters") | LLM | Interprets signals with transaction-level context |
| Actionable tips | LLM | Generates personalized advice from transaction descriptions |
| What to prioritize for *this* user | LLM | Filters noise, accounts for user context |
| Negotiation messaging | LLM | Explains data quality issues conversationally |

**Dependencies:**
- Existing `AnalysisService` for filtered transaction query patterns
- Existing `Category` model for category metadata
- Claude API (Anthropic SDK) for LLM reasoning

**Acceptance Criteria:**
- Given 6 months of transaction data, the agent returns 3-5 ranked savings recommendations
- Each recommendation includes deterministic data (signal, severity, savings estimate) AND LLM-generated reasoning and tips
- Deterministic layer completes in <1 second; full response with LLM in <5 seconds
- A2A endpoint returns valid response matching schema
- When data is insufficient, agent returns `needs_input` with LLM-generated explanation of trade-offs
- LLM layer degrades gracefully: if LLM is unavailable, return deterministic results with template-based reasoning as fallback

### Phase 2: Budget Generation & State

**Scope:**
- `BudgetBuilder`: Generate personalized budget from spending history
- Support 4 strategies: maintain, optimize, aggressive, goal_based
- `generate-budget` skill added to agent card
- Fixed vs. discretionary category classification
- `AgentState` model for persisting active budgets and recommendation history
- `follow-up` skill: Compare actuals against budget targets

**Acceptance Criteria:**
- Budget covers all categories with non-trivial spending
- Fixed costs are preserved; discretionary costs are adjusted per strategy
- Goal-based strategy correctly back-calculates required cuts to hit savings target
- Budget sums are consistent (income = budgeted + projected_savings)
- Active budget is persisted and retrievable across sessions
- Follow-up correctly compares actuals vs. targets and generates adherence report

### Phase 3: Proactive Monitoring & Agent Orchestration

**Scope:**
- `SpendingMonitor`: Background process that runs daily, checks for anomalies, pushes alerts
- `MonitorCheckpoint` model for tracking monitoring state
- Alert push: Budget Advisor initiates calls to registered listener agents (Minty)
- `subscribe` endpoint for agents to register as alert listeners
- `SubAgentOrchestrator`: Discover and invoke sub-agents (subscription-auditor as first integration)
- Graceful degradation when sub-agents are unavailable

**Acceptance Criteria:**
- Monitor detects spending spikes within 24 hours
- Alerts are pushed to registered listener agents with correct priority
- Budget Advisor discovers and invokes subscription-auditor when available
- When sub-agents are unreachable, Budget Advisor returns its own analysis with a note about unavailable enrichments
- Monitor runs without impacting API performance (background task)

### Phase 4: Advanced Reasoning & Ecosystem

**Scope:**
- Multi-turn LLM reasoning: Agent remembers past conversations and builds on prior advice
- Cross-category correlation: LLM identifies non-obvious patterns across spending categories and life events
- Peer benchmarking: Anonymous cohort comparisons (requires opt-in data aggregation)
- Bill Negotiator and Tax Optimizer sub-agent integrations
- Third-party agent deployment documentation and SDK
- Integration with Scenario Planning for "what-if I follow this budget" projections

---

## Constraints & Considerations

### Privacy & Security
- The agent operates entirely on the user's own data — no data leaves the Spearmint instance
- A2A authentication uses the same bearer token as the REST API
- No PII is logged in agent invocation records
- Third-party agents must authenticate and are subject to the same data access controls
- Alert push targets must be pre-registered and authenticated

### Data Quality
- Recommendations are only as good as transaction categorization; agent should negotiate (not silently degrade) when >20% of transactions are uncategorized
- Minimum data requirement: 3 months of history for meaningful trend analysis; agent should communicate reduced confidence with less data via the negotiation protocol

### Tone & Framing
- Recommendations should be supportive, not judgmental ("You could save..." not "You're overspending on...")
- Always present as suggestions, not mandates
- Include positive reinforcement ("Your savings rate of 27% is strong")
- Follow-ups should celebrate wins ("You came in under budget on Shopping — that saved you $80")

### Performance
- Target response time: <3 seconds for typical analysis (6 months, ~1000 transactions)
- Monitor background task: <10 seconds per user per daily run
- Sub-agent orchestration: 10-second timeout per sub-agent; fail open with partial results
- For larger datasets, consider pre-computation or caching of category-level aggregates

---

## Open Questions

1. **Category classification:** Should we add a `budget_category_type` field (fixed/variable/discretionary/periodic) to the Category model, or derive it heuristically from spending patterns?
2. **Multi-person budgets:** Should the agent produce a household budget or per-person budgets? Both?
3. **Budget persistence:** How long should budget history be retained? Should users be able to view past budgets and adherence trends?
4. ~~**LLM integration timing:**~~ **RESOLVED** — Hybrid from Phase 1. Deterministic layer handles math/thresholds, LLM handles interpretation/advice. Template-based fallback when LLM is unavailable.
5. **Notification channel:** When the agent pushes a proactive alert to Minty, how should Minty surface it? (Chat bubble, notification badge, email digest?)
6. **Third-party trust model:** What vetting or sandboxing is needed for third-party Budget Advisor implementations that access user financial data?
7. **Monitor scheduling:** Should the monitor run as a background thread in the API process, a separate worker process, or a scheduled job (cron/Celery)?
8. **LLM cost management:** How to handle LLM API costs for proactive monitoring (Phase 3)? Per-user rate limits? Cache common patterns? Only use LLM for high-priority alerts?

---

## References

- [AI Financial Assistant PRD](../AI_ASSISTANT_PRD.md) — User Story #8 (recommendations)
- [MCP Server PRD](../MCP_SERVER_PRD.md) — MCP integration surface
- [Analysis Service](../../core-api/src/financial_analysis/services/analysis_service.py) — Existing spending analysis logic
- [Scenario Service](../../core-api/src/financial_analysis/services/scenario_service.py) — Scenario planning integration point
- [Google A2A Protocol](https://github.com/google/A2A) — Agent-to-Agent protocol specification
