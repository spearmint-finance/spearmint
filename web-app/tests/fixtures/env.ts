/**
 * Environment configuration for E2E tests.
 * Override via environment variables when running in CI or non-default environments.
 *
 * Usage:
 *   BASE_URL=http://staging.example.com API_BASE_URL=http://api.staging.example.com npx playwright test
 */

export const BASE_URL = process.env.BASE_URL ?? 'http://localhost:5173';
export const API_BASE_URL = process.env.API_BASE_URL ?? 'http://localhost:8000';
