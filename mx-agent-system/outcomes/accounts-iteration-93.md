# Accounts Iteration 93 — Entity Auto-Assignment in Transaction Rules

**Date:** 2026-03-23
**PR:** #245
**Focus:** Extend transaction rules to auto-assign entities alongside categories

## Before
- Category rules could only assign a category to matching transactions
- No way to automatically assign entities based on patterns
- Rules required category_id (mandatory)

## After
- Rules can assign category, entity, or both
- category_id is now optional (nullable) — entity-only rules are possible
- Backend validates at least one of category/entity is set
- apply_category_rules returns entity_assigned_count
- auto_categorize_transaction sets both category and entity from matching rule
- Frontend form has Entity dropdown alongside Category
- Rules list shows Entity column
- UI renamed from "Category Rules" to "Transaction Rules"

## Outcome
- Human intervention: No
- Measurable: Yes — entity auto-assignment now available
- Regressions: None — existing category-only rules work unchanged
