# Accounts Iteration 15 — CSV Export for Transactions

**Date:** 2026-03-16
**PR:** #100
**Status:** Shipped

## Focus

Add CSV export capability to the transactions page.

## What Changed

### Before
- No way to export transactions from the UI
- Users had to manually copy data or use external tools

### After
- "Export CSV" button in the transactions toolbar
- Downloads all filtered transactions (up to 10,000 rows) as CSV
- Respects current search/filter criteria
- Resolves linked account names
- Headers: Date, Description, Amount, Type, Category, Account, Classification, Transfer, Notes, Tags
- Proper CSV escaping, dated filename

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 CSV export capability)

## Verification
- PR #100 merged to main 2026-03-16T14:17:35Z
