# Home Renovation Tracking

A major home renovation is one of the best examples of why [Capital Expense tracking](../concepts/capex-vs-opex.md) matters. Without it, a kitchen remodel makes you look broke. With it, you see the investment clearly.

## The Problem

You decide to renovate your kitchen. Over 3 months, you spend:
- $8,000 at Home Depot
- $5,000 to a contractor
- $2,000 on appliances
- **$15,000 total**

Your normal monthly spending is $4,000.

### Without CapEx Separation

| Month | "Expenses" | Your Reaction |
|-------|-----------|---------------|
| January | $4,000 | Normal |
| February | $12,000 | 😱 "I'm broke!" |
| March | $8,000 | 😰 "Still overspending!" |
| April | $4,000 | 😅 "Finally normal" |

Your budgeting app is useless during the renovation. Every alert fires. Every chart looks terrible.

### With CapEx Separation

| Month | Operating | CapEx | Reaction |
|-------|-----------|-------|----------|
| January | $4,000 | $0 | Normal spending |
| February | $4,000 | $8,000 | Normal spending + renovation investment |
| March | $4,000 | $4,000 | Normal spending + renovation investment |
| April | $4,000 | $3,000 | Normal spending + renovation wrap-up |

Your **operating expenses stayed constant**. You invested $15,000 in your home. Completely different picture.

## Setting Up Renovation Tracking

### Option 1: Tag-Based Tracking

Use tags to group renovation expenses:

1. Create tag: "Kitchen Reno 2025"
2. For each renovation purchase:
   - Set classification to **Capital Expense**
   - Add the "Kitchen Reno 2025" tag

### Option 2: Category-Based Tracking

Create a dedicated category:

```
Capital Investments
├── Home Improvements
│   ├── Kitchen Renovation
│   ├── Bathroom Renovation
│   └── Other
├── Vehicles
└── Equipment
```

### Option 3: Combined

Use both — classification for calculation, tags for project tracking.

## Day-to-Day During Renovation

### Importing Receipts

As you make purchases:
1. Import your credit card/bank statement
2. Find renovation transactions
3. Mark as Capital Expense
4. Add project tag

### Quick Classification

Create a rule if you're making many purchases at the same place:

| Pattern | Classification |
|---------|---------------|
| HOME DEPOT | Capital Expense |

⚠️ **Be careful:** Not all Home Depot purchases are CapEx. You might buy light bulbs there. Review and adjust as needed.

## Contractor Payments

Large contractor payments are definitely CapEx:

| Transaction | Amount | Classification |
|-------------|--------|---------------|
| JOHNSON CONSTRUCTION | $5,000 | Capital Expense |
| CITY PERMIT FEE | $500 | Capital Expense |
| PLUMBER LLC | $1,200 | Capital Expense |

## Monitoring the Project

### Project Dashboard

Filter by your renovation tag to see:
- Total spent to date
- Breakdown by category (materials, labor, permits)
- Timeline of spending
- Remaining budget (if you set one)

### vs Operating Expenses

Compare side-by-side:
- Operating expenses: Still normal?
- Renovation spending: On track?

## When the Renovation Ends

### Final Tally

Generate a report:
- All transactions tagged with the renovation
- Total cost
- Breakdown by vendor/category
- Timeline

### Record for Taxes/Sale

Renovation costs can add to your home's cost basis, reducing capital gains when you sell. Keep this report!

### Archive the Tag

Mark the project complete:
- Final amount: $15,247
- Completed: April 2025
- Notes: Kitchen remodel, new appliances

## Multiple Renovations

Tracking several projects? Use distinct tags:

| Tag | Status | Total |
|-----|--------|-------|
| Kitchen Reno 2025 | Complete | $15,247 |
| Bathroom Update | In Progress | $3,500 |
| Deck Rebuild | Planned | $0 |

Each project is tracked separately while all are classified as CapEx.

## Impact on Forecasting

### Short-Term

During renovation, cash flow projections account for the CapEx drain. You can toggle:
- **Include CapEx**: See total cash impact
- **Exclude CapEx**: See operating trajectory

### Long-Term

After renovation, projections return to normal because the operating expense baseline wasn't affected.

## The Bigger Picture

### Asset Building vs Spending

That $15,000 didn't disappear. It:
- Increased your home's value
- Improved your quality of life
- May reduce future maintenance costs

Spearmint helps you see this clearly instead of just showing a scary spending number.

### Informed Decisions

With clear CapEx tracking, you can ask:
- "Can we afford this renovation without impacting our savings rate?"
- "What's our operating runway if we proceed?"
- "How does this compare to past investments?"

---

**Related:**
- [CapEx vs OpEx](../concepts/capex-vs-opex.md) — The full concept
- [Classifications](../concepts/classifications.md) — How CapEx affects calculations
- [Cash Flow Analysis](../features/cash-flow-analysis.md) — Toggle CapEx in reports

