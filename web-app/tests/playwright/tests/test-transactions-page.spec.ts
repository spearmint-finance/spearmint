import { test, expect } from '@playwright/test';

test('transactions page should load and display data', async ({ page }) => {
  // Navigate to transactions page
  await page.goto('/transactions');

  // Wait for page to load
  await page.waitForLoadState('networkidle');

  // Take a screenshot of the page
  await page.screenshot({ path: 'transactions-page-error.png', fullPage: true });

  // Check if there are any console errors
  const errors: string[] = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(msg.text());
      console.log('Browser console error:', msg.text());
    }
  });

  // Check for React error boundaries
  const errorText = await page.locator('body').textContent();
  console.log('Page content:', errorText?.substring(0, 500));

  // Try to find the DataGrid
  const dataGrid = page.locator('.MuiDataGrid-root');
  const dataGridExists = await dataGrid.count();
  console.log('DataGrid found:', dataGridExists > 0);

  // Check if loading spinner is present
  const loading = page.locator('[role="progressbar"]');
  const isLoading = await loading.count();
  console.log('Loading spinner present:', isLoading > 0);

  // Wait a bit more
  await page.waitForTimeout(3000);

  // Take another screenshot
  await page.screenshot({ path: 'transactions-page-after-wait.png', fullPage: true });

  // Get all text on page to see what's displayed
  const bodyText = await page.locator('body').textContent();
  console.log('Full page text:', bodyText);

  // Print any errors found
  if (errors.length > 0) {
    console.log('Console errors found:', errors);
  }
});
