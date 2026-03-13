PRD: Scenario-Based Financial Forecasting (Condensed)

Product: Spearmint Personal Finance Engine Feature: Scenario-Based Financial Forecasting Status: Ready for Implementation | Updated: 2026-01-21

Claude prompt - 

I have included a PRD that describes the new scenario planning features we want to add.  Add the additional endpoints needed to in the existing scenarios folder of this collection - 44359130-9f8d4a5e-eb0c-4a5c-8086-e28a5cc10a3a using the postman mcp sever that you have access to. include the nessecary inputs and outputs needed to implement the new feature

Postman prompt (create all in spec - 
I have included a PRD that describes the new scenario planning features we want to add. Add the additional information needed to the existing spec (paths, schemas, responses, etc) needed to implement the new feature(s). 

Claude prompt (create all in spec local) - 
I have included a PRD that describes the new scenario planning features we want to add. Add the additional information needed to the existing spec in postman /workspace/postman/specs/Spearmint Core API/index.yaml . The spec already has scenario endpoints but they need enhancement to match the PRD. Add a comprehensive components section with proper schemas and improve the existing endpoint documentation.   Also include any additional paths, schemas, responses, etc needed to implement the new feature(s).

Postman prompt (create tests) - 
Generate tests for the create scenario request

Postman prompt (create only in collection) - 
I have included a PRD that describes the new scenario planning features we want to add. We want to work only on the create functionality at the moment. Add the additional endpoint needed to in the existing scenarios folder of the collection. include the a success and a validation error example. 

Executive Summary

Users want to model "what-if" scenarios against their projections. This feature lets users define hypothetical adjustments (income changes, expense shocks) and see side-by-side comparisons of baseline vs. scenario projections.

Expected Impact: 40% increase in projection engagement, 60% reduction in scenario-related support tickets.

Problem Statement

Users face financial decisions (job transitions, major expenses, life events) but can only see one projection—their current trajectory. They can't experiment with adjustments without spreadsheets or mental math, creating decision paralysis.

Evidence: 88 related support tickets in 90 days. 14/15 interviewed users would use the feature weekly. 12/15 currently use spreadsheets for manual modeling. Competitors (YNAB, Mint, Personal Capital) lack robust scenario modeling.

Goals & Success Metrics

Metric

Target

Timeframe

Active users creating scenarios

35%

3 months post-launch

Avg. scenarios per user/month

4

3 months post-launch

User satisfaction rating

4.5/5

1 month post-launch

Scenario ticket reduction

60%

2 months post-launch

User Stories (MVP)

Simulate job loss — Model 100% income reduction from a specific date, see updated runway

Model expense changes — Increase/decrease expense categories by percentage or fixed amount, see cash flow impact

Compare baseline vs. scenario — Dual-line chart with delta metrics (runway change, minimum balance difference)

Quick preview without saving — Run ephemeral scenarios for rapid iteration

Save scenarios — Name, save, view, edit, delete saved scenarios

Refresh saved scenarios — Re-run with current transaction data

Deferred: One-time events, multi-factor scenarios, scenario sharing.

User Workflows

Workflow 1: Quick Preview (No Save)

Navigate to Projections page → Click "Run Scenario"

Configure in modal: adjustment type (Income/Expense Change), category, amount, start date

Click "Preview Scenario" → System displays side-by-side comparison

Review metrics (runway, min balance, cash flow impact) → Discard or iterate

Performance: Preview in <2 seconds.

Workflow 2: Save and Revisit

After previewing, click "Save Scenario" → Enter name

Later, navigate to "Saved Scenarios" list → Click to view

Click "Refresh" to recalculate with current data

Functional Requirements

FR-1: Scenario Configuration

Adjuster Type

Parameters

Example

Income Change

Category, % change (+/- 1-100%), start date, end date (optional)

"Reduce Salary 100% starting June 2026"

Expense Change

Category, % change (+/- 1-1000%), start date, end date (optional)

"Increase Rent 20% starting March 2026"

FR-2: Calculation Engine

Uses existing projections engine as baseline

Applies adjusters to historical average calculations

Generates scenario series (date/balance pairs) for charting

Calculates deltas: runway change, min balance difference, total impact

FR-3: Scenario Preview (Ephemeral)

Configuration in modal/overlay, no database persistence

Generates comparison chart and metrics on demand

FR-4: Scenario Persistence

Stored with: name, configuration, created date, last run date

Full CRUD operations

"Refresh" to re-run with current data

FR-5: Comparison Visualization

Dual-line chart: Baseline vs. Scenario over time

Metrics card: Runway delta, Min Balance delta, Total Cash Flow Impact

Timestamp: "Calculated as of [datetime]"

Non-Functional Requirements

Performance: Preview/refresh <2s (p95); list page <500ms (p95)

Data integrity: Read-only operations; never modifies transaction data; uses same logic as baseline projections

Mobile: All features work on mobile; touch-friendly forms; responsive charts

Accessibility: Keyboard navigable; screen reader compatible; WCAG AA color contrast

Technical Constraints

Must use existing projections service — no separate calculation logic

Classification-aware: adjusters respect classification rules (don't adjust transfers/internal transactions)

Requires 3+ months of transaction history for accurate baselines

API-first: backend owns calculation logic, frontend consumes via API

Out of Scope (Future)

One-time event modeling, multi-factor scenarios, scenario sharing/collaboration, scenario-vs-scenario comparison, confidence intervals, scenario notifications.

Open Questions (Resolved)

Adjustments apply to all transactions in selected category (respecting classification exclusions)

Saved scenarios become stale on new imports; user must manually refresh

No limit on saved scenarios in MVP

Success Criteria

[ ] Preview job loss and expense increase scenarios in <30 seconds

[ ] Side-by-side baseline vs. scenario chart with delta metrics

[ ] Save, list, refresh, and delete scenarios

[ ] Calculations complete in <2 seconds (p95)

[ ] No modification of actual transaction data

[ ] Mobile and accessible (keyboard nav, screen reader)