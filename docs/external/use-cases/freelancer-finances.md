# Freelancer Finances

Freelancers, contractors, and gig workers face unique financial challenges: irregular income, business expenses mixed with personal, quarterly taxes, and reimbursable client expenses. Spearmint handles all of this.

## The Freelancer Challenge

| Challenge | Why It's Hard |
|-----------|--------------|
| **Irregular income** | Can't predict monthly earnings |
| **Mixed expenses** | Business and personal in same accounts |
| **Tax preparation** | Need clear business expense records |
| **Client reimbursements** | Track what clients owe you |
| **Cash flow timing** | Invoice paid 60 days later |
| **Multiple income streams** | Different clients, platforms, projects |

## Setting Up for Freelance

### Account Structure

Create accounts that separate business and personal:

| Account | Type | Purpose |
|---------|------|---------|
| Personal Checking | Checking | Personal expenses |
| Business Checking | Checking | Business income/expenses |
| Personal Savings | Savings | Emergency fund |
| Tax Savings | Savings | Set aside for quarterly taxes |
| Business Credit | Credit Card | Business expenses |
| Personal Credit | Credit Card | Personal expenses |

### Business vs Personal Categories

Create clear category structures:

**Business Categories:**
- Business > Software & Tools
- Business > Marketing
- Business > Office Supplies
- Business > Travel
- Business > Professional Services
- Business > Equipment

**Income Categories:**
- Income > Client Work
- Income > Retainer
- Income > Products
- Income > Passive

## Tracking Irregular Income

### Income by Client

Tag income by client or project:

| Transaction | Amount | Client Tag |
|-------------|--------|------------|
| Invoice #1234 | $5,000 | Acme Corp |
| Retainer Feb | $2,500 | Beta Inc |
| Project X | $8,000 | Gamma LLC |

### Income Analysis

Spearmint shows:
- Income by month (see the variability)
- Income by client (diversification check)
- Average monthly income (for projections)
- Income trends (growing or shrinking?)

### Forecasting Variable Income

Use [forecasting](../features/forecasting.md) with appropriate methods:
- **Moving Average** — Smooths out month-to-month swings
- **Conservative estimates** — Use worst-case for planning

## Business Expense Tracking

### Automatic Categorization

Create rules for common business expenses:

| Pattern | Category |
|---------|----------|
| ADOBE, FIGMA, GITHUB | Software & Tools |
| GOOGLE ADS, FACEBOOK | Marketing |
| STAPLES, AMAZON OFFICE | Office Supplies |
| DELTA, UNITED, MARRIOTT | Travel |

### Tax-Deductible Expenses

Tag expenses for tax time:
- Add "Tax Deductible" tag
- Or use Business parent category
- Generate year-end report for accountant

## Client Reimbursements

Track expenses clients should reimburse:

### Step 1: Mark as Reimbursable

When you pay for something a client should cover:
1. Find the transaction (e.g., $400 conference ticket)
2. Set classification to **Reimbursable**
3. Add client tag

### Step 2: Track Pending

View all unreimbursed expenses:
- Navigate to **Transactions**
- Filter by Classification = Reimbursable
- Filter by unlinked (no matching reimbursement)

### Step 3: Match When Paid

When the client reimburses:
1. Import the payment
2. Link to the original expense
3. Both are excluded from your personal income/expense

**Result:** Clear view of what's owed, accurate personal finances.

## Quarterly Tax Planning

### Set Aside for Taxes

As a freelancer, you pay quarterly estimated taxes. Spearmint helps:

1. Track net business income monthly
2. Estimate quarterly tax liability (typically 25-30% of net)
3. Transfer to Tax Savings account
4. Track transfers separately

### Tax Savings Workflow

When you receive client payment:
1. $5,000 hits Business Checking
2. Transfer $1,500 (30%) to Tax Savings
3. Spearmint tracks the transfer, doesn't count as expense

At quarter end:
- Tax Savings account shows set-aside amount
- Pay estimated taxes from this account
- Stay out of trouble with the IRS

## Cash Flow Management

### Invoice Aging

Track outstanding invoices:
- Money earned but not yet received
- Use forecasting to project when cash arrives

### Runway Calculation

Critical for freelancers:
- Current cash on hand
- Average monthly expenses
- **Months of runway** = Cash ÷ Expenses

### Seasonality

Some freelance work is seasonal:
- Use year-over-year analysis
- Identify slow months
- Build reserves during busy periods

## Separating Business and Personal

### The Ideal Setup

Completely separate accounts make everything easier:
- Business income → Business Checking
- Business expenses → Business Credit or Checking
- Pay yourself → Transfer to Personal
- Personal spending → Personal accounts

### The Reality

Many freelancers mix accounts. Spearmint handles this:
- Tag transactions as Business or Personal
- Classify appropriately
- Generate Business-only reports for taxes
- Generate Personal-only reports for budgeting

## Year-End Tax Reporting

Generate reports for your accountant:

### Business Income Report
- All income by source
- Totals by category
- Client breakdown

### Business Expense Report
- All deductible expenses
- Organized by tax category
- Receipts reference (if you add notes)

### Summary
- Net business income (profit)
- Quarterly estimated tax payments made
- Home office calculations (if applicable)

---

**Related:**
- [Classifications](../concepts/classifications.md) — Reimbursable handling
- [Forecasting](../features/forecasting.md) — Variable income projections
- [Reporting](../features/reporting.md) — Tax preparation reports

