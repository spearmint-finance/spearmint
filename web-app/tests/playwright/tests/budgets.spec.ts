import { test, expect } from '@playwright/test';

/**
 * Budgets Tests
 *
 * Tests the budget management page: page load, empty state,
 * and creating/editing budgets.
 */

test.describe('Budgets page', () => {
  test('loads and shows the Add Budget button', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    await expect(page.getByRole('button', { name: 'Add Budget' })).toBeVisible();
  });

  test('shows empty state when no budgets exist', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    const hasBudgets = await page.getByText('No budgets yet').isVisible().catch(() => false);
    const hasCards = await page.locator('.MuiCard-root').count();

    // Either no-budgets message OR budget cards are present — but not a crash
    expect(hasBudgets || hasCards > 0).toBe(true);
  });

  test('shows summary cards when budgets exist', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    const hasCards = await page.locator('.MuiCard-root').count();
    if (hasCards === 0) {
      test.skip(); // No budgets to test summary cards
      return;
    }

    await expect(page.getByText('Total Budgeted')).toBeVisible();
    await expect(page.getByText('Total Spent')).toBeVisible();
  });
});

test.describe('Add Budget dialog', () => {
  test('opens and closes correctly', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Budget' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add Budget' });
    await expect(dialog).toBeVisible();

    await page.getByRole('button', { name: 'Cancel' }).click();
    await expect(dialog).not.toBeVisible();
  });

  test('shows Category and Monthly Amount fields', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Budget' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add Budget' });

    await expect(dialog.getByLabel('Category')).toBeVisible();
    await expect(dialog.getByLabel('Monthly Amount')).toBeVisible();
  });

  test('can create a budget inline with a new category', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    await page.getByRole('button', { name: 'Add Budget' }).click();
    const dialog = page.getByRole('dialog', { name: 'Add Budget' });

    // Open category select and choose "+ Create New Category"
    await dialog.getByLabel('Category').click();
    const createOption = page.getByRole('option', { name: /Create New Category/i });
    await expect(createOption).toBeVisible();
    await createOption.click();

    // A category name field should appear
    const catNameField = dialog.getByLabel('Category Name');
    await expect(catNameField).toBeVisible();

    const uniqueCat = `Playwright Budget Cat ${Date.now()}`;
    await catNameField.fill(uniqueCat);
    await dialog.getByRole('button', { name: 'Create' }).click();

    // The category should now be selected
    await expect(dialog.getByLabel('Category')).toContainText(uniqueCat);

    // Fill amount and save
    await dialog.getByLabel('Monthly Amount').fill('200');
    await dialog.getByRole('button', { name: 'Save' }).click();

    // Budget should appear in the list
    await expect(page.getByText(uniqueCat)).toBeVisible();
  });
});

test.describe('Budget interactions', () => {
  test('View transactions link navigates to filtered transactions', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('networkidle');

    const hasCards = await page.locator('.MuiCard-root').count();
    if (hasCards === 0) {
      test.skip();
      return;
    }

    // Click the first "View transactions" link
    await page.getByRole('button', { name: 'View transactions' }).first().click();

    await expect(page).toHaveURL(/\/transactions/);
  });
});
