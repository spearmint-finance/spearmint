import { test, expect } from '@playwright/test';

test.describe('Transaction Paging and Filtering', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/transactions');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000);
  });

  test('should display transactions on first page', async ({ page }) => {
    // Check that we have transactions displayed
    const rows = page.locator('.MuiDataGrid-row');
    const rowCount = await rows.count();
    console.log(`Rows on first page: ${rowCount}`);
    expect(rowCount).toBeGreaterThan(0);

    // Check total count is displayed
    const pagination = page.locator('.MuiTablePagination-displayedRows');
    const paginationText = await pagination.textContent();
    console.log(`Pagination text: ${paginationText}`);
    expect(paginationText).toContain('of');

    await page.screenshot({ path: 'test-screenshots/page-1.png' });
  });

  test('should navigate to page 2 and show different transactions', async ({ page }) => {
    // Get first transaction on page 1
    await page.waitForSelector('.MuiDataGrid-row');
    const firstRowPage1 = page.locator('.MuiDataGrid-row').first();
    const firstDescPage1 = await firstRowPage1.locator('[data-field="description"]').textContent();
    console.log(`First transaction on page 1: ${firstDescPage1}`);

    // Click next page button
    const nextButton = page.locator('button[aria-label="Go to next page"]');
    await nextButton.click();
    await page.waitForTimeout(1000);

    // Get first transaction on page 2
    await page.waitForSelector('.MuiDataGrid-row');
    const firstRowPage2 = page.locator('.MuiDataGrid-row').first();
    const firstDescPage2 = await firstRowPage2.locator('[data-field="description"]').textContent();
    console.log(`First transaction on page 2: ${firstDescPage2}`);

    // They should be different
    expect(firstDescPage1).not.toBe(firstDescPage2);

    // Check pagination shows page 2
    const pagination = page.locator('.MuiTablePagination-displayedRows');
    const paginationText = await pagination.textContent();
    console.log(`Pagination text on page 2: ${paginationText}`);
    expect(paginationText).toMatch(/26.*50/); // Should show something like "26-50 of X"

    await page.screenshot({ path: 'test-screenshots/page-2.png' });
  });

  test('should change page size and update display', async ({ page }) => {
    // Check initial rows (default 25)
    await page.waitForSelector('.MuiDataGrid-row');
    const initialRows = await page.locator('.MuiDataGrid-row').count();
    console.log(`Initial rows (page size 25): ${initialRows}`);
    expect(initialRows).toBe(25);

    // Change page size to 10
    const pageSizeSelect = page.locator('[aria-label="Rows per page:"]');
    await pageSizeSelect.click();
    await page.locator('li[data-value="10"]').click();
    await page.waitForTimeout(1000);

    // Check rows changed
    const newRows = await page.locator('.MuiDataGrid-row').count();
    console.log(`Rows after changing to page size 10: ${newRows}`);
    expect(newRows).toBe(10);

    await page.screenshot({ path: 'test-screenshots/page-size-10.png' });
  });

  test('should navigate back to page 1 from page 2', async ({ page }) => {
    // Go to page 2
    const nextButton = page.locator('button[aria-label="Go to next page"]');
    await nextButton.click();
    await page.waitForTimeout(1000);

    // Get first transaction on page 2
    const firstDescPage2 = await page.locator('.MuiDataGrid-row').first()
      .locator('[data-field="description"]').textContent();

    // Go back to page 1
    const prevButton = page.locator('button[aria-label="Go to previous page"]');
    await prevButton.click();
    await page.waitForTimeout(1000);

    // Get first transaction on page 1
    const firstDescPage1 = await page.locator('.MuiDataGrid-row').first()
      .locator('[data-field="description"]').textContent();

    // Should be different
    expect(firstDescPage1).not.toBe(firstDescPage2);

    // Check pagination shows page 1
    const pagination = page.locator('.MuiTablePagination-displayedRows');
    const paginationText = await pagination.textContent();
    console.log(`Back to page 1, pagination: ${paginationText}`);
    expect(paginationText).toMatch(/1.*25/);

    await page.screenshot({ path: 'test-screenshots/back-to-page-1.png' });
  });

  test('should apply filters and reset to page 1', async ({ page }) => {
    // Go to page 2 first
    const nextButton = page.locator('button[aria-label="Go to next page"]');
    await nextButton.click();
    await page.waitForTimeout(1000);

    // Open filters
    const moreFiltersButton = page.locator('button:has-text("More Filters")');
    await moreFiltersButton.click();
    await page.waitForTimeout(500);

    // Select Expense type
    const transactionTypeSelect = page.locator('select[name="transaction_type"]');
    await transactionTypeSelect.selectOption('Expense');

    // Apply filters
    const applyButton = page.locator('button:has-text("Apply Filters")');
    await applyButton.click();
    await page.waitForTimeout(1000);

    // Check we're back on page 1
    const pagination = page.locator('.MuiTablePagination-displayedRows');
    const paginationText = await pagination.textContent();
    console.log(`After filtering, pagination: ${paginationText}`);
    expect(paginationText).toMatch(/1.*25/);

    await page.screenshot({ path: 'test-screenshots/filtered-page-1.png' });
  });

  test('should uncheck capital expenses filter and update transactions', async ({ page }) => {
    // Get initial total
    const initialTotal = page.locator('text=Total Expenses').locator('..').locator('p').nth(1);
    const initialTotalText = await initialTotal.textContent();
    console.log(`Initial total expenses: ${initialTotalText}`);

    // Open filters
    const moreFiltersButton = page.locator('button:has-text("More Filters")');
    await moreFiltersButton.click();
    await page.waitForTimeout(500);

    // Uncheck "Include Capital Expenses"
    const capitalExpensesCheckbox = page.locator('input[type="checkbox"]').nth(0); // First checkbox
    const isChecked = await capitalExpensesCheckbox.isChecked();
    console.log(`Capital expenses checkbox initially checked: ${isChecked}`);

    if (isChecked) {
      await capitalExpensesCheckbox.click();
    }

    // Apply filters
    const applyButton = page.locator('button:has-text("Apply Filters")');
    await applyButton.click();
    await page.waitForTimeout(1000);

    // Get new total
    const newTotal = page.locator('text=Total Expenses').locator('..').locator('p').nth(1);
    const newTotalText = await newTotal.textContent();
    console.log(`Total after unchecking capital expenses: ${newTotalText}`);

    // Total should change (be less if there are capital expenses)
    expect(newTotalText).not.toBe(initialTotalText);

    await page.screenshot({ path: 'test-screenshots/no-capital-expenses.png' });
  });

  test('should uncheck transfers filter and update transactions', async ({ page }) => {
    // Get initial total
    const initialTotal = page.locator('text=Total Expenses').locator('..').locator('p').nth(1);
    const initialTotalText = await initialTotal.textContent();
    console.log(`Initial total expenses: ${initialTotalText}`);

    // Open filters
    const moreFiltersButton = page.locator('button:has-text("More Filters")');
    await moreFiltersButton.click();
    await page.waitForTimeout(500);

    // Uncheck "Include Transfers"
    const transfersCheckbox = page.locator('input[type="checkbox"]').nth(1); // Second checkbox
    const isChecked = await transfersCheckbox.isChecked();
    console.log(`Transfers checkbox initially checked: ${isChecked}`);

    if (isChecked) {
      await transfersCheckbox.click();
    }

    // Apply filters
    const applyButton = page.locator('button:has-text("Apply Filters")');
    await applyButton.click();
    await page.waitForTimeout(1000);

    // Get new total
    const newTotal = page.locator('text=Total Expenses').locator('..').locator('p').nth(1);
    const newTotalText = await newTotal.textContent();
    console.log(`Total after unchecking transfers: ${newTotalText}`);

    await page.screenshot({ path: 'test-screenshots/no-transfers.png' });
  });

  test('should combine filters and paging', async ({ page }) => {
    // Open filters
    const moreFiltersButton = page.locator('button:has-text("More Filters")');
    await moreFiltersButton.click();
    await page.waitForTimeout(500);

    // Select Expense type and date range
    const transactionTypeSelect = page.locator('select[name="transaction_type"]');
    await transactionTypeSelect.selectOption('Expense');

    const startDateInput = page.locator('input[name="start_date"]');
    await startDateInput.fill('2025-09-01');

    const endDateInput = page.locator('input[name="end_date"]');
    await endDateInput.fill('2025-09-30');

    // Uncheck both capital expenses and transfers
    const capitalExpensesCheckbox = page.locator('input[type="checkbox"]').nth(0);
    if (await capitalExpensesCheckbox.isChecked()) {
      await capitalExpensesCheckbox.click();
    }

    const transfersCheckbox = page.locator('input[type="checkbox"]').nth(1);
    if (await transfersCheckbox.isChecked()) {
      await transfersCheckbox.click();
    }

    // Apply filters
    const applyButton = page.locator('button:has-text("Apply Filters")');
    await applyButton.click();
    await page.waitForTimeout(1000);

    // Check we have results
    const rows = page.locator('.MuiDataGrid-row');
    const rowCount = await rows.count();
    console.log(`Rows after combined filters: ${rowCount}`);

    // Get pagination info
    const pagination = page.locator('.MuiTablePagination-displayedRows');
    const paginationText = await pagination.textContent();
    console.log(`Pagination with filters: ${paginationText}`);

    // Try to go to page 2 if available
    const nextButton = page.locator('button[aria-label="Go to next page"]');
    const isNextEnabled = await nextButton.isEnabled();
    console.log(`Next page button enabled: ${isNextEnabled}`);

    if (isNextEnabled) {
      await nextButton.click();
      await page.waitForTimeout(1000);

      const page2Pagination = await page.locator('.MuiTablePagination-displayedRows').textContent();
      console.log(`Page 2 pagination: ${page2Pagination}`);
    }

    await page.screenshot({ path: 'test-screenshots/combined-filters-paging.png' });
  });
});
