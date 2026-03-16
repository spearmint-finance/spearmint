# Accounts Iteration 8 — Account Filter on Transactions List

**Date:** 2026-03-16
**PR:** #89
**Status:** Shipped

## Focus

Add account_id filter to transactions list endpoint and UI — missing core workflow after Plaid/Akoya integration.

## What Changed

### Before
- No way to filter transactions by account (backend or frontend)
- Summary stats always reflected all transactions regardless of any account context
- Transactions page had no account awareness

### After
- **Backend:**
  - `account_id` query parameter on `GET /api/transactions` (Optional[int], gt=0)
  - `TransactionFilter.account_id` filter condition in service layer
  - Summary/count query includes `account_id` for correct per-account stats
  - OpenAPI spec updated with new parameter
- **Frontend:**
  - Account dropdown in Advanced Filters dialog (populated from accounts API)
  - Direct fetch for getTransactions (bypasses SDK v0.0.15 which predates the param)
  - Credentials forwarding and structured error parsing on the fetch call

## Security Review
- SQL injection: mitigated (FastAPI int typing + SQLAlchemy parameterized queries)
- Auth forwarding: fetch uses `credentials: 'include'`
- Base URL: derived from SDK config to avoid divergence
- Input validation: `gt=0` constraint on account_id

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 account filter capability on transactions page)

## Verification
- PR #89 merged to main 2026-03-16T13:18:10Z
