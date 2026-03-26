import { test, expect } from '@playwright/test';

/**
 * Transactions Tests
 *
 * Tests transaction listing, filtering, creation, and editing.
 * Works against any database state.
 */

const API = 'http://localhost:8000/api';

test.describe('Transactions page layout', () => {
  test('shows toolbar buttons', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await expect(page.getByRole('button', { name: 'New Transaction' })).toBeVisible();
    await expect(page.getByRole('button', { name: /Export CSV/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Smart Categorize/i })).toBeVisible();
  });

  test('shows search input and filter button', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await expect(page.getByPlaceholder('Search transactions...')).toBeVisible();
    await expect(page.getByRole('button', { name: /More Filters/i })).toBeVisible();
  });

  test('shows summary stat cards', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    // Stat cards render after API data loads — give extra time
    await expect(page.getByText('Total Income')).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('Total Expenses')).toBeVisible();
    await expect(page.getByText('Net Income')).toBeVisible();
  });
});

test.describe('Transaction search and filtering', () => {
  test('search input triggers a filtered result', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    const search = page.getByPlaceholder('Search transactions...');
    await search.fill('ZZZNOMATCH_PLAYWRIGHT_9999');
    await page.waitForTimeout(800); // debounce + API round-trip

    await expect(page.getByText(/No transactions match/i)).toBeVisible({ timeout: 10000 });
  });

  test('clear all button appears when search is active', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    const search = page.getByPlaceholder('Search transactions...');
    await search.fill('test');
    await page.waitForTimeout(200);

    await expect(page.getByRole('button', { name: 'Clear All' })).toBeVisible();

    await page.getByRole('button', { name: 'Clear All' }).click();
    await expect(search).toHaveValue('');
  });

  test('More Filters dialog opens and closes', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: /More Filters/i }).click();
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    // Filters dialog uses "Cancel" button to close
    await dialog.getByRole('button', { name: 'Cancel' }).click();
    await expect(dialog).not.toBeVisible();
  });

  test('filters dialog contains expected filter fields', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: /More Filters/i }).click();
    const dialog = page.getByRole('dialog');

    await expect(dialog.getByLabel(/Start Date/i)).toBeVisible();
    await expect(dialog.getByLabel(/End Date/i)).toBeVisible();
  });

  test('URL params pre-populate account filter', async ({ page }) => {
    // When navigating from another page with account_id, filter is applied
    await page.goto('/transactions?account_id=999999');
    await page.waitForLoadState('load');
    // Page should load without crashing — filter just produces empty results
    await expect(page.locator('body')).not.toContainText('Something went wrong');
  });
});

test.describe('New transaction form', () => {
  test('form opens when New Transaction is clicked', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: 'New Transaction' }).click();

    // A dialog should appear with the transaction form
    const dialog = page.getByRole('dialog');
    await expect(dialog.getByRole('textbox', { name: 'Description' })).toBeVisible();
    await expect(dialog.getByRole('spinbutton', { name: 'Amount' })).toBeVisible();
    await expect(dialog.getByLabel('Date')).toBeVisible();
  });

  test('can create a transaction when an account exists', async ({ page, request }) => {
    // Create an account via API so we have one to attach the transaction to
    const accountRes = await request.post(`${API}/accounts`, {
      data: {
        account_name: `Playwright Txn Test Account ${Date.now()}`,
        account_type: 'checking',
        currency: 'USD',
        opening_balance: 0,
      },
    });

    if (!accountRes.ok()) {
      test.skip(); // Can't create account — skip test
      return;
    }

    const account = await accountRes.json();
    const accountId = account.account_id;

    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: 'New Transaction' }).click();
    await page.waitForTimeout(300);

    const txDialog = page.getByRole('dialog');
    await txDialog.getByRole('textbox', { name: 'Description' }).fill('Playwright Test Transaction');
    await txDialog.getByRole('spinbutton', { name: 'Amount' }).fill('42.00');

    // Clear and set the date field — scope to dialog to avoid DataGrid column header match
    const dateField = txDialog.getByLabel('Date');
    await dateField.clear();
    await dateField.fill('2024-01-15');

    // Select a category (required field) — pick the first real option (skip placeholder at index 0)
    const categorySelect = txDialog.getByRole('combobox', { name: 'Category' });
    if (await categorySelect.isVisible()) {
      await categorySelect.click();
      const firstRealOption = page.getByRole('option').nth(1);
      if (await firstRealOption.isVisible()) {
        await firstRealOption.click();
      }
    }

    await page.getByRole('button').filter({ hasText: /^(Save|Create|Submit)$/i }).click();

    // Success snackbar or transaction appears in list
    const success = page.getByText(/Transaction (created|updated|saved)/i);
    const inGrid = page.getByText('Playwright Test Transaction');
    await expect(success.or(inGrid)).toBeVisible({ timeout: 10000 });

    // Cleanup: delete account via API
    await request.delete(`${API}/accounts/${accountId}`);
  });
});

test.describe('Smart Categorize dialog', () => {
  test('Smart Categorize button opens the dialog', async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('load');

    await page.getByRole('button', { name: /Smart Categorize/i }).click();

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();
    await expect(dialog.getByText('Smart Categorization')).toBeVisible();

    // Close it — use the text button (not the icon button)
    await dialog.getByRole('button', { name: 'Close' }).last().click();
    await expect(dialog).not.toBeVisible();
  });
});
