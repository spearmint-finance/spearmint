# Accounts Iteration 36 — Reports Empty State Message Improvement

**Date:** 2026-03-20
**PR:** #133
**Status:** Shipped

## Focus

Improve the Reports page empty state message to guide users to the correct UI for entity creation.

## What Changed

### Before
- Message said "create one via the API first" — misleading since entities are created via sidebar UI

### After
- When no entities: "Create an entity using 'Manage Entities' in the sidebar..."
- When entities exist but none selected: "Select an entity from the sidebar..."

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (1 misleading message → 2 context-aware messages)

## Verification
- PR #133 merged to main 2026-03-20T01:43:03Z
