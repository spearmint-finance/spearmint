# Demo Data Package

**Status:** Draft
**Priority:** P1 (star growth blocker)
**Owner:** Accounts team
**Gate:** G1 (prerequisite for screenshots and first-run experience)
**Directive:** TBD

---

## Problem

When a new user runs `docker-compose up -d` and opens Spearmint, they see an empty dashboard with no data. This creates two critical problems:

1. **README screenshots are impossible** — Directive #253 (add screenshots to README) is blocked because there's no representative data to capture. An empty app screenshot actively hurts star conversion.
2. **First-run experience is empty** — The "time to value" is too long. Users must manually create accounts, import CSVs, and categorize transactions before they see what Spearmint can do. Most will bounce before getting there.

Every successful open-source finance app (Firefly III: 14k+ stars, Actual Budget: 15k+ stars) ships with either demo data, a guided tour, or prominent screenshots of a populated app. Spearmint has none of these.

## Solution

Ship a demo data package that:
1. Pre-populates the app with realistic financial data on first run (opt-in or default for demo mode)
2. Showcases ALL major features: multi-entity, CapEx/OpEx, splits, relationships, categories, reports
3. Provides the exact data needed for compelling README screenshots

## Scope

### In Scope

- **Seed script** (`core-api/scripts/seed_demo_data.py` or similar) that populates the database with demo data
- **Docker integration** — `DEMO_MODE=true` environment variable triggers seed on first start
- **2 entities**: "Personal" and "Side Business" (demonstrates multi-entity)
- **6 accounts**: Checking, Savings, Credit Card (personal) + Business Checking, Business Credit Card, Brokerage (business)
- **~200 transactions** spanning 6 months with realistic patterns:
  - Recurring: rent, salary, subscriptions, utilities
  - Variable: groceries, dining, gas, entertainment
  - CapEx: laptop purchase, home improvement
  - Transfers: checking→savings, CC payments
  - Splits: shared dinner (split across personal + business entity)
  - Reimbursements: business expense reimbursed to personal
- **Categories**: 15-20 categories with hierarchy (Housing > Rent, Housing > Utilities, etc.)
- **Transaction rules**: 3-5 auto-categorization rules (demonstrates automation)
- **Balance snapshots**: Monthly snapshots for balance history charts

### Out of Scope

- User accounts/authentication (not yet implemented — #141)
- Budget data (not yet implemented — #144)
- Plaid/bank linking
- AI assistant conversations
- Custom import profiles

## Acceptance Criteria

1. Running `docker-compose up -d` with `DEMO_MODE=true` populates the database with demo data
2. Dashboard shows: category pie chart with data, cash flow trends, net worth card with positive trajectory
3. Accounts page shows 6 accounts across 2 entities
4. Transactions page shows ~200 categorized transactions with splits and relationships visible
5. Reports page generates meaningful output for all 7 report types
6. Analysis page shows income/expense trends with actual data
7. Entity switcher works — switching entities filters data correctly
8. Net worth shows realistic trajectory (growing over 6 months)
9. At least 2 CapEx transactions appear, demonstrating the CapEx/OpEx separation
10. Seed script is idempotent — running twice doesn't duplicate data
11. `DEMO_MODE=false` (default) starts with a clean database as today

## Data Design Guidelines

- Use realistic but obviously fake data (e.g., "Acme Corp" not real company names)
- Dollar amounts should be realistic for a US household ($3,500/mo rent, $85k salary, etc.)
- Transaction descriptions should look like real bank descriptions ("WHOLE FOODS MKT #10234", "SPOTIFY USA")
- Dates should be relative to current date (not hardcoded) so charts always look current
- Net worth should show a positive trend (psychologically appealing in screenshots)

## Impact on North Star

**Direct**: Unblocks directive #253 (README screenshots) which is the single highest-impact change for star conversion. Every high-star open-source project has prominent screenshots.

**Indirect**: Reduces time-to-value from ~30 minutes (manual setup) to ~2 minutes (docker-compose up). Users who see a populated app are far more likely to star.

## Dependencies

- None — uses existing API endpoints and database models
- Prerequisite for: #253 (screenshots)

## Estimated Effort

Small-medium. The accounts team already has extensive test fixture patterns. The seed script reuses existing API create endpoints.
