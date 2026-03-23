# Accounts Iteration 98 — Holding Edit Capability

**Date:** 2026-03-23
**PR:** #251
**Status:** Shipped

## Focus
Add the ability to edit existing investment holdings in the portfolio tab.

## Changes
- **Backend:** Added `PUT /accounts/holdings/{holding_id}` endpoint with `HoldingUpdate` schema (all fields optional) and `update_holding` service method
- **Frontend:** Added edit icon button on each holding row. Clicking pre-fills the add/edit form with the holding's current values. Form title toggles between "New Holding" and "Edit Holding"
- **SDK bypass:** Portfolio summary endpoint now uses direct `fetch` to get correct snake_case field names (the SDK returned camelCase, causing `holding_id` to be undefined)

## Before / After
- **Before:** Holdings could only be created or deleted. Correcting a mistake required deleting and re-creating the holding.
- **After:** Holdings can be edited in-place — symbol, quantity, dates, cost basis, and current value can all be updated.

## Human intervention needed
No

## Measurable outcome
Yes — Playwright test confirms full add/edit/delete lifecycle works end-to-end.
