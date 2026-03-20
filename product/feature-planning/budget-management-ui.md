# Product Requirements Document: Budget Management UI

**Product:** Spearmint Personal Finance Engine
**Feature:** Budget Management — Create, Track, and Adjust Budgets
**Owner:** Accounts Team
**Status:** Draft
**Last Updated:** 2026-03-20
**Gate:** G1 (Sovereign Foundation) / G2 (Intelligent Analyst)
**Priority:** P1

---

## Executive Summary

Budgeting is the #1 use case for personal finance applications. Every major competitor (YNAB, Actual Budget, Monarch Money, Firefly III) offers budget management. Spearmint has a `Budget` database model but no API endpoints and no frontend UI. This PRD defines the MVP budget management feature.

## Problem Statement

Users who download Spearmint to manage their finances expect to set spending limits by category and track progress against those limits. Without budgeting, Spearmint is an analysis tool — powerful but not a daily driver. This is the single largest feature gap for user adoption.

## User Stories

1. **As a user**, I want to set monthly spending limits for each category so I can control my spending.
2. **As a user**, I want to see how much I've spent vs. my budget for each category this month so I can adjust my behavior.
3. **As a user**, I want to be alerted when I'm close to exceeding a budget so I can act before overspending.
4. **As a user**, I want to reallocate unused budget from one category to another so my budget reflects my actual priorities.

## Scope

### In Scope (MVP)

#### Backend

1. **Enhance Budget model** — add `entity_id` (FK), `is_active` (boolean), `updated_at` (timestamp), `notes` (text). Add relationship to Category.
2. **Budget CRUD API** — `GET/POST/PUT/DELETE /api/budgets` with entity scoping
3. **Budget summary endpoint** — `GET /api/budgets/summary` returns budget vs. actual spending for the current period, with percentage used per category
4. **Budget period support** — Monthly budgets (MVP). The `period_type` column already supports Daily/Weekly/Monthly/Quarterly/Yearly but MVP only needs Monthly.

#### Frontend

5. **Budget page** — new route `/budgets` accessible from sidebar navigation
6. **Budget overview** — card layout showing each budget category with progress bar (green < 75%, yellow 75-90%, red > 90%)
7. **Add/edit budget form** — select category, set amount, set period
8. **Budget vs. actual chart** — bar chart comparing budgeted vs. actual spending by category
9. **Month selector** — navigate between months to see historical budget performance

### Out of Scope (Future)

- Envelope budgeting (drag-and-drop reallocation between categories) — G2
- Budget advisor agent integration — separate PRD exists
- Proactive alerts and notifications — G2
- Rollover of unused budget to next month — G2
- Multi-person budget tracking — G2
- Budget templates and quick-start wizards — G2

## Acceptance Criteria

1. User can create a budget for any existing category with a monthly amount
2. Budget overview page shows all active budgets with progress bars colored by utilization
3. Budget summary correctly calculates actual spending from transactions in the budget period
4. Budgets are scoped to the active entity (consistent with accounts and transactions)
5. Budget data persists across sessions
6. Page is responsive (works on mobile viewport)
7. Empty state with CTA when no budgets exist

## Technical Notes

- The `Budget` model exists at `core-api/src/financial_analysis/database/models.py:351-373` — needs enhancement
- Category relationship already exists via `category_id` FK
- Actual spending can be calculated by summing transactions for the category within the budget period (similar logic to expense reports)
- Entity scoping pattern is established in accounts and transactions — follow the same pattern

## Competitive Reference

| Competitor | Budget Feature |
|------------|---------------|
| YNAB | Envelope budgeting with drag-and-drop reallocation — the gold standard |
| Actual Budget | Envelope budgeting, rollover, goal tracking |
| Monarch Money | Category budgets with progress bars, rollover |
| Firefly III | Category budgets, auto-generated, piggy banks |
| Spearmint (current) | DB model only — no API, no UI |

## Success Metrics

- Users can create and track budgets within 2 minutes of first visit to the budget page
- Budget page loads in < 1 second
- Feature parity with Firefly III's basic budget functionality
