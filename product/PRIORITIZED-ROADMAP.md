# Spearmint Prioritized Roadmap

**Last Updated:** 2026-03-22
**Owner:** Product Team
**North Star Metric:** GitHub Stars (current: 0, target: 1,000+)

---

## Current Gate: G1 — Sovereign Foundation

**Goal:** Be the best self-hosted personal finance ledger on the market.

**Status:** 85% complete (11/13 items done) — core transaction, account, reporting, import, and split workflows are production-ready. Key remaining items are authentication (#141) and budget management (#144). Transaction relationships are functional (auto-detection + linking) but need UI polish.

### G1 Checklist

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Transaction CRUD (create, read, update, delete) | Done | Full frontend + backend |
| 2 | Account management (multi-type, balance history) | Done | Checking, savings, credit card, loan, 401k, brokerage |
| 3 | CSV import with saved profiles | Done | Import profiles, history tracking, deduplication |
| 4 | Categorization rules engine | Done | Pattern matching on description, source, amount, payment method |
| 5 | Classification rules engine | Done | Income/expense/cashflow exclusions with priority system |
| 6 | Reports (balance, summary, income, expense, reconciliation, capex, receivables) | Done | 7 report types |
| 7 | Net worth tracking | Done | Multi-entity scoped, entity switcher |
| 8 | Dashboard with charts | Done | Category pie chart, trends, cash flow, net worth card |
| 9 | Multi-entity support | Done | Entity CRUD, entity-scoped accounts and P&L |
| 10 | **Authentication & authorization** | **Not Started** | **P0 blocker — no auth on any endpoint (#141)** |
| 11 | **Budget management UI** | **Not Started** | DB model exists, no frontend implementation (#144) |
| 12 | Transaction relationships (transfers, reimbursements) | Partial | Auto-detection + linking works; UI shows link icon + tooltip. Missing: relationship type display, manual link form, bidirectional navigation (#147) |
| 13 | Transaction splits | Done | Full split form, "Split Evenly", inline entity selector, grid indicator, amount validation. Shipped by accounts team (iterations 58-66) |

### G1 Completion Criteria

G1 is complete when:
- All items above are "Done"
- A new user can install via `docker-compose up -d`, create an account, import a CSV, and see their net worth — all within 10 minutes
- The README provides clear setup instructions

---

## Gate G2 — Intelligent Analyst

**Goal:** Answer "What if?" questions. Differentiate through CapEx/OpEx separation and confidence modeling.

**Status:** Not started (blocked by G1 completion)

### G2 Priority Items

| Priority | Item | Owner | PRD |
|----------|------|-------|-----|
| P1 | Scenario builder (full implementation) | Dashboard team | [scenario-builder-completion.md](feature-planning/scenario-builder-completion.md) |
| P1 | Confidence-based forecasting (upper/lower bounds) | Dashboard team | [confidence-based-forecasting.md](feature-planning/confidence-based-forecasting.md) |
| P2 | Budget management (envelopes, drag-and-drop reallocation) | Accounts team | [budget-management-ui.md](feature-planning/budget-management-ui.md) |
| P2 | Budget advisor agent (A2A) | Product team | [budget-advisor-agent.md](feature-planning/budget-advisor-agent.md) |
| P2 | Account reconciliation | Accounts team | [account-reconciliation.md](feature-planning/account-reconciliation.md) |
| P2 | AI assistant completion (4 stub endpoints) | Accounts/Platform team | — (directive #227) |
| P3 | Mobile responsive design | Accounts + Dashboard | — (directive #229) |
| P3 | Bank data aggregation (Plaid) | Accounts team | [bank-data-aggregation.md](feature-planning/bank-data-aggregation.md) |

---

## Gate G3 — Private Cloud

**Goal:** Managed hosting option with user-held encryption keys.

**Status:** Future — not scoped

---

## Active Priorities (Ranked)

These are the items that should be worked on NOW, in priority order:

| Rank | Item | Target Team | Rationale |
|------|------|-------------|-----------|
| 1 | **Authentication & authorization** | Accounts / Platform | Directive: #141. PRD: [authentication-authorization.md](feature-planning/authentication-authorization.md). Without auth, the app cannot be exposed to a network. Single biggest blocker to real-world adoption. |
| 2 | **Budget management UI** | Accounts team | Directive: #144. PRD: [budget-management-ui.md](feature-planning/budget-management-ui.md). Budgeting is the #1 reason people use personal finance apps. |
| 3 | ~~**README & setup documentation**~~ | ~~Marketing team~~ | **Done** (PR #146). Complete README rewrite with competitive positioning, Docker quick start, feature comparison table. |
| 4 | **Analysis page export fix** | Dashboard team | Directive: #221. Export button downloads empty placeholder CSV — zero actual data. Quick fix: pass analysis data to ExportButton. |
| 5 | **Transaction relationships UI** | Accounts team | Directive: #147. Backend detection exists — needs frontend polish for transfers, reimbursements, CC payments. |
| 6 | **Dashboard green color palette** | Dashboard team | Directive: #148. User feedback: match monochrome green to Spearmint branding. |
| 7 | **Scenario builder completion** | Dashboard team | Directive: #150. PRD: [scenario-builder-completion.md](feature-planning/scenario-builder-completion.md). Save/load, charts, all adjuster types. |
| 8 | **Confidence intervals in scenarios** | Dashboard team | Directive: #208. PRD: [confidence-based-forecasting.md](feature-planning/confidence-based-forecasting.md). First-mover differentiator — no competitor offers this. |
| 9 | **Multi-currency display** | Accounts team | Directive: #217. PRD: [multi-currency-display.md](feature-planning/multi-currency-display.md). Read currency from account data instead of hardcoding USD. Enables international adoption. |
| 10 | **Error feedback (snackbar)** | Accounts + Dashboard | Directive: #224. Replace 10 silent console.error failures with user-visible snackbar. Pattern established in PR #206. |
| 11 | **Multi-entity on marketing site** | Marketing team | Directive: #152. Shipped feature not yet marketed. |

---

## Completed Work (by team)

### Accounts Team (71+ iterations, as of 2026-03-22)
- Full account CRUD with multi-type support (checking, savings, credit card, loan, 401k, brokerage)
- Entity-scoped net worth calculation
- Balance history and reconciliation
- Transaction form with account selector, tags, categories, entity assignment
- CSV import with auto-account creation from Tiller, deduplication
- CSV export with loading state
- Transaction splits: full form, "Split Evenly", inline entity selector, grid indicator, amount validation
- Transaction relationships: auto-detection for transfers, CC payments, reimbursements, dividend reinvestments
- Entity system: CRUD, M2M account-entity, direct + inherited entity assignment on transactions, bulk entity assign
- Category management: entity-scoped categories with hierarchy, search, type filter, entity filter, inline editor, transaction count per category, snackbar feedback, duplicate name validation
- Accessibility improvements (aria labels, confirmation dialogs)
- Date range validation, batch clear validation, error feedback
- Debug logging cleanup (print → proper logging)
- Searchable category filter with Autocomplete on transactions page
- Enhanced "Create New Category" dialog with parent and entity info

### Dashboard Team (8 iterations)
- Category pie chart with responsive layout
- Cash flow trends visualization
- Net worth card
- Deep-dive links to analysis pages
- Income/expense trend charts

### Marketing Team (16 iterations)
- Next.js marketing site with hero, features, pricing pages
- SEO optimization, WCAG 2 AA accessibility
- Currently in maintenance mode
