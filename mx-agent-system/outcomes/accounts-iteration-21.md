# Accounts Iteration 21 — P&L and Cash Flow Reports (Phase 3)

**Date:** 2026-03-16
**PR:** #116
**Status:** Shipped

## Focus

P&L and cash flow statement endpoints plus Reports page UI.

## What Changed

### Before
- No financial statement generation
- No reports page in the application

### After
- GET /api/entities/{id}/pnl — revenue/expense aggregation by category
- GET /api/entities/{id}/cashflow — operating/investing/financing classification
- Reports page at /reports with P&L and Cash Flow tabs
- Date range selector (defaults to YTD)
- P&L: Revenue/expense tables by category, totals, net income line, CSV export
- Cash Flow: Operating/investing/financing sections with aggregated line items
- Tax line item chips, skeleton loading, error states, empty state

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 2 financial statement endpoints, 0 → 1 Reports page with 2 tabs)

## Verification
- PR #116 merged to main 2026-03-16T22:01:24Z
