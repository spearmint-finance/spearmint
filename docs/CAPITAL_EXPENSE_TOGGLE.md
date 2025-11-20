# Capital Expense Toggle - User Guide

## Overview

The Financial Analysis system has a built-in toggle to **exclude or include capital expenses** in your analysis. This allows you to view your **operating expenses** separately from **capital investments**.

## How It Works

### The Toggle: Analysis Mode vs Complete Mode

Located at the top of the Analysis, Income Deep-Dive, and Expense Deep-Dive pages:

```
[ANALYSIS] [COMPLETE]
```

### Analysis Mode (Default)
✅ **Recommended for monthly/quarterly budget analysis**

**What it shows:**
- Operating income only (regular salary, business revenue)
- Operating expenses only (groceries, utilities, gas, insurance)

**What it excludes:**
- Transfers between your own accounts
- Capital expenses (vehicle purchases, equipment, property improvements)
- Non-operating income (loan disbursements, investment distributions)

**Use this mode when you want to:**
- Track your monthly spending trends
- See if you're living within your means
- Compare month-to-month expenses
- Calculate your savings rate on operating income

**Example:**
```
Analysis Mode (September):
Income:    $6,500 (salary)
Expenses:  -$4,200 (groceries, utilities, gas, insurance, dining)
Net Flow:  $2,300 ✅ Positive cash flow from operations

Excluded from view:
- $35,000 car purchase (capital expense)
- $5,000 transfer to savings (internal transfer)
```

### Complete Mode
✅ **Recommended for total net worth and tax analysis**

**What it shows:**
- ALL transactions including:
  - Operating income and expenses
  - Capital expenses (vehicles, equipment, property)
  - Transfers between accounts
  - All income types

**Use this mode when you want to:**
- See total cash movement
- Prepare for taxes (need all expenses including CapEx)
- Track net worth changes
- Verify all bank transactions are accounted for

**Example:**
```
Complete Mode (September):
Income:    $6,500 (salary)
Expenses:  -$39,200 (includes $35,000 car + $4,200 operating)
Net Flow:  -$32,700 ❌ Net negative due to car purchase

All transactions shown:
- $35,000 car purchase ✅ Included
- $5,000 transfer to savings ✅ Included
```

## Setting Up Capital Expenses

For this toggle to work effectively, you need to classify your capital expense transactions:

### Step 1: Create Capital Expense Classification

Run the setup script:
```bash
python add_capital_expense_classification.py --simple
```

This creates a classification with:
- `exclude_from_expense_calc = True` (excluded from operating expenses)
- `exclude_from_income_calc = True` (not income)
- `exclude_from_cashflow_calc = False` (real cash outflow)

### Step 2: Categorize Your Transactions

For each capital purchase:

1. **Create appropriate categories:**
   - Vehicle Purchase
   - Equipment
   - Home Improvement
   - Property Investment

2. **Apply the classification:**
   - Go to the transaction
   - Set Category: "Vehicle Purchase" (for example)
   - Set Classification: "Capital Expense"

### Step 3: Set Up Auto-Classification Rules

Create rules to automatically classify future capital expenses:

**Rule: Vehicle Purchases**
```
IF Category = "Vehicle Purchase"
OR (Amount < -$5,000 AND Description contains "car|vehicle|auto")
THEN Apply "Capital Expense" classification
```

**Rule: Equipment**
```
IF Category = "Equipment" AND Amount < -$1,000
THEN Apply "Capital Expense" classification
```

## Practical Examples

### Example 1: Monthly Budget Analysis

**Scenario:** You want to see if you're spending too much on groceries

**Action:** Use **Analysis Mode**

**Why:** This excludes the $20,000 you spent on a new car last month, giving you an accurate view of your operating expenses

**Result:**
```
Groceries: $800/month average ✅ Clean trend data
(Car purchase excluded from analysis)
```

### Example 2: Year-End Tax Preparation

**Scenario:** You need to report all expenses for tax deductions

**Action:** Use **Complete Mode**

**Why:** Your accountant needs ALL expenses including capital purchases for depreciation calculations

**Result:**
```
Operating Expenses: $50,000
Capital Expenses: $45,000 (car $35k + computer $3k + furniture $7k)
Total Deductions: $95,000
```

### Example 3: Savings Rate Calculation

**Scenario:** You want to know what % of your operating income you're saving

**Action:** Use **Analysis Mode**

**Why:** Including capital purchases would make your savings rate look artificially low

**Result:**
```
Operating Income: $78,000/year
Operating Expenses: $48,000/year
Savings Rate: 38% ✅ Accurate operating savings

vs. Complete Mode:
Total Income: $78,000
Total Expenses: $93,000 (includes $45k capital)
Savings Rate: -19% ❌ Misleading (shows negative due to one-time purchases)
```

## Visual Indicators

### Analysis Mode Active
```
ℹ️ Analysis Mode: Excludes transfers and capital expenses
   (vehicles, equipment, property) - shows only operating
   income and expenses for clearer financial insights
```

### Complete Mode Active
```
ℹ️ Complete Mode: Shows all transactions including
   transfers and capital expenses
```

## Common Questions

### Q: Why don't I see my car purchase in Analysis mode?
**A:** Because it's classified as a capital expense. Capital expenses are excluded from operating expense analysis to prevent distortion of your monthly spending trends. Switch to **Complete Mode** to see it.

### Q: My expenses seem too low. What's wrong?
**A:** You're probably in Analysis Mode with capital expenses properly classified. This is correct! Your operating expenses SHOULD be lower than your total expenses. Switch to Complete Mode to see everything.

### Q: How do I see ONLY capital expenses?
**A:**
1. Go to Transactions page
2. Filter by Classification = "Capital Expense"
3. Or run: `python view_capital_expenses.py`

### Q: Can I have different capital expense types?
**A:** Yes! Run the advanced setup:
```bash
python add_capital_expense_classification.py --advanced
```

This creates:
- Property Capital Expense
- Vehicle Capital Expense
- Equipment Capital Expense

### Q: What if I accidentally classify something as capital expense?
**A:** Simply edit the transaction and change the classification back to "Regular Transaction"

## Best Practices

### 1. Use Analysis Mode for Regular Reviews
- Monthly spending reviews
- Budget tracking
- Trend analysis
- Savings rate calculation

### 2. Use Complete Mode for:
- Tax preparation
- Net worth tracking
- Loan applications (show all assets purchased)
- Verifying all bank transactions imported

### 3. Consistently Classify Capital Expenses
Set a threshold (e.g., $500 or $1,000) and classify anything above that amount with multi-year usefulness as capital.

### 4. Review Quarterly
Every quarter, check your capital expense transactions to ensure they're properly classified.

## Summary

| Feature | Analysis Mode | Complete Mode |
|---------|---------------|---------------|
| **Purpose** | Operating budget & trends | Total cash movement |
| **Operating Income** | ✅ Shown | ✅ Shown |
| **Operating Expenses** | ✅ Shown | ✅ Shown |
| **Capital Expenses** | ❌ Hidden | ✅ Shown |
| **Transfers** | ❌ Hidden | ✅ Shown |
| **Use For** | Monthly analysis, budgets | Taxes, net worth, verification |
| **Savings Rate** | Operating savings % | Total savings % |
| **Best For** | Day-to-day financial health | Complete financial picture |

---

**Quick Actions:**
- 📊 Switch modes using the toggle at the top of any analysis page
- 🚗 Set up capital expenses: `python add_capital_expense_classification.py`
- 📈 View capital expenses: `python view_capital_expenses.py`
- 📖 Full guide: See `capital-expenses-guide.md`
