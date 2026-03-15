# Accounts Iteration 5 — Skeleton Loading Cards

**Date shipped:** 2026-03-15
**PR:** #77 MERGED
**North star:** 1 user-visible improvement shipped (target: 1)

## What Was Before
- AccountsPage showed a bare LinearProgress bar during loading
- No spatial context about what content was loading

## What Changed
- Replaced LinearProgress with MUI Skeleton components
- Loading state shows page title, net worth skeleton, and three account card skeletons
- Skeletons mirror the actual page layout dimensions

## What Is After
- Users see placeholder cards while data loads, reducing perceived load time
- Layout doesn't shift when real content renders

## Metrics
- Files changed: 1 (`web-app/src/components/Accounts/AccountsPage.tsx`)
- Lines added: 22, removed: 2
- Human intervention needed: No
- Regressions: None
