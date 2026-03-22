# Accounts Iteration 83 — Display Splits in Transaction Detail

**Date:** 2026-03-22
**PR:** #232
**Focus:** Show split transaction breakdown in the transaction detail dialog

## Before
- Transaction detail dialog did not show splits at all
- Users could only see/edit splits in the transaction form

## After
- Split items displayed as bordered cards with category name, description, and amount
- Header shows "Split into N items"
- Only appears when the transaction has splits

## Outcome
- Human intervention: No
- Measurable: Yes — split transactions now visible in detail view
- Regressions: None
