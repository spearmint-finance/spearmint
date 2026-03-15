# Accounts Iteration 2 — Edit Account Details

**Date shipped:** 2026-03-15
**PR:** #69 MERGED
**North star:** 1 user-visible improvement shipped (target: 1)

## What Was Before
- AccountDetailsDialog had no edit functionality — only view + delete + add balance
- Users who needed to change account name, institution, or notes had to delete and recreate the account

## What Changed
- Added edit/save/cancel toggle in the dialog title bar (pencil icon, save icon, close icon)
- Inline form with fields: Account Name (required), Institution Name, Account Number Last 4, Notes
- Input validation: account name required, last 4 digits sanitized to digits only
- Error alert on mutation failure
- Form resets from current account data each time edit mode is entered

## What Is After
- Users can edit account details directly from the account details dialog
- Changes persist immediately via the existing `updateAccount` API
- Zero TypeScript errors in the modified file

## Metrics
- Files changed: 1 (`web-app/src/components/Accounts/AccountDetailsDialog.tsx`)
- Lines added: 146, removed: 33
- Human intervention needed: No
- Regressions: None
