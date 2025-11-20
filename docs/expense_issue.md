# Expense Deep-Dive Analysis Submenu

## Overview

Add a dedicated Expense analysis submenu to provide detailed breakdowns and insights into spending patterns, helping users better understand where their money is going and identify opportunities for savings.

## Current State

- ✅ Analysis page shows high-level expense summary card
- ✅ Category breakdown shows top expense categories with pie chart
- ❌ No way to drill down into individual expense transactions
- ❌ No detailed spending pattern analysis
- ❌ Cannot identify unusual spending or data quality issues
- ❌ No ability to compare spending across time periods

## Problem Statement

Users need to:
1. **Understand spending patterns** - Detailed breakdown by category with transaction lists
2. **Validate data quality** - Identify miscategorized transactions (income marked as expenses)
3. **Track spending trends** - See how expenses change over time by category
4. **Identify savings opportunities** - Find high-spend categories and unusual transactions
5. **Budget tracking** - Compare actual spending against expected patterns

Currently, the high-level summary doesn't provide enough detail to:
- Verify the accuracy of expense calculations
- Identify which specific transactions contribute to each category
- Spot unusual spending patterns or anomalies
- Compare spending across different time periods
- Find recurring expenses that could be optimized

## Proposed Solution

### Expense Analysis Submenu

Add a new route `/analysis/expenses` with comprehensive expense analysis:

#### 1. Expense Overview Section
- **Total Expenses Card** with period comparison
- **Spending Categories Summary** - Count and percentage by category
- **Fixed vs. Variable Expenses** - Recurring vs. one-time spending
- **Top Spending Categories** - Highest expense categories
- **Spending Velocity** - Average daily/weekly/monthly burn rate
- **Comparison Metrics** - vs. previous period, vs. same period last year

#### 2. Category Breakdown
- **Expandable category cards** showing:
  - Category name and icon
  - Total amount and percentage of total expenses
  - Transaction count
  - Average transaction amount
  - Trend indicator (up/down vs. previous period)
  - Click to expand → show transaction list

- **Transaction List per Category**:
  - Date, Description, Amount
  - Payment method
  - Link to view/edit transaction
  - Highlight unusual items (outliers, duplicates, high amounts)
  - Quick actions (recategorize, split, mark as transfer)

#### 3. Expense Trends Chart
- **Time series visualization** (Line/Bar/Area/Stacked charts)
- **Breakdown by category** - Show spending composition over time
- **Period selection** - Daily/Weekly/Monthly/Quarterly/Yearly
- **Comparison mode** - Compare current vs. previous period
- **Cumulative view** - Track spending accumulation over period

#### 4. Spending Analysis
- **Essential vs. Discretionary** - Categorize by necessity
  - Essential: Housing, utilities, groceries, transportation, insurance
  - Discretionary: Dining, entertainment, shopping, travel

- **Fixed vs. Variable**:
  - Fixed: Rent, subscriptions, insurance (recurring, predictable)
  - Variable: Groceries, gas, utilities (recurring, fluctuating)
  - One-time: Repairs, purchases, medical

- **Payment Method Breakdown**:
  - Credit card
  - Debit card
  - Cash
  - Check
  - Transfer

#### 5. Spending Insights
- **Top Merchants** - Where you spend the most
- **Recurring Expenses** - Subscriptions and regular bills
- **Unusual Transactions** - Outliers and anomalies
- **Spending Patterns**:
  - Day of week analysis (Do you spend more on weekends?)
  - Time of month analysis (Beginning vs. end of month)
  - Seasonal patterns

#### 6. Data Quality Indicators
- **Warning badges** for potential issues:
  - ⚠️ Income categories appearing in expenses
  - ⚠️ Transfer categories in expenses (e.g., "Transfer to Savings")
  - ⚠️ Duplicate transactions (same amount, date, merchant)
  - ⚠️ Unusual amounts (outliers, very high/low)
  - ⚠️ Uncategorized transactions
  - ⚠️ Missing or vague descriptions

#### 7. Spending Goals & Budgets
- **Category budget tracking** (if budgets are set)
- **Spending alerts** - Approaching or exceeding budget
- **Savings opportunities** - Categories with highest potential for reduction
- **Spending efficiency score** - Overall financial health metric

#### 8. Export & Actions
- **Export detailed report** (CSV/PDF) with all expense transactions
- **Filter & search**:
  - By category, merchant, amount range
  - By date range
  - By payment method
  - By keywords in description
- **Quick actions**:
  - Recategorize transaction
  - Split transaction (e.g., grocery bill with household items)
  - Mark as transfer
  - Add notes
  - Flag for review

### UI/UX Design

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Analysis > Expenses                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ [Date Range Picker]  [Analysis/Complete Toggle]  [Filter]  [Export]     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  💰 Expense Overview                                                     │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┬────────┐ │
│  │ Total        │ Avg. Daily   │ Top Category │ Fixed vs Var │ Change │ │
│  │ Expenses     │ Spending     │              │              │        │ │
│  │ $8,245       │ $274.83      │ Groceries    │ 60% / 40%    │ -2.3%  │ │
│  └──────────────┴──────────────┴──────────────┴──────────────┴────────┘ │
│                                                                           │
│  📊 Spending Breakdown                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │  [Pie Chart]           [Bar Chart: Top 10 Categories]               │ │
│  │  Essential: 65%        Groceries    ████████████  $1,450            │ │
│  │  Discretionary: 35%    Utilities    ████████      $980              │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  📈 Expense Trend                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │         [Stacked Area Chart: Expenses by Category Over Time]        │ │
│  │  [Toggle: Line / Bar / Area / Stacked]  [Period: Monthly ▼]         │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  📂 Expenses by Category                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ ▶ Groceries                        $1,450 (17.6%)  ↑5.2%  [35 txn] │ │
│  │ ▶ Utilities                          $980 (11.9%)  ↓2.1%  [12 txn] │ │
│  │ ▶ Dining & Restaurants               $875 (10.6%)  ↑12%   [28 txn] │ │
│  │ ▶ Transportation                     $650  (7.9%)  →0.0%  [15 txn] │ │
│  │ ▶ Entertainment                      $420  (5.1%)  ↑8.5%  [10 txn] │ │
│  │ ⚠️ ▶ Uncategorized ⚠️                  $145  (1.8%)         [8 txn] │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  When expanded:                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ ▼ Groceries                        $1,450 (17.6%)  ↑5.2%  [35 txn] │ │
│  │   [Search] [Filter by merchant] [Sort by: Date ▼]                   │ │
│  │   ┌─────────────────────────────────────────────────────────────┐   │ │
│  │   │ 2025-10-02  Whole Foods Market     $127.45  💳 Credit  [Edit]│   │ │
│  │   │ 2025-09-30  Trader Joe's            $89.23  💳 Credit  [Edit]│   │ │
│  │   │ 2025-09-28  Costco                 $234.56  💳 Debit   [Edit]│   │ │
│  │   │ 2025-09-25  Safeway                 $45.67  💵 Cash    [Edit]│   │ │
│  │   │ ... (show more) ...                                           │   │ │
│  │   └─────────────────────────────────────────────────────────────┘   │ │
│  │   📊 Merchant Breakdown:                                             │ │
│  │   - Whole Foods: $450 (31%)   - Costco: $380 (26%)                  │ │
│  │   - Trader Joe's: $320 (22%)  - Safeway: $300 (21%)                 │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
│                                                                           │
│  💡 Spending Insights                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐ │
│  │ • You spent 12% more on Dining this month                           │ │
│  │ • 3 potential duplicate transactions found                          │ │
│  │ • Your utility bills are 15% lower than last month                  │ │
│  │ • 8 uncategorized transactions need review                          │ │
│  └─────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

### Frontend Components

```
frontend/src/components/Analysis/Expenses/
├── ExpenseDeepDivePage.tsx           # Main expense analysis page
├── ExpenseOverviewCards.tsx          # Summary statistics cards
├── ExpenseTrendChart.tsx             # Time series chart with multiple views
├── ExpenseCategoryList.tsx           # Expandable category list
├── ExpenseCategoryItem.tsx           # Individual category card
├── ExpenseTransactionList.tsx        # Transaction list per category
├── SpendingBreakdownCharts.tsx       # Pie/Bar charts for breakdown
├── SpendingInsights.tsx              # AI-generated insights
├── MerchantAnalysis.tsx              # Top merchants within category
├── DataQualityWarnings.tsx           # Data quality indicators
├── ExpenseFilters.tsx                # Advanced filtering options
└── SpendingPatterns.tsx              # Pattern analysis (day/time/seasonal)
```

### API Endpoints

**Already Exist:**
- ✅ `GET /api/analysis/expenses` - Expense analysis with category breakdown
- ✅ `GET /api/analysis/cashflow/trends` - Trend data
- ✅ `GET /api/transactions` - Transaction list with filtering

**May Need Enhancements:**
- `GET /api/analysis/expenses/trends` - Time series by category
- `GET /api/analysis/expenses/merchants` - Top merchants analysis
- `GET /api/analysis/expenses/patterns` - Spending pattern detection
- `GET /api/analysis/expenses/insights` - AI-generated insights
- `GET /api/analysis/expenses/recurring` - Recurring expense detection

### New Features Needed

1. **Advanced Transaction Filtering** - Multi-criteria filtering and search
2. **Anomaly Detection** - Flag suspicious or unusual expense transactions
3. **Duplicate Detection** - Identify potential duplicate expenses
4. **Merchant Extraction** - Parse and group by merchant from descriptions
5. **Pattern Recognition** - Identify spending patterns (day of week, time of month)
6. **Spending Insights** - Generate actionable insights from data
7. **Budget Comparison** - Compare actual vs. budget (if budgets exist)

## Navigation

Update Analysis submenu:

```
Analysis
├── Overview (current /analysis page)
├── Income → /analysis/income
├── Expenses → /analysis/expenses (NEW)
└── Cash Flow → /analysis/cashflow (Future)
```

## Success Criteria

- [ ] Users can navigate to `/analysis/expenses` from Analysis page
- [ ] Expense overview shows total, averages, and key metrics
- [ ] Category breakdown is expandable to show transactions
- [ ] Transaction lists are searchable and filterable
- [ ] Data quality warnings highlight miscategorized items
- [ ] Trend chart visualizes spending over time by category
- [ ] Merchant analysis shows top vendors per category
- [ ] Spending insights provide actionable recommendations
- [ ] Export functionality generates detailed expense report
- [ ] Quick actions allow recategorization without leaving page
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Performance is optimized for large transaction sets (100+ per category)

## User Stories

1. **As a user**, I want to see which grocery stores I spend the most at, so I can optimize where I shop
2. **As a user**, I want to identify duplicate transactions, so I can dispute or remove them
3. **As a user**, I want to see my spending patterns by day of week, so I can understand when I spend most
4. **As a user**, I want to compare this month's dining expenses to last month, so I can track my progress
5. **As a user**, I want to find all uncategorized transactions, so I can properly categorize them
6. **As a user**, I want to see which expense categories increased the most, so I can focus on reducing them

## Out of Scope (Future Enhancements)

- Budget creation and management (separate feature)
- Predictive expense forecasting
- Spending goal tracking
- Receipt attachment and OCR
- Tax category grouping
- Bill negotiation recommendations
- Subscription management and cancellation

## Dependencies

- ✅ Analysis API endpoints (already implemented)
- ✅ Chart components (already implemented)
- ❌ Merchant extraction/parsing logic (needs implementation)
- ❌ Pattern detection algorithms (needs implementation)
- ❌ Duplicate detection logic (needs implementation)
- ❌ Transaction recategorization API (needs implementation)
- ❌ Advanced filtering backend support (needs implementation)

## Related Issues

- Related to #10 (Phase 5: Frontend Features)
- Related to #12 (Income Deep-Dive) - Similar pattern
- Follows Task 2: Analysis & Reports Components (completed)
- May require data cleanup for existing miscategorized transactions

## Implementation Estimate

- **Frontend Development:** 3-4 days
- **API Enhancements:** 1-2 days
- **Pattern Detection Logic:** 1 day
- **Testing & Polish:** 1 day
- **Total:** 6-8 days

## Priority

**High** - Critical for understanding spending patterns and identifying savings opportunities

## Acceptance Criteria

1. Expense deep-dive page accessible from Analysis menu
2. Overview cards show key expense metrics
3. Category breakdown displays all expense categories with totals
4. Each category is expandable to show transaction list
5. Transaction lists support search and filtering
6. Trend chart shows spending over time with multiple visualization options
7. Data quality warnings highlight issues
8. Merchant analysis groups transactions by vendor
9. Export generates comprehensive CSV with all expense data
10. Page loads and renders within 2 seconds for datasets up to 1000 transactions
