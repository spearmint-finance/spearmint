# Cash Flow Analysis

Cash flow analysis shows how money moves through your accounts — what comes in, what goes out, and what's left.

## Understanding Cash Flow

**Cash Flow = Income - Expenses**

Simple in theory, but accurate calculation requires:
- Excluding transfers (money moving between your accounts)
- Excluding credit card payments (already counted as charges)
- Optionally excluding capital expenses (investments, not spending)

Spearmint handles all of this automatically through [Classifications](../concepts/classifications.md).

## Cash Flow Dashboard

The Cash Flow view provides:

### Summary Metrics

| Metric | Description |
|--------|-------------|
| **Total Income** | All money coming in (salary, interest, refunds) |
| **Total Expenses** | All money going out (excluding transfers) |
| **Net Cash Flow** | Income minus Expenses |
| **Savings Rate** | Net Cash Flow / Income × 100% |

### Time Periods

View cash flow by:
- **Daily** — Day-by-day detail
- **Weekly** — Week-over-week patterns
- **Monthly** — Standard monthly view
- **Quarterly** — Business quarter view
- **Yearly** — Annual summary

### Date Ranges

Select custom date ranges:
- Last 30 days
- Last 3 months
- Year to date
- Last year
- Custom range

## Waterfall Chart

The waterfall chart visualizes how money flows:

```
┌──────────────────────────────────────────────────────┐
│  Income        ████████████████████████  +$8,500     │
│  Groceries     ████  -$600                           │
│  Housing       ████████████  -$2,100                 │
│  Utilities     ██  -$350                             │
│  Transport     ███  -$450                            │
│  Shopping      ███  -$520                            │
│  Entertainment ██  -$280                             │
│  Other         ███  -$400                            │
│  ─────────────────────────────────────               │
│  Net Cash Flow ████████  +$3,800                     │
└──────────────────────────────────────────────────────┘
```

## Analysis View vs Complete View

### Analysis View (Default)

Shows your **true financial picture**:
- ✅ Transfers excluded
- ✅ Credit card payments excluded
- ✅ Reimbursements handled correctly
- ✅ CapEx optionally separated

**Use for:** Understanding your actual financial health

### Complete View

Shows **all transactions as recorded**:
- Transfers included
- All payments shown
- Matches bank statements

**Use for:** Reconciliation, auditing, finding discrepancies

### Toggle Views

Switch between views using the toggle in the Cash Flow header. Both views are valid — they serve different purposes.

## CapEx Filter

Toggle **"Exclude CapEx"** to see operating cash flow:

| View | What It Shows |
|------|---------------|
| Include CapEx | Total cash movement (including renovations, major purchases) |
| Exclude CapEx | Operating cash flow (daily living expenses only) |

### Example

This month you:
- Earned $8,000
- Spent $3,000 on living expenses
- Spent $15,000 on a kitchen renovation

| Metric | Include CapEx | Exclude CapEx |
|--------|--------------|---------------|
| Income | $8,000 | $8,000 |
| Expenses | $18,000 | $3,000 |
| Net Cash Flow | -$10,000 | +$5,000 |
| Interpretation | "Losing money!" | "Saving well, plus investing in home" |

## Cash Flow by Account

See how each account contributes:

| Account | Income | Expenses | Net |
|---------|--------|----------|-----|
| Checking | $8,500 | $4,200 | +$4,300 |
| Credit Card | — | $2,100 | -$2,100 |
| Savings | $12 | — | +$12 |
| **Total** | **$8,512** | **$6,300** | **+$2,212** |

## Cash Flow Trends

Track how your cash flow changes over time:

- **Monthly trend** — Is your savings rate improving?
- **Seasonal patterns** — Higher expenses in December? Summer?
- **Year-over-year** — How does this January compare to last?

## Cash Flow Reports

Export cash flow data:
- **Summary report** — Key metrics in printable format
- **Detailed report** — Transaction-level breakdown
- **CSV export** — For further analysis

---

**Related:**
- [Classifications](../concepts/classifications.md) — How exclusions work
- [CapEx vs OpEx](../concepts/capex-vs-opex.md) — Separating investments from spending
- [Reporting](reporting.md) — Full reporting capabilities

