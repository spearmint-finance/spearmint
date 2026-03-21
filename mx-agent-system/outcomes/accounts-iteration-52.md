# Accounts Iteration 52 — Fix entity creation failing on submit

**Date:** 2026-03-21
**PR:** #174
**Status:** Shipped

## What changed

Entity creation failed when the user hit submit because the frontend API calls used trailing slashes (`/api/entities/`), which triggered a FastAPI 307 redirect. When running through the Vite dev proxy, the redirect Location header pointed to the backend host directly (port 8000), causing the browser to bypass the proxy.

## Root cause

FastAPI's `redirect_slashes=True` (default) redirects `POST /api/entities/` to `POST /api/entities` via 307. The Vite dev proxy set `changeOrigin: true`, causing the redirect Location to use the backend host. The browser followed the redirect directly to the backend, bypassing the proxy.

## Before

- Entity creation failed silently on submit in dev mode
- Snackbar showed error message

## After

- Entity creation works reliably
- No 307 redirect needed — calls hit the route directly

## Verification

- TestClient: entity creation returns 201 without trailing slash
- Vite build succeeds

## Human intervention

Yes — user reported the bug.

## Measurable outcome

Yes — entity creation now works.
