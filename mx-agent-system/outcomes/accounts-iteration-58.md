# Accounts Iteration 58 — Fix entity assignment + boolean properties + splits + transfer categories

**Date:** 2026-03-21
**PR:** #184
**Status:** Shipped

## What changed

Fixed entity assignment silently failing due to SDK Zod strict mode stripping unknown fields (entityId, isCapitalExpense, boolean properties). Bypassed SDK with direct fetch for create/update in transactions API. Also fixed transaction splits and transfer category handling.

## Root cause

SDK's Zod `.object()` strict mode was dropping fields not in the schema definition before reaching the API. All boolean properties and entity_id were silently stripped.

## Human intervention

No

## Measurable outcome

Yes — entity assignment, boolean properties, and splits now persist correctly through create/update operations.
