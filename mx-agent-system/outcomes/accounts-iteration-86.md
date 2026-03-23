# Accounts Iteration 86 — Backend Split Amount Validation

**Date:** 2026-03-22
**PR:** #238
**Focus:** Add server-side validation that split amounts sum to transaction amount

## Before
- Backend accepted splits with any amounts regardless of transaction total
- Data model docstring stated invariant but code didn't enforce it
- Only frontend validated split sums

## After
- Both create and update paths validate split sum matches transaction amount (0.01 tolerance)
- Returns 400 with descriptive error message on mismatch
- Update path uses new amount if provided, otherwise validates against existing amount

## Outcome
- Human intervention: No
- Measurable: Yes — data integrity enforced at API boundary
- Regressions: None
