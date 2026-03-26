import { test, expect } from '@playwright/test';

/**
 * Budgets Tests
 *
 * Tests the budget management page: page load, empty state,
 * and creating/editing budgets.
 */

/** Click the primary "Add Budget" button in the page header */
async function clickAddBudget(page: any) {
  await page.getByRole('button', { name: 'Add Budget' }).first().click();
}

test.describe('Budgets page', () => {
  test('loads and shows the Add Budget button', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

    await expect(page.getByRole('button', { name: 'Add Budget' }).first()).toBeVisible();
  });

  test('shows empty state when no budgets exist', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

    // Wait for either the empty state message or budget cards to appear
    // (LinearProgress shows while loading, then one of these replaces it)
    await expect(
      page.getByText('No budgets yet').or(page.locator('.MuiCard-root').first())
    ).toBeVisible({ timeout: 10000 });
  });

  test('shows summary cards when budgets exist', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

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
    await page.waitForLoadState('load');

    await clickAddBudget(page);
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    await dialog.getByRole('button', { name: 'Cancel' }).click();
    await expect(dialog).not.toBeVisible();
  });

  test('shows Category and Monthly Amount fields', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

    await clickAddBudget(page);
    const dialog = page.getByRole('dialog');

    await expect(dialog.getByLabel('Category')).toBeVisible();
    await expect(dialog.getByLabel('Monthly Amount')).toBeVisible();
  });

  test('can create a budget inline with a new category', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

    await clickAddBudget(page);
    const dialog = page.getByRole('dialog');

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

    // The category should now be selected (wait for React Query to refetch categories)
    // Use role=combobox to target only the Category select (not the Category Name text field)
    await expect(dialog.getByRole('combobox', { name: 'Category' })).toContainText(uniqueCat, { timeout: 8000 });

    // Fill amount and save
    await dialog.getByLabel('Monthly Amount').fill('200');
    await dialog.getByRole('button', { name: 'Create' }).click();

    // Wait for dialog to close, then budget card should appear in the list
    await expect(dialog).not.toBeVisible({ timeout: 5000 });
    await expect(page.getByRole('heading', { name: uniqueCat })).toBeVisible({ timeout: 10000 });
  });
});

test.describe('Budget interactions', () => {
  test('View transactions link navigates to filtered transactions', async ({ page }) => {
    await page.goto('/budgets');
    await page.waitForLoadState('load');

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
