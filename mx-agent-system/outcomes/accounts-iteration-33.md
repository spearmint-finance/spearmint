# Accounts Iteration 33 — Entity-Scoped Net Worth Calculation (Full-Stack)

**Date:** 2026-03-20
**PR:** #130
**Status:** Shipped

## Focus

Make net worth calculation respect entity selection — show entity-specific net worth instead of global total.

## What Changed

### Before
- Net worth card always showed total across ALL accounts regardless of entity selection
- Backend GET /accounts/net-worth had no entity_id parameter
- Frontend query key was static — no cache invalidation on entity switch

### After
- Backend: entity_id query parameter on GET /accounts/net-worth
- Service: get_net_worth passes entity_id to get_accounts filter
- Frontend: passes selectedEntityId to API call, query key includes entity_id
- Net worth card updates when user switches entities

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (net worth now entity-aware — 0 → 1 entity filter on net worth endpoint)

## Verification
- PR #130 merged to main 2026-03-20T01:32:58Z
