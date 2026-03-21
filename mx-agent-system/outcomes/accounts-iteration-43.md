# Accounts Iteration 43 — Fix transaction import on fresh installations

**Date:** 2026-03-20
**PR:** #143
**Status:** Shipped

## What changed

Transaction import failed with a raw SQL error ("no such table: transactions") on fresh installations because the database tables weren't auto-created on app startup. Users had to manually run `init_db.py` first.

## Root cause

The FastAPI app had no startup event to ensure database tables exist. The import service caught the `OperationalError` as a generic `Exception` and exposed the full SQL query in the user-facing error message.

## Changes

1. Added `on_event("startup")` to `main.py` that calls `Base.metadata.create_all()` to auto-create tables
2. Added `OperationalError` catch in `import_service.py` with user-friendly message
3. Replaced stray `print()` in `import_routes.py` with proper logger

## Before

- Fresh install → import error with raw SQL in response
- User had to manually run `init_db.py` before using the app

## After

- Tables auto-created on app startup
- Database errors show: "Database is not properly initialized. Please contact support or restart the application."
- No raw SQL leaks in user-facing errors

## Verification

- Fresh DB: 10179/10262 rows imported successfully (83 internal duplicates skipped)
- Missing tables: clean error message, no SQL leak
- 173 backend tests pass

## Human intervention

Yes — user reported the error, which triggered this investigation.

## Measurable outcome

Yes — import now works out of the box on fresh installations.
