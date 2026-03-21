# Accounts Iteration 60 — Auto-create accounts from Tiller XLSX import

**Date:** 2026-03-21
**PR:** #187
**Status:** Shipped

## What changed

When importing a Tiller Foundation Template XLSX, the import service now auto-detects the Accounts sheet and creates Account records with:
- Account name, institution, last-4 digits
- Type mapping (Tiller CREDIT -> credit_card, INDIVIDUAL -> brokerage, 529 -> investment, JTWROS -> brokerage, UTMA -> brokerage)
- Opening balance with balance snapshot
- Transaction linking via account_id (100% linkage rate)

Idempotent — re-importing skips existing accounts.

## Before
- Import only processed the Transactions sheet
- No accounts were auto-created
- Transactions had no account_id linkage

## After
- 19 accounts auto-created from Tiller template
- 9,027 transactions linked to accounts (100%)
- Import summary shows "Accounts: 19 created"
- Re-import shows "19 already existed"

## Human intervention

Yes — user requested this feature.

## Measurable outcome

Yes — accounts created and linked to transactions during import.
