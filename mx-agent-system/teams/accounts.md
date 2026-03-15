# Team: accounts

Display name: Accounts
Roleguide: `mx-agent-system/roleguides/accounts-leader.md`
Owner: Product Owner

## Named Memories (Source of Truth)

- `spearmint-accounts-leader-state`
- `spearmint-accounts-iteration-log`
- `spearmint-accounts-known-issues`

Global routing queue (all teams):
- `cross-team-escalations`

## Interfaces / What This Team Owns

- Account management — CRUD for all 9 account types (checking, savings, brokerage, investment, credit_card, loan, 401k, ira, other)
- Balance tracking, portfolio/holdings, reconciliation, net worth
- Transaction listing, categorization, classification, relationships
- Frontend components: `/web-app/src/components/Accounts/`, `/web-app/src/components/Transactions/`
- Backend routes/services: `/core-api/src/financial_analysis/api/routes/accounts.py`, `/core-api/src/financial_analysis/api/routes/transactions.py`

## Validation / Escalation Routing

To request validation from this team:
- Add a `validation-request` entry to `cross-team-escalations` with:
  - `Team = accounts`
  - acceptance criteria + evidence plan

Definition of done for a fulfilled request:
- An outcome memory is created and the `cross-team-escalations` entry is updated with:
  - `outcome_recorded = yes`
  - `outcome_memory_ref = <memory-id>`
