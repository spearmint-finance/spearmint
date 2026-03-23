import { test, expect } from '@playwright/test';

test.describe('Capital Expense Classification Rule', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');

    // Wait for the app to load
    await page.waitForLoadState('networkidle');
  });

  test('should apply capital expense rule to transactions', async ({ page }) => {
    // Navigate to Classifications page
    await page.getByRole('link', { name: /classifications/i }).click();
    await page.waitForLoadState('networkidle');

    // Find and click the "100 S Stratford Maint" rule
    const ruleRow = page.getByText('100 S Stratford Maint').first();
    await ruleRow.click();
    await page.waitForLoadState('networkidle');

    // Verify the rule settings
    const transactionType = page.getByLabel('Transaction Type');
    await expect(transactionType).toHaveValue('expense');

    const categoryPattern = page.getByLabel('Category Pattern');
    await expect(categoryPattern).toHaveValue('100 S Stratford Maint');

    const minAmount = page.getByLabel('Minimum Amount');
    await expect(minAmount).toHaveValue('2000');

    const maxAmount = page.getByLabel('Maximum Amount');
    await expect(maxAmount).toHaveValue('');

    // Click Test Rule button
    await page.getByRole('button', { name: 'Test Rule' }).click();

    // Wait for the alert and capture the message
    page.on('dialog', async dialog => {
      console.log('Test Rule Result:', dialog.message());
      expect(dialog.message()).toContain('transaction');
      await dialog.accept();
    });

    // Close the dialog
    await page.getByRole('button', { name: 'Cancel' }).click();

    // Now try to apply the rule
    await page.getByRole('button', { name: 'Apply Rules' }).click();
    await page.waitForLoadState('networkidle');

    // Wait for Apply Rules dialog
    await expect(page.getByText('Apply Rule: 100 S Stratford Maint')).toBeVisible();

    // Click Preview Changes
    await page.getByRole('button', { name: 'Preview Changes' }).click();
    await page.waitForLoadState('networkidle');

    // Check the preview results
    const transactionsMatched = page.getByText(/\d+ Transactions Would Be Updated/);
    await expect(transactionsMatched).toBeVisible();

    // Take a screenshot
    await page.screenshot({ path: 'apply-rules-preview.png', fullPage: true });

    // Get the actual count
    const previewText = await page.getByText(/\d+ Transactions Would Be Updated/).textContent();
    console.log('Preview Result:', previewText);

    // Apply the rules
    await page.getByRole('button', { name: 'Apply Rules' }).click();
    await page.waitForLoadState('networkidle');

    // Wait for success message or result
    await page.waitForTimeout(2000);

    // Take a screenshot of the result
    await page.screenshot({ path: 'apply-rules-result.png', fullPage: true });

    // Navigate to transactions to verify
    await page.getByRole('link', { name: /transactions/i }).click();
    await page.waitForLoadState('networkidle');

    // Search for "100 S Stratford Maint" category
    const searchBox = page.getByPlaceholder('Search transactions...');
    await searchBox.fill('100 S Stratford Maint');
    await page.waitForTimeout(1000); // Wait for debounce

    // Check if transactions are now classified as Capital Expense
    const capitalExpenseChips = page.getByText('Capital Expense');
    const count = await capitalExpenseChips.count();
    console.log('Transactions with Capital Expense classification:', count);

    // Take final screenshot
    await page.screenshot({ path: 'transactions-with-classification.png', fullPage: true });

    // Expect at least some transactions to be classified
    expect(count).toBeGreaterThan(0);
  });

  test('should check backend API directly', async ({ request }) => {
    // Test the rule directly via API
    const testRuleResponse = await request.post('http://localhost:8000/api/classification-rules/test', {
      data: {
        category_pattern: '100 S Stratford Maint',
        amount_min: undefined,
        amount_max: -2000,
      }
    });

    const testResult = await testRuleResponse.json();
    console.log('Backend Test Rule Result:', testResult);
    expect(testResult.matching_transactions).toBeGreaterThan(0);

    // Check transactions directly
    const transactionsResponse = await request.get('http://localhost:8000/api/transactions', {
      params: {
        search_text: '100 S Stratford Maint',
        limit: 100
      }
    });

    const transactions = await transactionsResponse.json();
    console.log('Total transactions found:', transactions.total);
    console.log('Transactions matching category:');

    transactions.transactions.forEach((t: any) => {
      console.log(`- Date: ${t.transaction_date}, Amount: ${t.amount}, Category: ${t.category?.category_name}, Classification: ${t.classification?.classification_name}`);
    });
  });
});
