# Accounts Iteration 41 — Normalize "nan" category names in data layer (KI-012)

**Date:** 2026-03-20
**PR:** #139
**Status:** Shipped

## What changed

The "nan" string comparison hack in TransactionList.tsx (KI-012) was duplicated in two locations and fragile. Moved the normalization to the `transformTransaction` data layer in `transactions.ts`, so UI components simply check for falsy values.

## Before

- Two locations in TransactionList.tsx checked `categoryName === "nan"`
- Logic duplicated and fragile (case-sensitive, string-specific)
- Root cause: pandas NaN values serialized as "nan" string during import

## After

- `transformTransaction` normalizes "nan", empty, and whitespace-only values to `undefined` for both `category_name` and `classification_name`
- TransactionList checks simplified to `!categoryName`
- Single source of truth for NaN handling

## Human intervention

None

## Measurable outcome

Yes — KI-012 resolved. Duplicated UI hack replaced with centralized data normalization.
