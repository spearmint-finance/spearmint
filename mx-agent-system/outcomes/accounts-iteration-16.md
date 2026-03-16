# Accounts Iteration 16 — Deep-Link Transactions by Account

**Date:** 2026-03-16
**PR:** #101
**Status:** Shipped

## Focus

Add URL-driven account filter and cross-page navigation from account details to filtered transactions.

## What Changed

### Before
- Transactions page filters were state-only — no URL persistence
- No way to navigate from account details to that account's transactions
- No way to share or bookmark a filtered transaction view

### After
- TransactionList reads ?account_id= from URL search params on mount
- AccountDetailsDialog has "View Transactions" button navigating to /transactions?account_id=N
- Filter badge reflects URL-driven filter
- Natural account → transactions navigation flow

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 cross-page navigation, 0 → 1 URL-driven filter)

## Verification
- PR #101 merged to main 2026-03-16T14:21:59Z
