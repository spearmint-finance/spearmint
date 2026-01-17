# Reporting

Spearmint provides comprehensive reporting to help you understand your finances and share insights.

## Available Reports

### Summary Report

A high-level overview of your financial health:

| Section | Contents |
|---------|----------|
| **Period Overview** | Date range, total transactions |
| **Income Summary** | Total income, top sources, trends |
| **Expense Summary** | Total expenses, top categories, trends |
| **Cash Flow** | Net cash flow, savings rate |
| **Key Metrics** | Average daily spend, largest transactions |

### Income Report

Detailed breakdown of all income:

- **By Source** — Salary, freelance, interest, dividends, refunds
- **By Account** — Which accounts receive income
- **By Period** — Monthly, quarterly, yearly trends
- **Regularity** — Recurring vs one-time income

### Expense Report

Detailed breakdown of all spending:

- **By Category** — Where money goes
- **By Account** — Which accounts spend
- **By Period** — Spending trends over time
- **Top Merchants** — Where you spend most

### Cash Flow Report

How money flows through your accounts:

- **Inflows vs Outflows** — Side-by-side comparison
- **Net by Period** — Monthly net cash flow
- **Running Balance** — Balance trajectory over time
- **Savings Rate** — What percentage you're saving

### Net Worth Report

Your complete financial picture:

| Assets | Liabilities |
|--------|-------------|
| Checking balances | Credit card balances |
| Savings balances | Loan balances |
| Investment values | Other debts |
| **Total Assets** | **Total Liabilities** |

**Net Worth = Assets - Liabilities**

### Reconciliation Report

For auditing and accuracy:

- **By Account** — Statement vs calculated balance
- **Discrepancies** — Accounts that don't match
- **Missing Transactions** — Gaps in import coverage
- **Duplicates** — Potential duplicate entries

## Generating Reports

### From the Dashboard

1. Navigate to **Reports**
2. Select report type
3. Choose date range
4. Apply filters (optional)
5. Click **Generate**

### Quick Reports

Common report presets:

| Preset | Period | Type |
|--------|--------|------|
| Monthly Summary | Last 30 days | Summary |
| Quarterly Review | Last 3 months | Full |
| Year in Review | Last 12 months | Summary |
| Tax Prep | Last calendar year | Income/Expense |

## Filtering Reports

Narrow down reports using filters:

| Filter | Options |
|--------|---------|
| **Date Range** | Last 30 days, last quarter, custom |
| **Accounts** | All, specific accounts |
| **Categories** | All, specific categories |
| **Classifications** | Include/exclude transfers, CapEx, etc. |
| **Amount Range** | Minimum and/or maximum |

## Report Views

### Analysis View

Default view with smart exclusions:
- Transfers excluded
- Credit card payments excluded
- Reimbursements handled correctly

Shows your **true financial picture**.

### Complete View

All transactions included:
- Transfers shown
- Every transaction counted

Matches **bank statements** for reconciliation.

## Export Formats

### JSON Export

Structured data for:
- Integration with other tools
- Custom analysis
- Data backup

### CSV Export

Spreadsheet-compatible for:
- Excel/Google Sheets analysis
- Importing to other software
- Sharing with accountants

### PDF Export (Coming Soon)

Printable reports for:
- Record keeping
- Sharing with partners
- Tax documentation

## Scheduled Reports

Set up automatic report generation:

1. Navigate to **Reports → Scheduled**
2. Click **Add Schedule**
3. Configure:
   - Report type
   - Frequency (weekly, monthly, quarterly)
   - Delivery (email, save to location)
4. Activate

## Report Insights

Reports include automated insights:

### Trend Indicators
- ↑ Spending up 15% from last month
- ↓ Income down 5% from same period last year
- → Cash flow stable over last 3 months

### Anomaly Flags
- ⚠️ Unusual spike in "Restaurants" category
- ⚠️ Income lower than 6-month average
- ⚠️ Savings rate below target

### Recommendations
Based on your data:
- "Consider reviewing subscription expenses"
- "Emergency fund covers 4.2 months"
- "On track for annual savings goal"

---

**Related:**
- [Cash Flow Analysis](cash-flow-analysis.md) — Interactive cash flow views
- [Categories](../concepts/categories.md) — How spending is categorized
- [Classifications](../concepts/classifications.md) — How calculations work

