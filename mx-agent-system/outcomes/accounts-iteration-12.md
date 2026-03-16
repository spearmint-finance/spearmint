# Accounts Iteration 12 — Show Linked Account Name in Transactions

**Date:** 2026-03-16
**PR:** #95
**Status:** Shipped

## Focus

Update transaction list and detail to show the linked account name instead of free-text source/payment_method.

## What Changed

### Before
- Account column showed the free-text `source` field
- Institution column showed the free-text `payment_method` field
- TransactionDetail had no account information

### After
- Account column resolves account name from accounts list when account_id is present
- Institution column resolves institution name from linked account
- Falls back to source/payment_method for unlinked transactions
- TransactionDetail shows "Account" field with name and institution for linked transactions

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (2 columns + 1 detail field upgraded to show real account data)

## Verification
- PR #95 merged to main 2026-03-16T13:35:05Z
