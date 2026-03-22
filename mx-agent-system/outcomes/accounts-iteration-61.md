# Accounts Iteration 61 — Fix entity_id clearing + add splits endpoint

**Date:** 2026-03-22
**PRs:** #189, #190
**Status:** Shipped

## What changed

1. **Fix entity_id clearing on category change (PR #189):** `updateTransaction()` in `transactions.ts` unconditionally set `entity_id = null` when not provided. Inline category editing sent only `{ category_id: X }`, which wiped the entity assignment. Fixed to only include `entity_id` when explicitly provided.

2. **Add split endpoint (PR #190):** Frontend's `setTransactionSplits()` called `PUT /transactions/{id}/splits` but no backend endpoint existed (404). Added the endpoint delegating to existing service logic.

## Human intervention

Yes — user reported both issues.

## Measurable outcome

Yes — entity assignments preserved during category changes; transaction splitting works end-to-end.
