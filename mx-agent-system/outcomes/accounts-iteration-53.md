# Accounts Iteration 53 — Entity scoping for categories

**Date:** 2026-03-21
**PR:** #175
**Status:** Shipped

## What changed

Added entity scoping to categories. Categories can now be assigned to a specific entity (entity_id = X) or left as global (entity_id = NULL). When listing categories for an entity, both entity-specific and global categories are returned.

## Before

- Categories were global — shared across all entities with no scoping
- No way to have entity-specific categories (e.g., "Office Rent" only for Business entity)

## After

- Categories have optional `entity_id` field (NULL = global)
- Backend: model, schema, service, and route all support entity_id
- Frontend: Entity column in category grid, entity selector in create/edit dialog
- Startup migration handles existing SQLite databases
- Entity filter returns entity-specific + global categories

## Verification

- 136 backend tests pass
- TestClient: global category has entity_id=None, scoped category has correct entity_id
- Entity filter correctly returns both global and entity-specific categories
- Vite build succeeds

## Human intervention

Yes — user requested entity-scoped categories with the clarification that categories can also span entities (global).

## Measurable outcome

Yes — new feature: entity-scoped categories with backwards-compatible global categories.
