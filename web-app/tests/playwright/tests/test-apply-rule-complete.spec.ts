import { test, expect } from '@playwright/test';

test('complete apply rule flow', async ({ page }) => {
  // Navigate to the app
  await page.goto('http://localhost:5176');

  // Wait for page to load
  await page.waitForLoadState('networkidle');

  // Navigate to Classifications
  await page.click('text=Classifications');
  await page.waitForTimeout(500);

  // Click on Classification Rules tab
  await page.click('text=Classification Rules');
  await page.waitForTimeout(1000);

  // Find the table and locate the "100 S Stratford Remodel" rule
  // Click the play button for that specific rule
  const ruleRow = page.locator('tr', { hasText: '100 S Stratford Remodel' });
  const playButton = ruleRow.locator('button[title="Apply This Rule"]').first();

  console.log('Found rule row, clicking play button...');
  await playButton.click();

  // Wait for dialog to open
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'step1-dialog-opened.png' });

  // Verify dialog opened with correct title
  const dialogTitle = await page.locator('h2:has-text("Apply Rule: 100 S Stratford Remodel")').textContent();
  console.log('Dialog title:', dialogTitle);
  expect(dialogTitle).toContain('100 S Stratford Remodel');

  // Click Preview Changes button
  console.log('Clicking Preview Changes...');
  const previewButton = page.locator('button:has-text("Preview Changes")');
  await previewButton.click();

  // Wait for preview results
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'step2-preview-results.png' });

  // Check for preview results
  const previewHeading = await page.locator('h6:has-text("Preview Results")').isVisible();
  console.log('Preview heading visible:', previewHeading);

  // Get the transaction count
  const transactionChip = await page.locator('div.MuiChip-label:has-text("Transactions Would Be Updated")').textContent();
  console.log('Preview shows:', transactionChip);

  // Click Apply Rules button
  console.log('Clicking Apply Rules...');
  const applyButton = page.locator('button:has-text("Apply Rules")');
  await applyButton.click();

  // Wait for application to complete
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'step3-apply-results.png' });

  // Check for success message
  const successAlert = await page.locator('div[role="alert"]:has-text("Successfully applied")').isVisible();
  console.log('Success alert visible:', successAlert);

  if (successAlert) {
    const successText = await page.locator('div[role="alert"]:has-text("Successfully applied")').textContent();
    console.log('Success message:', successText);
  }

  // Check that heading changed to "Application Results"
  const appResultsHeading = await page.locator('h6:has-text("Application Results")').isVisible();
  console.log('Application Results heading visible:', appResultsHeading);

  // Final screenshot
  await page.screenshot({ path: 'step4-final.png' });

  // Close the dialog
  await page.click('button:has-text("Close")');

  console.log('Test completed successfully!');
});
