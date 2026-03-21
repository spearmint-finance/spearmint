# Accounts Iteration 47 — Grid cleanup: remove Type/Balance/Classification columns

**Date:** 2026-03-21
**PRs:** #168-169
**Status:** Shipped

## What changed

Cleaned up the transaction data grid by removing obsolete columns (Type, Balance, Classification) that were left over after the classification-to-tags migration, and simplified the uncategorized transaction display.

## Before

- Grid showed Type, Balance, and Classification columns (no longer relevant after refactors)
- Account column showed only account name
- Uncategorized transactions had complex display logic

## After

- Removed Type, Balance, and Classification columns from grid
- Combined Account column with relevant info
- Simplified uncategorized display to clean text

## Verification

- Grid renders correctly with reduced columns
- No visual regressions

## Human intervention

Yes — user identified the stale columns.

## Measurable outcome

Yes — cleaner, more focused transaction grid.
