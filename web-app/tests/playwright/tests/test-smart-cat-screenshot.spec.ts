import { test, expect } from '@playwright/test';

test('screenshot smart categorize dialog', async ({ page }) => {
  await page.goto('http://localhost:5173/transactions');
  await page.waitForLoadState('networkidle');

  // Click Smart Categorize and wait for API response
  const [apiResponse] = await Promise.all([
    page.waitForResponse(resp => resp.url().includes('uncategorized-descriptions')),
    page.getByRole('button', { name: /Smart Categorize/i }).click(),
  ]);

  const data = await apiResponse.json();
  console.log(`API returned: ${data.total} descriptions, ${data.total_transactions} txns`);

  await page.waitForTimeout(1000);

  // Take screenshot
  await page.screenshot({ path: 'test-results/smart-cat-dialog.png', fullPage: false });

  // Check dialog header text
  const dialog = page.getByRole('dialog');
  const headerText = await dialog.locator('h2, h6, [class*="DialogTitle"]').first().textContent();
  console.log(`Dialog header: ${headerText}`);

  // Check first 5 items in the description list
  const items = dialog.locator('[class*="MuiCheckbox"]');
  const itemCount = await items.count();
  console.log(`Checkbox items in dialog: ${itemCount}`);

  // Get text of first few items
  const listItems = dialog.locator('[class*="MuiTypography-body2"]');
  const listCount = await listItems.count();
  for (let i = 0; i < Math.min(5, listCount); i++) {
    const text = await listItems.nth(i).textContent();
    console.log(`  Item ${i}: ${text}`);
  }

  // Check if Applied section exists
  const appliedSection = dialog.getByText('Applied');
  const hasApplied = await appliedSection.isVisible().catch(() => false);
  console.log(`Has 'Applied' section: ${hasApplied}`);

  // Verify the count shown
  expect(data.total).toBeLessThan(2500);
});
