# Accounts Iteration 18 — Date Range Presets in Transaction Filters

**Date:** 2026-03-16
**PR:** #104
**Status:** Shipped

## Focus

Add quick date range preset chips to the Advanced Filters dialog.

## What Changed

### Before
- Users had to manually type start/end dates for date filtering
- No preset options for common date ranges

### After
- 4 preset chips: "Last 30 days", "This month", "Last month", "Year to date"
- Clicking fills both date fields
- Active preset highlighted with filled primary chip
- Manual date editing still works independently

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 4 date range presets)

## Verification
- PR #104 merged to main 2026-03-16T14:29:04Z
