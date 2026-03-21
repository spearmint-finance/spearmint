# Accounts Iteration 39 — CSV export loading state

**Date:** 2026-03-20
**PR:** #137
**Status:** Shipped

## What changed

The Export CSV button on the transactions page had no loading/disabled state, allowing users to trigger multiple concurrent exports by clicking repeatedly. Added `isExporting` state with spinner icon, "Exporting..." text, and disabled button during export.

## Before

- Export CSV button remained clickable during export fetch
- No visual feedback that export was in progress
- Multiple concurrent exports possible

## After

- Button shows CircularProgress spinner and "Exporting..." text during export
- Button is disabled during export
- Returns to normal state on success or failure (via finally block)

## Human intervention

None

## Measurable outcome

Yes — UX improvement preventing duplicate exports. Consistent with existing Detect Relationships button pattern.
