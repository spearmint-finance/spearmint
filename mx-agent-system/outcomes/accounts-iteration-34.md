# Accounts Iteration 34 — Entity Name in Net Worth Card Title

**Date:** 2026-03-20
**PR:** #131
**Status:** Shipped

## Focus

Show entity name in net worth card title when viewing a specific entity.

## What Changed

### Before
- Net worth card always showed "Net Worth Overview" regardless of entity selection

### After
- Shows "Net Worth — [Entity Name]" when a specific entity is selected
- Falls back to "Net Worth Overview" when viewing all entities

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (entity name now visible in net worth card title)

## Verification
- PR #131 merged to main 2026-03-20T01:38:31Z
