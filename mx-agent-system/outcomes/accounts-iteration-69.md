# Accounts Iteration 69 — Inline Category Editor Filters by Row Entity

**Date:** 2026-03-22
**PR:** #199
**Focus:** Inline category dropdown in grid filters by the row's entity_id

## Before
- Inline category editor showed categories from global entity selector
- Editing a row with entity_id=2 while viewing "All Entities" showed all categories

## After
- Each row's inline category dropdown shows only categories matching the row's entity_id + global categories
- Categories fetched once (unfiltered) and filtered per-row at render time

## Outcome
- Human intervention: No
- Measurable: Yes — correct per-row category scoping
- Regressions: None
