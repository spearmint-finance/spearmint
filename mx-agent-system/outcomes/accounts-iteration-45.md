# Accounts Iteration 45 — Import fixes + SDK v0.0.95 + CI pipeline fix

**Date:** 2026-03-20
**PRs:** #154-163
**Status:** Shipped

## What changed

Multi-PR iteration addressing import reliability, SDK regeneration, and CI pipeline stability.

## Key changes

1. **Import fixes** (#154-155): SDK field name normalization for import payloads, nginx upload limit increase
2. **SDK v0.0.95** (#157-163): LibLab-generated SDK with ~70 method renames to match updated API surface, Transfer support
3. **CI pipeline fix**: Trailing slash issue in swagger-jsdoc causing build failures

## Before

- Import failed on large files due to nginx upload limit
- SDK method names out of sync with API after transfer refactor
- CI pipeline intermittently failing

## After

- Import handles large files reliably
- SDK v0.0.95 published with all method names aligned
- CI pipeline fully green

## Verification

- Full import cycle tested with 10K+ transactions
- SDK integration tests passing
- CI pipeline green on all PRs

## Human intervention

Yes — user coordinated SDK regeneration with LibLab.

## Measurable outcome

Yes — import reliability restored, SDK fully aligned with API.
