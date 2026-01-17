# Household Budgeting

Managing finances for a household with multiple people requires tracking shared expenses, individual spending, and complex money flows. Spearmint is designed for exactly this.

## The Challenge

Household finances are complex:
- **Shared expenses** — Mortgage, utilities, groceries
- **Individual expenses** — Personal subscriptions, hobbies
- **Shared income** — Both partners work
- **Complex accounts** — Joint and individual accounts
- **Reimbursements** — "I'll pay you back for dinner"

## Setting Up for a Household

### Step 1: Create All Accounts

Add every account in the household:

| Account | Type | Owner |
|---------|------|-------|
| Joint Checking | Checking | Shared |
| Partner A Checking | Checking | Partner A |
| Partner B Checking | Checking | Partner B |
| Joint Savings | Savings | Shared |
| Partner A Credit | Credit Card | Partner A |
| Partner B Credit | Credit Card | Partner B |

### Step 2: Define People

Spearmint supports tagging transactions by person:
- Partner A
- Partner B
- Kids (if applicable)
- Household (shared)

### Step 3: Import All Accounts

Import transactions from every account for a complete picture.

## Tracking Shared Expenses

### Automatic Household Expenses

Create categorization rules for obvious shared expenses:

| Pattern | Category | Person |
|---------|----------|--------|
| Mortgage, Rent | Housing | Household |
| Electric, Gas, Water | Utilities | Household |
| Internet, Phone | Bills | Household |

### Splitting Transactions

For purchases that mix personal and shared:

**Example:** $200 Costco run
- $150 groceries (Household)
- $30 Partner A personal items
- $20 Partner B personal items

Split the transaction to track accurately.

## Individual Spending

Each person's spending is tracked separately:

### Partner A Report
- Subscriptions: $50/month
- Hobbies: $200/month
- Personal care: $75/month

### Partner B Report
- Subscriptions: $30/month
- Hobbies: $150/month
- Fitness: $100/month

### Household Report
- Combined shared expenses
- Total income vs expenses
- Net household cash flow

## Handling Transfers Between Partners

When money moves between partners:

**Scenario:** Partner A pays for dinner, Partner B Venmos them back

| Transaction | Account | Classification |
|-------------|---------|---------------|
| -$80 Restaurant | Partner A Card | Expense |
| +$40 Venmo | Partner A Checking | Transfer |
| -$40 Venmo | Partner B Checking | Transfer |

The Venmo transfers are linked and excluded. The net effect:
- Partner A: $40 expense
- Partner B: $40 expense
- Total: $80 household dining expense

## Joint Account Best Practices

### Centralize Shared Expenses

Route all shared expenses through a joint account:
1. Both partners contribute monthly
2. Shared bills paid from joint
3. Individual accounts for personal

### Or, Track Contributions

If you pay shared expenses from individual accounts:
1. Tag with "Household"
2. Split expenses by who paid
3. Reconcile contributions monthly

## Household Budget Dashboard

View household finances at a glance:

### Income Section
- Partner A income
- Partner B income
- Other income (interest, dividends)
- **Total household income**

### Expense Section
- Shared expenses (housing, utilities, groceries)
- Partner A personal
- Partner B personal
- **Total household expenses**

### Summary
- Net cash flow
- Savings rate
- Runway (months of expenses covered)

## Reporting by Person

Generate reports for:

### Whole Household
All accounts, all transactions, complete picture

### Individual Partner
- Their accounts only
- Their share of splits
- Personal spending analysis

### Shared Only
- Joint accounts
- Transactions tagged "Household"
- Shared expense tracking

## Tips for Household Success

### Agree on Categories

Decide together what's "Household" vs individual:
- Is Netflix shared or personal?
- Are gym memberships individual?
- What about date nights?

### Regular Review

Weekly or monthly, review together:
- Are contributions balanced?
- Any unexpected spending?
- On track for savings goals?

### Use Tags Liberally

Tags help with flexible reporting:
- "Date Night"
- "Kids Activities"
- "Home Improvement"
- "Vacation Fund"

---

**Related:**
- [Transactions](../concepts/transactions.md) — Splits and tagging
- [Categories](../concepts/categories.md) — Organizing spending
- [Reporting](../features/reporting.md) — Generating household reports

