# Accounts Iteration 92 — Backend Error Message Surfacing

**Date:** 2026-03-22
**PR:** #244
**Focus:** Surface backend error details in transaction snackbar messages

## Before
- Error snackbars showed generic messages ("Failed to create transaction")
- Users couldn't see what actually went wrong (validation errors, data issues)

## After
- Error messages include backend detail when available
- e.g., "Failed to create transaction: Split amounts sum to 50 but transaction amount is 100"
- Applies to create, update, delete, inline edit, and inline category creation

## Outcome
- Human intervention: No
- Measurable: Yes — improved error feedback for users
- Regressions: None
