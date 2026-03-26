import { test, expect, Page } from '@playwright/test';

/**
 * Smoke Tests
 *
 * Verify every page loads without crashing and key navigation works.
 * These tests work against any database state (empty or populated).
 */

const PAGES = [
  '/dashboard',
  '/accounts',
  '/transactions',
  '/budgets',
  '/analysis',
  '/reports',
  '/import',
  '/settings',
];

async function expectPageLoads(page: Page, path: string) {
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      const text = msg.text();
      // Ignore known non-fatal browser noise
      if (!text.includes('favicon') && !text.includes('net::ERR_')) {
        errors.push(text);
      }
    }
  });

  await page.goto(path);
  await page.waitForLoadState('load');

  // Page must not show an error boundary or unhandled crash
  await expect(page.locator('body')).not.toContainText('Something went wrong');
  await expect(page.locator('body')).not.toContainText('Cannot read properties of');

  // No unexpected JS errors
  expect(errors, `Console errors on ${path}: ${errors.join(', ')}`).toHaveLength(0);
}

test.describe('Page load smoke tests', () => {
  for (const path of PAGES) {
    test(`${path} loads without errors`, async ({ page }) => {
      await expectPageLoads(page, path);
    });
  }
});

test.describe('Navigation', () => {
  test('sidebar navigation links are all present', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('load');

    // Sidebar uses ListItemButton (role=button), not anchor tags
    const navItems = ['Dashboard', 'Accounts', 'Transactions', 'Budgets', 'Analysis', 'Settings'];
    for (const item of navItems) {
      await expect(page.getByRole('button', { name: item })).toBeVisible();
    }
  });

  test('clicking sidebar links navigates correctly', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: 'Accounts' }).click();
    await expect(page).toHaveURL(/\/accounts/);

    await page.getByRole('button', { name: 'Transactions' }).click();
    await expect(page).toHaveURL(/\/transactions/);

    await page.getByRole('button', { name: 'Budgets' }).click();
    await expect(page).toHaveURL(/\/budgets/);

    await page.getByRole('button', { name: 'Settings' }).click();
    await expect(page).toHaveURL(/\/settings/);
  });

  test('root path redirects to dashboard', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('unknown path redirects to dashboard', async ({ page }) => {
    await page.goto('/nonexistent-route');
    await expect(page).toHaveURL(/\/dashboard/);
  });
});
