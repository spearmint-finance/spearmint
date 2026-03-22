# Accounts Iteration 66 — Split Amount Validation + Regression Test

**Date:** 2026-03-22
**PRs:** #195, #196
**Focus:** Validate split amounts sum before saving; entity-scoped category change regression test

## Before
- Split amounts could be saved even when sum didn't match parent transaction
- No regression test for entity-scoped category changes

## After
- Validation prevents saving splits when amounts don't sum to parent amount
- Regression test ensures entity_id is preserved when changing categories

## Outcome
- Human intervention: No
- Measurable: Yes — data integrity improved, regression coverage added
- Regressions: None
