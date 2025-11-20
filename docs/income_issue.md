# Income Deep-Dive Analysis Submenu

## Overview

Add a dedicated Income analysis submenu to provide detailed breakdowns and insights into income sources, helping users better understand where their money is coming from.

## Current State

- ✅ Analysis page shows high-level income summary card ($40,475.88 total)
- ✅ Category breakdown shows top income categories with pie chart
- ❌ No way to drill down into individual income transactions
- ❌ No detailed income source analysis
- ❌ Cannot identify data quality issues (e.g., Credit Card Payment showing as income)

## Problem Statement

Users need to:
1. **Understand income sources** - Detailed breakdown by category with transaction lists
2. **Validate data quality** - Identify miscategorized transactions (expenses marked as income)
3. **Track income trends** - See how income sources change over time
4. **Analyze patterns** - Understand regular vs. one-time income

Currently, the high-level summary doesn't provide enough detail to:
- Verify the accuracy of income calculations
- Identify which specific transactions contribute to each category
- Spot anomalies like the $990.48 Credit Card Payment incorrectly categorized as income

## Proposed Solution

### Income Analysis Submenu

Add a new route `/analysis/income` with comprehensive income analysis:

#### 1. Income Overview Section
- **Total Income Card** with period comparison
- **Income Sources Summary** - Count and percentage by category
- **Regular vs. One-time Income** - Recurring income identification
- **Growth Indicators** - Month-over-month, year-over-year changes

#### 2. Category Breakdown
- **Expandable category cards** showing:
  - Category name and icon
  - Total amount and percentage of total income
  - Transaction count
  - Average transaction amount
  - Click to expand → show transaction list

- **Transaction List per Category**:
  - Date, Description, Amount
  - Link to view/edit transaction
  - Highlight suspicious items (e.g., negative amounts, wrong category)

#### 3. Income Trends Chart
- **Time series visualization** (Line/Bar/Area charts)
- **Breakdown by category** - Stacked or grouped views
- **Period selection** - Daily/Weekly/Monthly/Quarterly/Yearly
- **Comparison mode** - Compare different time periods

#### 4. Income Source Analysis
- **Employment Income** - Paychecks, bonuses, reimbursements
- **Investment Income** - Dividends, interest, capital gains
- **Passive Income** - Rental income, royalties
- **Other Income** - Gifts, refunds, miscellaneous

#### 5. Data Quality Indicators
- **Warning badges** for potential issues:
  - ⚠️ Expense categories appearing in income (e.g., "Groceries")
  - ⚠️ Transfer categories in income (e.g., "Credit Card Payment")
  - ⚠️ Unusual amounts (outliers)
  - ⚠️ Uncategorized transactions

#### 6. Export & Actions
- **Export detailed report** (CSV/PDF) with all income transactions
- **Quick actions**:
  - Recategorize transaction
  - Mark as transfer
  - Add notes
  - Link related transactions

### UI/UX Design

```
┌─────────────────────────────────────────────────────────────┐
│ Analysis > Income                                            │
├─────────────────────────────────────────────────────────────┤
│ [Date Range Picker]  [Analysis/Complete Toggle]  [Export]   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 Income Overview                                          │
│  ┌──────────────┬──────────────┬──────────────┬───────────┐ │
│  │ Total Income │ Avg. Monthly │ Income       │ Growth    │ │
│  │ $43,040      │ $14,347      │ Sources: 7   │ +5.2%     │ │
│  └──────────────┴──────────────┴──────────────┴───────────┘ │
│                                                               │
│  📈 Income Trend                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │         [Line Chart: Income by Category Over Time]      │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  📂 Income by Category                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ▶ Yahoo Net Pay                    $17,956 (39.9%)  [>] │ │
│  │ ▶ Rental Income                     $8,122 (18.0%)  [>] │ │
│  │ ▶ Postman Net Pay                   $9,767 (21.7%)  [>] │ │
│  │ ▶ Dividends                         $7,527 (16.7%)  [>] │ │
│  │ ⚠️ ▶ Credit Card Payment ⚠️           $990  (2.2%)  [>] │ │
│  │ ⚠️ ▶ Groceries ⚠️                       $8  (0.0%)  [>] │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  When expanded:                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ ▼ Yahoo Net Pay                    $17,956 (39.9%)      │ │
│  │   ┌───────────────────────────────────────────────────┐ │ │
│  │   │ 2025-09-26  Payroll          $12,027.56  [Edit]  │ │ │
│  │   │ 2025-09-12  Payroll           $5,928.53  [Edit]  │ │ │
│  │   └───────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Technical Implementation

### Frontend Components

```
frontend/src/components/Analysis/Income/
├── IncomeDeepDivePage.tsx          # Main income analysis page
├── IncomeOverviewCards.tsx         # Summary statistics cards
├── IncomeTrendChart.tsx            # Time series chart
├── IncomeCategoryList.tsx          # Expandable category list
├── IncomeCategoryItem.tsx          # Individual category card
├── IncomeTransactionList.tsx       # Transaction list per category
├── IncomeSourceBreakdown.tsx       # Employment/Investment/Passive breakdown
└── DataQualityWarnings.tsx         # Data quality indicators
```

### API Endpoints (Already Exist)

- ✅ `GET /api/analysis/income` - Income analysis with category breakdown
- ✅ `GET /api/analysis/cashflow/trends` - Trend data
- ✅ `GET /api/transactions` - Transaction list with filtering

### New Features Needed

1. **Transaction Grouping** - Group transactions by income source type
2. **Anomaly Detection** - Flag suspicious income transactions
3. **Recategorization API** - Quick-edit transaction categories
4. **Income Pattern Recognition** - Identify regular vs. irregular income

## Navigation

Add submenu items under Analysis:

```
Analysis
├── Overview (current /analysis page)
├── Income → /analysis/income (NEW)
├── Expenses → /analysis/expenses (Future)
└── Cash Flow → /analysis/cashflow (Future)
```

## Success Criteria

- [ ] Users can navigate to `/analysis/income` from Analysis page
- [ ] Income overview shows total, averages, and key metrics
- [ ] Category breakdown is expandable to show transactions
- [ ] Data quality warnings highlight miscategorized items
- [ ] Trend chart visualizes income over time by category
- [ ] Export functionality generates detailed income report
- [ ] Quick actions allow recategorization without leaving page
- [ ] Responsive design works on mobile/tablet/desktop

## Out of Scope (Future Enhancements)

- Predictive income forecasting
- Income goal tracking
- Tax category grouping
- Multi-currency support

## Dependencies

- ✅ Analysis API endpoints (already implemented)
- ✅ Chart components (already implemented)
- ❌ Transaction recategorization API (needs implementation)
- ❌ Data quality validation rules (needs implementation)

## Related Issues

- Related to #10 (Phase 5: Frontend Features)
- Follows Task 2: Analysis & Reports Components (completed)
- May require data cleanup for existing miscategorized transactions

## Implementation Estimate

- **Frontend Development:** 2-3 days
- **API Enhancements:** 1 day
- **Testing & Polish:** 1 day
- **Total:** 4-5 days

## Priority

**High** - Directly addresses user need to validate income calculations and understand income sources
