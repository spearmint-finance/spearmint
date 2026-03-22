# Product Requirements Document: Confidence-Based Forecasting

**Product:** Spearmint Personal Finance Engine
**Feature:** Confidence-Based Forecasting — Probabilistic Ranges for Scenarios and Projections
**Owner:** Dashboard Team
**Status:** Draft
**Last Updated:** 2026-03-22
**Gate:** G2 (Intelligent Analyst)
**Priority:** P1
**Directive:** TBD (to be filed upon merge)
**Related:** [scenario-builder-completion.md](scenario-builder-completion.md) (P2, prerequisite scenario CRUD)

---

## Executive Summary

Spearmint's projection endpoints already generate confidence intervals (upper/lower bounds) using four statistical algorithms. However, the scenario builder produces only a single deterministic forecast line — users see exactly one future, with no sense of how certain or uncertain that prediction is. This creates a misleading sense of precision.

Confidence-based forecasting integrates the existing projection engine's statistical machinery into the scenario builder, giving users probability-weighted ranges (e.g., "80% chance your runway is 6-9 months") instead of a single number ("your runway is 7.5 months"). No competitor in the open-source personal finance space offers this — it is a genuine differentiator.

## Problem Statement

**Current behavior:** The scenario builder returns a single deterministic series. When a user simulates "Job Loss," they see: "Your runway is 7.5 months." This is false precision — it ignores variance in income patterns, expense volatility, and the inherent uncertainty of future financial outcomes.

**Target behavior:** The scenario builder returns a confidence-banded series. The user sees: "Your runway is 6–9 months (80% confidence)." The UI shows a shaded confidence band around the projected line, making uncertainty visible and actionable.

## Current State

### What exists (projection system)
- `ProjectionService` with 4 algorithms: linear regression, moving average, exponential smoothing, weighted average
- Each algorithm computes confidence intervals (upper/lower bounds) at configurable confidence levels (50%–99%)
- `ForecastChart` component already renders confidence bands (shaded area between bounds)
- Cashflow projection already derives confidence: `lower = income_lower - expense_upper`, `upper = income_upper - expense_lower`

### What exists (scenario system)
- `ScenarioService.preview()` builds a baseline from 6-month historical average, applies adjusters, computes KPIs
- Baseline is a flat monthly average repeated across the horizon — no variance modeling
- KPIs (runway, min balance, coverage) are single-point estimates
- `ScenarioResults` displays KPIs as single numbers, no ranges

### The gap
The projection and scenario systems are disconnected. The projection engine knows about variance; the scenario engine does not. Bridging them means feeding the projection engine's statistical output into the scenario engine's adjuster pipeline, so that scenarios inherit confidence intervals.

## User Stories

1. **As a user**, I want to see a confidence band on my scenario projection chart so I can understand how certain or uncertain the outcome is.
2. **As a user**, I want my runway estimate to show a range (e.g., "6–9 months at 80% confidence") so I can plan for the worst case, not just the expected case.
3. **As a user**, I want to adjust the confidence level (e.g., 80% vs 95%) to understand how outcomes change at different certainty thresholds.
4. **As a user**, I want to see which adjusters introduce the most uncertainty so I can focus my planning on the biggest unknowns.

## Scope

### In Scope (MVP)

#### Backend

1. **Integrate projection variance into scenario baseline** — Instead of using a flat 6-month average as the baseline, use the projection service's algorithm output (with confidence intervals) as the baseline series. The scenario engine should accept a `method` and `confidence_level` parameter and pass them through to the projection engine.

2. **Confidence-banded scenario series** — `ScenarioPreviewResponse` gains `scenario_upper_series` and `scenario_lower_series` fields alongside the existing `scenario_series`. These represent the scenario outcome at the upper and lower confidence bounds.

3. **Range-based KPIs** — Each KPI gains a range:
   - `runway_months` → `{ expected: float, lower: float, upper: float }`
   - `min_balance` → `{ expected: Decimal, lower: Decimal, upper: Decimal }`
   - `coverage_by_person` → per-person ranges

4. **Confidence level parameter** — `ScenarioPreviewRequest` gains optional `confidence_level` (float, 0.5–0.99, default 0.80) and `method` (enum, default LINEAR_REGRESSION).

#### Frontend

5. **Confidence band on scenario chart** — Reuse the existing `ForecastChart` confidence-band rendering (shaded area) for scenario results. The chart shows the expected scenario line with a shaded confidence band.

6. **Range display for KPIs** — `ScenarioResults` shows each KPI as a range: "Runway: 6–9 months (80%)" instead of "Runway: 7.5 months."

7. **Confidence level control** — Add a confidence level slider (matching the one in `ProjectionControls`) to the scenario builder form.

### Out of Scope

- Monte Carlo simulation (computationally expensive, future enhancement)
- Per-adjuster uncertainty attribution (user story 4 deferred to follow-up)
- Correlation modeling between income and expense variance
- Historical backtesting of scenario accuracy
- Custom probability distributions (all algorithms use symmetric intervals)

## Acceptance Criteria

1. Scenario preview response includes `scenario_upper_series` and `scenario_lower_series` arrays with the same structure as `scenario_series`
2. KPIs display as ranges (expected + lower + upper) in both API response and UI
3. Confidence level is configurable (0.5–0.99) via both API parameter and UI slider
4. Projection method is selectable (4 algorithms) in the scenario builder
5. Scenario chart renders a shaded confidence band around the projected line
6. Changing confidence level dynamically updates the band width and KPI ranges
7. Default confidence level is 80% (not 95%) to avoid overly wide bands that reduce actionability
8. When historical data is insufficient for variance estimation (< 30 days), fall back to a fixed ±15% band with a warning indicator

## Technical Approach (Guidance, Not Prescription)

The implementation team decides the "how." This section provides context, not directives.

**Key insight:** The projection service already computes confidence intervals for income and expenses independently. The simplest integration path is:
1. In `ScenarioService.preview()`, replace the flat baseline with output from `ProjectionService.project_income()` and `ProjectionService.project_expenses()` (which include upper/lower bounds)
2. Apply adjusters to all three series (expected, upper, lower) independently
3. Compute KPIs for all three series to produce ranges

**Existing infrastructure to leverage:**
- `ProjectionService` methods already accept `method` and `confidence_level`
- `ForecastChart` already renders `upperBound` and `lowerBound` with a shaded `Area` between them
- `ProjectionControls` has confidence level slider UI that can be reused

**Schema change guidance:**
- `ScenarioPreviewResponse` needs 2 new fields (`scenario_upper_series`, `scenario_lower_series`)
- `ScenarioKPIs` fields change from single values to range objects
- `ScenarioPreviewRequest` needs 2 new optional fields (`confidence_level`, `method`)
- These are additive — no breaking changes to the existing API

## Competitive Reference

| Competitor | Confidence in Forecasting |
|------------|--------------------------|
| Monarch Money | Basic projections, no confidence intervals |
| YNAB | No forecasting at all |
| Copilot | Income/expense projections, no confidence bands |
| Firefly III | No forecasting |
| Actual Budget | No forecasting |
| Lunch Money | No forecasting |
| **Spearmint (current)** | Confidence intervals in projections only, not in scenarios |
| **Spearmint (target)** | Confidence intervals in both projections AND scenarios — unique in market |

No competitor (commercial or open-source) offers probability-weighted scenario simulation for personal finance. This is a genuine first-mover opportunity.

## Success Metrics

| Metric | Target |
|--------|--------|
| Scenario preview API returns confidence bands | Yes (all responses include upper/lower series) |
| KPIs rendered as ranges in UI | Yes |
| Confidence level configurable | Yes (slider works, API parameter accepted) |
| No regression in existing projection confidence intervals | All existing projection tests pass |
| Chart renders confidence band for scenarios | Visual verification via Playwright screenshot |

## Dependencies

- **Scenario CRUD (directive #150)** — Not a hard dependency for the confidence feature itself, but the full user experience benefits from being able to save and revisit confidence-banded scenarios. Can be developed in parallel.
- **Projection service stability** — The existing projection algorithms and confidence interval calculations must remain correct and performant.

## Risks

| Risk | Mitigation |
|------|------------|
| Confidence bands too wide to be useful (especially at 95%) | Default to 80% confidence, which produces tighter bands. Let users adjust. |
| Historical data insufficient for meaningful variance estimation | Fall back to ±15% fixed band with visual warning when < 30 days of data |
| Performance impact of running projections inside scenario engine | The projection service is already optimized; benchmark before and after |
| User confusion about what confidence bands mean | Add tooltip: "This shaded area shows where your balance is likely to fall X% of the time, based on your historical income and expense patterns." |
