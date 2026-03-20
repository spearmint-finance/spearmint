# Accounts Iteration 29 — Date Range Validation on Balance and Report Endpoints

**Date:** 2026-03-20
**PR:** #126
**Status:** Shipped

## Focus

Add date range validation to prevent reversed date ranges from returning empty results silently.

## What Changed

### Before
- Balance history, P&L, and cash flow endpoints accepted start_date > end_date
- Queries returned empty results with no error indication

### After
- 422 validation error when start_date is after end_date
- Clear error message: "start_date must be before or equal to end_date"
- Applied to 3 endpoints: GET /accounts/{id}/balances, GET /entities/{id}/pnl, GET /entities/{id}/cashflow

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 3 date range validations added)

## Verification
- PR #126 merged to main 2026-03-20T01:07:49Z
