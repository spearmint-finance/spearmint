# Accounts Iteration 46 — Classification-to-tags migration (3 phases)

**Date:** 2026-03-21
**PRs:** #165-167
**Status:** Shipped

## What changed

Complete removal of the classification system, replaced with a lightweight tags model. Executed in 3 phases:
1. Phase 1: Add tags model, migrate data, add tag CRUD endpoints
2. Phase 2: Switch analysis/reports from classifications to tags
3. Phase 3: Remove classification system entirely (models, routes, schemas, services, UI components)

## Before

- Transaction model had 4 dimensions: type + category + classification + is_transfer
- ClassificationRule, TransactionClassification models with full CRUD
- 8 UI components for classification management
- ~6,000+ lines of classification code

## After

- Transaction model simplified to: type + category + tags
- 6 seed tags: capital-expense, tax-deductible, recurring, reimbursable, exclude-from-income, exclude-from-expenses
- Tag editing on TransactionForm and TransactionDetail
- ~6,000+ lines removed

## Verification

- All backend tests pass after each phase
- Reports page correctly uses tags instead of classifications
- Tag CRUD working end-to-end

## Human intervention

Yes — user approved the phased migration approach.

## Measurable outcome

Yes — massive simplification: ~6,000 lines removed, 4-dimension model reduced to 3.
