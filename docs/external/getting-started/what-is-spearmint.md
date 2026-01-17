# What is Spearmint?

**Spearmint is a "Personal CFO" — a self-hosted financial engine that transforms your bank data into professional-grade accounting intelligence.**

## The Problem

For over a decade, Mint.com showed millions of people the value of automated financial tracking. But when it shut down, it revealed a gap in the market: most personal finance apps are designed to *track* spending, not to *manage* wealth.

Current alternatives often fail when life gets complex:

- **A $20,000 home renovation** gets treated the same as a grocery bill — destroying your "monthly spending" chart
- **Work trip reimbursements** count as personal expenses until you remember to exclude them
- **Transfers between your own accounts** get double-counted or create confusion
- **Irregular income** from freelancing or bonuses breaks simple budget assumptions

You need a tool that understands cash flow, capital investments, and forecasting — not just a list of transactions.

## The Solution

Spearmint treats your household finances like a business, giving you the same analytical tools a CFO would use:

### 🏦 True Financial Picture

Separate your **Operating Expenses** (groceries, utilities, subscriptions) from **Capital Investments** (renovations, vehicles, equipment). See your actual monthly "burn rate" without one-time purchases distorting the view.

### 🔄 Smart Relationship Detection

Spearmint automatically detects:
- Transfers between your own accounts
- Credit card payments and their corresponding charges
- Reimbursements (pending money owed to you)

These are excluded from income/expense calculations so your numbers are accurate.

### 📊 Confidence-Based Forecasting

Answer "What if?" questions:
- What if I lose my job next month?
- What's my financial runway?
- How confident am I in that December bonus?

Spearmint provides statistical projections with confidence intervals, not just straight-line guesses.

### 🔐 Your Data, Your Hardware

Everything runs locally via Docker. No monthly fees. No cloud storage limits. No company shutting down and taking your financial history with it.

## Key Differentiators

| Feature | Spearmint | Typical Finance Apps |
|---------|-----------|---------------------|
| **CapEx Separation** | ✅ Toggle any transaction as Capital Expense | ❌ Everything is "spending" |
| **Transfer Detection** | ✅ Auto-detected and excluded from calculations | ⚠️ Manual or inconsistent |
| **Reimbursement Tracking** | ✅ Shadow ledger of money owed to you | ❌ Counted as personal expense |
| **Forecasting** | ✅ Multiple algorithms with confidence intervals | ⚠️ Basic linear projections |
| **Data Ownership** | ✅ Self-hosted, you own everything | ❌ Stored on vendor servers |
| **Cost** | ✅ Free forever (you provide hardware) | ❌ $5-15/month subscriptions |
| **History Limits** | ✅ Unlimited (limited only by your storage) | ❌ Often 1-2 years |

## Who is Spearmint For?

Spearmint is designed for people who:

- **Want control** over their financial data
- **Have complex finances** — investments, rentals, side income, shared expenses
- **Value accuracy** over simplicity
- **Are comfortable** running Docker on a home server or NAS
- **Miss Mint** but want something more powerful

## How It Works

1. **Install** — One `docker-compose up` command gets you running
2. **Import** — Drag and drop your bank CSV/Excel files
3. **Map Once** — Tell Spearmint which columns are Date, Amount, Description
4. **Analyze** — Get instant insights into income, expenses, cash flow
5. **Forecast** — Project your financial future with confidence

---

**Ready to get started?** → [Installation Guide](installation.md)

