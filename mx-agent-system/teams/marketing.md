# Team: marketing

Display name: Marketing
Roleguide: `mx-agent-system/roleguides/marketing-leader.md`
Owner: Product Owner

## Named Memories (Source of Truth)

- `spearmint-marketing-leader-state`
- `spearmint-marketing-iteration-log`
- `spearmint-marketing-known-issues`

Global routing queue (all teams):
- `cross-team-escalations`

## Interfaces / What This Team Owns

- Marketing site design, development, and deployment (Next.js 15, Tailwind CSS, Framer Motion, Cloudflare Pages)
- Marketing site content (copy, images, landing pages)
- Site performance, SEO, analytics, and uptime
- Location in monorepo: `/marketing-site/`

## Validation / Escalation Routing

To request validation from this team:
- Add a `validation-request` entry to `cross-team-escalations` with:
  - `Team = marketing`
  - acceptance criteria + evidence plan

Definition of done for a fulfilled request:
- An outcome memory is created and the `cross-team-escalations` entry is updated with:
  - `outcome_recorded = yes`
  - `outcome_memory_ref = <memory-id>`
