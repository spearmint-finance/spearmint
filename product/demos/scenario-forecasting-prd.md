# PRD: Scenario-Based Financial Forecasting

**Product:** Spearmint Personal Finance Engine
**Feature:** Scenario-Based Financial Forecasting
**Owner:** Product Team
**Status:** Ready for Implementation
**Last Updated:** 2026-01-21

---

## Executive Summary

Users love Spearmint's projection feature but consistently request the ability to model "what-if" scenarios. Support tickets and user interviews reveal a clear need: users want to understand how financial decisions or life events would impact their runway, savings, and cash flow before those events occur.

This PRD defines Scenario-Based Financial Forecasting—a feature that lets users define hypothetical adjustments (income changes, expense shocks, one-time events) and see side-by-side comparisons of baseline vs. scenario projections.

**Expected Impact:**
- Increase user engagement with projection features by 40%
- Reduce support tickets asking "how do I model X scenario?" by 60%
- Enable users to make informed financial decisions with confidence

---

## Problem Statement

### The User Problem

Spearmint users face important financial decisions but lack tools to explore potential outcomes:

- **Job transitions:** "What if I lose my job?" "Can I afford to take a lower-paying role?"
- **Major expenses:** "What if my rent increases 20%?" "Can I afford a car payment?"
- **Life events:** "What if I have a baby and need to reduce my hours?" "What happens if I retire early?"

Currently, users see only one projection—their current trajectory. They can't experiment with adjustments without manually creating duplicate accounts or doing mental math. This creates decision paralysis and reduces confidence in their financial planning.

### Evidence

**Support Ticket Analysis (Last 90 Days):**
- 47 tickets asking "How do I model job loss?"
- 23 tickets asking "Can I see what happens if my expenses increase?"
- 18 tickets asking "How long will my savings last if I stop working?"

**User Interview Insights (N=15):**
- 14/15 users said they'd use a "what-if" scenario feature weekly
- 12/15 users currently use spreadsheets for manual scenario modeling
- 10/15 users said this feature would make Spearmint their "primary financial planning tool"

**Competitive Analysis:**
- YNAB, Mint, and Personal Capital lack robust scenario modeling
- Niche tools (ProjectionLab, Boldin) offer this but lack transaction import and classification
- Opportunity to differentiate with integrated scenario modeling

---

## Goals & Success Metrics

### Goals

1. **Enable confident decision-making:** Users can answer "what-if" questions in under 30 seconds
2. **Increase projection usage:** Drive 40% increase in users viewing projections weekly
3. **Reduce support burden:** Decrease scenario-related support tickets by 60%

### Success Metrics

| Metric | Target | Timeframe |
|--------|--------|-----------|
| % of active users who create scenarios | 35% | 3 months post-launch |
| Avg. scenarios created per user per month | 4 | 3 months post-launch |
| User satisfaction (feature rating) | 4.5/5 | 1 month post-launch |
| Reduction in scenario-related tickets | 60% | 2 months post-launch |

---

## User Stories

### Primary User Stories

**As a user, I want to:**

1. **Simulate job loss** so I can see how long my savings will last and plan accordingly
   - *Acceptance:* User can model 100% income reduction starting on a specific date and see updated runway projection

2. **Model expense changes** so I can understand the impact of rent increases, new car payments, or lifestyle changes
   - *Acceptance:* User can increase/decrease specific expense categories by a percentage or fixed amount and see cash flow impact

3. **Compare baseline vs. scenario side-by-side** so I can clearly see the difference in outcomes
   - *Acceptance:* User sees dual-line chart with baseline and scenario projections, plus delta metrics (runway change, minimum balance difference)

4. **Experiment with multiple scenarios** without saving them so I can quickly explore different possibilities
   - *Acceptance:* User can run "preview" scenarios that don't persist, allowing rapid iteration

5. **Save scenarios for future reference** so I can return to important what-if models later
   - *Acceptance:* User can name and save a scenario, then view/edit/delete saved scenarios from a list

6. **Re-run saved scenarios with fresh data** so I can see how the outcome changes as my financial situation evolves
   - *Acceptance:* User can click "Refresh" on a saved scenario to re-calculate with current transaction data

### Secondary User Stories

**As a user, I want to:**

7. **Model one-time events** (emergency fund withdrawal, bonus receipt, large purchase) so I can see temporary impacts
   - *Future iteration:* Not included in MVP

8. **Create multi-factor scenarios** (job loss AND rent increase) so I can model worst-case situations
   - *Future iteration:* Not included in MVP

9. **Share scenarios with financial advisors or partners** so we can discuss plans collaboratively
   - *Future iteration:* Not included in MVP

---

## User Workflows

### Workflow 1: Quick Preview (No Save)

**Primary use case:** User wants to quickly explore "what if my rent goes up $200/month?"

1. User navigates to Projections page
2. User clicks "Run Scenario" button
3. Modal opens with scenario configuration form
4. User selects adjustment type: "Expense Change"
5. User selects category: "Rent"
6. User enters adjustment: +$200/month
7. User specifies start date: "2026-03-01"
8. User clicks "Preview Scenario"
9. System displays side-by-side comparison:
   - Baseline projection (existing trajectory)
   - Scenario projection (with rent increase applied)
   - Key metrics: Runway months (baseline vs. scenario), minimum balance, total cash flow impact
10. User reviews, then clicks "Discard" to return to baseline view

**Performance requirement:** Preview generation completes in <2 seconds

### Workflow 2: Save and Revisit

**Primary use case:** User wants to save a "job loss" scenario to monitor over time

1. User follows steps 1-8 from Workflow 1
2. After reviewing preview, user clicks "Save Scenario"
3. User enters scenario name: "Job Loss - June 2026"
4. System saves scenario and adds it to "Saved Scenarios" list
5. User can later navigate to "Saved Scenarios" page
6. User sees list of saved scenarios with metadata (name, created date, last run)
7. User clicks on "Job Loss - June 2026"
8. System displays the scenario results (may be stale if transaction data has changed)
9. User clicks "Refresh" to re-run with current data
10. System recalculates and updates the display

**Performance requirement:** Scenario save completes instantly; refresh completes in <2 seconds

---

## Functional Requirements

### FR-1: Scenario Configuration

Users can configure scenarios with the following adjusters:

| Adjuster Type | Parameters | Example |
|---------------|------------|---------|
| **Income Change** | - Category (Salary, Freelance, etc.)<br>- Percentage change (+/- 1-100%)<br>- Start date<br>- End date (optional) | "Reduce Salary by 100% starting June 1, 2026" |
| **Expense Change** | - Category (Rent, Groceries, etc.)<br>- Percentage change (+/- 1-1000%)<br>- Start date<br>- End date (optional) | "Increase Rent by 20% starting March 1, 2026" |

**MVP Scope:** Income and Expense changes only
**Future:** One-time events, multi-factor scenarios, custom date ranges

### FR-2: Scenario Calculation Engine

The system must:
- Use the existing projections engine as the baseline
- Apply adjusters to historical average calculations
- Recalculate projected cash flow with adjustments applied
- Generate scenario series (date/balance pairs) for charting
- Calculate delta metrics (runway change, min balance difference, total impact)

**Key calculation:**
- Baseline runway: X months
- Scenario runway: Y months
- Delta: Y - X months (display as "+3 months" or "-5 months")

### FR-3: Scenario Preview (Ephemeral)

Users can preview scenarios without saving:
- Configuration happens in a modal/overlay UI
- Preview generates comparison chart and metrics
- No persistence to database
- User can iterate rapidly (change parameters, re-preview)

### FR-4: Scenario Persistence (Saved Scenarios)

Users can save scenarios for future reference:
- Scenarios stored with: name, configuration (adjusters), created date, last run date
- Users can view list of saved scenarios
- Users can edit saved scenario configuration
- Users can delete saved scenarios
- Users can "refresh" a saved scenario to re-run with current data

### FR-5: Comparison Visualization

The comparison view displays:
- **Dual-line chart:** Baseline vs. Scenario projections over time
- **Key metrics card:**
  - Runway: Baseline vs. Scenario (with delta)
  - Minimum Balance: Baseline vs. Scenario (with delta)
  - Total Cash Flow Impact: Cumulative difference over projection period
- **Generated timestamp:** "Calculated as of [datetime]"

---

## Non-Functional Requirements

### NFR-1: Performance

- Scenario preview generation: <2 seconds (p95)
- Saved scenario refresh: <2 seconds (p95)
- Scenario list page load: <500ms (p95)

### NFR-2: Data Integrity

- Scenarios are **read-only operations**—they never modify actual transaction data
- Scenario calculations use the same logic as baseline projections for consistency
- Scenarios must integrate with existing projections engine (no duplicate calculation logic)

### NFR-3: Mobile Responsiveness

- All scenario features must work on mobile devices
- Scenario configuration form must be touch-friendly
- Comparison charts must be readable on small screens (vertical layout if needed)

### NFR-4: Accessibility

- Scenario configuration forms must be keyboard-navigable
- Charts must have text alternatives for screen readers
- Color contrast must meet WCAG AA standards

---

## Technical Constraints

1. **Integration with Projections Engine:** Must use the existing projections service—no separate calculation logic
2. **Classification-Aware:** Adjusters must respect transaction classification rules (e.g., don't adjust transfers or internal transactions)
3. **Historical Data Dependency:** Scenarios depend on at least 3 months of transaction history for accurate baseline calculations
4. **API-First Design:** Frontend consumes scenarios via API endpoints (backend owns calculation logic)

---

## Out of Scope (Future Iterations)

The following are explicitly **not** included in the MVP:

- One-time event modeling (single large purchase, bonus receipt)
- Multi-factor scenarios (job loss AND rent increase in same scenario)
- Scenario sharing/collaboration
- Scenario comparison (comparing Scenario A vs. Scenario B)
- Confidence intervals for scenario projections
- Scenario notifications ("Your scenario runway dropped below 6 months")

---

## Open Questions

- **Q:** Should scenario adjustments apply to all transactions in a category or only unclassified ones?
  - **A:** All transactions in the selected category (respecting classification exclusions like transfers)

- **Q:** What happens if a user creates a scenario and then imports new transactions?
  - **A:** Saved scenarios become stale. User must manually "Refresh" to recalculate with new data.

- **Q:** Should there be a limit on the number of saved scenarios per user?
  - **A:** Not in MVP. Monitor usage and add limits if storage becomes an issue.

---

## Designs & Mockups

*[Link to Figma designs]*
*[Link to user flow diagrams]*
*[Link to wireframes]*

*(In a real PRD, these would be embedded or linked)*

---

## Success Criteria Checklist

Before marking this feature "complete," we must validate:

- [ ] User can preview a job loss scenario in <30 seconds
- [ ] User can preview an expense increase scenario in <30 seconds
- [ ] User sees side-by-side baseline vs. scenario comparison chart
- [ ] User sees delta metrics (runway change, min balance difference)
- [ ] User can save a scenario with a custom name
- [ ] User can view list of saved scenarios
- [ ] User can refresh a saved scenario to re-run with current data
- [ ] User can delete a saved scenario
- [ ] All scenario calculations complete in <2 seconds (p95)
- [ ] Scenario adjustments do not modify actual transaction data
- [ ] Feature works on mobile devices (iOS Safari, Android Chrome)
- [ ] Feature is accessible (keyboard navigation, screen reader compatible)

---

## Appendix: User Research Quotes

> "I've been wanting to know if I could handle losing my job for months. I tried to do the math in my head but it's too complicated with all my recurring expenses." — User #4, Beta Interview

> "I use spreadsheets to model different scenarios, but it's tedious and error-prone. If Spearmint could do this, I'd never need my spreadsheet again." — User #9, Beta Interview

> "I love the projections feature, but it's only one possible future. What I really need is to see multiple futures and compare them." — User #12, Beta Interview

> "This would make me feel so much more in control of my finances. Right now I'm just guessing what would happen if things change." — User #15, Beta Interview

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-21 | Product Team | Initial PRD for MVP scope |

---

**Next Steps:**
1. Engineering review and API design (Phase 1)
2. Design finalization (Figma mockups)
3. Sprint planning and estimation
4. Implementation kickoff
