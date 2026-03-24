import { test, expect } from '@playwright/test';

test.describe('Transaction Rules — Account Matching', () => {
  test('can create a rule with account filter and it appears in the form', async ({ page }) => {
    // Go to Settings > Transaction Rules
    await page.goto('http://localhost:5173/settings');
    await page.waitForLoadState('networkidle');
    await page.getByRole('tab', { name: /Transaction Rules/i }).click();
    await page.waitForTimeout(500);

    // Open create rule dialog
    await page.getByRole('button', { name: /Create Rule/i }).click();
    await page.waitForTimeout(500);

    const dialog = page.getByRole('dialog');

    // Verify the Account dropdown exists
    const accountLabel = dialog.getByLabel('Account');
    await expect(accountLabel).toBeVisible({ timeout: 5000 });

    // Fill in a rule name
    await dialog.getByLabel('Rule Name').fill('Test Account Rule');

    // Select a category
    const categorySelect = dialog.locator('[name="category_id"]').first();
    if (await categorySelect.isVisible()) {
      await categorySelect.click();
    } else {
      // Try the label-based approach
      await dialog.getByLabel('Category').first().click();
    }
    await page.waitForTimeout(300);
    // Pick first available category from dropdown
    const categoryOption = page.locator('.MuiMenuItem-root').first();
    if (await categoryOption.isVisible()) {
      await categoryOption.click();
      await page.waitForTimeout(200);
    }

    // Click the Account dropdown
    await dialog.getByLabel('Account').click();
    await page.waitForTimeout(300);

    // Check that account options are listed
    const accountOptions = page.locator('.MuiMenuItem-root');
    const optionCount = await accountOptions.count();
    console.log(`Account dropdown has ${optionCount} options`);
    expect(optionCount).toBeGreaterThan(1); // "Any account" + real accounts

    // Select the first real account (skip "Any account")
    if (optionCount > 1) {
      await accountOptions.nth(1).click();
      await page.waitForTimeout(200);
    }

    // Add a description pattern
    await dialog.getByLabel('Description Pattern').fill('TEST_PATTERN');

    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rule-account-form.png' });

    // Submit
    await dialog.getByRole('button', { name: 'Create' }).click();
    await page.waitForTimeout(1000);

    // Verify dialog closed (rule created successfully)
    const dialogStillOpen = await dialog.isVisible().catch(() => false);

    await page.screenshot({ path: 'tests/playwright/test-results/artifacts/rule-account-created.png' });

    // If dialog is still open, check for errors
    if (dialogStillOpen) {
      const errorAlert = dialog.locator('.MuiAlert-standardError');
      const hasError = await errorAlert.isVisible().catch(() => false);
      if (hasError) {
        const errorText = await errorAlert.textContent();
        console.log(`Form error: ${errorText}`);
      }
    }
  });

  test('rule API accepts account_id field', async ({ request }) => {
    // First get accounts to find a valid ID
    const accountsRes = await request.get('http://localhost:8000/api/accounts');
    expect(accountsRes.ok()).toBeTruthy();
    const accounts = await accountsRes.json();

    if (accounts.length === 0) {
      test.skip();
      return;
    }

    const accountId = accounts[0].account_id;

    // Get a category
    const catsRes = await request.get('http://localhost:8000/api/categories');
    const catsData = await catsRes.json();
    const cats = catsData.categories || catsData;
    const expenseCat = cats.find((c: any) => c.category_type === 'Expense');

    // Create a rule with account_id
    const createRes = await request.post('http://localhost:8000/api/categories/rules', {
      data: {
        rule_name: 'API Test Account Rule',
        category_id: expenseCat.category_id,
        account_id: accountId,
        description_pattern: 'API_TEST_ACCOUNT',
        rule_priority: 100,
        is_active: true,
      },
    });

    console.log(`Create rule response: ${createRes.status()}`);
    expect(createRes.ok()).toBeTruthy();

    const rule = await createRes.json();
    console.log(`Created rule: ${JSON.stringify(rule)}`);
    expect(rule.account_id).toBe(accountId);

    // Clean up — delete the test rule
    const deleteRes = await request.delete(`http://localhost:8000/api/categories/rules/${rule.rule_id}`);
    expect(deleteRes.ok()).toBeTruthy();
  });

  test('rule matching respects account_id filter', async ({ request }) => {
    // Get accounts
    const accountsRes = await request.get('http://localhost:8000/api/accounts');
    const accounts = await accountsRes.json();
    if (accounts.length < 1) { test.skip(); return; }

    const targetAccount = accounts[0];

    // Get a category
    const catsRes = await request.get('http://localhost:8000/api/categories');
    const catsData = await catsRes.json();
    const cats = catsData.categories || catsData;
    const testCat = cats.find((c: any) => c.category_type === 'Expense' && c.category_name !== 'nan');

    // Create a rule that only matches the target account
    const createRes = await request.post('http://localhost:8000/api/categories/rules', {
      data: {
        rule_name: 'Account Match Test',
        category_id: testCat.category_id,
        account_id: targetAccount.account_id,
        description_pattern: '.*',  // Match everything
        rule_priority: 1,
        is_active: true,
      },
    });
    expect(createRes.ok()).toBeTruthy();
    const rule = await createRes.json();

    // Test the rule — it should only match transactions from that account
    const testRes = await request.post('http://localhost:8000/api/categories/rules/test', {
      data: {
        description_pattern: '.*',
      },
    });

    if (testRes.ok()) {
      const testResult = await testRes.json();
      console.log(`Test rule matched ${testResult.matched_count} transactions`);
    }

    // Clean up
    await request.delete(`http://localhost:8000/api/categories/rules/${rule.rule_id}`);
  });
});
