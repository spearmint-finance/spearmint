## Problem

The application currently tracks transactions excellently but has no concept of actual account balances. Users cannot:

- Track account balances over time
- Reconcile imported transactions against actual account statements
- See historical balance trends
- Verify that all transactions are accounted for
- Track multiple accounts with their individual balances
- Calculate net worth across all accounts

This makes it difficult to:
- Ensure data completeness and accuracy
- Understand true financial position at any point in time
- Detect missing or duplicate transactions
- Track wealth accumulation over time
- Validate that transaction categorization matches reality

## Proposed Solution

Add comprehensive account balance tracking and reconciliation functionality with special support for hybrid brokerage accounts.

### Core Features

#### 1. Account Management
- Create/edit/delete accounts with properties:
  - Account name
  - Account type (Checking, Savings, Brokerage, Investment, Credit Card, Loan, 401k, IRA, etc.)
  - **Account subtype** for hybrid accounts (e.g., "Brokerage with Cash")
  - Institution name
  - Account number (last 4 digits)
  - Currency
  - Active/inactive status

#### 2. Hybrid Brokerage Account Support (NEW)
Many brokerage accounts (like Fidelity, Vanguard, Schwab) mix cash and investments:
- **Dual Balance Tracking**:
  - Cash/Core position (money market funds, FDIC sweep)
  - Investment holdings value (stocks, ETFs, mutual funds)
  - Total account value (cash + investments)
- **Transaction Classification Enhancement**:
  - Investment purchases/sales affect both cash and investment balances
  - Dividends/interest increase cash position
  - Internal journals between cash and investments
  - Fee deductions from cash position
- **Smart Reconciliation**:
  - Import total account value from statements
  - Separately track cash position changes
  - Auto-calculate investment value from transactions

#### 3. Enhanced Balance Tracking
- **Manual Balance Entries**: Record balance snapshots with date
- **Calculated Running Balance**: Based on transactions
- **Balance History**: Track balance over time
- **Multiple Balance Components** for brokerage accounts:
  - Cash balance (core position, money market)
  - Investment value (securities held)
  - Total balance (combined)
  - Statement balance (from broker)
  - Calculated balance (from transactions)

#### 4. Reconciliation System
- **Standard Account Reconciliation**:
  1. Enter statement ending balance and date
  2. System calculates expected balance from transactions
  3. Show discrepancies if any
  4. Mark transactions as cleared/reconciled
  5. Save reconciliation record
- **Brokerage Account Reconciliation**:
  1. Enter total account value from statement
  2. Enter cash/core position separately (optional)
  3. System validates against transaction history
  4. Identifies missing dividends, fees, or trades
- **Discrepancy Detection**: Highlight unmatched amounts
- **Reconciliation History**: Track all past reconciliations

#### 5. Multi-Account Support
- Link transactions to specific accounts
- Account-level filtering in all views
- Cross-account transfer validation
- **Consolidated views**:
  - Net worth (all accounts)
  - Liquid assets (cash/checking/savings)
  - Investment portfolio (all investment accounts)
  - Debt summary (credit cards, loans)

### Database Schema Additions

```sql
-- New tables needed
CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    account_name VARCHAR(100) NOT NULL,
    account_type VARCHAR(50) NOT NULL, -- 'checking', 'savings', 'brokerage', 'credit_card', etc.
    account_subtype VARCHAR(50), -- 'cash_management', 'investment_only', 'hybrid', etc.
    institution_name VARCHAR(100),
    account_number_last4 VARCHAR(4),
    currency VARCHAR(3) DEFAULT 'USD',
    is_active BOOLEAN DEFAULT true,
    has_cash_component BOOLEAN DEFAULT false, -- True for brokerage accounts with cash
    has_investment_component BOOLEAN DEFAULT false, -- True for investment accounts
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE account_balances (
    balance_id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(account_id),
    balance_date DATE NOT NULL,
    -- Standard balance fields
    total_balance DECIMAL(15, 2) NOT NULL, -- Total account value
    balance_type VARCHAR(20), -- 'statement', 'calculated', 'reconciled'
    -- Hybrid account fields (nullable for non-brokerage accounts)
    cash_balance DECIMAL(15, 2), -- Cash/core position
    investment_value DECIMAL(15, 2), -- Securities value
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP,
    UNIQUE(account_id, balance_date, balance_type)
);

CREATE TABLE investment_holdings (
    holding_id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(account_id),
    symbol VARCHAR(20) NOT NULL,
    description VARCHAR(200),
    quantity DECIMAL(15, 6) NOT NULL,
    cost_basis DECIMAL(15, 2),
    current_value DECIMAL(15, 2),
    as_of_date DATE NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE reconciliations (
    reconciliation_id INTEGER PRIMARY KEY,
    account_id INTEGER REFERENCES accounts(account_id),
    statement_date DATE NOT NULL,
    -- Standard reconciliation
    statement_balance DECIMAL(15, 2) NOT NULL,
    calculated_balance DECIMAL(15, 2) NOT NULL,
    -- Hybrid account reconciliation (nullable)
    statement_cash_balance DECIMAL(15, 2),
    calculated_cash_balance DECIMAL(15, 2),
    statement_investment_value DECIMAL(15, 2),
    calculated_investment_value DECIMAL(15, 2),
    -- Results
    discrepancy_amount DECIMAL(15, 2),
    is_reconciled BOOLEAN DEFAULT false,
    reconciled_at TIMESTAMP,
    notes TEXT
);

-- Add to existing transactions table
ALTER TABLE transactions ADD COLUMN account_id INTEGER REFERENCES accounts(account_id);
ALTER TABLE transactions ADD COLUMN is_cleared BOOLEAN DEFAULT false;
ALTER TABLE transactions ADD COLUMN cleared_date DATE;
-- For investment transactions
ALTER TABLE transactions ADD COLUMN affects_cash_balance BOOLEAN DEFAULT true;
ALTER TABLE transactions ADD COLUMN affects_investment_value BOOLEAN DEFAULT false;
ALTER TABLE transactions ADD COLUMN security_symbol VARCHAR(20);
ALTER TABLE transactions ADD COLUMN security_quantity DECIMAL(15, 6);
```

### API Endpoints

- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/{id}` - Update account
- `DELETE /api/accounts/{id}` - Delete account (if no transactions)

- `GET /api/accounts/{id}/balances` - Get balance history
- `POST /api/accounts/{id}/balances` - Add balance entry
- `GET /api/accounts/{id}/current-balance` - Get latest balance

- `POST /api/accounts/{id}/reconcile` - Start reconciliation
- `GET /api/accounts/{id}/reconciliations` - Get reconciliation history
- `PUT /api/reconciliations/{id}` - Update reconciliation

### Frontend Components

#### Account Management Page
- List of accounts with current balances
- Add/edit account dialog
- Account type icons and colors
- Quick balance update button

#### Balance History View
- Chart showing balance over time
- Table of balance entries
- Add manual balance entry
- Compare statement vs calculated

#### Reconciliation Wizard
- Step-by-step reconciliation process
- Transaction checklist
- Discrepancy calculator
- Previous reconciliation reference

#### Net Worth Dashboard
- Total assets vs liabilities
- Stacked chart by account
- Period-over-period comparison
- Account contribution breakdown

### Transaction Pattern Handling

Based on real-world brokerage account data, the system should handle:

#### Cash Position Changes
- **FDIC/Money Market Sweeps**: "Purchase Into Core Account" / "Redemption From Core"
  - Affects: Cash balance only (internal movement)
- **Interest Earned**: "Interest Earned FDIC Insured Deposit"
  - Affects: Increases cash balance
- **Dividends**: "Dividend Received [Security Name]"
  - Affects: Increases cash balance (unless reinvested)

#### Investment Transactions
- **Buy Orders**: "You Bought [Security Name]"
  - Affects: Decreases cash, increases investment value
- **Sell Orders**: "You Sold [Security Name]"
  - Affects: Increases cash, decreases investment value
- **Journal Entries**: "Journaled Auto Journal" / "Journaled Jnl Vs A/c Types"
  - Affects: Internal transfers, may not affect total balance

#### Account Transfers
- **401k/IRA Rollovers**: "Vanguard Target [Date] - withdrawal"
  - Affects: Increases both cash and/or investments
- **External Transfers**: "Transferred to/from [Account]"
  - Affects: Changes total account balance

### Visual Mockup

```
┌─────────────────────────────────────────────────────────────┐
│ Accounts Overview                                           │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐│
│ │ 🏦 Chase Checking          Balance: $5,234.67         ││
│ │    Last reconciled: 10/01/2025                         ││
│ │    [Reconcile] [View History]                          ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────────────────────┐│
│ │ 💳 Chase Sapphire           Balance: -$2,134.22        ││
│ │    Last reconciled: 09/30/2025                         ││
│ │    [Reconcile] [View History]                          ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────────────────────┐│
│ │ 📈 Fidelity Brokerage       Total: $1,245,678.90       ││
│ │    Cash: $45,678.90 | Investments: $1,200,000.00      ││
│ │    Last updated: 10/08/2025                            ││
│ │    [Update Balance] [View Holdings] [Reconcile]       ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ Total Net Worth: $1,248,779.35                             │
│ Liquid Assets: $50,913.57 | Investments: $1,200,000.00     │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase 1: Database & Backend (Week 1)
- [ ] Create database schema
- [ ] Add Account model
- [ ] Add AccountBalance model
- [ ] Add Reconciliation model
- [ ] Create account service layer
- [ ] Update transaction model with account_id

### Phase 2: API Layer (Week 1-2)
- [ ] Implement account CRUD endpoints
- [ ] Add balance tracking endpoints
- [ ] Create reconciliation endpoints
- [ ] Add account filtering to existing endpoints

### Phase 3: Basic Frontend (Week 2)
- [ ] Account list page
- [ ] Add/edit account dialog
- [ ] Display current balances
- [ ] Link accounts in transaction import

### Phase 4: Balance Tracking (Week 3)
- [ ] Balance history chart
- [ ] Manual balance entry
- [ ] Running balance calculation
- [ ] Balance discrepancy alerts

### Phase 5: Reconciliation (Week 3-4)
- [ ] Reconciliation wizard UI
- [ ] Transaction clearing workflow
- [ ] Discrepancy resolution
- [ ] Reconciliation history

### Phase 6: Net Worth & Analytics (Week 4)
- [ ] Net worth dashboard
- [ ] Multi-account analytics
- [ ] Balance projections
- [ ] Account performance metrics

## Benefits

✅ **Complete Financial Picture** - Know exact balances, not just transactions
✅ **Error Detection** - Find missing or duplicate transactions
✅ **Account Verification** - Ensure records match bank statements
✅ **Net Worth Tracking** - See wealth accumulation over time
✅ **Multi-Account Support** - Manage all accounts in one place
✅ **Audit Trail** - Complete reconciliation history

## Success Criteria

- [ ] Can create and manage multiple accounts
- [ ] Can track balance history per account
- [ ] Can reconcile accounts against statements
- [ ] Can see net worth across all accounts
- [ ] Can filter transactions by account
- [ ] Can detect and resolve discrepancies
- [ ] All existing functionality continues to work
- [ ] Performance remains acceptable with balance calculations

## Backward Compatibility

- All existing transactions will work without account assignment
- Account assignment is optional but recommended
- Gradual migration path for existing users
- No breaking changes to current API

## Related Issues

- Could enhance #18 (Dividend Reinvestment) with investment account tracking
- Complements transaction classification with account-level organization
- Enables future investment portfolio tracking features

---

**Estimated Effort:** 40-60 hours
**Priority:** High
**Type:** Major Feature Enhancement
**Breaking Changes:** None