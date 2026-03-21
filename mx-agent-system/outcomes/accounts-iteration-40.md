# Accounts Iteration 40 — Replace debug prints with proper logging

**Date:** 2026-03-20
**PR:** #138
**Status:** Shipped

## What changed

The `import_service.py` had 11 `print(f"DEBUG: ...")` statements that output unconditionally to stdout. Replaced with `logger.debug()` calls that respect log level configuration.

## Before

- 11 print statements writing debug info to stdout on every import
- No way to suppress debug output in production
- Inconsistent with other services that use `logging.getLogger(__name__)`

## After

- All debug output uses `logger.debug()` with `%s` formatting
- Output respects log level configuration
- Consistent with transaction_service.py, classification_service.py patterns

## Human intervention

None

## Measurable outcome

Yes — 11 debug print statements eliminated from production stdout.
