# Accounts Iteration 55 — Multi-entity assignment for accounts

**Date:** 2026-03-21
**PR:** #177
**Status:** Shipped

## What changed

Accounts can now belong to multiple entities via a many-to-many relationship (account_entities join table). Supports shared accounts like a checking account used for both personal and business.

## Human intervention

Yes — user requested multi-entity accounts.

## Measurable outcome

Yes — new feature: multi-entity account assignment with multi-select UI.
