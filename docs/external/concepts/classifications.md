# Classifications

Classifications are the secret sauce that makes Spearmint's financial calculations accurate. They tell Spearmint *how* a transaction should affect your numbers.

## The Problem Classifications Solve

Consider these scenarios:

| Transaction | Amount | Is it really an expense? |
|-------------|--------|-------------------------|
| Grocery shopping | $150 | ✅ Yes |
| Credit card payment | $2,000 | ❌ No — you already counted the charges |
| Transfer to savings | $500 | ❌ No — money is still yours |
| Work trip hotel | $400 | ⚠️ Sort of — you'll be reimbursed |
| Kitchen renovation | $15,000 | ⚠️ Debatable — it's an investment |

If you count all of these as "expenses," your monthly spending looks terrifying. Classifications fix this.

## System Classifications

Spearmint includes 10 built-in classifications:

| Classification | Exclude from Income | Exclude from Expense | Exclude from Cash Flow |
|----------------|--------------------|--------------------|----------------------|
| **Regular Income** | ❌ | ✅ | ❌ |
| **Regular Expense** | ✅ | ❌ | ❌ |
| **Transfer** | ✅ | ✅ | ✅ |
| **Credit Card Payment** | ✅ | ✅ | ✅ |
| **Credit Card Receipt** | ✅ | ✅ | ✅ |
| **Reimbursable** | ✅ | ✅ | ❌ |
| **Reimbursement** | ✅ | ✅ | ❌ |
| **Refund** | ✅ | ❌ | ❌ |
| **Capital Expense** | ✅ | ✅ | ❌ |
| **Investment** | ✅ | ✅ | ✅ |

### How They Work

- **Exclude from Income**: Won't count toward "Total Income"
- **Exclude from Expense**: Won't count toward "Total Expenses"  
- **Exclude from Cash Flow**: Won't affect net cash flow calculations

## Real Examples

### Transfer: $500 from Checking to Savings

Classification: **Transfer**
- ❌ Not income (in Savings)
- ❌ Not expense (from Checking)
- ❌ No cash flow impact (net zero)

**Result:** Your totals stay accurate.

### Credit Card Payment: $2,000

Classification: **Credit Card Payment**
- ❌ Not an expense (the individual charges were already counted)
- Linked to the Credit Card Receipt on the card

**Result:** Charges count once, not twice.

### Work Trip: $400 Hotel

Classification: **Reimbursable**
- Tracked separately as money owed to you
- Excluded from personal expense calculations
- When reimbursed, linked to cancel out

**Result:** Your personal spending isn't inflated by work expenses.

### Kitchen Renovation: $15,000

Classification: **Capital Expense**
- Excluded from regular "monthly expenses"
- Appears in Capital Investment reports
- Still affects cash flow (money left your account)

**Result:** Your monthly budget isn't blown by one-time investments.

## Classification Rules

You can create rules to automatically classify transactions based on patterns:

### Rule Components

| Field | Description | Example |
|-------|-------------|---------|
| **Pattern** | Text to match in description | "VENMO", "ZELLE" |
| **Pattern Type** | How to match | Contains, Starts with, Regex |
| **Priority** | Which rule wins on conflict | 1-100 (higher wins) |
| **Classification** | What to assign | Transfer |

### Example Rules

| Pattern | Classification | Purpose |
|---------|---------------|---------|
| `VENMO`, `ZELLE` | Transfer | P2P payments |
| `PAYMENT THANK YOU` | Credit Card Payment | Card payments |
| `PAYROLL` | Regular Income | Salary deposits |
| `DIVIDEND` | Regular Income | Investment dividends |

## Analysis View vs Complete View

Spearmint offers two ways to view your data:

### Analysis View (Default)
Respects all classifications. Shows your "true" financial picture:
- Transfers excluded
- Reimbursements excluded
- Capital expenses separated

**Use for:** Understanding your actual financial health

### Complete View
Ignores classifications. Shows every transaction at face value:
- All transactions included
- Useful for reconciliation
- Matches bank statements

**Use for:** Auditing, finding discrepancies, reconciling with bank

---

**Related:**
- [Categories](categories.md) — What type of spending
- [CapEx vs OpEx](capex-vs-opex.md) — Deep dive on capital expenses

