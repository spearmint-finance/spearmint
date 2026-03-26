# Spearmint Prioritized Roadmap

**Last Updated:** 2026-03-23 (iteration 19)
**Owner:** Product Team
**North Star Metric:** GitHub Stars (current: 0, target: 1,000+)

---

## Current Gate: G1 — Sovereign Foundation

**Goal:** Be the best self-hosted personal finance ledger on the market.

**Status:** 92% complete (12/13 items done) — only authentication (#141) remains. Since last update (2026-03-24): accounts team shipped budget management (full CRUD + bar chart + inline editing), transaction relationship UI (type labels, icons, click navigation), demo data package (DEMO_MODE), multi-currency display (Phase 1 — locale detection, currency selector, account component display), and smart categorization (LLM-powered batch categorization).

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
| 11 | Budget management UI | Done | Full CRUD API, progress bars, month navigation, bar chart, inline editing, entity-scoped (#144, PR #17/#22/#23) |
| 12 | Transaction relationships (transfers, reimbursements) | Done | Auto-detection + linking, type-specific labels and icons, click-to-navigate linked transactions (#147, PR #16) |
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
| P2 | Account reconciliation | Accounts team | [account-reconciliation.md](feature-planning/account-reconciliation.md) — **In Progress**: backend complete, creation form + history view shipped (PR #241). Missing: transaction-clearing UI, real-time balance, cleared indicator |
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
| 2 | ~~Budget management UI~~ | Accounts team | **DONE** (PR #17/#22/#23). Full CRUD API, progress bars, bar chart, inline editing, entity scoping. |
| 3 | ~~Demo data package~~ | Accounts team | **DONE** (PR #15/#21). DEMO_MODE=true seeds 693 txns, 2 entities, 6 accounts, 9 budgets, rules, holdings. |
| 4 | **README screenshots** | Accounts + Dashboard | Directive: #253. UNBLOCKED by #273. Capture screenshots of populated dashboard, transactions, reports, budgets. |
| 5 | **Analysis page export fix** | Dashboard team | Directive: #221. Export button downloads empty placeholder CSV — zero actual data. Quick fix: pass analysis data to ExportButton. |
| 6 | ~~Transaction relationships UI~~ | Accounts team | **DONE** (PR #16). Type-specific labels, icons, bidirectional click navigation. |
| 7 | **Dashboard green color palette** | Dashboard team | Directive: #148. User feedback: match monochrome green to Spearmint branding. |
| 8 | **Scenario builder completion** | Dashboard team | Directive: #150. PRD: [scenario-builder-completion.md](feature-planning/scenario-builder-completion.md). Save/load, charts, all adjuster types. |
| 9 | **Confidence intervals in scenarios** | Dashboard team | Directive: #208. PRD: [confidence-based-forecasting.md](feature-planning/confidence-based-forecasting.md). First-mover differentiator — no competitor offers this. |
| 10 | ~~Multi-currency display~~ | Accounts team | **DONE Phase 1** (PR #18/#19/#20). Locale-aware formatting, currency selector, account component display. Phase 2 (exchange rates) is G2. |
| 11 | **Error feedback (snackbar)** | Accounts + Dashboard | Directive: #224. ~86% done — 77 snackbar calls across major flows (PR #244). 7 edge-case gaps remain (scenario builder, export, rule testing). |
| 12 | **Multi-entity on marketing site** | Marketing team | Directive: #152. Shipped feature not yet marketed. |

---

## Completed Work (by team)

### Accounts Team (90+ iterations, as of 2026-03-23)
- Full account CRUD with multi-type support (checking, savings, credit card, loan, 401k, brokerage)
- Entity-scoped net worth calculation
- Balance history and reconciliation
- Transaction form with account selector, tags, categories, entity assignment
- CSV import with auto-account creation from Tiller, deduplication
- CSV export with loading state
- Transaction splits: full form, "Split Evenly", inline entity selector, grid indicator, amount validation, portion indicator chip, split breakdown in detail dialog, entity filter support
- Transaction relationships: auto-detection for transfers, CC payments, reimbursements, dividend reinvestments
- Entity system: CRUD, M2M account-entity, direct + inherited entity assignment on transactions, bulk entity assign
- Category management: entity-scoped categories with hierarchy, search, type filter, entity filter, inline editor, transaction count per category, snackbar feedback, duplicate name validation, **category merge/reassign workflow**
- **Holdings CRUD**: creation form and delete capability in portfolio tab with gain/loss display
- **Transaction rules extended**: auto-assign entities alongside categories, promoted to top-level Settings tab, renamed from "Category Rules" to "Transaction Rules"
- **Reconciliation creation form**: start reconciliation with statement date/balance in account details (backend fully implemented, frontend creation + history view)
- **Snackbar error feedback**: 77 instances across major flows (PR #244 added backend error detail surfacing)
- Account search bar with search-aware empty state
- Accessibility improvements (aria labels, confirmation dialogs)
- Date range validation, batch clear validation, error feedback
- Debug logging cleanup (print → proper logging)
- Searchable category filter with Autocomplete on transactions page
- Enhanced "Create New Category" dialog with parent and entity info
- Duplicate transaction action, bulk category assignment
- **Smart categorization**: LLM-powered batch categorization with GPT-4o-mini, three-step review flow, inline category/rule creation
- **Reconciliation completion**: Transaction clearing UI, cleared indicators, real-time balance tracking
- **Entity auto-inheritance**: Transactions auto-inherit entity from single-entity accounts
- **Demo data package**: DEMO_MODE=true seeds 693 txns, 2 entities, 6 accounts, rules, holdings, budgets
- **Budget management**: Full CRUD API, progress bars, bar chart, inline editing, month navigation, entity scoping
- **Transaction relationship UI**: Type-specific labels (Transfer, CC Payment, Reimbursement), icons, click-to-navigate
- **Multi-currency Phase 1**: Locale-aware formatting, currency selector (20 ISO 4217), account component display
- **Transfer exclusion**: Auto-exclude Transfer-category transactions from analysis

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
