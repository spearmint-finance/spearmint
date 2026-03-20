# Accounts Iteration 23 — Entity Reassignment in AccountDetailsDialog + Pagination Fix

**Date:** 2026-03-20
**PR:** #120
**Status:** Shipped

## Focus

Allow entity reassignment for existing accounts via AccountDetailsDialog edit mode, and fix pagination label corruption.

## What Changed

### Before
- Accounts could only be assigned to an entity during creation (AddAccountDialog)
- No way to reassign an existing account to a different entity without recreating it
- Entity name not shown in account details read-only view
- Transaction list pagination label showed corrupted control character instead of EN DASH
- accounts.ts getAccounts had trailing comma in fetch call

### After
- Entity dropdown in AccountDetailsDialog edit form (same pattern as AddAccountDialog)
- Current entity name and type displayed in read-only Details tab
- Pagination label correctly shows "1–25 of N" with proper EN DASH (U+2013)
- Clean fetch call in accounts.ts

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 entity reassignment workflow, 1 pagination display bug fixed)

## Verification
- PR #120 merged to main 2026-03-20T00:45:58Z
