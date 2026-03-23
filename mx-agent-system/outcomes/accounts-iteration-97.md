# Accounts Iteration 97 — Transaction Rule Form Validation + SDK Bypass

**Date:** 2026-03-23
**PR:** #249
**Status:** Shipped

## Focus
Improve transaction rule form validation and fix SDK incompatibility preventing entity-only rule creation.

## Changes
- **SDK bypass for rule CRUD**: All category rule API calls (list, get, create, update, delete, test, apply) now use direct `fetch` instead of the SDK, which required `categoryId` and lacked `entityId`
- **Frontend form validation**: Rules must have at least one assignment target (category or entity), at least one matching pattern, and valid amount ranges. Errors shown via MUI Alert component
- **Backend validation**: Rule updates now reject removal of both category and entity assignments
- **Rule application improvements**: Category and entity assignments tracked separately; `entity_assigned_count` shown in Apply Rules results dialog
- **Playwright tests**: 4 tests covering validation errors, rule creation, and apply results

## Before / After
- **Before:** Creating an entity-only rule failed with SDK validation error. Form used `window.alert()` for validation. Rule application didn't distinguish category vs entity assignments.
- **After:** Entity-only rules can be created. Form shows inline Alert errors. Apply dialog shows both category and entity assignment counts.

## Human intervention needed
No

## Measurable outcome
Yes — 4 Playwright tests pass confirming form validation and CRUD functionality.
