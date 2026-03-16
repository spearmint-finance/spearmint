# Marketing Iteration 16 — Centralize Config & Dynamic Sitemap/Robots

**Date:** 2026-03-16
**PR:** #96 (merged)
**Focus:** Centralize hardcoded URLs into config.ts and generate sitemap/robots from code

## What Changed
- Created `src/config.ts` with SITE_URL, GITHUB_URL, GITHUB_DOCS_URL
- Replaced 6 hardcoded GitHub URLs across 7 components with config imports
- Converted static `public/sitemap.xml` → `src/app/sitemap.ts` (Next.js Metadata API)
- Converted static `public/robots.txt` → `src/app/robots.ts` (Next.js Metadata API)
- Updated `layout.tsx` metadataBase to use shared SITE_URL
- Updated `JsonLd.tsx` to use shared SITE_URL and GITHUB_URL

## Metrics
- **North Star (Lighthouse UX Score):** Before: deferred. After: deferred.
- **Build:** passes, 10 routes including generated sitemap.xml and robots.txt
- **Tests:** 19 Playwright tests pass, 0 axe violations
- **Human intervention:** no
- **Measurable outcome:** yes (0 hardcoded URLs outside config.ts; sitemap/robots env-configurable)

## Files Changed
- `marketing-site/src/config.ts` — NEW: centralized site configuration
- `marketing-site/src/app/sitemap.ts` — NEW: replaces public/sitemap.xml
- `marketing-site/src/app/robots.ts` — NEW: replaces public/robots.txt
- `marketing-site/public/sitemap.xml` — DELETED
- `marketing-site/public/robots.txt` — DELETED
- `marketing-site/src/app/layout.tsx` — use SITE_URL from config
- `marketing-site/src/app/pricing/page.tsx` — use GITHUB_URL from config
- `marketing-site/src/components/Header.tsx` — use GITHUB_URL from config
- `marketing-site/src/components/Hero.tsx` — use GITHUB_URL from config
- `marketing-site/src/components/CTA.tsx` — use GITHUB_URL from config
- `marketing-site/src/components/Footer.tsx` — use GITHUB_URL, GITHUB_DOCS_URL from config
- `marketing-site/src/components/JsonLd.tsx` — use SITE_URL, GITHUB_URL from config
- `marketing-site/src/components/agents/AgentCTA.tsx` — use GITHUB_URL from config
