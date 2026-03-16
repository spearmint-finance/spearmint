# Accounts Iteration 9 — sort_by Column Allowlist

**Date:** 2026-03-16
**PR:** #90
**Status:** Shipped

## Focus

Add allowlist validation to the `sort_by` parameter on the transactions list endpoint to prevent arbitrary model attribute access via `getattr`.

## What Changed

### Before
- `sort_by` accepted any string and used `getattr(Transaction, filters.sort_by, Transaction.transaction_date)` — could probe any model attribute including sensitive fields like `external_transaction_id`

### After
- `ALLOWED_SORT_COLUMNS` allowlist: `transaction_date`, `amount`, `description`, `source`, `transaction_type`, `created_at`, `updated_at`
- Invalid values fall back to `transaction_date`
- No arbitrary `getattr` access to model internals

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 sort_by validation; KI-010 resolved)

## Verification
- PR #90 merged to main 2026-03-16T13:21:07Z
