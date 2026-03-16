# Team: dashboard

Display name: Dashboard
Roleguide: `mx-agent-system/roleguides/dashboard-leader.md`
Owner: Product Owner

## Named Memories (Source of Truth)

- `spearmint-dashboard-leader-state`
- `spearmint-dashboard-iteration-log`
- `spearmint-dashboard-known-issues`

Global routing queue (all teams):
- `cross-team-escalations`

## Interfaces / What This Team Owns

- Dashboard page (`/dashboard`) — the app's default landing page
- Overview cards (income, expenses, net cash flow, ratio, savings rate, daily cash flow)
- Net worth display and account balances quick view
- Financial charts (trend line, category breakdown, expense bar)
- Recent transactions summary
- Analysis hooks and API client (`useAnalysis.ts`, `api/analysis.ts`)
- Backend analysis routes and services
- Chart components (`TrendLineChart`, `CategoryPieChart`, `CategoryBarChart`)

## Validation / Escalation Routing

To request validation from this team:
- Add a `validation-request` entry to `cross-team-escalations` with:
  - `Team = dashboard`
  - acceptance criteria + evidence plan

Definition of done for a fulfilled request:
- An outcome memory is created and the `cross-team-escalations` entry is updated with:
  - `outcome_recorded = yes`
  - `outcome_memory_ref = <memory-id>`
