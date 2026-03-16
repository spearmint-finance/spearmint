# Product Requirements Document: Business Entity Separation

**Product:** Spearmint Personal Finance Engine
**Feature:** Multi-Entity Support for Business, Rental Property, and Personal Finance Separation
**Owner:** Accounts Team
**Status:** Draft
**Last Updated:** 2026-03-16

---

## Executive Summary

Spearmint currently treats all accounts and transactions as a single flat financial picture. Users who own small businesses, rental properties, or side hustles cannot separate business finances from personal ones. This makes it impossible to generate a business P&L, track rental property profitability, or prepare accurate tax documents without manual spreadsheet work outside the app.

This PRD defines **multi-entity support** — the ability to create distinct financial entities (personal, business, rental property) with their own accounts, transactions, and financial statements. Each entity functions as an independent "book" with its own P&L, cash flow statement, and tax-relevant categorization.

**Expected Impact:**
- Enable users to manage personal and business finances in one app without co-mingling
- Generate per-entity P&L and cash flow statements for accounting and tax filing
- Support IRS Schedule C (business) and Schedule E (rental property) tax category mapping
- Reduce time spent on manual bookkeeping and tax prep from hours to minutes
- Position Spearmint for small business owners, landlords, and freelancers — not just W-2 employees

---

## Problem Statement

### The User Problem

1. **Co-mingled finances:** A user who owns an LLC and two rental properties sees all transactions in one list. Business expenses, rental income, and personal spending are indistinguishable without manual tagging.

2. **No business financial statements:** There's no way to generate a P&L or cash flow statement for a specific business. Users export to Excel and manually build these reports for their accountant.

3. **Tax preparation pain:** At tax time, users must manually separate business deductions (Schedule C), rental income/expenses (Schedule E), and personal transactions. This is error-prone and time-consuming.

4. **Rental property tracking:** Landlords need per-property P&L (rent income vs. mortgage, repairs, insurance, property taxes, depreciation). The current flat structure can't provide this.

5. **Account confusion:** A user's personal checking, business checking, and rental property escrow account all appear in the same list with no grouping.

### The Technical Problem

1. **No entity concept:** The data model has no grouping mechanism above the account level. Accounts and transactions exist in a global namespace.

2. **No financial statement generation:** While summary stats exist (income/expense totals), there are no structured P&L or cash flow statement reports.

3. **No tax line mapping:** Transaction categories have no connection to IRS form line items.

---

## User Stories

### P0 — Must Have

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-001 | As a small business owner, I want to create a separate business entity so that I can track business finances independently from personal | Entity CRUD; accounts assignable to entities; transactions filtered by entity |
| US-002 | As a landlord, I want to create an entity for each rental property so that I can track income and expenses per property | Entity type "rental_property" with address field; per-property account grouping |
| US-003 | As a business owner, I want to generate a P&L statement for my business for any date range so that I can share it with my accountant | P&L endpoint: revenue, COGS, gross profit, operating expenses by category, net income |
| US-004 | As a user, I want to switch between entities in the app so that I can view each entity's accounts and transactions separately | Entity switcher in sidebar or header; all pages filter by selected entity |
| US-005 | As a user, I want a "Personal" entity created by default so that my existing accounts continue to work without changes | Migration creates default entity; existing accounts assigned to it |

### P1 — Should Have

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-006 | As a business owner, I want to generate a cash flow statement so that I can understand operating, investing, and financing cash flows | Cash flow endpoint: operating (net income + adjustments), investing (capex), financing (loans, equity) |
| US-007 | As a user preparing taxes, I want transaction categories mapped to IRS tax line items so that I can see my deductions organized by schedule | Category model extended with `tax_line_item`; Schedule C and Schedule E mappings |
| US-008 | As a user, I want to split a transaction across entities so that a personal credit card purchase for business can be properly allocated | Transaction split by entity; split amount tracking |
| US-009 | As a user, I want to see a consolidated net worth view across all entities so that I get a complete financial picture | Aggregate net worth API includes all entities; entity breakdown in response |

### P2 — Nice to Have

| ID | Story | Acceptance Criteria |
|---|---|---|
| US-010 | As a landlord, I want to track depreciation schedules for my properties | Depreciation model: asset, method, useful life, placed-in-service date |
| US-011 | As a business owner, I want to export my P&L as a PDF for my accountant | PDF generation from P&L data |
| US-012 | As a user, I want to import a chart of accounts for my business from QuickBooks or Xero | CSV import mapping; standard chart of accounts templates |

---

## Data Model Changes

### New Table: `entities`

```
entities
├── entity_id          INT PK AUTO_INCREMENT
├── entity_name        VARCHAR(100) NOT NULL
├── entity_type        ENUM('personal', 'business', 'rental_property', 'side_hustle') NOT NULL
├── tax_id             VARCHAR(20) NULL          -- EIN for businesses
├── address            TEXT NULL                  -- For rental properties
├── fiscal_year_start  DATE DEFAULT '01-01'       -- Most businesses use calendar year
├── is_default         BOOLEAN DEFAULT FALSE      -- One default entity (personal)
├── notes              TEXT NULL
├── created_at         DATETIME
└── updated_at         DATETIME
```

### Modified Table: `accounts`

```diff
accounts
+ ├── entity_id        INT FK → entities.entity_id NULL  -- NULL = default/personal entity
```

- **Migration:** Add `entity_id` as nullable FK. Create a default "Personal" entity. Optionally assign existing accounts to it (or leave NULL to mean "default").
- **Non-breaking:** Existing queries that don't filter by entity_id continue to work. The entity filter is additive.

### Modified Table: `categories`

```diff
categories
+ ├── tax_line_item    VARCHAR(100) NULL    -- e.g. "Schedule C Line 18 - Office Expenses"
+ ├── entity_id        INT FK NULL          -- Entity-specific categories (NULL = global)
```

- Business categories may differ from personal ones. A "Repairs" category for a rental property maps to Schedule E Line 14, while a "Repairs" category for a business maps to Schedule C Line 21.
- Global categories (entity_id = NULL) are available to all entities.

### New Table: `entity_members` (Future — Multi-User)

Not in scope for V1, but the entity model naturally extends to multi-user: each entity can have members with roles (owner, accountant, bookkeeper). This is noted here for data model foresight.

---

## API Design

### Entity CRUD

| Method | Path | Description |
|---|---|---|
| POST | `/api/entities` | Create an entity |
| GET | `/api/entities` | List all entities |
| GET | `/api/entities/{id}` | Get entity details |
| PUT | `/api/entities/{id}` | Update entity |
| DELETE | `/api/entities/{id}` | Delete entity (must reassign or delete accounts first) |

### Entity-Scoped Queries

All existing list endpoints gain an optional `entity_id` query parameter:

| Endpoint | Change |
|---|---|
| `GET /api/accounts` | Add `?entity_id=N` filter |
| `GET /api/transactions` | Add `?entity_id=N` filter (via account.entity_id join) |
| `GET /api/accounts/net-worth` | Add `?entity_id=N` for per-entity net worth |

### Financial Statements

| Method | Path | Description |
|---|---|---|
| GET | `/api/entities/{id}/pnl` | P&L statement for date range |
| GET | `/api/entities/{id}/cashflow` | Cash flow statement for date range |

#### P&L Response Shape

```json
{
  "entity_id": 2,
  "entity_name": "Acme LLC",
  "period": { "start": "2026-01-01", "end": "2026-03-31" },
  "revenue": {
    "total": 45000.00,
    "by_category": [
      { "category": "Sales Revenue", "amount": 40000.00 },
      { "category": "Service Revenue", "amount": 5000.00 }
    ]
  },
  "expenses": {
    "total": 28000.00,
    "by_category": [
      { "category": "Rent", "amount": 6000.00, "tax_line": "Schedule C Line 20b" },
      { "category": "Supplies", "amount": 3200.00, "tax_line": "Schedule C Line 22" },
      { "category": "Contractor Payments", "amount": 12000.00, "tax_line": "Schedule C Line 11" },
      { "category": "Software/SaaS", "amount": 2400.00, "tax_line": "Schedule C Line 18" },
      { "category": "Insurance", "amount": 4400.00, "tax_line": "Schedule C Line 15" }
    ]
  },
  "net_income": 17000.00
}
```

#### Cash Flow Response Shape

```json
{
  "entity_id": 2,
  "period": { "start": "2026-01-01", "end": "2026-03-31" },
  "operating": {
    "net_income": 17000.00,
    "adjustments": [],
    "total": 17000.00
  },
  "investing": {
    "items": [
      { "description": "Equipment purchase", "amount": -5000.00 }
    ],
    "total": -5000.00
  },
  "financing": {
    "items": [
      { "description": "Loan payment", "amount": -2000.00 },
      { "description": "Owner contribution", "amount": 10000.00 }
    ],
    "total": 8000.00
  },
  "net_change": 20000.00,
  "beginning_cash": 15000.00,
  "ending_cash": 35000.00
}
```

---

## Frontend Design

### Entity Switcher

- **Location:** Sidebar or top header, always visible
- **Behavior:** Dropdown showing all entities + "All Entities" option
- **Effect:** Selecting an entity filters accounts, transactions, and net worth to that entity
- **URL:** Persisted as `?entity_id=N` query param for bookmarkability
- **Default:** "Personal" entity selected on first load

### Accounts Page Changes

- Account cards grouped by entity (if "All Entities" view)
- AddAccountDialog includes entity selector
- AccountDetailsDialog shows entity assignment

### Transactions Page Changes

- Entity filter in Advanced Filters (in addition to account filter)
- CSV export includes entity column
- Summary stats scoped to selected entity

### New: Reports Page

- **P&L tab:** Date range selector, entity selector, table view of revenue/expenses by category
- **Cash Flow tab:** Same selectors, operating/investing/financing breakdown
- **Export:** CSV and PDF export options

---

## Implementation Plan

### Phase 1: Foundation (Backend — 2-3 iterations)

1. **Entity model + CRUD endpoints** — new table, migration, routes, service
2. **Account.entity_id** — add FK, migration, filter support on list endpoint
3. **Transaction entity filtering** — join through account.entity_id

### Phase 2: Frontend Entity Integration (3-4 iterations)

4. **Entity switcher component** — sidebar dropdown, context provider
5. **Accounts page entity scoping** — filter by entity, show entity in cards
6. **Transactions page entity scoping** — entity filter, CSV export column
7. **AddAccountDialog + AccountDetailsDialog** — entity selector

### Phase 3: Financial Statements (3-4 iterations)

8. **P&L endpoint** — aggregate income/expenses by category for entity + period
9. **Cash flow endpoint** — classify transactions by operating/investing/financing
10. **Reports page UI** — P&L and cash flow views with date range picker
11. **Tax line mapping** — category.tax_line_item, Schedule C/E presets

### Phase 4: Polish (2-3 iterations)

12. **Transaction entity splitting** — split a transaction across entities
13. **Consolidated view** — "All Entities" net worth and summary
14. **PDF/CSV export** — export P&L and cash flow statements

**Total estimated scope: 10-14 iterations**

---

## Migration Strategy

### Data Migration

1. Create `entities` table
2. Insert default entity: `("Personal", "personal", is_default=true)`
3. Add `entity_id` column to `accounts` (nullable)
4. Optionally: `UPDATE accounts SET entity_id = 1` (assign all existing accounts to Personal)
5. Add `tax_line_item` column to `categories` (nullable)

### Rollback Plan

- `entity_id` on accounts is nullable — removing the column is non-destructive
- Entity table can be dropped without affecting existing functionality
- All changes are additive; no existing columns or tables are modified

---

## Constraints and Risks

| Risk | Mitigation |
|---|---|
| Entity concept adds complexity to every query | Entity filter is optional; NULL entity_id means "default" |
| P&L accuracy depends on correct categorization | Provide category templates per entity type; highlight uncategorized transactions |
| Tax line mapping varies by jurisdiction | Start with US IRS schedules only; make tax_line_item freeform text |
| Multi-entity transactions (split across entities) | Phase 4; defer until basic entity separation is validated |
| Performance with entity joins on large datasets | entity_id is indexed; join through accounts table is O(1) with FK index |

---

## Success Metrics

| Metric | Baseline | Target |
|---|---|---|
| Entities created per user | 0 | ≥ 2 (personal + at least one business/rental) |
| P&L statements generated per month | 0 | ≥ 1 per business entity |
| Time to generate P&L | N/A (manual Excel) | < 5 seconds |
| Tax line coverage | 0% | ≥ 80% of Schedule C and Schedule E lines |

---

## Appendix A: IRS Schedule Mapping Reference

### Schedule C (Business Income)

| Line | Description | Suggested Category |
|---|---|---|
| 1 | Gross receipts/sales | Sales Revenue |
| 10 | Commissions and fees | Commissions |
| 11 | Contract labor | Contractor Payments |
| 13 | Depreciation | Depreciation |
| 15 | Insurance | Business Insurance |
| 16a | Mortgage interest | Mortgage Interest |
| 17 | Legal and professional | Legal & Professional |
| 18 | Office expense | Office Expenses |
| 20b | Rent (other business property) | Rent |
| 22 | Supplies | Supplies |
| 24a | Travel | Business Travel |
| 24b | Meals (50%) | Business Meals |
| 25 | Utilities | Utilities |
| 27a | Other expenses | Other Business Expenses |

### Schedule E (Rental Income)

| Line | Description | Suggested Category |
|---|---|---|
| 3 | Rents received | Rental Income |
| 5 | Advertising | Advertising |
| 6 | Auto and travel | Auto & Travel |
| 7 | Cleaning and maintenance | Cleaning & Maintenance |
| 8 | Commissions | Commissions |
| 9 | Insurance | Rental Insurance |
| 10 | Legal and professional | Legal & Professional |
| 12 | Mortgage interest | Mortgage Interest |
| 14 | Repairs | Repairs |
| 16 | Taxes | Property Taxes |
| 17 | Utilities | Utilities |
| 18 | Depreciation | Depreciation |
| 19 | Other | Other Rental Expenses |
