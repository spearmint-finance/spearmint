# Accounts Iteration 27 — Error Feedback for Balance Snapshot and Delete Failures

**Date:** 2026-03-20
**PR:** #124
**Status:** Shipped

## Focus

Add visible error feedback when balance snapshot creation or account deletion fails.

## What Changed

### Before
- Balance snapshot creation failure: no user feedback (silent failure)
- Account deletion failure: no user feedback (silent failure)

### After
- Error Alert shown below the balance form when addBalanceMutation fails
- Error Alert shown in the delete confirmation dialog when deleteAccountMutation fails

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 2 error feedback UI states added)

## Verification
- PR #124 merged to main 2026-03-20T01:00:17Z
