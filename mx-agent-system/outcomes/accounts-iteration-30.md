# Accounts Iteration 30 — Batch Clear Transaction List Validation

**Date:** 2026-03-20
**PR:** #127
**Status:** Shipped

## Focus

Add input validation to transaction batch clear endpoint to prevent empty and oversized requests.

## What Changed

### Before
- TransactionClearRequest accepted any size list including empty
- Empty lists silently returned 0 cleared
- No upper bound — could submit 10,000+ IDs

### After
- min_length=1: rejects empty transaction_ids lists (422)
- max_length=1000: caps batch size at 1000 IDs (422)
- Pydantic schema validation — automatic 422 response

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 2 list bounds added)

## Verification
- PR #127 merged to main 2026-03-20T01:13:14Z
