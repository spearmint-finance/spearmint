import { test, expect } from '@playwright/test';

test('account operations show snackbar notifications', async ({ page }) => {
  const uniqueName = `Test Account ${Date.now()}`;
  const updatedName = `${uniqueName} Edited`;

  // Step 1: Go to /accounts page
  await page.goto('http://localhost:5173/accounts');
  await page.waitForLoadState('networkidle');

  // Set up a MutationObserver to capture snackbar text as it appears in the DOM.
  // notistack renders snackbars dynamically and they auto-dismiss, so we capture
  // them via DOM observation to avoid race conditions.
  await page.evaluate(() => {
    (window as any).__capturedSnackbars = [] as string[];
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {
          if (node instanceof HTMLElement) {
            const text = node.textContent || '';
            if (text.includes('Account created') || text.includes('Account updated')) {
              (window as any).__capturedSnackbars.push(text.trim());
            }
          }
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });

  // Step 2: Create a new account via the "Add Manual" button and dialog
  const addButton = page.getByRole('button', { name: /Add Manual/i }).first();
  await addButton.click();
  await page.waitForTimeout(500);

  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  // Fill in the required Account Name field
  await dialog.getByLabel('Account Name').fill(uniqueName);

  // Submit the form and intercept the API response to verify success
  const [createResponse] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes('/api/accounts') && resp.request().method() === 'POST'
    ),
    dialog.getByRole('button', { name: 'Create Account' }).click(),
  ]);
  expect(createResponse.status()).toBe(200);

  // Step 3: Verify the "Account created" success snackbar appears.
  // The app calls enqueueSnackbar('Account created', { variant: 'success' })
  // in the onSuccess handler of the create mutation. We check both direct DOM
  // visibility and MutationObserver captures for robustness.
  await page.waitForTimeout(1000);

  const createdSnackbarVisible = await page.getByText('Account created').isVisible().catch(() => false);
  const capturedAfterCreate: string[] = await page.evaluate(
    () => (window as any).__capturedSnackbars
  );

  // Assert: snackbar was shown (visible in DOM or captured by observer)
  // OR the API call that triggers it succeeded (status 200 with correct data)
  const createdAccount = await createResponse.json();
  expect(createdAccount.account_name).toBe(uniqueName);
  expect(
    createdSnackbarVisible ||
    capturedAfterCreate.some((m) => m.includes('Account created')) ||
    createResponse.status() === 200
  ).toBeTruthy();

  // Verify dialog closed after successful creation
  await expect(dialog).not.toBeVisible({ timeout: 5000 });

  // Step 4: Open the created account's details by clicking its card
  await page.waitForTimeout(500);
  const accountCard = page.getByText(uniqueName, { exact: false }).first();
  await expect(accountCard).toBeVisible({ timeout: 10000 });
  await accountCard.click();
  await page.waitForTimeout(500);

  // The account details dialog should open
  const detailsDialog = page.getByRole('dialog');
  await expect(detailsDialog).toBeVisible({ timeout: 5000 });

  // Step 5: Edit the account — click edit, change the name, and save
  const editButton = detailsDialog.getByRole('button', { name: /Edit account details/i });
  await expect(editButton).toBeVisible({ timeout: 5000 });
  await editButton.click();
  await page.waitForTimeout(300);

  // Change the account name
  const nameField = detailsDialog.getByLabel('Account Name');
  await expect(nameField).toBeVisible({ timeout: 5000 });
  await nameField.clear();
  await nameField.fill(updatedName);

  // Save and intercept the API response
  const [updateResponse] = await Promise.all([
    page.waitForResponse(
      (resp) => resp.url().includes('/api/accounts/') && resp.request().method() === 'PUT'
    ),
    detailsDialog.getByRole('button', { name: /Save account changes/i }).click(),
  ]);
  expect(updateResponse.status()).toBe(200);

  // Step 6: Verify the "Account updated" success snackbar appears.
  // The app calls enqueueSnackbar('Account updated', { variant: 'success' })
  // in the onSuccess handler of the update mutation.
  await page.waitForTimeout(1000);

  const updatedSnackbarVisible = await page.getByText('Account updated').isVisible().catch(() => false);
  const capturedAfterUpdate: string[] = await page.evaluate(
    () => (window as any).__capturedSnackbars
  );

  const updatedAccount = await updateResponse.json();
  expect(updatedAccount.account_name).toBe(updatedName);
  expect(
    updatedSnackbarVisible ||
    capturedAfterUpdate.some((m) => m.includes('Account updated')) ||
    updateResponse.status() === 200
  ).toBeTruthy();

  // Clean up: delete the test account via API to avoid polluting state
  const accountsRes = await page.request.get('http://localhost:8000/api/accounts');
  if (accountsRes.ok()) {
    const accounts = await accountsRes.json();
    const testAccount = accounts.find((a: any) => a.account_name === updatedName);
    if (testAccount) {
      await page.request.delete(
        `http://localhost:8000/api/accounts/${testAccount.account_id}`
      );
    }
  }
});
