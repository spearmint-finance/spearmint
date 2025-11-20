# Capital Expenses - Quick Start Guide

## TL;DR

**Capital expenses** are large asset purchases (>$500-$1000) that last multiple years. Your system can handle them perfectly using the **Classification System**.

## 3-Step Setup (5 minutes)

### Step 1: Add Classification (Choose One)

**Option A - Simple (Recommended)**
```bash
python add_capital_expense_classification.py --simple
```

**Option B - Advanced (Multiple Categories)**
```bash
python add_capital_expense_classification.py --advanced
```

### Step 2: Create Asset Categories

Go to UI and create categories:
- `Vehicle Purchase`
- `Home Improvement`
- `Equipment`
- `Technology Assets`

### Step 3: Apply to Transactions

For each capital purchase:
1. Set **Category**: Vehicle Purchase, Equipment, etc.
2. Set **Classification**: Capital Expense
3. Done!

## What This Does

### Before Classification:
```
Expense Analysis (September):
- Groceries: $800
- New Car: $35,000  ← Distorts monthly trends!
- Utilities: $200
- Gas: $150
Total: $36,150 (not representative of normal spending)
```

### After Classification:
```
Expense Analysis (September):
- Groceries: $800
- Utilities: $200
- Gas: $150
Total: $1,150 (accurate operating expenses)

Cash Flow Analysis:
- Operating Expenses: -$1,150
- Capital Expenses: -$35,000
- Total Cash Out: -$36,150 (real money spent)

CapEx Report:
- New Car: $35,000 (asset acquired)
```

## Common Scenarios

### Scenario 1: Car Purchase
```
Transaction:
  Description: 2025 Toyota Camry
  Amount: -$35,000
  Category: Vehicle Purchase
  Classification: Capital Expense ✅

Result:
  ✅ Excluded from expense trends
  ✅ Included in cash flow
  ✅ Tracked separately for taxes
```

### Scenario 2: New Laptop
```
Transaction:
  Description: MacBook Pro 16"
  Amount: -$3,499
  Category: Equipment
  Classification: Capital Expense ✅

Result:
  ✅ Doesn't distort monthly spending analysis
  ✅ Shows in cash flow (money actually spent)
  ✅ Easy to find for depreciation/taxes
```

### Scenario 3: Home Improvement
```
Transaction:
  Description: New HVAC System
  Amount: -$8,500
  Category: Home Improvement
  Classification: Capital Expense ✅

Result:
  ✅ Separate from regular home maintenance
  ✅ Tracked for home cost basis
  ✅ Easy tax deduction tracking
```

## Classification Settings Explained

| Setting | Value | Why |
|---------|-------|-----|
| Exclude from Income | ✅ Yes | Capital purchases are not income |
| Exclude from Expense | ✅ Yes | Tracked separately, not operating costs |
| Exclude from Cash Flow | ❌ No | Real money left your account |

## Automation with Rules

Set up once, apply forever:

**Rule: Auto-Classify Vehicle Purchases**
```
IF Category = "Vehicle Purchase"
OR (Amount < -$5,000 AND Description contains "car|vehicle|auto")
THEN Apply "Capital Expense" classification
```

**Rule: Auto-Classify Large Equipment**
```
IF Category = "Equipment" AND Amount < -$1,000
THEN Apply "Capital Expense" classification
```

## Quick Reference

### What IS a Capital Expense:
- ✅ Vehicle purchase
- ✅ New roof, HVAC, major renovations
- ✅ Computers, business equipment (>$500)
- ✅ Major appliances (refrigerator, washer/dryer)
- ✅ Property down payments
- ✅ Business furniture and fixtures

### What is NOT a Capital Expense:
- ❌ Vehicle maintenance/repairs
- ❌ Home repairs and maintenance
- ❌ Software subscriptions
- ❌ Utilities and insurance
- ❌ Small tools and supplies (<$500)
- ❌ Consumables (gas, office supplies)

## Threshold Guidelines

| User Type | Suggested Threshold |
|-----------|-------------------|
| Personal Finance | $500 - $1,000 |
| Small Business | $1,000 - $2,500 |
| Larger Business | Follow IRS Section 179 |

## Verify It's Working

1. **Check Expense Analysis** (`/analysis/expenses`)
   - Should NOT show capital purchases
   - Clean monthly/quarterly trends

2. **Check Cash Flow** (`/analysis/cashflow`)
   - Should show capital purchases
   - Accurate cash position

3. **Run CapEx Report** (Transactions page)
   - Filter by Classification = "Capital Expense"
   - See all asset purchases

## Tax Time Benefits

✅ Easy to generate CapEx report for accountant
✅ Track depreciable assets automatically
✅ Find Section 179 eligible purchases
✅ Calculate cost basis for property/vehicles
✅ Separate personal vs business assets (using tags)

## Files Reference

- **Full Guide**: `capital-expenses-guide.md` (comprehensive documentation)
- **Setup Script**: `add_capital_expense_classification.py` (one-time setup)
- **This File**: Quick reference and examples

## Need Help?

See the full guide at `capital-expenses-guide.md` for:
- Detailed examples
- Loan financing scenarios
- Depreciation tracking
- Integration with categories and tags
- Best practices
- Future enhancement roadmap

---

**Ready to start?** Run the setup script, create your categories, and start classifying! 🚀
