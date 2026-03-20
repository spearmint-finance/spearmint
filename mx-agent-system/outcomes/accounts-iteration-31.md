# Accounts Iteration 31 — CSV Export for Cash Flow Statement

**Date:** 2026-03-20
**PR:** #128
**Status:** Shipped

## Focus

Add CSV export to the Cash Flow tab, matching the existing P&L export.

## What Changed

### Before
- P&L tab had CSV export button
- Cash Flow tab had no export capability

### After
- "Export CSV" button on Cash Flow tab header
- Exports operating/investing/financing sections with item descriptions and amounts
- Includes section totals and net change in cash
- File named cashflow-{entity}-{start}-to-{end}.csv

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 cash flow CSV export)

## Verification
- PR #128 merged to main 2026-03-20T01:17:27Z
