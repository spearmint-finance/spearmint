# Account Reconciliation

**Status:** Draft
**Priority:** P2
**Gate:** G2
**Target Team:** Accounts team
**Directive:** #226
**Related Issue:** PKI-014
**Existing Spec:** `docs/account_balance_issue.md` (338-line detailed spec)

---

## Problem Statement

Users cannot verify that imported transactions are complete and accurate. There is no way to:
- Compare a bank statement balance against the calculated balance from transactions
- Mark transactions as cleared/reconciled
- Detect missing or duplicate transactions
- Track discrepancies over time

This is a fundamental personal finance feature — users need confidence that their data is correct. Every major competitor (YNAB, Firefly III, GnuCash, Actual Budget) supports reconciliation.

---

## Competitive Context

| App | Reconciliation | Statement Import | Balance History |
|-----|---------------|-----------------|-----------------|
| YNAB | Yes (manual) | No | Yes |
| Firefly III | Yes (manual) | CSV | Yes |
| GnuCash | Yes (manual) | OFX/QFX | Yes |
| Actual Budget | Yes (manual) | No | Yes |
| **Spearmint** | **No** | CSV only | **Partial (chart exists)** |

---

## Proposed Solution (Phase 1 — G2 scope)

### Core Reconciliation Flow

1. User selects an account and enters the statement ending date and balance
2. System calculates the expected balance from all transactions up to that date
3. System shows the difference (discrepancy) if any
4. User reviews and marks individual transactions as "cleared" (checkbox per transaction)
5. As transactions are cleared, the cleared balance updates in real-time
6. When cleared balance matches statement balance, reconciliation is complete
7. System saves a reconciliation record with timestamp

### Database Changes

1. **Add `is_cleared` boolean to transactions table** — tracks whether each transaction has been verified against a bank statement
2. **Add `reconciliations` table** — stores reconciliation records (account_id, statement_date, statement_balance, calculated_balance, discrepancy, status, completed_at)

### Frontend Changes

1. **Reconciliation page** (new route: `/accounts/:id/reconcile`)
   - Statement balance input form
   - Transaction list with "cleared" checkboxes
   - Running cleared balance vs. statement balance display
   - Discrepancy indicator
   - "Finish Reconciliation" button (enabled when balanced)

2. **Cleared indicator on transaction list** — small checkmark icon for reconciled transactions

3. **Reconciliation history** on account detail page — list of past reconciliations

### API Changes

1. `POST /accounts/:id/reconciliations` — start a new reconciliation
2. `PATCH /transactions/:id` — add `is_cleared` field to update
3. `POST /accounts/:id/reconciliations/:id/complete` — mark reconciliation as done
4. `GET /accounts/:id/reconciliations` — list reconciliation history

---

## Acceptance Criteria

- [ ] User can start a reconciliation for any account
- [ ] User can enter statement date and ending balance
- [ ] System calculates and displays expected balance from transactions
- [ ] User can mark individual transactions as cleared
- [ ] Running cleared balance updates in real-time
- [ ] Discrepancy is shown when cleared balance != statement balance
- [ ] Reconciliation can be completed when balanced (or with noted discrepancy)
- [ ] Past reconciliations are viewable in history
- [ ] Cleared transactions show a visual indicator in the main transaction list

---

## Out of Scope (Phase 1)

- Investment holdings tracking and valuation
- Hybrid brokerage account support (cash + investments)
- Automatic bank statement import (OFX/QFX)
- Automated reconciliation matching
- These are covered in the detailed spec at `docs/account_balance_issue.md` for future phases

---

## Impact on North Star

- Reconciliation is a trust-building feature — users who reconcile are more likely to continue using the app
- Required for any user managing real finances (not just exploring)
- Differentiates from simpler expense trackers that don't support reconciliation
- Open source contributors with accounting background will expect this
