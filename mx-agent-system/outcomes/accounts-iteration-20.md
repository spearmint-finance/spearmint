# Accounts Iteration 20 — Frontend Entity Switcher and Scoping (Phase 2)

**Date:** 2026-03-16
**PR:** #115
**Status:** Shipped

## Focus

Frontend entity switcher dropdown and entity-scoped filtering for accounts and transactions.

## What Changed

### Before
- No frontend awareness of entities
- All accounts and transactions shown in a single unscoped view

### After
- Entity types, API client, React Query hooks, and context provider
- Entity switcher dropdown in sidebar (shown when >1 entity exists)
- AccountsPage: filtered by selected entity via query key
- TransactionList: entity_id passed to useTransactions and CSV export
- "All Entities" option shows everything

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 entity switcher, 0 → 1 entity context, 2 pages scoped by entity)

## Verification
- PR #115 merged to main 2026-03-16T20:24:21Z
