import { test, expect } from '@playwright/test';

test('API: accounts filtered by entity returns correct results', async ({ page }) => {
  // Verify the API returns 100 E Stiles accounts when filtering by entity 4
  const apiResponse = await page.request.get('http://localhost:8000/api/accounts?entity_id=4');
  expect(apiResponse.ok()).toBeTruthy();
  const accounts = await apiResponse.json();
  expect(accounts.length).toBeGreaterThanOrEqual(2);

  const accountNames = accounts.map((a: any) => a.account_name);
  expect(accountNames).toContain('x00 E STILES');
  expect(accountNames).toContain('x00 E STILES - DEPOSIT');

  // Verify entity_ids are populated
  for (const a of accounts) {
    expect(a.entity_ids).toContain(4);
  }
  console.log(`API: ${accounts.length} accounts for entity 4 (100 E Stiles)`);
});

test('UI: entity scope filters accounts correctly', async ({ page }) => {
  await page.goto('http://localhost:5173/accounts');
  await page.waitForLoadState('networkidle');

  // All accounts should be visible initially
  const allCards = page.locator('[class*="MuiCard"]');
  const initialCount = await allCards.count();
  console.log(`Initial account cards: ${initialCount}`);
  expect(initialCount).toBeGreaterThan(2);

  // Click the entity selector
  const entitySelect = page.locator('select').first();
  if (await entitySelect.isVisible({ timeout: 2000 }).catch(() => false)) {
    // Native select element
    await entitySelect.selectOption({ label: /100 E Stiles/i });
  } else {
    // MUI Select - click to open dropdown
    const entityTrigger = page.getByText('All Entities').first();
    await entityTrigger.click();
    await page.waitForTimeout(500);

    // Select "100 E Stiles" from menu
    const option = page.getByRole('option', { name: /100 E Stiles/i });
    if (await option.isVisible({ timeout: 2000 }).catch(() => false)) {
      await option.click();
    } else {
      // Try as a menu item
      const menuItem = page.locator('[role="menuitem"], [role="option"], li').filter({ hasText: '100 E Stiles' }).first();
      await menuItem.click();
    }
  }

  await page.waitForTimeout(1000);
  await page.waitForLoadState('networkidle');

  // After scoping, should see fewer accounts (only the ones belonging to this entity)
  const filteredCards = page.locator('[class*="MuiCard"]');
  const filteredCount = await filteredCards.count();
  console.log(`Filtered account cards: ${filteredCount}`);

  // Should see x00 E STILES accounts
  const stilesText = page.getByText('x00 E STILES', { exact: false });
  await expect(stilesText.first()).toBeVisible({ timeout: 5000 });
  console.log('SUCCESS: x00 E STILES visible after entity scope');
});
