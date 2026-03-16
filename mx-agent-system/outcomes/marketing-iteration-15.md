# Marketing Iteration 15 — Axe-Core Accessibility Tests & WCAG Contrast Fixes

**Date:** 2026-03-16
**PR:** #92 (merged)
**Focus:** Add automated accessibility scanning and fix all WCAG 2 AA color contrast violations

## What Changed
- Added `@axe-core/playwright` dependency for automated WCAG 2 AA scanning
- Added 7 new Playwright tests: 404 page validation, footer link validation, and axe-core scans on all 5 pages (12→19 total)
- Fixed 6 accessibility violations found by axe-core:
  - Brand color `--spearmint` darkened from #43A047 (3.3:1) to #338033 (4.91:1)
  - CTA body text opacity: text-white/80 → text-white/95 (4.78:1)
  - Budget Advisor badge: text-teal → text-teal-700 (4.94:1)
  - Subscription Auditor badge: text-amber-600 → text-amber-700 (4.65:1)
  - Hybrid architecture taglines: text-gray-500 → text-gray-600 (6.96:1)
  - Footer headings: h3 → p (fixes heading-order violation)

## Metrics
- **North Star (Lighthouse UX Score):** Before: deferred. After: deferred.
- **Build:** passes, all 8 pages statically generated
- **Tests:** 19 Playwright tests pass (7 new), 0 axe-core violations across all pages
- **Human intervention:** no
- **Measurable outcome:** yes (0 WCAG 2 AA violations verified by automated scanning)

## Files Changed
- `marketing-site/package.json` — added @axe-core/playwright
- `marketing-site/src/app/globals.css` — spearmint color adjustment
- `marketing-site/src/components/CTA.tsx` — text opacity fix
- `marketing-site/src/components/Footer.tsx` — heading semantic fix
- `marketing-site/src/components/agents/AgentCTA.tsx` — text opacity fix
- `marketing-site/src/components/agents/HybridArchitecture.tsx` — text color fix
- `marketing-site/src/components/agents/MeetTheAgents.tsx` — badge color fixes
- `marketing-site/tests/marketing-site.spec.ts` — 7 new tests
