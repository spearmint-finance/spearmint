# Accounts Iteration 1 — NetWorthCard Division-by-Zero Fix

**Date shipped:** 2026-03-15
**PR:** #67 MERGED
**North star:** 1 user-visible improvement shipped (target: 1)

## What Was Before
- `NetWorthCard.tsx` had division-by-zero bugs in percentage calculations (asset ratio, liquid %, investment %)
- When a user had zero assets or zero total balances, the component displayed `NaN%` instead of `0.0%`
- All `NetWorth` type fields (`string | number`) were used directly in arithmetic without coercion, causing TypeScript errors
- Only `snake_case` field names were used, ignoring `camelCase` SDK variants

## What Changed
- Added zero-division guards: percentages return 0 when denominator is 0
- Added `Number()` coercion for all `NetWorth` fields at the top of the component
- Handled both `snake_case` and `camelCase` field variants (`net_worth`/`netWorth`, `liquid_assets`/`liquidAssets`, `as_of_date`/`asOfDate`, `account_breakdown`/`accountBreakdown`)
- Added null guard on `as_of_date` display

## What Is After
- NetWorthCard renders correctly with zero assets, zero liabilities, or both zero
- All percentage displays show `0.0%` instead of `NaN%` when denominators are zero
- Zero TypeScript errors in `NetWorthCard.tsx` (previously 17 type errors)
- Component works correctly with both SDK (camelCase) and direct API (snake_case) responses

## Metrics
- Files changed: 1 (`web-app/src/components/Accounts/NetWorthCard.tsx`)
- TypeScript errors fixed in file: 17 → 0
- Human intervention needed: No
- Regressions: None
