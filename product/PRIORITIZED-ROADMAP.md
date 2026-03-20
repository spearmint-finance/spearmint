# Spearmint Prioritized Roadmap

**Last Updated:** 2026-03-20
**Owner:** Product Team
**North Star Metric:** GitHub Stars (current: 0, target: 1,000+)

---

## Current Gate: G1 — Sovereign Foundation

**Goal:** Be the best self-hosted personal finance ledger on the market.

**Status:** 90% complete — core transaction, account, reporting, and import workflows are production-ready. Key remaining items are authorization and budget management.

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
| 10 | **Authentication & authorization** | **Not Started** | **P1 blocker — no auth on any endpoint (KI-002)** |
| 11 | **Budget management UI** | **Not Started** | DB model exists, no frontend implementation |
| 12 | Transaction relationships (transfers, reimbursements) | Partial | Detection endpoints exist, UI minimal |
| 13 | Transaction splits | Partial | Form exists, backend complete |

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
| P1 | Scenario builder (full implementation) | Dashboard team | — |
| P1 | Confidence-based forecasting (upper/lower bounds) | Dashboard team | — |
| P2 | Budget management (envelopes, drag-and-drop reallocation) | Accounts team | — |
| P2 | Budget advisor agent (A2A) | Product team | [budget-advisor-agent.md](feature-planning/budget-advisor-agent.md) |
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
| 1 | **Authentication & authorization** | Accounts / Platform | Without auth, the app cannot be exposed to a network. This is the single biggest blocker to real-world adoption and star growth. |
| 2 | **Budget management UI** | Accounts team | Budgeting is the #1 reason people use personal finance apps (YNAB's entire value proposition). The DB model exists — this needs a frontend. |
| 3 | **README & setup documentation** | Marketing team | First impression for GitHub visitors. Clear install instructions, screenshots, and feature overview directly drive stars. |
| 4 | **Transaction relationships UI** | Accounts team | Transfer detection and reimbursement tracking are built on the backend but lack frontend polish. |
| 5 | **Scenario builder completion** | Dashboard team | Currently stubbed. This is a core Horizon 2 differentiator. |

---

## Completed Work (by team)

### Accounts Team (40+ iterations)
- Full account CRUD with multi-type support
- Entity-scoped net worth calculation
- Balance history and reconciliation
- Transaction form with account selector
- CSV export, tag filtering, pagination
- Accessibility improvements (aria labels, confirmation dialogs)
- Entity reassignment in account details

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
