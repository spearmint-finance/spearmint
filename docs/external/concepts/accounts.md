# Accounts

Accounts in Spearmint represent your financial containers — the places where money lives and moves.

## Account Types

Spearmint supports various account types, each with specific behaviors:

| Type | Description | Example |
|------|-------------|---------|
| **Checking** | Primary spending account | Chase Checking |
| **Savings** | Savings and emergency funds | Ally Savings |
| **Credit Card** | Credit accounts (liability) | Chase Sapphire |
| **Brokerage** | Investment accounts with cash and holdings | Fidelity Brokerage |
| **Investment** | Pure investment accounts | Vanguard 401k |
| **401k** | Employer retirement accounts | Company 401k |
| **IRA** | Individual retirement accounts | Roth IRA |
| **Loan** | Loans and mortgages (liability) | Auto Loan |
| **Other** | Anything else | HSA, FSA, etc. |

## Creating an Account

1. Navigate to **Accounts** in the sidebar
2. Click **Add Account**
3. Fill in:
   - **Name** — A friendly name (e.g., "Chase Checking")
   - **Type** — Select from the account types above
   - **Institution** — The bank or brokerage name
   - **Account Number** (optional) — Last 4 digits for reference

## Hybrid Brokerage Accounts

One of Spearmint's unique capabilities is handling **hybrid accounts** — brokerage accounts that contain both:

- **Cash** — Spendable money (affects cash flow)
- **Investments** — Holdings like stocks and funds (affects net worth)

When you mark an account as a brokerage, Spearmint:
- Separates cash transactions from investment transactions
- Includes cash in spending power calculations
- Includes investments in net worth calculations

## Balance Reconciliation

Spearmint tracks two balance values for each account:

### Statement Balance
The balance reported by your bank. You update this periodically from your statements.

### Calculated Balance
The balance Spearmint calculates from your imported transactions.

### Why They Might Differ

| Difference | Possible Cause |
|------------|----------------|
| Statement > Calculated | Missing transactions in Spearmint |
| Calculated > Statement | Duplicate transactions imported |
| Off by exact amount | Single missing or duplicate transaction |
| Random variance | Pending transactions not yet settled |

### Reconciling Your Accounts

1. Navigate to the account detail view
2. Compare Statement vs Calculated balance
3. If different, review recent transactions for:
   - Missing imports
   - Duplicate entries
   - Incorrect amounts

Regular reconciliation ensures your data is accurate for analysis and forecasting.

## Linking Accounts to Import Profiles

When you [create an Import Profile](../features/import-profiles.md), you can link it to a specific account. This means:

- Imported transactions automatically associate with the correct account
- Account-specific rules can be applied
- Cash flow by account becomes available

## Account-Level Analysis

With accounts set up, you can:

- **Filter transactions** by account
- **View cash flow** per account
- **See balances** across all accounts
- **Detect transfers** between your accounts

---

**Next:** [Learn about Transactions](transactions.md)

