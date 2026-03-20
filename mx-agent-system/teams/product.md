# Team: product

Display name: Product
Roleguide: `mx-agent-system/roleguides/product-leader.md`
Owner: Product Owner

## Named Memories (Source of Truth)

- `spearmint-product-leader-state`
- `spearmint-product-iteration-log`
- `spearmint-product-known-issues`

Global routing queue (all teams):
- `cross-team-escalations`

## Interfaces / What This Team Owns

- Product roadmap and prioritization (`product/PRIORITIZED-ROADMAP.md`)
- Competitive analysis and market positioning (`product/competitive/`)
- Feature planning and PRDs (`product/feature-planning/`)
- Goal/gate definitions and assessments
- Cross-team directives (GitHub issues with `product-directive` label)
- Customer feedback synthesis and user signal analysis
- North star metric ownership (GitHub Stars)

## Validation / Escalation Routing

To request a product decision from this team:
- Add a `validation-request` entry to `cross-team-escalations` with:
  - `Team = product`
  - acceptance criteria + evidence plan

Definition of done for a fulfilled request:
- An outcome memory is created and the `cross-team-escalations` entry is updated with:
  - `outcome_recorded = yes`
  - `outcome_memory_ref = <memory-id>`
