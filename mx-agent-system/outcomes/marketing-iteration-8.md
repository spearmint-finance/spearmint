# Marketing Iteration 8 — Sitemap & robots.txt

**Date:** 2026-03-14
**PR:** #63 (merged)
**Focus:** Add robots.txt and sitemap.xml for search engine crawling

## What Changed
- Added `public/robots.txt` allowing all crawlers with sitemap reference
- Added `public/sitemap.xml` listing all 5 pages with priority weights
- Static files compatible with `output: "export"` config

## Metrics
- **North Star (Lighthouse UX Score):** Before: deferred. After: deferred.
- **SEO:** robots.txt and sitemap ready for crawler indexing once deployed

## Human Intervention
- No

## Measurable Outcome
- Yes — both files present in build output, verifiable post-deploy
