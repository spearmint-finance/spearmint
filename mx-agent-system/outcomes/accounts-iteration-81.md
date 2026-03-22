# Accounts Iteration 81 — Duplicate Transaction

**Date:** 2026-03-22
**PR:** #224
**Focus:** Add duplicate transaction action to transaction detail dialog

## Before
- No way to duplicate a transaction — users had to manually re-enter all fields

## After
- "Duplicate" button in transaction detail dialog actions
- Opens create form pre-filled with the source transaction's data (today's date, same amount/category/account/tags/splits)
- Supports TransactionForm's new `defaultTransaction` prop for pre-filling in create mode

## Outcome
- Human intervention: No
- Measurable: Yes — reduces friction for recurring manual entries
- Regressions: None
