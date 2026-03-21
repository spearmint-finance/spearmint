# Accounts Iteration 54 — Filter categories by entity in transaction forms

**Date:** 2026-03-21
**PR:** #176
**Status:** Shipped

## What changed

TransactionForm and TransactionList now pass the selected entity ID to useCategories, so category dropdowns only show categories that belong to the selected entity plus global categories.

## Human intervention

No

## Measurable outcome

Yes — category dropdowns now entity-aware.
