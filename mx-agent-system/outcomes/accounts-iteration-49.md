# Accounts Iteration 49 — Migrate getTransactions from direct fetch to SDK

**Date:** 2026-03-21
**PR:** #171
**Status:** Shipped

## What changed

Migrated the `getTransactions` function from a manual `fetch` call with hand-built URL and query params to the SDK's `transactionsApi.listTransactions()` method.

## Before

- `getTransactions` used raw `fetch()` with manual URLSearchParams construction
- Comment stated: "SDK v0.0.15 predates the account_id query param"
- Imported the default `sdk` object just to extract the base URL
- Inconsistent with all other transaction CRUD operations which used the SDK

## After

- All transaction API functions now use the SDK consistently
- Removed manual URL/query param construction (30+ lines)
- Removed unused `sdk` default import
- SDK handles serialization, base URL, and request formatting

## Verification

- TypeScript: no new errors in transactions.ts
- Vite production build: succeeds
- 136 backend tests: all pass
- PR #171 merged and deployed

## Human intervention

No — autonomous gap selection and implementation.

## Measurable outcome

Yes — KI-011 resolved. All 5 transaction API functions now use the SDK consistently.
