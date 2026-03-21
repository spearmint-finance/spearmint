# Accounts Iteration 59 — Future-date validation + categories CHECK constraint

**Date:** 2026-03-21
**PRs:** #185, #186
**Status:** Shipped

## What changed

1. Removed future-date restriction from transaction date validation (PR #185). Demo data had dates like 2026-03-31 — all edits to these transactions were silently failing with 400 errors.
2. Migrated categories CHECK constraint to include 'Transfer' type (PR #186). Import was failing 10,174 of 10,262 rows because the constraint only allowed Income/Expense/Both. After fix: 10,179 successful, 0 failed.

## Root cause

- `DataValidator.validate_date()` rejected future dates — blocking all edits to transactions with upcoming dates
- SQLite CHECK constraint on categories table didn't include 'Transfer' — blocking import of transfer-type categories

## Human intervention

No

## Measurable outcome

Yes — import success rate went from ~1% to ~99.2%. Transaction editing unblocked for future-dated records.
