import { test, expect } from '@playwright/test';

test('smart categorize should not show already-categorized descriptions', async ({ page }) => {
  // First verify API returns correct data
  const apiRes = await page.request.get('http://localhost:8000/api/transactions/uncategorized-descriptions?offset=0&limit=100');
  const apiData = await apiRes.json();
  const apiDescs = apiData.descriptions.map((d: any) => d.description);

  // These should NOT be in the uncategorized list
  expect(apiDescs).not.toContain('APPLE.COM/BILL XXX-XXX-7753 CA');
  expect(apiDescs.filter((d: string) => d.includes('YOU BOUGHT VANGUARD'))).toHaveLength(0);
  expect(apiDescs.filter((d: string) => d.includes('AUTOMATIC PAYMENT - THANK'))).toHaveLength(0);
  console.log(`API: ${apiData.total} uncategorized descriptions (correct)`);

  // Now open the Smart Categorize dialog in the UI
  await page.goto('http://localhost:5173/transactions');
  await page.waitForLoadState('networkidle');

  // Intercept the uncategorized-descriptions API call to see what the frontend receives
  const [apiResponse] = await Promise.all([
    page.waitForResponse(resp => resp.url().includes('uncategorized-descriptions')),
    page.getByRole('button', { name: /Smart Categorize/i }).click(),
  ]);

  const responseData = await apiResponse.json();
  console.log(`Frontend received: ${responseData.total} descriptions, ${responseData.total_transactions} txns`);

  // The dialog should show the correct count
  await page.waitForTimeout(1000);

  // Check the dialog content
  const dialogText = await page.getByRole('dialog').textContent();

  // Should NOT contain APPLE.COM/BILL in the selectable list
  const appleCheckbox = page.getByRole('dialog').getByText('APPLE.COM/BILL XXX-XXX-7753 CA');
  const appleVisible = await appleCheckbox.isVisible().catch(() => false);
  console.log(`APPLE.COM/BILL visible in dialog: ${appleVisible}`);

  // Should show ~2367, not 2597
  expect(responseData.total).toBeLessThan(2500);
  expect(appleVisible).toBeFalsy();
});
