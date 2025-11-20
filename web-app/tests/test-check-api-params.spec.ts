import { test, expect } from '@playwright/test';

test('check API parameters when paging', async ({ page }) => {
  const apiCalls: any[] = [];

  // Intercept API calls
  page.on('request', request => {
    if (request.url().includes('/api/transactions')) {
      apiCalls.push({
        url: request.url(),
        method: request.method()
      });
      console.log('API Request:', request.url());
    }
  });

  await page.goto('http://localhost:5173/transactions');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);

  console.log('\n=== PAGE 1 API CALL ===');
  console.log(apiCalls[apiCalls.length - 1]?.url);

  // Click next page
  const nextButton = page.locator('button[aria-label="Go to next page"]');
  await nextButton.click();
  await page.waitForTimeout(2000);

  console.log('\n=== PAGE 2 API CALL ===');
  console.log(apiCalls[apiCalls.length - 1]?.url);

  // Check that offset changed
  const page1Url = apiCalls[apiCalls.length - 2]?.url || '';
  const page2Url = apiCalls[apiCalls.length - 1]?.url || '';

  console.log('\nPage 1 has offset=0:', page1Url.includes('offset=0'));
  console.log('Page 2 has offset=25:', page2Url.includes('offset=25'));

  expect(page1Url).toContain('offset=0');
  expect(page2Url).toContain('offset=25');
});
