# Forecasting

Spearmint's forecasting engine helps you answer "What if?" questions about your financial future.

## Why Forecasting Matters

Knowing your current balance is useful. Knowing where you'll be in 6 months is powerful:

- "How long until I run out of money if I lose my job?"
- "Can I afford this purchase and still hit my savings goal?"
- "What's my financial runway?"

## Projection Basics

Spearmint analyzes your historical data to project future income and expenses:

### What It Considers
- **Income patterns** — Regular salary, irregular freelance, dividends
- **Expense patterns** — Monthly bills, seasonal spending, one-time purchases
- **Trends** — Are expenses growing? Is income stable?

### What It Produces
- **Projected income** — Expected future income
- **Projected expenses** — Expected future spending
- **Net cash flow projection** — Income minus expenses
- **Balance projection** — Where your balances will be

## Projection Methods

Spearmint offers multiple forecasting algorithms:

| Method | Best For | How It Works |
|--------|----------|--------------|
| **Linear Regression** | Stable trends | Fits a trend line to your data |
| **Moving Average** | Smoothing noise | Averages recent periods |
| **Exponential Smoothing** | Recent data matters more | Weighted average favoring recent |
| **Weighted Average** | General use | Configurable weights by period |

### Choosing a Method

- **Stable salary, predictable expenses?** → Linear Regression
- **Variable income, want to smooth?** → Moving Average
- **Recent changes matter most?** → Exponential Smoothing
- **Want control over weighting?** → Weighted Average

## Confidence Intervals

Projections aren't guarantees — they're educated guesses. Spearmint shows confidence intervals:

```
                    Expected Case
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
Best Case            Your Path          Worst Case
  (+15%)                                  (-15%)
```

### Interpreting Confidence

| Scenario | Meaning |
|----------|---------|
| **Best Case** | If things go better than average |
| **Expected** | Most likely outcome based on history |
| **Worst Case** | If things go worse than average |

The width of the interval reflects uncertainty. Highly variable income = wider intervals.

## Scenarios

Create custom scenarios to model different futures:

### Creating a Scenario

1. Navigate to **Projections → Scenarios**
2. Click **Create Scenario**
3. Name it (e.g., "Job Loss", "New Baby", "Retirement")
4. Add adjusters

### Adjusters

Adjusters modify the baseline projection:

| Adjuster Type | Example |
|---------------|---------|
| **Income Change** | "Salary drops 50% starting July" |
| **Expense Change** | "Add $500/month for childcare" |
| **One-time Event** | "Receive $10,000 bonus in December" |
| **Recurring Change** | "Cancel $200/month subscriptions" |

### Comparing Scenarios

View multiple scenarios side-by-side:
- Current trajectory vs job loss
- With renovation vs without
- Early retirement vs working longer

## Projection Horizon

Forecast different time frames:

| Horizon | Use Case |
|---------|----------|
| **3 months** | Near-term planning |
| **6 months** | Medium-term decisions |
| **12 months** | Annual planning |
| **24+ months** | Long-term goals |

Longer horizons have more uncertainty (wider confidence intervals).

## Accuracy Metrics

Spearmint tracks how accurate past projections were:

| Metric | Description |
|--------|-------------|
| **MAPE** | Mean Absolute Percentage Error |
| **RMSE** | Root Mean Square Error |
| **MAE** | Mean Absolute Error |
| **R²** | How well the model fits your data |

Lower error = more reliable projections. If accuracy is low, consider:
- Using a different projection method
- Providing more historical data
- Accepting wider confidence intervals

## Financial Runway

A key output: **How long can you sustain your current lifestyle?**

```
Monthly Expenses: $5,000
Current Savings: $60,000

Runway: 12 months

At current trajectory:
  6 months → $30,000 remaining
  12 months → $0 remaining
```

This is your emergency fund in months, not dollars.

## Using Forecasts Effectively

### Regular Review
Check projections monthly. Are they tracking reality?

### Update After Big Changes
New job? Major purchase? Rerun projections with fresh data.

### Don't Over-Optimize
Forecasts are guides, not guarantees. Use them for direction, not precision.

---

**Related:**
- [Cash Flow Analysis](cash-flow-analysis.md) — Current state analysis
- [CapEx vs OpEx](../concepts/capex-vs-opex.md) — Exclude one-time investments from projections

