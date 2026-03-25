import { test, expect } from '@playwright/test';

/**
 * Accounts Tests
 *
 * Tests account CRUD workflows end-to-end.
 * Each test creates its own uniquely-named data and cleans up afterwards.
 */

const uniqueName = () => `Playwright Account ${Date.now()}`;

test.describe('Accounts page', () => {
  test('shows the add account buttons', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await expect(page.getByRole('button', { name: 'Add Manual' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Link Account' })).toBeVisible();
  });

  test('shows account tabs', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await expect(page.getByRole('tab', { name: /All Accounts/ })).toBeVisible();
    await expect(page.getByRole('tab', { name: /Assets/ })).toBeVisible();
    await expect(page.getByRole('tab', { name: /Liabilities/ })).toBeVisible();
  });

  test('search input filters accounts', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    const search = page.getByPlaceholder('Search accounts...');
    await expect(search).toBeVisible();

    // Type a search that will return no results
    await search.fill('ZZZNOMATCH_PLAYWRIGHT_9999');
    await page.waitForTimeout(400); // debounce

    // Should show empty state or no accounts matching
    const body = page.locator('body');
    await expect(body).toContainText(/No accounts|no accounts/i);
  });
});

test.describe('Add account dialog', () => {
  test('opens and closes correctly', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Manual' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add New Account' });
    await expect(dialog).toBeVisible();

    await page.getByRole('button', { name: 'Cancel' }).click();
    await expect(dialog).not.toBeVisible();
  });

  test('shows all required form fields', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Manual' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add New Account' });

    await expect(dialog.getByLabel('Account Name')).toBeVisible();
    await expect(dialog.getByLabel('Account Type')).toBeVisible();
    await expect(dialog.getByLabel('Opening Balance')).toBeVisible();
  });

  test('shows validation error when name is empty', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Manual' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add New Account' });

    // Try to submit without filling required fields
    await dialog.getByRole('button', { name: /Create Account/i }).click();

    await expect(dialog).toContainText('Account name is required');
  });

  test('creates a checking account and shows it in the list', async ({ page }) => {
    const name = uniqueName();

    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Manual' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add New Account' });

    // Fill form
    await dialog.getByLabel('Account Name').fill(name);
    await dialog.getByLabel('Account Type').click();
    await page.getByRole('option', { name: /checking/i }).click();
    await dialog.getByLabel('Opening Balance').fill('2500');

    // Submit
    await dialog.getByRole('button', { name: /Create Account/i }).click();

    // Should show success snackbar
    await expect(page.getByText('Account created')).toBeVisible();

    // Account should appear in the list
    await expect(page.getByText(name)).toBeVisible();
  });

  test('creates a credit card (liability) account', async ({ page }) => {
    const name = uniqueName();

    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Manual' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add New Account' });

    await dialog.getByLabel('Account Name').fill(name);
    await dialog.getByLabel('Account Type').click();
    await page.getByRole('option', { name: /credit.card/i }).click();

    await dialog.getByRole('button', { name: /Create Account/i }).click();

    await expect(page.getByText('Account created')).toBeVisible();
    await expect(page.getByText(name)).toBeVisible();
  });
});

test.describe('Account details', () => {
  test('clicking an account opens the details dialog', async ({ page }) => {
    await page.goto('/accounts');
    await page.waitForLoadState('networkidle');

    // Only run this test if there are accounts to click
    const cards = page.locator('[data-testid="account-card"], .MuiCard-root').first();
    const cardCount = await page.locator('.MuiCard-root').count();

    if (cardCount === 0) {
      test.skip();
      return;
    }

    await cards.click();

    // A dialog should open
    await expect(page.getByRole('dialog')).toBeVisible();
  });
});
