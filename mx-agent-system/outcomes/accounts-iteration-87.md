# Accounts Iteration 87 — Portfolio Gain/Loss Display Improvements

**Date:** 2026-03-22
**PR:** #239
**Focus:** Improve portfolio gain/loss display for null and zero values

## Before
- Total gain/loss showed $0.00 in red when cost basis data was unavailable
- Zero gain/loss showed red color (same as loss)
- Individual holdings only showed percentage chip, not dollar amount

## After
- Null total gain/loss shows "N/A" in neutral text color
- Zero gain/loss shows neutral color (not red)
- Individual holdings show gain/loss dollar amount in secondary text (e.g., "+$1,234.56")

## Outcome
- Human intervention: No
- Measurable: Yes — clearer portfolio information display
- Regressions: None
