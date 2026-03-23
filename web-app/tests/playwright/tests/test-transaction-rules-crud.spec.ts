import { test, expect } from '@playwright/test';

test.describe('Transaction Rules CRUD', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    await page.waitForLoadState('networkidle');
    await page.getByRole('tab', { name: /Transaction Rules/i }).click();
    await page.waitForTimeout(500);
  });

  test('validation: shows error when no assignment target selected', async ({ page }) => {
    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);

    const dialog = page.getByRole('dialog');

    // Fill in rule name and a pattern but no category or entity
    await dialog.getByLabel('Rule Name').fill('Test No Assignment');
    await dialog.getByLabel('Description Pattern').fill('%test%');

    // Submit via the Create button
    await dialog.getByRole('button', { name: 'Create' }).click();
    await page.waitForTimeout(500);

    // Should show error alert in the dialog
    const errorAlert = dialog.locator('.MuiAlert-standardError');
    await expect(errorAlert).toBeVisible({ timeout: 3000 });
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rules-no-assignment-error.png' });
  });

  test('validation: shows error when no pattern provided', async ({ page }) => {
    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);

    const dialog = page.getByRole('dialog');

    // Fill in rule name only
    await dialog.getByLabel('Rule Name').fill('Test No Pattern');

    // Select a category via the combobox
    const categoryCombobox = dialog.getByRole('combobox').first();
    await categoryCombobox.click();
    await page.waitForTimeout(300);
    // Pick the first non-None option
    const options = page.getByRole('option');
    const optCount = await options.count();
    if (optCount > 1) {
      await options.nth(1).click();
    } else if (optCount > 0) {
      await options.first().click();
    }
    await page.waitForTimeout(300);

    // Submit
    await dialog.getByRole('button', { name: 'Create' }).click();
    await page.waitForTimeout(500);

    // Should show error about patterns
    const errorAlert = dialog.locator('.MuiAlert-standardError');
    await expect(errorAlert).toBeVisible({ timeout: 3000 });
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rules-no-pattern-error.png' });
  });

  test('create rule with category and pattern, verify in list', async ({ page }) => {
    // Use a unique name to avoid collisions from prior runs
    const ruleName = `PW Rule ${Date.now()}`;

    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);

    const dialog = page.getByRole('dialog');

    // Fill in rule name
    await dialog.getByLabel('Rule Name').fill(ruleName);

    // Fill in description pattern
    await dialog.getByLabel('Description Pattern').fill('%pw-test-pattern%');

    // Select a category via combobox
    const comboboxes = dialog.getByRole('combobox');
    const categoryCombobox = comboboxes.first();
    await categoryCombobox.click();
    await page.waitForTimeout(300);
    const options = page.getByRole('option');
    const optCount = await options.count();
    if (optCount > 1) {
      await options.nth(1).click();
    }
    await page.waitForTimeout(300);

    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rules-filled-form.png' });

    // Submit
    await dialog.getByRole('button', { name: 'Create' }).click();

    // Dialog should close
    await expect(dialog).not.toBeVisible({ timeout: 10000 });

    // Rule should appear in the list (wait for query refetch)
    await expect(page.getByText(ruleName)).toBeVisible({ timeout: 10000 });
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rules-after-create.png' });
  });

  test('apply rules dialog shows entity assigned count', async ({ page }) => {
    // First create a rule so Apply Rules is enabled
    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);
    const createDialog = page.getByRole('dialog');
    await createDialog.getByLabel('Rule Name').fill('Apply Test Rule');
    await createDialog.getByLabel('Description Pattern').fill('%apply-test%');
    const combobox = createDialog.getByRole('combobox').first();
    await combobox.click();
    await page.waitForTimeout(300);
    const opts = page.getByRole('option');
    if (await opts.count() > 1) await opts.nth(1).click();
    await page.waitForTimeout(300);
    await createDialog.getByRole('button', { name: 'Create' }).click();
    await expect(createDialog).not.toBeVisible({ timeout: 10000 });

    // Now click Apply Rules button
    const applyButton = page.getByRole('button', { name: /Apply Rules/i });
    await expect(applyButton).toBeEnabled({ timeout: 5000 });
    await applyButton.click();
    await page.waitForTimeout(500);

    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    // Find and click the apply/confirm button in the dialog
    const applyConfirm = dialog.getByRole('button', { name: /Apply/i }).last();
    await applyConfirm.click();

    // Should show results including entity assigned count
    await expect(dialog.getByText(/Entities Assigned/i)).toBeVisible({ timeout: 10000 });
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rules-apply-result.png' });
  });
});
