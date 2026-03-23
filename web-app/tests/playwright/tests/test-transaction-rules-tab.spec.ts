import { test, expect } from '@playwright/test';

test.describe('Transaction Rules Tab', () => {
  test('Transaction Rules tab is visible at top level in Settings', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/settings-before-rules.png' });

    // Check all tab labels
    const tabs = page.getByRole('tab');
    const tabCount = await tabs.count();
    const tabLabels: string[] = [];
    for (let i = 0; i < tabCount; i++) {
      tabLabels.push((await tabs.nth(i).textContent()) || '');
    }
    console.log('Settings tabs:', tabLabels);

    // Transaction Rules should be a top-level tab
    const rulesTab = page.getByRole('tab', { name: /Transaction Rules/i });
    await expect(rulesTab).toBeVisible();
  });

  test('Transaction Rules tab shows rules list with Create Rule button', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    // Click Transaction Rules tab
    const rulesTab = page.getByRole('tab', { name: /Transaction Rules/i });
    await rulesTab.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/settings-rules-tab.png' });

    // Should see Create Rule button
    const createButton = page.getByRole('button', { name: /Create Rule/i });
    await expect(createButton).toBeVisible();

    // Should see Apply Rules button
    const applyButton = page.getByRole('button', { name: /Apply Rules/i });
    await expect(applyButton).toBeVisible();
  });

  test('Create Rule form shows Entity dropdown', async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');

    // Click Transaction Rules tab
    await page.getByRole('tab', { name: /Transaction Rules/i }).click();
    await page.waitForTimeout(500);

    // Click Create Rule
    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/settings-rules-form.png' });

    // Should see the dialog
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();

    // Should have Entity label (the form label, not the alert text)
    await expect(dialog.locator('label').filter({ hasText: 'Entity' })).toBeVisible();

    // Should have Category label
    await expect(dialog.locator('label').filter({ hasText: 'Category' })).toBeVisible();

    // Should have "Assignment (at least one required)" text
    await expect(dialog.getByText('Assignment (at least one required)')).toBeVisible();
  });
});
