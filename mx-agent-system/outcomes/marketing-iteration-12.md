# Marketing Iteration 12 Outcome — 2026-03-15

## Focus
Performance — convert Hero and Features to server components

## What Changed
- Removed `"use client"` and framer-motion from Hero.tsx and Features.tsx
- Both now render as React Server Components (zero client JS)
- Hero content renders in initial HTML — improves LCP for above-the-fold
- Features grid renders statically with no hydration delay
- Combined with iteration 11: 4 of 13 client components now server components

## Lighthouse Scores
- Before: Deferred (no production deploy)
- After: Deferred (no production deploy)

## Validation
- Build passes
- ESLint clean
- 12/12 Playwright tests pass (39.1s, down from 41.9s)

## PR
- #79 — merged to main

## Human Intervention
- No

## Measurable Outcome
- Yes: 2 more components converted to server components, test suite 7% faster
