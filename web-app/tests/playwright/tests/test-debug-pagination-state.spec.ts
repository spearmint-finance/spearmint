import { test, expect } from '@playwright/test';

test('debug pagination state changes', async ({ page }) => {
  // Monitor console logs from the page
  page.on('console', msg => {
    if (msg.text().includes('PAGINATION') || msg.text().includes('useTransactions')) {
      console.log('Page console:', msg.text());
    }
  });

  await page.goto('/transactions');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  console.log('\n=== Initial state ===');
  let paginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log('Pagination:', paginationText);

  console.log('\n=== Clicking next page ===');
  const nextButton = page.locator('button[aria-label="Go to next page"]');

  // Check if button is enabled
  const isEnabled = await nextButton.isEnabled();
  console.log('Next button enabled:', isEnabled);

  if (!isEnabled) {
    console.log('ERROR: Next button is disabled!');
    return;
  }

  await nextButton.click();

  // Wait for network request
  await page.waitForTimeout(500);

  console.log('\n=== After click (500ms) ===');
  paginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log('Pagination:', paginationText);

  await page.waitForTimeout(1000);

  console.log('\n=== After click (1500ms total) ===');
  paginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log('Pagination:', paginationText);

  await page.waitForTimeout(1500);

  console.log('\n=== After click (3000ms total) ===');
  paginationText = await page.locator('.MuiTablePagination-displayedRows').textContent();
  console.log('Pagination:', paginationText);

  await page.screenshot({ path: 'test-screenshots/pagination-debug.png' });
});
