# Accounts Iteration 85 — Holdings Gain/Loss Zero-Value Fix

**Date:** 2026-03-22
**PR:** #237
**Focus:** Fix holdings gain/loss calculation for zero cost basis and zero current value edge cases

## Before
- Gain/loss calculation used Python truthiness which silently skipped when cost_basis or current_value was 0
- Holdings with zero cost basis (gifted shares, spinoffs) showed no gain/loss data
- Holdings with zero current value (total loss) showed no gain/loss data
- Frontend would crash on `.toFixed(1)` if gain_loss_percent was null (JSON null vs undefined)

## After
- Uses `is not None` checks so 0 values are properly handled
- Zero cost basis: shows absolute gain/loss, skips percentage (infinite)
- Zero current value: shows -100% loss correctly
- Frontend uses `!= null` to handle both null and undefined

## Outcome
- Human intervention: No
- Measurable: Yes — correct gain/loss display for edge case holdings
- Regressions: None
