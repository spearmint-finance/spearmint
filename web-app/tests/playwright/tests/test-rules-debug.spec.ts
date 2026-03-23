import { test, expect } from '@playwright/test';

test('debug: submit rule form with no assignment', async ({ page }) => {
  // Capture all console messages
  page.on('console', msg => console.log(`BROWSER [${msg.type()}]:`, msg.text()));

  await page.goto('/settings');
  await page.waitForLoadState('networkidle');
  await page.getByRole('tab', { name: /Transaction Rules/i }).click();
  await page.waitForTimeout(500);

  await page.getByRole('button', { name: /Create Rule/i }).click();
  await page.waitForTimeout(500);

  const dialog = page.getByRole('dialog');

  // Fill required fields - click first to focus, then type
  const ruleNameInput = dialog.getByLabel('Rule Name');
  await ruleNameInput.click();
  await ruleNameInput.fill('Debug Test');

  const descInput = dialog.getByLabel('Description Pattern');
  await descInput.click();
  await descInput.fill('%debug%');

  // Blur to trigger change
  await dialog.getByLabel('Rule Name').click();

  await page.screenshot({ path: 'tests/playwright/test-results/artifacts/debug-before-submit.png' });

  // Click Create button
  const createBtn = dialog.getByRole('button', { name: 'Create' });
  console.log('Create button found:', await createBtn.count());
  console.log('Create button disabled:', await createBtn.isDisabled());
  console.log('Create button type:', await createBtn.getAttribute('type'));

  // Try submitting the form directly
  await page.evaluate(() => {
    const form = document.querySelector('form');
    console.log('Form found:', !!form);
    if (form) {
      form.requestSubmit();
    }
  });

  // Also try clicking the button
  await createBtn.click({ force: true });

  // Wait and take screenshot
  await page.waitForTimeout(1000);

  // Scroll dialog content to top to see error
  await dialog.locator('.MuiDialogContent-root').evaluate(el => el.scrollTop = 0);
  await page.waitForTimeout(300);

  await page.screenshot({ path: 'tests/playwright/test-results/artifacts/debug-after-submit.png' });

  // Check for error alert anywhere in dialog
  const errorAlerts = dialog.locator('.MuiAlert-standardError');
  const errorCount = await errorAlerts.count();
  console.log('Error alerts found:', errorCount);

  if (errorCount > 0) {
    const errorText = await errorAlerts.first().textContent();
    console.log('Error text:', errorText);
  }

  // Also check all alerts
  const allAlerts = dialog.locator('.MuiAlert-root');
  const alertCount = await allAlerts.count();
  console.log('Total alerts:', alertCount);
  for (let i = 0; i < alertCount; i++) {
    const text = await allAlerts.nth(i).textContent();
    const severity = await allAlerts.nth(i).getAttribute('class');
    console.log(`Alert ${i}: "${text}" class="${severity}"`);
  }

  expect(errorCount).toBeGreaterThan(0);
});
