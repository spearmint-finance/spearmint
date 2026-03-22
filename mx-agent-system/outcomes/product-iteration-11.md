# Product Iteration 11 — Multi-Currency Display PRD

**Date:** 2026-03-22
**Focus:** Multi-currency display support PRD and directive (PKI-008)
**Stars:** 0 → 0
**Human Intervention:** No
**Measurable Outcome:** Yes

## What Shipped

- **PRD:** `product/feature-planning/multi-currency-display.md` — phased approach (Phase 1: read currency from account data; Phase 2: exchange rates + locale preferences)
- **Directive:** #217 filed to Accounts team (P2)
- **Feature Index:** Updated to include multi-currency PRD
- **Roadmap:** Updated with directive #217 at priority rank 8
- **Roadmap refresh:** Updated accounts team completed work to reflect category management improvements (PRs #196-#210)

## Codebase Audit Findings

- 5 backend locations with hardcoded 'USD' defaults
- 12 frontend component files with hardcoded "USD"
- 37+ occurrences of hardcoded "en-US" locale
- Backend Account model already has `currency` field — frontend ignores it

## Competitive Context

- Firefly III, Actual Budget, GnuCash all support multi-currency
- Spearmint is in the minority that doesn't
- International users are a significant segment of OSS personal finance tool users

## Gate Progress

- G1: 11/13 items (unchanged — auth and budget remain the blockers)
- Active directives: 8 (was 7 — added #217)
- All known issues now have directives

## Prior Art

- Accounts team KI-003 flagged hardcoded USD
- No prior PRD or strategic decision existed
- Codebase audit performed to document exact scope
