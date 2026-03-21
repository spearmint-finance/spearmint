# Accounts Iteration 51 — Consolidate currency formatting to shared utility

**Date:** 2026-03-21
**PR:** #173
**Status:** Shipped

## What changed

Replaced hardcoded local `formatCurrency` functions in BalanceHistoryChart and NetWorthCard with the shared `formatCurrency` utility from `utils/formatters.ts`. Added a `decimals` parameter to the shared utility to support both compact (0 decimals) and precise (2 decimals) formatting.

## Before

- BalanceHistoryChart and NetWorthCard each had their own `formatCurrency` with hardcoded 'USD'
- Shared utility only supported 2 decimal places
- 3 different currency formatting implementations

## After

- Single shared `formatCurrency(amount, currency, decimals)` utility
- Components use `formatCompact = (v) => formatCurrency(v, "USD", 0)` for compact display
- Consistent formatting across all account components

## Verification

- TypeScript: no errors
- Vite build: succeeds, bundle size decreased
- PR #173 merged

## Human intervention

No — autonomous identification and fix.

## Measurable outcome

Yes — KI-003 resolved. Currency formatting consolidated from 3 implementations to 1.
