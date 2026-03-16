# Accounts Iteration 17 — Deduplicate formatCurrency Utility

**Date:** 2026-03-16
**PR:** #103
**Status:** Shipped

## Focus

Remove duplicate formatCurrency functions from AccountsPage and AccountDetailsDialog, use shared utility.

## What Changed

### Before
- AccountsPage, AccountDetailsDialog, and NetWorthCard each had their own local formatCurrency
- 3 copies of essentially the same function

### After
- AccountsPage and AccountDetailsDialog use shared formatCurrency from utils/formatters.ts
- NetWorthCard retains its local version (intentionally uses 0 decimal places for large numbers)
- Partially addresses KI-003 (hardcoded USD) — shared utility accepts currency parameter

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (3 duplicates → 1 shared + 1 intentional local)

## Verification
- PR #103 merged to main 2026-03-16T14:26:11Z
