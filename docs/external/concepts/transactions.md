# Transactions

Transactions are the atomic units of your financial life — every deposit, purchase, transfer, and payment.

## Transaction Fields

Each transaction in Spearmint contains:

| Field | Description | Example |
|-------|-------------|---------|
| **Date** | When the transaction occurred | 2025-01-15 |
| **Amount** | The value (positive = income, negative = expense) | -45.99 |
| **Description** | What the bank recorded | "AMAZON.COM*1A2B3C" |
| **Category** | The spending category | "Shopping" |
| **Account** | Which account this belongs to | "Chase Checking" |
| **Classification** | How it affects calculations | "Regular Expense" |

## Understanding Amounts

Spearmint uses a consistent sign convention:

- **Positive amounts** = Money coming IN (income, deposits, refunds)
- **Negative amounts** = Money going OUT (expenses, purchases, payments)

Some bank exports use opposite conventions. When you [set up an Import Profile](../features/import-profiles.md), you can configure how to interpret the bank's format.

## Transaction Relationships

Transactions can be related to each other:

### Transfers
When you move money between your own accounts:
- $500 withdrawal from Checking
- $500 deposit to Savings

Spearmint [detects these pairs](../features/relationship-detection.md) and links them so they don't inflate your income or expense totals.

### Credit Card Payments
When you pay your credit card bill:
- $1,200 payment from Checking
- $1,200 receipt on Credit Card

These are linked to prevent double-counting.

### Reimbursements
When you pay for something that will be reimbursed:
- $350 expense for work travel
- $350 deposit when reimbursed

Linking these shows your true out-of-pocket spending.

## Transaction Splits

A single transaction can be split across multiple purposes or people.

### Split by Category
A $150 Walmart purchase might be:
- $80 Groceries
- $50 Household
- $20 Electronics

### Split by Person
For households with shared expenses, a $200 dinner might be:
- $100 attributed to "Mom"
- $100 attributed to "Dad"

This enables per-person spending analysis.

## Editing Transactions

Click any transaction to view and edit:

- **Description** — Add notes or clean up bank text
- **Category** — Assign or change the category
- **Classification** — Change how it affects calculations
- **Tags** — Add custom tags for organization
- **Account** — Correct the associated account

## Bulk Operations

For efficiency, you can select multiple transactions and:

- Assign the same category
- Apply the same classification
- Add tags
- Delete (use carefully)

## Duplicate Detection

When importing, Spearmint checks for potential duplicates based on:
- Date
- Amount
- Description similarity

Suspected duplicates are flagged for your review.

---

**Related:**
- [Categories](categories.md) — Organize by spending type
- [Classifications](classifications.md) — Control calculation behavior
- [Relationship Detection](../features/relationship-detection.md) — Auto-link related transactions

