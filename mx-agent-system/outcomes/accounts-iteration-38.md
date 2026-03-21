# Accounts Iteration 38 — Include entity_id in GET and PUT account responses

**Date:** 2026-03-20
**PR:** #136
**Status:** Shipped

## What changed

The `get_account()` and `update_account()` endpoints in `accounts.py` were missing `entity_id` from their response dicts. The `list_accounts()` and `create_account()` endpoints already included it, creating an API inconsistency that broke entity-scoped operations when reading or updating individual accounts.

## Before

- GET `/accounts/{id}` response: no `entity_id` field
- PUT `/accounts/{id}` response: no `entity_id` field
- Frontend entity-scoped views couldn't determine entity association from individual account fetches

## After

- All four account endpoints (list, create, get, update) consistently return `entity_id`
- Entity-scoped account detail views work correctly

## Human intervention

None

## Measurable outcome

Yes — API response contract now includes `entity_id` consistently across all endpoints. 2-line fix, 173 tests passing.
