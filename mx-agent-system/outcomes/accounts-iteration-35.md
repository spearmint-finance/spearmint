# Accounts Iteration 35 — Account Count in Entity Switcher

**Date:** 2026-03-20
**PR:** #132
**Status:** Shipped

## Focus

Show account count per entity in the sidebar entity switcher dropdown.

## What Changed

### Before
- Entity dropdown showed entity name and type label only

### After
- Shows account count alongside type label: "Business · 3"
- Only displayed when account_count > 0

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 account count display in entity switcher)

## Verification
- PR #132 merged to main 2026-03-20T01:41:21Z
