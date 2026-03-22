# Product Requirements Document: Authentication & Authorization

**Product:** Spearmint Personal Finance Engine
**Feature:** User Authentication, Session Management, and Access Control
**Owner:** Accounts / Platform Team
**Status:** Draft
**Last Updated:** 2026-03-22
**Gate:** G1 (Sovereign Foundation)
**Priority:** P0 — Critical blocker for real-world deployment
**Directive:** #141
**Related Known Issue:** PKI-001

---

## Executive Summary

Spearmint has **zero user authentication**. Every API endpoint is publicly accessible. There is no User model, no login page, no session management, no protected routes, and no auth middleware. The app cannot be exposed to any network — not even a home LAN — without risking complete data exposure. This is the single largest blocker to real-world adoption and is rated P0.

This PRD scopes a **minimal, self-hosted-friendly authentication system** that gets Spearmint from "completely open" to "securely usable by a household." It deliberately avoids complex multi-tenancy, OAuth federation, and enterprise RBAC — those are future enhancements if needed.

## Problem Statement

**Current behavior:** Any HTTP client on the network can read, modify, or delete all financial data. A user who runs `docker-compose up -d` and exposes port 80 is immediately vulnerable.

**Target behavior:** Users must register and log in. API requests require a valid JWT token. The frontend redirects unauthenticated users to a login page. Each user sees only their own data.

## Current State

### What exists
- **API key authentication** for MCP server clients (Claude Desktop, Gemini CLI) — `POST /api/auth/api-keys` with SHA-256 hashed keys
- **Person model** for transaction attribution (not users — persons don't have credentials)
- **Entity model** for multi-entity accounting (personal, business, rental property)
- CORS configured (but allows all origins in dev)
- Nginx reverse proxy with no auth layer

### What's completely missing
- User model / table
- Registration and login flows
- Password hashing (no bcrypt/argon2 in dependencies)
- JWT token issuance and verification (no python-jose in dependencies)
- Auth middleware on any API route
- Protected routes in the frontend
- Auth context / hook in React
- Session management of any kind
- User-data isolation

## User Stories

1. **As a new user**, I want to create an account with email and password so I can start using Spearmint.
2. **As a returning user**, I want to log in and have the app remember my session so I don't need to re-authenticate on every visit.
3. **As a user**, I want to be confident that no one else on my network can see my financial data without my credentials.
4. **As a self-hosted admin**, I want a simple setup that doesn't require configuring external OAuth providers or identity services.
5. **As a household**, we want multiple users to each have their own login and see their own entities and data.

## Scope

### In Scope (MVP)

#### Backend

1. **User model** — New database table: `id`, `email` (unique), `password_hash`, `display_name`, `is_active`, `is_admin`, `created_at`, `updated_at`. Relationship: User has many Entities.

2. **Registration endpoint** — `POST /api/auth/register` with email, password, display name. First user automatically becomes admin. Password hashed with bcrypt (via passlib).

3. **Login endpoint** — `POST /api/auth/login` returns a JWT access token (short-lived, 15 min) and a refresh token (long-lived, 7 days). Uses python-jose for JWT.

4. **Token refresh endpoint** — `POST /api/auth/refresh` exchanges a valid refresh token for a new access token.

5. **Auth middleware** — FastAPI dependency (`get_current_user`) that extracts and validates JWT from `Authorization: Bearer <token>` header. Applied to ALL routes except `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`, and `/api/health`.

6. **User-data isolation** — Entities gain a `user_id` foreign key. All queries filter by `current_user.id`. A user can only see their own entities, accounts, transactions, and derived data (reports, projections, scenarios).

7. **Existing API key auth preserved** — MCP API keys continue to work. API keys gain a `user_id` foreign key so MCP clients act on behalf of a specific user.

8. **Password requirements** — Minimum 8 characters. No other complexity rules (avoid annoying users who are managing their own self-hosted instance).

#### Frontend

9. **Login page** — Email and password form at `/login`. Clean, minimal design matching existing UI.

10. **Registration page** — Email, password, confirm password, display name at `/register`. Only shown during initial setup or when admin invites.

11. **Auth context** — React context providing `user`, `isAuthenticated`, `login()`, `logout()`, `register()`. Stores JWT in `localStorage` (acceptable for self-hosted; HttpOnly cookies are a future enhancement).

12. **Protected routes** — All existing routes wrapped in an auth guard that redirects to `/login` if no valid token exists.

13. **Axios interceptor** — Automatically attaches `Authorization: Bearer <token>` to all API requests. On 401 response, attempts token refresh; if refresh fails, redirects to login.

14. **Logout** — Clears tokens from localStorage, redirects to login.

#### Configuration

15. **Environment variables** — `JWT_SECRET` (required, generated on first run if not set), `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` (default 15), `JWT_REFRESH_TOKEN_EXPIRE_DAYS` (default 7).

16. **Database migration** — Alembic migration adding `users` table and `user_id` FK to `entities` and `api_keys` tables.

### Out of Scope (Future Enhancements)

- OAuth/OIDC external providers (Google, GitHub login)
- Multi-factor authentication (TOTP, WebAuthn)
- Role-based access control beyond admin/user
- Password reset via email (requires SMTP — not available in all self-hosted setups)
- HttpOnly cookie-based sessions (current: localStorage JWT)
- Account lockout after failed attempts
- Audit logging of auth events
- Admin user management UI
- SSO / SAML
- Rate limiting on auth endpoints

## Acceptance Criteria

1. A new Spearmint instance prompts for registration (first user becomes admin)
2. Subsequent visitors see a login page — cannot access any data without credentials
3. All API endpoints (except auth + health) return 401 without a valid JWT
4. Logged-in users see only their own entities, accounts, and transactions
5. JWT access tokens expire after 15 minutes; refresh tokens after 7 days
6. Existing MCP API key auth continues to work (keys now scoped to a user)
7. Password stored as bcrypt hash — never in plaintext
8. `docker-compose up -d` still works — JWT_SECRET auto-generated if not provided
9. No external service dependencies (no OAuth provider, no SMTP required)
10. Existing data migration: on first startup after auth is added, all existing entities are assigned to the first registered user

## Technical Approach (Guidance, Not Prescription)

The implementation team decides the "how." This section provides context.

**Recommended dependencies:**
- `passlib[bcrypt]` for password hashing
- `python-jose[cryptography]` for JWT
- Both are standard, well-maintained, and commonly used with FastAPI

**Migration strategy for existing data:**
- The `users` table is new — no data to migrate
- `entities.user_id` is added as nullable initially
- After the first user registers, a migration script assigns all orphaned entities to that user
- Then `user_id` is made non-nullable

**Auth middleware pattern (FastAPI):**
```python
# Pseudocode — implementation team decides actual structure
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401)
    return user
```

**Frontend auth pattern:**
- AuthContext wraps the app at the top level
- ProtectedRoute component checks `isAuthenticated` before rendering children
- Axios request interceptor adds Bearer token
- Axios response interceptor handles 401 → refresh → retry flow

## Competitive Reference

| Competitor | Auth Approach |
|------------|--------------|
| Firefly III | Email/password, OAuth optional, API tokens |
| Actual Budget | Local password (file-level), no multi-user |
| Monarch Money | Email/password + Google SSO |
| YNAB | Email/password + Apple/Google SSO |
| **Spearmint (current)** | None — completely open |
| **Spearmint (target)** | Email/password with JWT. Simple, self-hosted-friendly, no external dependencies. |

Firefly III's approach is the closest model — email/password as the primary auth method with API tokens for integrations. Spearmint already has API tokens; this PRD adds the user auth layer.

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Passwords in plaintext | bcrypt hashing (cost factor 12) — never stored or logged in plaintext |
| JWT secret exposure | Generated per-instance, stored in environment variable, not in codebase |
| Token theft from localStorage | Acceptable risk for self-hosted (user controls their browser). Future: move to HttpOnly cookies. |
| Brute force login | Out of scope for MVP. Future: rate limiting + account lockout. |
| SQL injection in auth queries | SQLAlchemy parameterized queries (standard across codebase) |
| CORS misconfiguration | Tighten CORS to specific origin in production (currently allows all) |

## Success Metrics

| Metric | Target |
|--------|--------|
| All non-auth API endpoints return 401 without token | Yes |
| First-run setup creates admin user | Yes |
| Multi-user data isolation verified | Yes (user A cannot see user B's entities) |
| Existing MCP API key flow unbroken | Yes |
| No plaintext passwords anywhere (DB, logs, API responses) | Yes |
| Docker quick-start still works without manual JWT_SECRET config | Yes |

## Dependencies

- **Database migration tooling** — Alembic must be configured and working
- **No external services** — This is a pure backend + frontend change

## Risks

| Risk | Mitigation |
|------|------------|
| Breaking existing data (entities have no user_id) | Careful migration: nullable FK → assign to first user → make non-nullable |
| MCP API key auth regression | Test MCP flows explicitly after auth middleware is added |
| Self-hosted users forgetting password (no email reset) | Document: admin can reset via CLI. Future: add email-based reset when SMTP is available. |
| Scope creep into OAuth/RBAC | PRD explicitly excludes these. Implementation team should resist. |
