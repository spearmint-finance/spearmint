# Marketing Iteration 3 — CI/CD Pipeline for Cloudflare Pages

**Date:** 2026-03-14
**PR:** #58 (merged)
**Focus:** Create CI/CD pipeline to unblock deployments and Lighthouse measurement

## What Changed
- Created `.github/workflows/marketing-site-deploy.yml` with path-filtered triggers on `main` and `marketing-production`
- Configured `next.config.ts` with `output: "export"` for static site generation
- Concurrency groups prevent deploy queue stacking
- Uses `cloudflare/wrangler-action@v3` for Pages deployment

## Metrics
- **North Star (Lighthouse UX Score):** Before: deferred. After: still deferred — Cloudflare secrets not yet configured.
- **Build:** passes in CI (5 pages statically generated)
- **Deploy:** blocked — `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` secrets need to be added by repo admin

## Blocker
- Repo admin must configure Cloudflare secrets in GitHub repo settings before deploys will work

## Human Intervention
- Required: repo admin must add Cloudflare secrets

## Measurable Outcome
- Partial — pipeline runs, build succeeds, deploy blocked on secret configuration
