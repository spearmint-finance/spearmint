# Accounts Iteration 6 — Input Sanitization + Refresh Feedback

**Date shipped:** 2026-03-15
**PR:** #80 MERGED
**North star:** 1 user-visible improvement shipped (target: 1)

## What Was Before
- AddAccountDialog last4 input accepted non-digit characters (inconsistent with edit form)
- Refresh button had no visual feedback during data refetch

## What Changed
- Strip non-digit characters from last4 input inline (regex replace)
- Added spinning animation and disabled state to refresh button during fetch

## What Is After
- Consistent input sanitization across add and edit flows
- Clear visual feedback when refresh is in progress

## Metrics
- Files changed: 2 (`AccountsPage.tsx`, `AddAccountDialog.tsx`)
- Lines added: 17, removed: 2
- Human intervention needed: No
- Regressions: None
