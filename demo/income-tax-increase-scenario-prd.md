PRD: Income Tax Increase Scenario Modeling (Condensed)

Product: Spearmint Personal Finance Engine Feature: Income Tax Increase Scenario Modeling Status: Ready for Implementation | Updated: 2026-03-13

Claude prompt -

I have included a PRD that describes the new income tax increase scenario feature we want to add. Add the additional endpoints needed to in the existing scenarios folder of this collection - 44359130-9f8d4a5e-eb0c-4a5c-8086-e28a5cc10a3a using the postman mcp sever that you have access to. include the nessecary inputs and outputs needed to implement the new feature

Postman prompt (create all in spec -
I have included a PRD that describes the new income tax increase scenario feature we want to add. Add the additional information needed to the existing spec (paths, schemas, responses, etc) needed to implement the new feature(s).

Claude prompt (create all in spec local) -
I have included a PRD that describes the new income tax increase scenario feature we want to add. Add the additional information needed to the existing spec in postman /workspace/postman/specs/Spearmint Core API/index.yaml . The spec already has scenario endpoints but they need enhancement to match the PRD. Add a comprehensive components section with proper schemas and improve the existing endpoint documentation. Also include any additional paths, schemas, responses, etc needed to implement the new feature(s).

Postman prompt (create tests) -
Generate tests for the tax scenario create request

Postman prompt (create only in collection) -
I have included a PRD that describes the new income tax increase scenario feature we want to add. We want to work only on the tax rate configuration functionality at the moment. Add the additional endpoint needed to in the existing scenarios folder of the collection. include a success and a validation error example.

Executive Summary

Users want to model the impact of income tax rate changes on their take-home pay and long-term financial health. This feature lets users define hypothetical federal, state, and local tax rate adjustments and see side-by-side comparisons of current vs. projected after-tax income, savings capacity, and cash flow runway.

Expected Impact: 30% increase in scenario engagement, 50% reduction in tax-planning-related support tickets.

Problem Statement

Users facing potential tax bracket changes (promotions, relocations, policy changes) have no way to model how increased tax burdens affect their disposable income and savings trajectory. They resort to external tax calculators that don't integrate with their actual spending data, creating fragmented financial planning.

Evidence: 62 related support tickets in 90 days. 11/15 interviewed users said tax impact modeling would influence major financial decisions. 13/15 currently use separate spreadsheets or online calculators. No competitor (YNAB, Mint, Personal Capital) offers integrated tax scenario modeling against real transaction data.

Goals & Success Metrics

Metric

Target

Timeframe

Active users creating tax scenarios

25%

3 months post-launch

Avg. tax scenarios per user/month

3

3 months post-launch

User satisfaction rating

4.5/5

1 month post-launch

Tax-related ticket reduction

50%

2 months post-launch

User Stories (MVP)

Model federal tax increase — Apply a new effective federal tax rate, see impact on monthly take-home pay and annual savings

Model state tax change (relocation) — Compare current state tax rate vs. a new state's rate, see net income difference

Model combined tax burden — Adjust federal, state, and local rates together, see cumulative impact on cash flow runway

Quick preview without saving — Run ephemeral tax scenarios for rapid iteration

Save tax scenarios — Name, save, view, edit, delete saved tax scenarios

Refresh saved tax scenarios — Re-run with current income data

Deferred: Tax bracket modeling with progressive rates, deduction optimization, estimated quarterly tax payments, multi-year tax projections.

User Workflows

Workflow 1: Quick Preview (No Save)

Navigate to Scenarios page → Click "New Tax Scenario"

Configure in modal: current effective rate, proposed rate, tax type (Federal/State/Local), applicable income categories, effective date

Click "Preview Impact" → System displays side-by-side comparison

Review metrics (monthly take-home delta, annual savings impact, runway change) → Discard or iterate

Performance: Preview in <2 seconds.

Workflow 2: Save and Revisit

After previewing, click "Save Scenario" → Enter name (e.g., "Move to California", "2027 Tax Bracket Bump")

Later, navigate to "Saved Scenarios" list → Click to view

Click "Refresh" to recalculate with current income data

Workflow 3: Relocation Comparison

Create scenario with current state tax rate → Save as baseline

Create second scenario with target state's tax rate → Save

Compare both against current projections on comparison view

Functional Requirements

FR-1: Tax Scenario Configuration

Tax Adjuster Type

Parameters

Example

Federal Rate Change

Current effective rate (%), proposed rate (%), effective date, end date (optional)

"Federal rate increases from 22% to 24% starting January 2027"

State Rate Change

Current state, proposed state (or custom rate), effective date, end date (optional)

"Relocate from Texas (0%) to California (9.3%) starting June 2026"

Local Rate Change

Current rate (%), proposed rate (%), effective date, end date (optional)

"City tax increases from 1.5% to 2.0% starting January 2027"

Combined Rate Change

Any combination of federal, state, and local adjustments applied together

"Federal +2%, State +3.3% starting January 2027"

FR-2: Tax Calculation Engine

Uses existing income data from projections engine as baseline gross income

Applies current effective tax rates to calculate baseline net income

Applies proposed tax rates to calculate scenario net income

Computes deltas: monthly take-home difference, annual net income change, cumulative impact over projection period

Accounts for income categories (salary, freelance, investment) with different tax treatments

FR-3: Tax Scenario Preview (Ephemeral)

Configuration in modal/overlay, no database persistence

Generates comparison chart and metrics on demand

Shows monthly and annual impact breakdowns

FR-4: Tax Scenario Persistence

Stored with: name, tax configuration (rates, types, dates), created date, last run date

Full CRUD operations

"Refresh" to re-run with current income data

FR-5: Tax Impact Visualization

Dual-line chart: Current Net Income vs. Scenario Net Income over time

Metrics card: Monthly Take-Home Delta, Annual Savings Impact, Runway Change, Effective Rate Comparison

Breakdown table: Tax impact by income category

Timestamp: "Calculated as of [datetime]"

Non-Functional Requirements

Performance: Preview/refresh <2s (p95); list page <500ms (p95)

Data integrity: Read-only operations; never modifies transaction data; uses same income data as baseline projections

Mobile: All features work on mobile; touch-friendly forms; responsive charts

Accessibility: Keyboard navigable; screen reader compatible; WCAG AA color contrast

Technical Constraints

Must use existing projections service — no separate calculation logic

Classification-aware: tax adjustments only apply to income categories (excludes transfers, refunds, reimbursements)

Requires 3+ months of income transaction history for accurate baselines

API-first: backend owns calculation logic, frontend consumes via API

Tax rates are effective rates (not marginal/bracket-based) in MVP

Out of Scope (Future)

Progressive/marginal tax bracket modeling, deduction and credit optimization, estimated quarterly tax payments, multi-year tax projections, tax-loss harvesting scenarios, retirement contribution tax impact, scenario sharing/collaboration.

Open Questions (Resolved)

Tax rates are user-input effective rates, not auto-calculated from brackets (simplicity for MVP)

Investment income uses same rate as earned income in MVP; separate capital gains rates deferred

Saved tax scenarios become stale on new imports; user must manually refresh

No limit on saved tax scenarios in MVP

Success Criteria

[ ] Preview federal and state tax increase scenarios in <30 seconds

[ ] Side-by-side current vs. scenario net income chart with delta metrics

[ ] Save, list, refresh, and delete tax scenarios

[ ] Calculations complete in <2 seconds (p95)

[ ] No modification of actual transaction data

[ ] Mobile and accessible (keyboard nav, screen reader)