# Marketing Iteration 10 Outcome — 2026-03-15

## Focus
JSON-LD structured data + unused asset cleanup

## What Changed
- Created `JsonLd.tsx` component with Organization, WebSite, SoftwareApplication, and BreadcrumbList schemas
- Added Organization + WebSite JSON-LD to all pages via layout
- Added SoftwareApplication JSON-LD to homepage
- Added BreadcrumbList JSON-LD to all 4 subpages (features, how-it-works, pricing, agents)
- Removed 5 unused placeholder SVGs from public/ (file.svg, globe.svg, next.svg, vercel.svg, window.svg)

## Lighthouse Scores
- Before: Deferred (no production deploy)
- After: Deferred (no production deploy)

## Validation
- Build passes
- ESLint clean
- 12/12 Playwright tests pass
- JSON-LD verified in static HTML output for all 6 pages

## PR
- #70 — merged to main

## Human Intervention
- No

## Measurable Outcome
- Yes: 3 schema types (Organization, WebSite, SoftwareApplication) + BreadcrumbList on 4 subpages rendered in build output; 5 unused files removed
