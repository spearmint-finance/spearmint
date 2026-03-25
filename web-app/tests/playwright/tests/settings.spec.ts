import { test, expect } from '@playwright/test';

/**
 * Settings Tests
 *
 * Tests the settings page tabs: categories, transaction rules,
 * preferences, theme, and API keys.
 */

test.describe('Settings page', () => {
  test('loads and shows all tabs', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    await expect(page.getByRole('tab', { name: 'Categories' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Transaction Rules' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Preferences' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Theme' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'API Keys' })).toBeVisible();
  });

  test('defaults to Categories tab', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    const categoriesTab = page.getByRole('tab', { name: 'Categories' });
    await expect(categoriesTab).toHaveAttribute('aria-selected', 'true');
  });

  test('can switch between tabs', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    await page.getByRole('tab', { name: 'Transaction Rules' }).click();
    await expect(page.getByRole('tab', { name: 'Transaction Rules' })).toHaveAttribute('aria-selected', 'true');

    await page.getByRole('tab', { name: 'Preferences' }).click();
    await expect(page.getByRole('tab', { name: 'Preferences' })).toHaveAttribute('aria-selected', 'true');

    await page.getByRole('tab', { name: 'Theme' }).click();
    await expect(page.getByRole('tab', { name: 'Theme' })).toHaveAttribute('aria-selected', 'true');

    await page.getByRole('tab', { name: 'API Keys' }).click();
    await expect(page.getByRole('tab', { name: 'API Keys' })).toHaveAttribute('aria-selected', 'true');
  });
});

test.describe('Categories tab', () => {
  test('shows the category management grid', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    // The categories tab is default
    await expect(page.getByRole('tab', { name: 'Categories' })).toHaveAttribute('aria-selected', 'true');
    // Categories panel should be present (grid or list)
    await expect(page.locator('[role="tabpanel"]').first()).toBeVisible();
  });
});

test.describe('Transaction Rules tab', () => {
  test('shows the rules panel', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    await page.getByRole('tab', { name: 'Transaction Rules' }).click();
    await page.waitForLoadState('networkidle');

    // Rules panel should be rendered (grid or empty state)
    await expect(page.locator('[role="tabpanel"]').first()).toBeVisible();
  });
});

test.describe('API Keys tab', () => {
  test('shows API key section', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    await page.getByRole('tab', { name: 'API Keys' }).click();
    await page.waitForLoadState('networkidle');

    await expect(page.locator('[role="tabpanel"]').first()).toBeVisible();
  });
});
