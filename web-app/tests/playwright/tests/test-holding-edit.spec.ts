import { test, expect } from '@playwright/test';

test('edit holding via account details portfolio tab', async ({ page }) => {
  await page.goto('http://localhost:5173/accounts');
  await page.waitForLoadState('networkidle');

  // Find an investment account card and click it
  const accountCards = page.locator('[class*="MuiCard"]');
  const cardCount = await accountCards.count();

  let foundInvestment = false;
  for (let i = 0; i < cardCount; i++) {
    const cardText = await accountCards.nth(i).textContent();
    if (cardText && (cardText.includes('brokerage') || cardText.includes('investment') || cardText.includes('Fidelity'))) {
      await accountCards.nth(i).click();
      foundInvestment = true;
      break;
    }
  }

  if (!foundInvestment) {
    test.skip();
    return;
  }

  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  // Click Portfolio tab
  const portfolioTab = dialog.getByRole('tab', { name: /Portfolio/i });
  if (await portfolioTab.count() === 0) {
    test.skip();
    return;
  }
  await portfolioTab.click();
  await page.waitForTimeout(1000);

  // Add a test holding
  await dialog.getByRole('button', { name: /Add Holding/i }).click();
  await page.waitForTimeout(300);

  await dialog.getByLabel('Symbol').fill('EDITTEST');
  await dialog.getByLabel('Quantity').fill('100');
  await dialog.getByLabel('Cost Basis').fill('5000');
  await dialog.getByLabel('Current Value').fill('5500');

  await dialog.getByRole('button', { name: /^Add$/i }).click();

  // Wait for form to close and holding to appear
  await expect(dialog.getByText('EDITTEST')).toBeVisible({ timeout: 10000 });
  // Wait for the add form to fully close
  await expect(dialog.getByText('New Holding')).not.toBeVisible({ timeout: 5000 });
  await page.screenshot({ path: 'tests/playwright/test-results/artifacts/holding-before-edit.png' });

  // Click the edit button for our test holding
  const holdingItem = dialog.locator('li').filter({ hasText: 'EDITTEST' });
  await holdingItem.getByTitle('Edit holding').click();
  await page.waitForTimeout(500);

  // The form should show with Edit Holding title
  await expect(dialog.getByText('Edit Holding')).toBeVisible({ timeout: 5000 });
  await page.screenshot({ path: 'tests/playwright/test-results/artifacts/holding-edit-form.png' });

  // Update the quantity and value
  await dialog.getByLabel('Quantity').fill('200');
  await dialog.getByLabel('Current Value').fill('11000');

  // Save
  await dialog.getByRole('button', { name: /^Save$/i }).click();
  await page.waitForTimeout(2000);

  // Verify updated values (quantity is displayed as decimal e.g. 200.000000)
  await expect(dialog.getByText(/200.*shares/)).toBeVisible({ timeout: 5000 });
  await page.screenshot({ path: 'tests/playwright/test-results/artifacts/holding-after-edit.png' });

  // Clean up: delete the test holding
  const updatedItem = dialog.locator('li').filter({ hasText: 'EDITTEST' });
  page.once('dialog', d => d.accept());
  await updatedItem.getByTitle('Delete holding').click();
  await page.waitForTimeout(1000);
});
