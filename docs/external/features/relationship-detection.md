# Relationship Detection

Spearmint automatically detects relationships between transactions — transfers, credit card payments, and reimbursements — so your financial calculations stay accurate.

## Why Relationships Matter

Without relationship detection:

| Transaction | Account | Counted As |
|-------------|---------|------------|
| -$500 Transfer Out | Checking | Expense |
| +$500 Transfer In | Savings | Income |

**Result:** Your "income" and "expenses" are both inflated by $500.

With relationship detection:

| Transaction | Account | Classification |
|-------------|---------|---------------|
| -$500 Transfer Out | Checking | Transfer (excluded) |
| +$500 Transfer In | Savings | Transfer (excluded) |

**Result:** Accurate totals. The money just moved; you didn't earn or spend it.

## Types of Relationships

### Transfers

Money moving between your own accounts:
- Checking → Savings
- Savings → Brokerage
- Account → Account

**Detection criteria:**
- Same amount (opposite signs)
- Within a few days
- Between accounts you own

### Credit Card Payments

When you pay your credit card bill:
- Checking account: -$1,500 (payment)
- Credit Card: +$1,500 (receipt)

**Why it matters:** The individual charges on the card were already counted as expenses. The payment is just settling the debt — not a new expense.

### Reimbursements

When you're paid back for something:
- Original expense: -$400 (hotel for work)
- Reimbursement: +$400 (company pays you back)

**Linking these:**
- Shows the expense as "net zero" for you
- Tracks pending reimbursements
- Keeps personal spending accurate

## Automatic Detection

Spearmint scans for potential relationships using:

| Factor | How It's Used |
|--------|---------------|
| **Amount** | Must match (or be very close) |
| **Date** | Within configurable window (default: 7 days) |
| **Accounts** | Both must be yours (for transfers) |
| **Direction** | One in, one out |

### Detection Confidence

Matches are scored by confidence:
- **High** — Strong match, auto-linked
- **Medium** — Likely match, flagged for review
- **Low** — Possible match, suggested only

### Running Detection

Detection runs:
- Automatically after imports
- On-demand via "Detect Relationships" button
- Periodically in background

## Manual Linking

For relationships Spearmint misses, link manually:

1. Open one transaction
2. Click **Link to Related Transaction**
3. Search for the matching transaction
4. Select the relationship type
5. Confirm

## Reviewing Detected Relationships

Navigate to **Transactions → Relationships** to see:

### Pending Review
Relationships detected but not confirmed:
- Review the match
- Confirm or reject
- Fix if wrong type

### Linked Transactions
All confirmed relationships:
- Click to see both sides
- Unlink if incorrect

### Unmatched Candidates
Transactions that *might* have relationships but couldn't be matched:
- Solo transfer amounts
- Reimbursement received but original expense unclear

## Relationship Types in Detail

### Transfer

```
Checking Account                    Savings Account
─────────────────                   ───────────────
-$500 "Transfer to Savings"    ←→   +$500 "Transfer from Checking"
```

Both transactions excluded from income/expense calculations.

### Credit Card Payment

```
Checking Account                    Credit Card
─────────────────                   ────────────
-$1,500 "Payment to Chase"     ←→   +$1,500 "Payment Received"
```

Payment excluded (debt settlement, not spending).
Individual charges on the card are still counted as expenses.

### Reimbursement

```
Work Trip Expense                   Reimbursement
─────────────────                   ─────────────
-$400 "Marriott Hotel"         ←→   +$400 "Expense Reimbursement"
```

Original expense marked as "Reimbursable" (excluded from personal spending).
Reimbursement marked as "Reimbursement" (excluded from income).
Net effect: $0 personal expense.

## Handling Edge Cases

### Partial Reimbursements
If only part is reimbursed, you can:
- Split the original transaction
- Link only the reimbursed portion

### Different Amounts
Sometimes amounts don't match exactly (fees, interest):
- Manually link with override
- Note the discrepancy

### Cross-Month Transfers
Transfer sent Dec 31, received Jan 2:
- Detection window spans months
- Both transactions properly linked

---

**Related:**
- [Classifications](../concepts/classifications.md) — How relationships affect calculations
- [Transactions](../concepts/transactions.md) — Transaction fundamentals

