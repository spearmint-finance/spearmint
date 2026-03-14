# Marketing Iteration 2 — Autonomous Agents Page

**Date:** 2026-03-14
**PR:** #57 (merged)
**Focus:** Add /agents page showcasing Spearmint's AI agent roster

## What Changed
- Added `/agents` page with 6 sections: hero, why agents, agent profiles (5 agents), hybrid architecture explainer, A2A protocol flow, CTA
- Agent profiles: Minty, Budget Advisor, Subscription Auditor, Bill Negotiator, Tax Optimizer
- Added animated agent illustrations with Framer Motion
- Added "Agents" to site navigation (desktop + mobile)
- Added Playwright test suite with 12 tests covering all pages, sections, and navigation

## Metrics
- **North Star (Lighthouse UX Score):** Before: deferred. After: deferred (no Cloudflare deploy pipeline yet).
- **Build:** passes, 5 pages statically generated (added /agents)
- **Tests:** 12 Playwright tests pass

## Human Intervention
- No

## Measurable Outcome
- Yes — 5 pages build and render, 12 Playwright tests pass
