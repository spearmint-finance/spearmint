# Accounts Iteration 26 — Replace Silent Exception Swallowing with Logged Warnings

**Date:** 2026-03-20
**PR:** #123
**Status:** Shipped

## Focus

Replace bare `except Exception: pass` blocks with logged warnings in transaction and classification services.

## What Changed

### Before
- 3 exception handlers silently swallowed ALL errors (including database failures) with bare `pass`
- No visibility into auto-classification or relationship linking failures

### After
- All 3 handlers now log warnings with transaction IDs and full exception info
- Non-fatal behavior preserved — exceptions don't break the request
- Failures visible in application logs for debugging
- Added `import logging` and `logger` to both services

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (3 silent exception handlers → 3 logged warnings)

## Verification
- PR #123 merged to main 2026-03-20T00:57:25Z
