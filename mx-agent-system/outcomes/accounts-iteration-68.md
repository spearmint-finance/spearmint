# Accounts Iteration 68 — Filter Categories by Transaction Entity in Edit Form

**Date:** 2026-03-22
**PR:** #198
**Focus:** Category dropdown uses transaction's entity_id in edit mode, not global selector

## Before
- Editing a transaction with entity_id=2 while viewing "All Entities" showed all categories
- "Create New Category" from form created global categories even in entity scope

## After
- Category dropdown filters by the transaction's own entity_id when editing
- Changing entity field re-filters categories dynamically
- "Create New Category" inherits entity scope from form

## Outcome
- Human intervention: No
- Measurable: Yes — correct category scoping in edit mode
- Regressions: None
