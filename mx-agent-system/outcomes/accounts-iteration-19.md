# Accounts Iteration 19 — Entity Model and CRUD (Business Separation Phase 1)

**Date:** 2026-03-16
**PR:** #114
**Status:** Shipped

## Focus

Backend entity model and CRUD endpoints for business entity separation.

## What Changed

### Before
- No concept of business entities — all accounts lived in a flat list
- No way to separate personal, business, or rental property finances

### After
- Entity model: entity_id, entity_name, entity_type (personal/business/rental_property/side_hustle), tax_id, address, fiscal_year_start_month, is_default
- Entity CRUD: POST/GET/PUT/DELETE /api/entities with account count, default protection, account reassignment checks
- Account.entity_id: nullable FK to entities with index
- AccountCreate/Update/Response: entity_id field
- TransactionFilter: entity_id via Account join
- GET /api/transactions?entity_id=N, GET /api/accounts?entity_id=N

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 entity model, 0 → 4 CRUD endpoints, 0 → 2 entity filters)

## Verification
- PR #114 merged to main 2026-03-16T19:56:37Z
