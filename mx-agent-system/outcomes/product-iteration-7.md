# Product Iteration 7 — Confidence-Based Forecasting PRD

**Date:** 2026-03-22
**Focus:** Write PRD for confidence-based forecasting (last G2 PRD gap)
**PR:** #207 (merged)
**Directive Filed:** #208 (P1, Dashboard team)

## What Shipped

- **PRD:** `product/feature-planning/confidence-based-forecasting.md` — bridges the gap between the projection engine (which has confidence intervals) and the scenario builder (which is deterministic)
- **Feature Index:** Updated to include new PRD, removed from "PRDs Needed" list
- **Roadmap:** Updated with PRD reference for G2 confidence-based forecasting item
- **Directive #208:** Filed to Dashboard team with acceptance criteria and technical context

## Key Decision

Scoped MVP to integration of existing statistical machinery (projection engine confidence intervals) into the scenario builder — not Monte Carlo simulation or custom distributions. This is achievable because:
1. `ProjectionService` already computes upper/lower bounds with 4 algorithms
2. `ForecastChart` already renders confidence bands
3. Changes to scenario API are additive (no breaking changes)

## Competitive Context

No competitor (commercial or open-source) offers probability-weighted scenario simulation for personal finance. This is a first-mover differentiator.

## Metrics

- **Stars:** 0 → 0 (unchanged, pre-launch)
- **Directives filed this session:** 1 (#208)
- **Total active directives:** 7 (#141, #144, #147, #148, #150, #152, #208)
- **G2 PRDs complete:** All 3 now filed (scenario builder, confidence forecasting, budget management)
- **human_intervention:** no
- **measurable_outcome:** yes
