# Accounts Iteration 78 — Bulk Update Error Reporting

**Date:** 2026-03-22
**PR:** #218
**Focus:** Report per-transaction failures in bulk update instead of silently swallowing exceptions

## Before
- `PUT /transactions/bulk-update` caught exceptions with `except Exception: pass`
- Response only included `updated` count — no indication of failures
- Frontend showed success even on partial failures

## After
- Backend tracks each failure with transaction ID and error message
- Response includes `failed` array: `[{"id": 1, "error": "..."}]`
- Frontend shows warning snackbar on partial failure: "Updated N of M transactions. K failed."

## Outcome
- Human intervention: No
- Measurable: Yes — partial failures now visible to users
- Regressions: None
- Security review: Error messages contain only validation text (no sensitive data)
