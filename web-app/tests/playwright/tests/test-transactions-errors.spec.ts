import { test, expect } from '@playwright/test';

test('capture console errors on transactions page', async ({ page }) => {
  const consoleMessages: any[] = [];
  const errors: any[] = [];

  // Capture all console messages
  page.on('console', msg => {
    consoleMessages.push({
      type: msg.type(),
      text: msg.text(),
      location: msg.location()
    });
    console.log(`[${msg.type()}]`, msg.text());
  });

  // Capture page errors
  page.on('pageerror', error => {
    errors.push(error);
    console.log('PAGE ERROR:', error.message);
    console.log('Stack:', error.stack);
  });

  // Navigate to transactions page
  console.log('Navigating to transactions page...');
  await page.goto('/transactions');

  // Wait for network to be idle
  await page.waitForLoadState('networkidle');

  // Wait a bit more
  await page.waitForTimeout(2000);

  // Print all errors
  console.log('\n=== CONSOLE MESSAGES ===');
  consoleMessages.forEach(msg => {
    console.log(`[${msg.type}] ${msg.text}`);
  });

  console.log('\n=== PAGE ERRORS ===');
  errors.forEach(err => {
    console.log(err.message);
    console.log(err.stack);
  });

  // Check DOM
  const html = await page.content();
  console.log('\n=== HTML LENGTH ===', html.length);

  // Take screenshot
  await page.screenshot({ path: 'transactions-debug.png', fullPage: true });
});
