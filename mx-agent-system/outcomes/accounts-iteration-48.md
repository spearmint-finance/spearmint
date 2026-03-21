# Accounts Iteration 48 — Boolean transaction properties + analysis query update

**Date:** 2026-03-21
**PR:** #170
**Status:** Shipped

## What changed

Added boolean computed properties to the transaction model for common attribute checks (e.g., is_recurring, is_tax_deductible), derived from the tag system. Updated analysis queries to use these properties.

## Before

- Checking transaction attributes required manual tag lookups
- Analysis queries used raw tag string comparisons

## After

- Boolean properties on transaction model for quick attribute checks
- Analysis queries use boolean properties for cleaner logic

## Verification

- Backend tests pass
- Boolean properties correctly reflect tag state

## Human intervention

Yes — user directed the boolean properties approach.

## Measurable outcome

Yes — cleaner API surface for transaction attribute checks.
