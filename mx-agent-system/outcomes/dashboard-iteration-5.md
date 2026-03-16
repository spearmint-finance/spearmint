# Dashboard Iteration 5 — Smooth Date Range Transitions

**Date:** 2026-03-16
**PR:** #110 (merged, commit 422179f)
**Human intervention:** No
**Measurable outcome:** Yes — eliminated jarring full-page flash on date range change

## Focus

Keep previous dashboard data visible during date range filter changes instead of showing a full-page spinner.

## Before

- Changing the date range caused the entire dashboard to flash to a "Loading dashboard data..." spinner
- All cards, charts, and sections disappeared momentarily as the query key changed
- Poor UX for a filter that should feel instant

## After

- `placeholderData` on useFinancialSummary and useCashFlowTrends keeps previous data visible
- Subtle LinearProgress bar below header shows data is refreshing
- First page load still shows full-page spinner (correct — no previous data to display)

## Files Changed

- `web-app/src/hooks/useAnalysis.ts`
- `web-app/src/components/Dashboard/Dashboard.tsx`
