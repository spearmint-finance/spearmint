# Accounts Iteration 37 — Sort Account Cards by Balance

**Date:** 2026-03-20
**PR:** #134
**Status:** Shipped

## Focus

Sort account cards by balance (highest first) in the Assets and Liabilities tabs.

## What Changed

### Before
- Account cards displayed in API return order (typically creation order)
- Users had to scan through all cards to find highest-value accounts

### After
- Assets tab: sorted by balance descending (highest first)
- Liabilities tab: sorted by absolute balance descending
- All Accounts tab: maintains original order

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 sort order applied to account cards)

## Verification
- PR #134 merged to main 2026-03-20T01:46:37Z
