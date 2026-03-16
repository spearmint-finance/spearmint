# Accounts Iteration 13 — Filter Count Badge + Clear All Fix

**Date:** 2026-03-16
**PR:** #97
**Status:** Shipped

## Focus

Add active filter count badge to "More Filters" button and fix Clear All not resetting account_id filter.

## What Changed

### Before
- "More Filters" button had no visual indicator of active filters
- "Clear All" didn't reset the account_id filter (bug from iteration 8)

### After
- Badge on "More Filters" shows count of active advanced filters
- Badge hidden when no filters are active
- Clear All properly resets all filters including account_id

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (1 bug fix + 1 UX improvement)

## Verification
- PR #97 merged to main 2026-03-16T13:47:51Z
