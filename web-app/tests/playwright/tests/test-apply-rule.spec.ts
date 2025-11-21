import { test, expect } from '@playwright/test';

test('test apply rule button', async ({ page }) => {
  // Navigate to the app
  await page.goto('http://localhost:5176');

  // Wait for page to load
  await page.waitForLoadState('networkidle');

  // Click on Classifications link in navigation
  await page.click('text=Classifications');

  // Wait for the page to load
  await page.waitForTimeout(1000);

  // Click on Classification Rules tab
  await page.click('text=Classification Rules');

  // Wait for rules to load
  await page.waitForTimeout(1000);

  // Take a screenshot before clicking
  await page.screenshot({ path: 'before-click.png' });

  // Find the first play button (Apply This Rule)
  const playButton = page.locator('button[aria-label="Apply This Rule"]').first();

  // Check if button exists
  const buttonExists = await playButton.count();
  console.log('Play button count:', buttonExists);

  if (buttonExists > 0) {
    // Click the play button
    await playButton.click();

    // Wait for dialog to appear
    await page.waitForTimeout(1000);

    // Take screenshot after click
    await page.screenshot({ path: 'after-click.png' });

    // Check if dialog opened
    const dialogTitle = page.locator('h2:has-text("Apply Rule:")');
    const dialogVisible = await dialogTitle.isVisible();
    console.log('Dialog visible:', dialogVisible);

    // Get dialog title text
    if (dialogVisible) {
      const titleText = await dialogTitle.textContent();
      console.log('Dialog title:', titleText);
    }
  } else {
    console.log('No play button found');
    await page.screenshot({ path: 'no-button.png' });
  }
});
