# Multi-Currency Display Support

**Status:** Draft
**Priority:** P2
**Gate:** G1 (Phase 1) / G2 (Phase 2)
**Target Team:** Accounts team (frontend + backend)
**Directive:** #217
**Related Issue:** PKI-008

---

## Problem Statement

Spearmint hardcodes USD currency throughout the frontend (12 component files, 37 locale references) and uses "en-US" for all number formatting. While the backend Account model already stores a `currency` field (ISO 4217), the frontend ignores it and always formats amounts as USD.

This blocks international adoption — a key driver for GitHub stars from the global open-source community. Competitors like Firefly III and Actual Budget support multi-currency out of the box.

---

## Competitive Context

| App | Multi-Currency | Exchange Rates | Locale-Aware |
|-----|---------------|----------------|--------------|
| Firefly III | Yes | Manual + auto (via API) | Yes |
| Actual Budget | Yes (per-account) | No | Partial |
| GnuCash | Yes | Manual + online quotes | Yes |
| YNAB | No (single currency) | No | Partial |
| Monarch Money | Yes | Auto | Yes |
| **Spearmint** | **Schema only — display is USD-only** | **No** | **No** |

Spearmint is in the minority of apps that don't support basic multi-currency display.

---

## Proposed Solution

### Phase 1 — Currency-Aware Display (G1 scope, P2)

**Goal:** Display amounts in the currency stored on each account. No exchange rates, no aggregation changes.

#### Backend Changes

1. **Ensure currency is returned in all API responses** that include monetary amounts
   - Account responses already include `currency` — verify all endpoints
   - Transaction responses should inherit currency from their account

2. **No new endpoints needed** — currency data already exists in the schema

#### Frontend Changes

1. **Update `formatCurrency()` in `web-app/src/utils/formatters.ts`**
   - Accept currency parameter from account data instead of defaulting to "USD"
   - Use `Intl.NumberFormat` with the account's currency code
   - Detect locale from `navigator.language` instead of hardcoding "en-US"

2. **Update all 12 component files** that hardcode "USD":
   - `BalanceHistoryChart.tsx` — use account.currency
   - `NetWorthCard.tsx` — use account.currency (or entity's primary currency for aggregations)
   - `AnalysisSummaryCards.tsx` — use account.currency
   - `CategoryBreakdown.tsx` — use account.currency
   - `ExpenseCategoryList.tsx` — use account.currency
   - `ExpenseOverviewCards.tsx` — use account.currency
   - `IncomeCategoryList.tsx` — use account.currency
   - `IncomeOverviewCards.tsx` — use account.currency
   - `ProjectionsDashboard.tsx` — use account.currency
   - `ScenarioCompassion.tsx` — use account.currency

3. **Update `web-app/src/api/accounts.ts`**
   - Remove `|| "USD"` fallback (line 69) — require currency from backend

4. **Handle mixed-currency aggregation gracefully**
   - When aggregating across accounts with different currencies, display a warning
   - Do NOT convert — just show "Mixed currencies" indicator
   - Individual account views show the correct currency

#### Acceptance Criteria

- [ ] All monetary amounts display in the currency stored on the account
- [ ] Number formatting respects browser locale (e.g., 1.234,56 for de-DE)
- [ ] Creating a new account allows selecting a currency (dropdown with common ISO 4217 codes)
- [ ] Existing accounts default to USD if no currency is set (backward compatible)
- [ ] Dashboard aggregations show a "mixed currencies" indicator when accounts use different currencies
- [ ] No exchange rate conversion is performed (amounts are summed as-is with a clear disclaimer)

### Phase 2 — Exchange Rates & Locale Preferences (G2 scope, P3)

**Goal:** Add exchange rate support for cross-currency aggregation and user-configurable locale preferences.

#### Scope (to be detailed in a separate PRD when G2 begins)

- User settings page with locale and preferred display currency
- Exchange rate provider integration (Open Exchange Rates API or similar)
- Automatic conversion for dashboard aggregations
- Historical exchange rates for accurate past reporting
- Currency conversion widget in transaction views

---

## Out of Scope

- Multi-currency transactions (a single transaction spanning two currencies, e.g., forex)
- Cryptocurrency support (tokens, wallets, blockchain integration)
- Real-time exchange rate streaming

---

## Technical Notes

### Backend Audit (current state)

| Location | Current Behavior | Phase 1 Change |
|----------|-----------------|----------------|
| `models.py:510` | `currency = Column(String(3), default='USD')` | Keep — backward compatible |
| `schemas/account.py:26` | `currency: str = Field(default='USD')` | Keep — backward compatible |
| `account_service.py:35` | `currency: str = 'USD'` default param | Keep — backward compatible |
| `import_service.py:629` | `currency='USD'` on import | Allow CSV column mapping for currency |
| `migrations/add_accounts_system.py:75` | `DEFAULT 'USD'` | Keep — migration is historical |

### Frontend Audit (current state)

- `formatCurrency()` in `formatters.ts` — central formatting function, accepts currency param but defaults to "USD"
- 12 component files pass "USD" explicitly — need to pass account.currency instead
- 37 occurrences of "en-US" — replace with `navigator.language` or user preference

---

## Impact on North Star

- **International users** represent a significant portion of open-source personal finance tool users
- Firefly III (12k+ stars) attributes part of its adoption to multi-currency support
- Multi-currency is the #1 feature request in personal finance app communities
- Expected: enables adoption in non-USD markets, directly supporting star growth
