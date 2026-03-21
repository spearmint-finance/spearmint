# Accounts Iteration 56 — Direct entity assignment on transactions

**Date:** 2026-03-21
**PR:** #178
**Status:** Shipped

## What changed

Transactions can now be explicitly assigned to an entity via entity_id. When null, inherits from account. Entity selector added to TransactionDetail dialog.

## Human intervention

Yes — user reported missing entity assignment on transactions.

## Measurable outcome

Yes — transactions can now be directly assigned to entities.
