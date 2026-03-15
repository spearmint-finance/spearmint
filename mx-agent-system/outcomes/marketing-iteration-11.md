# Marketing Iteration 11 Outcome — 2026-03-15

## Focus
Performance — convert CTA and ValueProps from client to server components

## What Changed
- Removed `"use client"` and `framer-motion` imports from CTA.tsx and ValueProps.tsx
- Both components now render as React Server Components (zero JS sent to client)
- Decorative below-fold fade-in animations removed (content unchanged)
- Net: -46 lines added / +25 lines = -21 lines, 2 fewer client component boundaries

## Lighthouse Scores
- Before: Deferred (no production deploy)
- After: Deferred (no production deploy)

## Validation
- Build passes
- ESLint clean
- 12/12 Playwright tests pass

## PR
- #76 — merged to main

## Human Intervention
- No

## Measurable Outcome
- Yes: 2 components converted from client to server, reducing JS bundle
