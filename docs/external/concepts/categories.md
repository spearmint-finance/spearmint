# Categories

Categories answer the question: *What kind of spending is this?*

While [Classifications](classifications.md) control how transactions affect your math, Categories help you understand *where* your money goes.

## Category Hierarchy

Categories in Spearmint can be nested, allowing detailed or high-level views:

```
Food & Dining
├── Groceries
├── Restaurants
├── Coffee Shops
└── Fast Food

Transportation
├── Gas
├── Public Transit
├── Ride Share
└── Parking

Housing
├── Rent/Mortgage
├── Utilities
├── Maintenance
└── Insurance
```

You can analyze at any level:
- "How much did I spend on **Food & Dining**?" → $800
- "How much specifically on **Groceries**?" → $450

## Default Categories

Spearmint comes with common categories pre-configured:

| Parent | Subcategories |
|--------|--------------|
| Income | Salary, Freelance, Interest, Dividends, Refunds |
| Food & Dining | Groceries, Restaurants, Coffee, Fast Food |
| Transportation | Gas, Public Transit, Parking, Ride Share |
| Housing | Rent/Mortgage, Utilities, Insurance, Maintenance |
| Shopping | Clothing, Electronics, Home Goods, Gifts |
| Entertainment | Streaming, Movies, Games, Hobbies |
| Health | Medical, Pharmacy, Gym, Personal Care |
| Travel | Flights, Hotels, Car Rental, Activities |
| Bills & Utilities | Phone, Internet, Subscriptions |
| Financial | Fees, Interest, Investments |

## Custom Categories

Create categories that match your life:

1. Navigate to **Categories** in settings
2. Click **Add Category**
3. Enter:
   - **Name** — e.g., "Dog Expenses"
   - **Parent** — Optional, to nest under another category
   - **Icon** — Optional visual identifier
4. Save

Your custom categories work exactly like built-in ones.

## Automatic Categorization

Spearmint can automatically assign categories based on patterns:

### Categorization Rules

| Pattern | Category | Example Matches |
|---------|----------|-----------------|
| `KROGER`, `PUBLIX`, `WHOLE FOODS` | Groceries | "KROGER #1234" |
| `SHELL`, `EXXON`, `BP` | Gas | "SHELL OIL 12345" |
| `NETFLIX`, `SPOTIFY`, `HULU` | Streaming | "NETFLIX.COM" |
| `UBER`, `LYFT` | Ride Share | "UBER TRIP" |

### Rule Priority

When multiple rules could match, the highest-priority rule wins. This lets you create:
- General rules (low priority): `AMAZON` → Shopping
- Specific rules (high priority): `AMAZON FRESH` → Groceries

## Uncategorized Transactions

Transactions without a matching rule are marked **Uncategorized**. Spearmint highlights these for your attention:

1. Review uncategorized transactions periodically
2. Assign categories manually, or
3. Create new rules to handle them automatically in the future

## Category Reports

Once categorized, you can:

### View Spending by Category
See a breakdown of where money goes:
- Pie chart of spending distribution
- Bar chart comparisons over time
- Drill-down from parent to child categories

### Track Trends
How does this month's "Restaurants" compare to last month? Last year?

### Set Budgets (Coming Soon)
Assign spending limits to categories and track progress.

## Tips for Effective Categorization

### Keep It Simple
Start with broad categories. Add detail only where it provides insight.

### Be Consistent
Decide once how to categorize edge cases. Is Costco "Groceries" or "Shopping"? Pick one and stick with it.

### Review Regularly
Spend 5 minutes weekly reviewing new transactions. Create rules for patterns you see.

---

**Related:**
- [Classifications](classifications.md) — How transactions affect math
- [Reporting](../features/reporting.md) — Category-based reports

