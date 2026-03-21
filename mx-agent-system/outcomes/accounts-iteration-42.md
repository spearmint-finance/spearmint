# Accounts Iteration 42 — Differentiate error responses in create_account

**Date:** 2026-03-20
**PR:** #140
**Status:** Shipped

## What changed

The `create_account` endpoint had a blanket `except Exception` that returned HTTP 400 for all errors, including database conflicts and unexpected server errors. Added specific exception handlers with appropriate status codes and safe error messages.

## Before

- All errors returned 400 with raw exception string (potential information disclosure)
- No way to distinguish validation errors from conflicts or server errors

## After

- ValueError → 400 (validation error with descriptive message)
- IntegrityError → 409 (conflict with safe generic message)
- Exception → 500 (unexpected error, no internals exposed)
- All error paths logged with appropriate severity

## Human intervention

None

## Measurable outcome

Yes — API error responses now use correct HTTP status codes and don't expose internal details.
