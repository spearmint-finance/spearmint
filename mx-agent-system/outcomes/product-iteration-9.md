# Product Iteration 9 — Authentication & Authorization PRD

**Date:** 2026-03-22
**Focus:** Write PRD for authentication & authorization (P0 G1 blocker)
**PR:** #213 (merged)
**Directive Updated:** #141 (comment with PRD details posted)

## What Shipped

- **PRD:** `product/feature-planning/authentication-authorization.md` — comprehensive scope for adding user auth from zero
- **Feature Index:** Updated — all identified features now have PRDs (no more "PRDs Needed" items)
- **Roadmap:** Updated with PRD reference for directive #141
- **Directive #141 comment:** Posted key scope decisions and acceptance criteria to the issue

## Key Decisions

1. **MVP scope:** Email/password + JWT tokens. No OAuth, no MFA, no email-based password reset.
2. **Self-hosted friendly:** No external service dependencies. JWT_SECRET auto-generated if not set.
3. **User-data isolation:** Entities gain `user_id` FK. All queries filter by current user.
4. **Migration strategy:** Existing entities assigned to first registered user; FK nullable initially, then made non-nullable.
5. **MCP API keys preserved:** Existing API key auth continues to work, keys scoped to a user.

## Codebase Audit Findings

- Zero auth in the entire app — no User model, no login page, no auth middleware
- Only API key auth exists (for MCP server clients, not users)
- Dependencies needed: `passlib[bcrypt]`, `python-jose[cryptography]`
- All 50+ API routes are completely unprotected

## Metrics

- **Stars:** 0 → 0
- **Feature Index:** All features now have PRDs (was missing auth PRD)
- **human_intervention:** no
- **measurable_outcome:** yes
