# Dashboard Iteration 8 — Deep Dive Links on Category Charts

**Date:** 2026-03-16
**PR:** #113 (merged, commit 9450adb)
**Human intervention:** No
**Measurable outcome:** Yes — category charts now link to analysis deep-dive pages

## Focus

Add "Deep Dive" navigation buttons to income and expense category charts.

## Before

- Category charts had no way to navigate to detailed analysis pages
- Users who wanted deeper breakdowns had to manually navigate

## After

- "Deep Dive" button on Top Income Categories links to /analysis/income
- "Deep Dive" button on Top Expense Categories links to /analysis/expenses
- Titles moved from chart component prop to inline headers with action buttons

## Files Changed

- `web-app/src/components/Dashboard/Dashboard.tsx`
