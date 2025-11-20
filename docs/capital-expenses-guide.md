# Capital Expenses (CapEx) Handling Guide

## Overview

Capital expenses are significant purchases of physical assets that provide long-term value (typically >1 year). Unlike regular operating expenses that are consumed within a year, capital expenses require special accounting treatment to accurately reflect your financial position.

## What are Capital Expenses?

**Capital Expenses (CapEx)** include:
- Real estate purchases (house, land, rental properties)
- Vehicles (cars, trucks, motorcycles)
- Major home improvements (roof replacement, HVAC system, addition)
- Business equipment (computers, machinery, furniture)
- Technology infrastructure (servers, network equipment)
- Large appliances with multi-year lifespan

**NOT Capital Expenses** (Operating Expenses):
- Regular maintenance and repairs
- Utility bills
- Groceries and consumables
- Insurance premiums
- Subscriptions and services
- Small repairs (<$500 typically)

## Current System Capabilities

The financial analysis system **already has the infrastructure** to handle capital expenses through the **Transaction Classification System**. Here's what exists:

### Available Classification Types

Based on your current database, you have these relevant classifications:

1. **Regular Transaction** (`REGULAR`) - Normal income/expenses
2. **Internal Transfer** (`TRANSFER`) - Moving money between accounts
3. **Loan Disbursement** (`LOAN_DISB`) - Receiving loan money
4. **Loan Payment - Principal** (`LOAN_PRINCIPAL`) - Loan principal payments
5. **Loan Payment - Interest** (`LOAN_INTEREST`) - Loan interest payments

### Classification Exclusion Flags

Each classification has three exclusion flags:
- `exclude_from_income_calc` - Exclude from income analysis
- `exclude_from_expense_calc` - Exclude from expense analysis
- `exclude_from_cashflow_calc` - Exclude from cash flow analysis

## Recommended Approach: Create Capital Expense Classification

### Option 1: Simple Approach (Recommended for Most Users)

**Create a new classification type for Capital Expenses:**

```sql
-- Create Capital Expense classification
INSERT INTO transaction_classifications (
    classification_name,
    classification_code,
    description,
    exclude_from_income_calc,
    exclude_from_expense_calc,
    exclude_from_cashflow_calc,
    is_system_classification,
    created_at,
    updated_at
) VALUES (
    'Capital Expense',
    'CAPITAL_EXPENSE',
    'What it is: Large purchase of assets with multi-year lifespan (vehicles, equipment, property improvements)

When to use: For significant asset purchases typically >$500-1000 that provide value for multiple years

Include/Exclude logic:
- Income calculation: EXCLUDED (not income)
- Expense calculation: EXCLUDED (not operating expense, tracked separately as CapEx)
- Cash flow calculation: INCLUDED (real cash outflow)',
    true,  -- exclude from income (it's not income)
    true,  -- exclude from regular expense analysis (track separately)
    false, -- include in cash flow (real money was spent)
    false, -- user-created classification
    datetime('now'),
    datetime('now')
);
```

**Benefits:**
- Capital expenses show in cash flow (where money actually moved)
- Excluded from regular expense analysis (prevents distortion of monthly spending)
- Can run separate reports for CapEx vs OpEx
- Easy to track asset purchases separately

### Option 2: Advanced Approach (For Business/Investment Properties)

**Create multiple classification types for different capital expense categories:**

```sql
-- Property Capital Expense
INSERT INTO transaction_classifications (
    classification_name,
    classification_code,
    description,
    exclude_from_income_calc,
    exclude_from_expense_calc,
    exclude_from_cashflow_calc,
    is_system_classification
) VALUES (
    'Property CapEx',
    'PROPERTY_CAPEX',
    'Property purchases and major improvements (roof, HVAC, additions, renovations)',
    true, true, false, false
);

-- Vehicle Capital Expense
INSERT INTO transaction_classifications (
    classification_name,
    classification_code,
    description,
    exclude_from_income_calc,
    exclude_from_expense_calc,
    exclude_from_cashflow_calc,
    is_system_classification
) VALUES (
    'Vehicle CapEx',
    'VEHICLE_CAPEX',
    'Vehicle purchases and major repairs/upgrades',
    true, true, false, false
);

-- Equipment Capital Expense
INSERT INTO transaction_classifications (
    classification_name,
    classification_code,
    description,
    exclude_from_income_calc,
    exclude_from_expense_calc,
    exclude_from_cashflow_calc,
    is_system_classification
) VALUES (
    'Equipment CapEx',
    'EQUIPMENT_CAPEX',
    'Business equipment, computers, machinery, tools, furniture',
    true, true, false, false
);
```

**Benefits:**
- More granular tracking of different asset types
- Easier to run category-specific depreciation analysis
- Better for businesses with diverse asset classes

## How to Use Capital Expense Classifications

### Step 1: Create the Classification

Use the Classification Management UI or run the SQL above to create your capital expense classification(s).

### Step 2: Categorize Your Capital Transactions

For each capital expense transaction:

1. **Transaction Category**: Create or use categories like:
   - `Vehicle Purchase`
   - `Home Improvement`
   - `Equipment`
   - `Property Investment`

2. **Transaction Classification**: Apply your new `Capital Expense` classification

3. **Example Transaction**:
   ```
   Date: 2025-09-15
   Description: New MacBook Pro 16" for business
   Amount: -$3,499.00
   Type: Expense
   Category: Equipment
   Classification: Capital Expense
   ```

### Step 3: Create Classification Rules for Automation

Set up rules to automatically classify future capital expenses:

**Example Rule 1: Vehicle Purchases**
```
Rule Name: Auto Classify Vehicle Purchases
Match Conditions:
  - Category = "Vehicle Purchase"
  - OR Amount < -$5,000 AND Description contains "car|vehicle|auto|truck"
Action: Apply "Capital Expense" classification
```

**Example Rule 2: Large Equipment**
```
Rule Name: Auto Classify Large Equipment
Match Conditions:
  - Category = "Equipment"
  - AND Amount < -$1,000
Action: Apply "Capital Expense" classification
```

### Step 4: Analyze Capital vs Operating Expenses

The system will now properly segregate your expenses:

**In Analysis Mode:**
- **Regular Expenses**: Operating expenses only (monthly bills, groceries, etc.)
- **Capital Expenses**: Excluded from expense trends (prevents distortion)
- **Cash Flow**: Shows both (actual money movement)

**Reports You Can Generate:**

1. **Operating Expense Analysis** (`/analysis/expenses`)
   - Shows only regular operating expenses
   - Clean trend analysis without capital purchases
   - Accurate monthly/quarterly spending patterns

2. **Cash Flow Analysis** (`/analysis/cashflow`)
   - Shows all money movement including CapEx
   - Identifies months with large asset purchases
   - True picture of cash position

3. **Capital Expense Report** (Custom Query)
   ```sql
   SELECT
       DATE(transaction_date) as purchase_date,
       description,
       amount,
       category_name
   FROM transactions t
   LEFT JOIN categories c ON t.category_id = c.category_id
   LEFT JOIN transaction_classifications tc ON t.classification_id = tc.classification_id
   WHERE tc.classification_code = 'CAPITAL_EXPENSE'
   ORDER BY transaction_date DESC;
   ```

## Handling Related Transactions

### Financed Capital Purchases

When you buy a capital asset with a loan, you'll have multiple related transactions:

**Example: Car Purchase with Auto Loan**

1. **Asset Purchase (Capital Expense)**
   ```
   Date: 2025-09-15
   Description: 2025 Toyota Camry
   Amount: -$35,000
   Type: Expense
   Category: Vehicle Purchase
   Classification: Capital Expense
   ```

2. **Loan Disbursement (Cash Inflow)**
   ```
   Date: 2025-09-15
   Description: Auto Loan - Toyota Financing
   Amount: +$28,000
   Type: Income
   Category: Loan Received
   Classification: Loan Disbursement
   ```

3. **Down Payment (Your Money)**
   ```
   Net cash flow: -$35,000 + $28,000 = -$7,000 (your down payment)
   ```

4. **Monthly Loan Payments (Future)**
   ```
   Monthly Payment: -$520
   Principal Portion: Classification = "Loan Payment - Principal"
   Interest Portion: Classification = "Loan Payment - Interest"
   ```

**Result:**
- Capital expense tracked: $35,000 asset
- Operating expense impact: Only interest (~$120/month)
- Cash flow impact: Down payment ($7,000) + monthly payments ($520)

### Down Payments and Deposits

For large purchases requiring down payments:

```
Transaction 1 (Down Payment):
  Description: Down payment for new roof
  Amount: -$2,000
  Classification: Capital Expense

Transaction 2 (Final Payment):
  Description: Final payment for new roof
  Amount: -$8,000
  Classification: Capital Expense

Total CapEx: $10,000
```

## Best Practices

### 1. Set a Threshold
Decide on a minimum amount for capital expenses:
- **Personal**: $500-$1,000
- **Small Business**: $1,000-$2,500
- **Larger Business**: Follow IRS Section 179 limits

### 2. Document Assets
Add detailed notes to capital expense transactions:
- Serial numbers (equipment)
- VIN (vehicles)
- Property address (real estate)
- Purchase date and warranty info
- Expected useful life

### 3. Track Depreciation (Optional)
For tax purposes, track depreciation separately:
- IRS Section 179 immediate expensing
- MACRS depreciation schedules
- Straight-line depreciation for simplicity

### 4. Review Annually
At year-end, review all capital expenses:
- Verify classifications are correct
- Generate CapEx report for tax prep
- Update asset register
- Calculate depreciation

## Integration with Existing Features

### Categories
Create specific categories for asset types:
- `Vehicle Purchase`
- `Home Improvement - Major`
- `Business Equipment`
- `Property Investment`
- `Technology Assets`

### Tags
Use tags for additional tracking:
- `tax-deductible`
- `depreciable`
- `business-asset`
- `rental-property`
- `section-179`

### Transaction Relationships
Link related transactions:
- Purchase → Loan Disbursement
- Down Payment → Final Payment
- Asset Sale → Original Purchase

## Future Enhancements

### Phase 1 (Current - Manual)
✅ Create capital expense classifications
✅ Manually categorize transactions
✅ Use existing analysis tools

### Phase 2 (Future Enhancement)
- Dedicated CapEx dashboard
- Asset register with depreciation tracking
- Automatic depreciation calculations
- Cost basis tracking for assets
- Disposal/sale tracking

### Phase 3 (Advanced)
- Integration with accounting software
- Tax form generation (4562, Schedule C)
- Asset lifecycle management
- ROI analysis per asset
- Lease vs buy analysis

## Example Scenarios

### Scenario 1: Home Office Setup

**Purchases:**
```
Desk:           -$800   → Classification: Capital Expense
Chair:          -$650   → Classification: Capital Expense
Monitor:        -$450   → Classification: Capital Expense
Keyboard/Mouse: -$150   → Classification: Regular Transaction
Total CapEx: $1,900
Total OpEx: $150
```

**Result:**
- Expense analysis shows $150 (ongoing operating costs)
- Cash flow shows -$2,050 (actual money spent)
- Capital expense report shows $1,900 in assets acquired

### Scenario 2: Rental Property Maintenance

**Transactions:**
```
New HVAC System:        -$8,500  → Classification: Capital Expense (Property CapEx)
Filter Replacement:     -$45     → Classification: Regular Transaction
Annual Inspection:      -$150    → Classification: Regular Transaction
Roof Replacement:       -$12,000 → Classification: Capital Expense (Property CapEx)

Total CapEx: $20,500
Total OpEx: $195/year
```

**Result:**
- Operating expenses: $195 (normal maintenance)
- Capital improvements: $20,500 (increase property value)
- Depreciation eligible: $20,500 over 27.5 years (residential rental)

### Scenario 3: Business Vehicle

**Purchase & Ongoing Costs:**
```
Vehicle Purchase:       -$45,000 → Classification: Capital Expense (Vehicle CapEx)
Trade-in Credit:        +$15,000 → Classification: Regular Transaction (Income)
Sales Tax:              -$3,000  → Classification: Capital Expense
Registration:           -$350    → Classification: Regular Transaction (Expense)
Insurance (annual):     -$1,800  → Classification: Regular Transaction (Expense)
Gas (monthly avg):      -$200    → Classification: Regular Transaction (Expense)
Maintenance (annual):   -$800    → Classification: Regular Transaction (Expense)

Net CapEx: $33,000 (depreciable)
Annual OpEx: $5,350 ($445/month)
```

## Summary

**Key Takeaways:**

1. ✅ **Current system supports capital expenses** via classifications
2. ✅ **Create a "Capital Expense" classification** with proper exclusion flags
3. ✅ **Exclude from expense analysis** to prevent distortion of operating costs
4. ✅ **Include in cash flow** to track actual money movement
5. ✅ **Use categories and tags** for granular tracking
6. ✅ **Set up classification rules** for automatic handling

This approach gives you clean operating expense trends while maintaining accurate cash flow records and proper capital expense tracking for tax purposes.

## Implementation Checklist

- [ ] Create Capital Expense classification type(s)
- [ ] Create asset-specific categories (Vehicle Purchase, Equipment, etc.)
- [ ] Set up classification rules for automation
- [ ] Reclassify existing capital purchases
- [ ] Document capital expense threshold policy
- [ ] Create tags for tax tracking (depreciable, section-179, etc.)
- [ ] Test expense analysis to verify exclusion
- [ ] Test cash flow to verify inclusion
- [ ] Generate year-end capital expense report
- [ ] Share with accountant for tax preparation

---

**Need Help?** Check the Classification Management UI at `/classifications` to create and manage your classification types.
