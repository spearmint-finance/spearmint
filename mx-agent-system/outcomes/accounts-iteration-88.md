# Accounts Iteration 88 — Category Merge/Reassign Workflow

**Date:** 2026-03-22
**PR:** #240
**Focus:** Add category merge functionality (reassign all items to target, then delete source)

## Before
- No way to merge or consolidate categories
- Users had to manually reassign each transaction and then delete the old category

## After
- Backend: PUT /categories/{id}/merge endpoint reassigns all transactions, splits, rules, budgets, and children
- Frontend: Merge icon button in category management grid with Autocomplete target selector dialog
- Success feedback shows count of reassigned items

## Outcome
- Human intervention: No
- Measurable: Yes — new category management workflow available
- Regressions: None
