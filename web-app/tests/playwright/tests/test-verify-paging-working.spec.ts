import { test, expect } from '@playwright/test';

test('verify paging is working - check data not display', async ({ page }) => {
  await page.goto('/transactions');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  // Get the actual data from the React component
  const rowCount = await page.evaluate(() => {
    const gridRoot = document.querySelector('.MuiDataGrid-root');
    if (!gridRoot) return 0;

    // Find all row elements (visible and virtualized)
    const rows = document.querySelectorAll('[data-id]');
    return rows.length;
  });

  console.log(`Total rows in DOM (including virtualized): ${rowCount}`);

  // Check pagination text
  const paginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log(`Pagination shows: ${paginationText}`);

  // Now test page navigation
  console.log('\n=== Testing Page 2 ===');
  const nextButton = page.locator('button[aria-label="Go to next page"]');
  await nextButton.click();
  await page.waitForTimeout(2000);

  const page2PaginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log(`Page 2 pagination shows: ${page2PaginationText}`);

  // Take screenshots
  await page.screenshot({ path: 'test-screenshots/verify-page-2.png', fullPage: true });

  expect(paginationText).toMatch(/1.*25/);
  expect(page2PaginationText).toMatch(/26.*50/);
});
