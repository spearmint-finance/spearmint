# Product Requirements Document: Scenario Builder Completion

**Product:** Spearmint Personal Finance Engine
**Feature:** Full Scenario Builder — Save, Compare, Visualize
**Owner:** Dashboard Team
**Status:** Draft
**Last Updated:** 2026-03-20
**Gate:** G2 (Intelligent Analyst)
**Priority:** P2

---

## Executive Summary

The scenario builder's preview mode is functional: users can simulate "What if?" outcomes (job loss, income reduction) with a deterministic engine that builds baselines from historical data. However, users cannot save scenarios, compare them side-by-side, or see chart visualizations. Completing this feature fulfills the core Horizon 2 differentiator: "Answer 'What if?' questions."

## Current State

### Working
- Simulation engine with 4 adjuster types (job_loss, income_reduction, expense_change, one_time)
- Preview-only API endpoint (`POST /api/scenarios/preview`)
- 6 scenario templates (Having a Baby, Buying a Home, Job Change, Tax Increase, Early Retirement, Starting a Business)
- Person-aware attribution via TransactionSplit
- KPI calculations (runway, min balance, coverage by person)
- Database models (Scenario, ScenarioAdjuster) with proper relationships

### Not Working
- No scenario persistence (CRUD endpoints)
- No chart visualization (series data exists but no charts)
- No scenario comparison view
- UI only supports 2 of 4 adjuster types (income_reduction, job_loss — missing expense_change, one_time)
- Template-to-scenario workflow not connected

## User Stories

1. **As a user**, I want to save a scenario so I can revisit it later without re-entering parameters.
2. **As a user**, I want to see a chart showing my projected balance over time under different scenarios so I can visually compare outcomes.
3. **As a user**, I want to compare my baseline projection against one or more scenarios side-by-side.
4. **As a user**, I want to start from a template (e.g., "Having a Baby") and customize it for my situation.

## Scope

### In Scope (MVP)

#### Backend
1. **Scenario CRUD API** — `GET/POST/PUT/DELETE /api/scenarios` for saving and managing scenarios
2. **Scenario list endpoint** — `GET /api/scenarios` returns user's saved scenarios
3. **Entity scoping** — Scenarios scoped to active entity (if applicable)

#### Frontend
4. **Balance projection chart** — Line chart showing projected balance over time (baseline vs. scenario)
5. **Save scenario flow** — After preview, option to name and save the scenario
6. **Saved scenarios list** — Page section listing saved scenarios with quick-view stats
7. **All 4 adjuster types in UI** — Add expense_change and one_time adjuster forms
8. **Template selector** — Pick from 6 templates to pre-populate the builder form

### Out of Scope
- Confidence intervals / probability-weighted scenarios (separate PRD)
- Multi-scenario comparison (3+ scenarios overlaid) — future enhancement
- Scenario sharing between entities
- Monte Carlo simulation

## Acceptance Criteria

1. User can create a scenario from scratch or from a template, preview it, and save it
2. Saved scenarios appear in a list with name, date, and key stats (runway, min balance)
3. Balance projection chart shows baseline (solid line) and scenario (dashed line) over the horizon
4. All 4 adjuster types are available in the UI
5. Saved scenarios persist across sessions
6. Scenarios can be edited and re-previewed

## Technical Notes

- Scenario and ScenarioAdjuster models are ready at `core-api/src/financial_analysis/database/models.py:422-466`
- ScenarioService at `core-api/src/financial_analysis/services/scenario_service.py` — the `simulate_scenario()` method already returns monthly series data (`month_series`) suitable for charting
- Frontend API client at `web-app/src/api/scenarios.ts` — needs CRUD functions added
- Use Recharts for the projection chart (already a project dependency)

## Competitive Reference

| Competitor | Scenario/Forecasting |
|------------|---------------------|
| Monarch Money | Basic projections, no what-if scenarios |
| YNAB | No forecasting |
| Copilot | Income/expense projections, no custom scenarios |
| Firefly III | No forecasting |
| **Spearmint (target)** | Custom scenarios with adjusters, person-aware, template-driven |

This is a genuine differentiator — no competitor in the open-source personal finance space offers person-aware scenario simulation.
