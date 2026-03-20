# Accounts Iteration 25 — Entity Label on Account Cards

**Date:** 2026-03-20
**PR:** #122
**Status:** Shipped

## Focus

Show which entity each account belongs to on the AccountsPage cards.

## What Changed

### Before
- Account cards showed name, institution, type, balance, and last 4 digits
- No indication of which entity an account belonged to without opening the details dialog

### After
- Small info-colored chip showing entity name appears on account cards
- Only shown when "All Entities" is selected AND multiple entities exist
- Hidden when viewing a specific entity (redundant) or single-entity setups (no ambiguity)

## Metrics
- Human intervention needed: No
- Measurable outcome: Yes (0 → 1 entity label display on account cards)

## Verification
- PR #122 merged to main 2026-03-20T00:54:34Z
