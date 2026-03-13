# PRD: Custom Scenario Creation & Life Event Modeling (Condensed)

**Product:** Spearmint Personal Finance Engine | **Feature:** Custom Scenario Creation | **Status:** Ready for Implementation | **Updated:** 2026-03-13

---

## Prompts

**Claude prompt —**

I have included a PRD that describes the new custom scenario creation features we want to add. Add the additional endpoints needed to in the existing scenarios folder of this collection - 44359130-9f8d4a5e-eb0c-4a5c-8086-e28a5cc10a3a using the postman mcp sever that you have access to. include the nessecary inputs and outputs needed to implement the new feature

**Postman prompt (create all in spec) —**
I have included a PRD that describes the new custom scenario creation features we want to add. Add the additional information needed to the existing spec (paths, schemas, responses, etc) needed to implement the new feature(s).

**Claude prompt (create all in spec local) —**
I have included a PRD that describes the new custom scenario creation features we want to add. Add the additional information needed to the existing spec in postman /workspace/postman/specs/Spearmint Core API/index.yaml . The spec already has scenario endpoints but they need enhancement to match the PRD. Add a comprehensive components section with proper schemas and improve the existing endpoint documentation. Also include any additional paths, schemas, responses, etc needed to implement the new feature(s).

**Postman prompt (create tests) —**
Generate tests for the custom scenario creation request

**Postman prompt (create only in collection) —**
I have included a PRD that describes the new custom scenario creation features we want to add. We want to work only on the scenario builder functionality at the moment. Add the additional endpoint needed to in the existing scenarios folder of the collection. include a success and a validation error example.

---

## Executive Summary

The existing scenario planning feature provides system-defined adjusters (income change, expense change) but users cannot create their own scenarios from scratch to model real life events. This feature adds a guided scenario builder that lets users compose multi-adjuster scenarios from a template library or from blank, modeling complex life events like having a baby, buying a house, or changing careers — all against their real financial data.

**Expected Impact:** 55% increase in scenario feature adoption, 3x increase in avg. scenarios per user, 45% reduction in "how do I model X" support tickets.

---

## Problem Statement

Users can preview and save single-adjuster scenarios today, but real life events involve multiple simultaneous financial changes. Having a baby means new insurance costs, childcare expenses, reduced income during leave, and medical bills — not just one adjustment. Users have no way to compose these multi-factor scenarios, and no starting point for common life events they want to model.

**Evidence:**
- 74 related support tickets in 90 days asking "how do I model [life event]"
- 13/15 interviewed users said they abandoned scenario planning because single adjustments felt unrealistic
- 10/15 said they'd use scenario planning weekly if they could model real life events
- Top requested events: having a baby (9), buying a home (8), job change (7), tax increase (6), retirement planning (5)

---

## Goals & Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| Users creating custom scenarios | 40% | 3 months post-launch |
| Avg. scenarios per user/month | 6 | 3 months post-launch |
| User satisfaction rating | 4.5/5 | 1 month post-launch |
| "How do I model X" ticket reduction | 45% | 2 months post-launch |
| Template usage rate | 60% of new scenarios | 3 months post-launch |

---

## User Stories (MVP)

- **Create from template** — Select a life event template (e.g., "Having a Baby"), see pre-populated adjusters, customize values, preview impact
- **Create from blank** — Start with an empty scenario, add adjusters one at a time, name it, preview, and save
- **Compose multi-adjuster scenarios** — Combine income changes, expense additions, expense changes, and one-time costs into a single scenario
- **Customize template values** — Modify any pre-filled amount, date, or category before previewing
- **Clone and modify** — Duplicate an existing saved scenario, change parameters, save as new
- **Compare custom scenarios** — View any saved scenario against baseline or against another saved scenario

**Deferred:** Community-shared templates, AI-suggested scenarios, scenario collaboration, probability weighting.

---

## User Workflows

### Workflow 1: Create from Template

1. Navigate to Scenarios page → Click **"Create Scenario"**
2. Browse template library: "Having a Baby", "Buying a Home", "Job Change", "Tax Increase", "Early Retirement", "Starting a Business"
3. Select template → System pre-fills adjusters with reasonable defaults and descriptions
4. Customize: adjust amounts, dates, categories to match personal situation
5. Click **"Preview"** → Review impact → Save or discard

**Performance:** Template load <500ms. Preview in <2 seconds.

### Workflow 2: Create from Blank

1. Navigate to Scenarios page → Click **"Create Scenario"** → Select **"Blank Scenario"**
2. Enter scenario name and optional description
3. Click **"Add Adjuster"** → Choose type (Income Change, Expense Addition, Expense Change, One-Time Cost)
4. Configure adjuster parameters → Repeat for additional adjusters
5. Click **"Preview"** → Review cumulative impact of all adjusters → Save or discard

### Workflow 3: Clone and Modify

1. Navigate to Saved Scenarios → Click **"..."** menu on existing scenario → Select **"Clone"**
2. System creates a copy with name "[Original Name] (Copy)"
3. Modify adjusters, add new ones, or remove existing ones
4. Preview and save as a new scenario

---

## Functional Requirements

### FR-1: Scenario Builder

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Name | Text (max 100 chars) | Yes | User-defined scenario name |
| Description | Text (max 500 chars) | No | Optional description of the life event being modeled |
| Template ID | Reference | No | If created from template, links back to source template |
| Adjusters | Array (1-20) | Yes (min 1) | List of financial adjustments that compose this scenario |

### FR-2: Adjuster Types

| Adjuster Type | Parameters | Example |
|---------------|------------|---------|
| **Income Change** | Category, % change (-100 to +200%), start date, end date (optional) | "Reduce Salary 100% for 12 weeks (parental leave)" |
| **Expense Addition** | Name, category, monthly amount, start date, end date (optional) | "Add Childcare $1,800/mo starting September 2026" |
| **Expense Change** | Category, % change (-100 to +1000%), start date, end date (optional) | "Increase Insurance 40% starting January 2027" |
| **One-Time Cost** | Name, amount, date, category | "Hospital delivery costs $5,000 in August 2026" |

### FR-3: Template Library

- Templates are read-only system records with a name, description, icon, and pre-configured adjuster list
- Each template adjuster includes a label, sensible default values, and a help tooltip explaining the assumption
- Users can browse and filter templates by category (Family, Housing, Career, Tax, Retirement)
- Template defaults are based on national averages with source citations in tooltips

**MVP Templates:**

| Template | Adjusters |
|----------|-----------|
| **Having a Baby** | Income reduction (parental leave), new expense (childcare), new expense (diapers/supplies), one-time cost (hospital), expense increase (insurance) |
| **Buying a Home** | New expense (mortgage), new expense (property tax), new expense (home insurance), new expense (maintenance), one-time cost (down payment + closing), expense removal (rent) |
| **Job Change** | Income change (new salary), expense change (commute), expense change (benefits/insurance) |
| **Tax Increase** | Income change (reduced take-home from higher effective rate) |
| **Early Retirement** | Income reduction (salary to $0), new expense (private health insurance), income addition (retirement withdrawals) |
| **Starting a Business** | Income reduction (salary), one-time cost (startup costs), new expense (business operating costs), income addition (projected revenue, delayed start) |

### FR-4: Multi-Adjuster Calculation Engine

- Applies all adjusters in a scenario to the baseline projection simultaneously
- Adjusters with overlapping date ranges stack (e.g., reduced income + increased expenses in same month)
- Calculates cumulative impact across all adjusters
- Generates scenario series (date/balance pairs) for charting
- Calculates deltas: runway change, min balance difference, total impact, monthly burn rate change

### FR-5: Scenario CRUD

- **Create:** Build from template or blank, validate, persist
- **Read:** List all saved scenarios with name, description, adjuster count, last run date
- **Update:** Edit name, description, add/remove/modify adjusters, re-preview
- **Delete:** Soft delete with confirmation dialog
- **Clone:** Deep copy all adjusters into a new scenario

### FR-6: Comparison Visualization

- **Dual-line chart:** Baseline vs. Scenario over time
- **Adjuster breakdown:** Table showing each adjuster's individual contribution to the total impact
- **Metrics card:** Runway delta, Min Balance delta, Monthly Burn Rate Change, Total Cash Flow Impact
- **Timestamp:** "Calculated as of [datetime]"

---

## Non-Functional Requirements

- **Performance:** Template list <500ms; scenario preview <2s (p95) regardless of adjuster count; scenario list <500ms (p95)
- **Data integrity:** Read-only operations; never modifies transaction data; calculation logic reuses existing projections engine
- **Mobile:** Scenario builder works on mobile; step-by-step wizard layout on small screens; touch-friendly adjuster cards
- **Accessibility:** Keyboard navigable; screen reader compatible; WCAG AA color contrast; adjuster form labels and help text accessible

---

## Technical Constraints

- Must use existing projections service for baseline calculations — no separate calculation logic
- Classification-aware: adjusters respect classification rules (don't adjust transfers/internal transactions)
- Requires 3+ months of income transaction history for accurate baselines
- API-first: backend owns calculation logic and template definitions, frontend consumes via API
- Templates are seeded data managed in code, not user-editable in MVP
- Maximum 20 adjusters per scenario to bound calculation complexity

---

## Out of Scope (Future)

Community-shared templates, AI-suggested scenarios based on spending patterns, scenario collaboration/sharing, probability weighting per adjuster, recurring one-time events, adjuster dependencies (if X then Y), scenario notifications/alerts, custom template creation by users.

---

## Open Questions (Resolved)

- Adjusters with overlapping date ranges stack additively (not multiplicatively)
- Template defaults use national averages; users must customize to their situation
- One-time costs are modeled as a single balance deduction on the specified date
- Saved scenarios become stale on new imports; user must manually refresh
- No limit on saved scenarios in MVP; 20 adjuster limit per scenario
- Clone creates a fully independent copy — changes to the clone do not affect the original

---

## Success Criteria

- [ ] Create a multi-adjuster "Having a Baby" scenario from template in <60 seconds
- [ ] Create a custom blank scenario with 3+ adjusters and preview cumulative impact
- [ ] Clone an existing scenario, modify adjusters, and save as new
- [ ] Side-by-side baseline vs. scenario chart with per-adjuster impact breakdown
- [ ] Save, list, edit, refresh, clone, and delete custom scenarios
- [ ] All 6 MVP templates available with sensible defaults and help tooltips
- [ ] Calculations complete in <2 seconds (p95) with up to 20 adjusters
- [ ] No modification of actual transaction data
- [ ] Mobile and accessible (keyboard nav, screen reader)
