import { test, expect } from '@playwright/test';
import {
  navigateTo,
  waitForPageLoad,
  waitForDialog,
  waitForToast,
  fillFormField,
  selectRadio,
  clickButton,
  waitForDataGrid,
  clickDataGridRow,
  getDataGridRowCount,
} from './utils/test-helpers';
import {
  generateTestTransaction,
  testTransactions,
  invalidTransactions,
  expectedValidationMessages,
} from './fixtures/test-data';

test.describe('Transaction CRUD Operations', () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, '/transactions');
    await waitForDataGrid(page);
  });

  test.describe('Create Transaction', () => {
    test('should open create transaction dialog', async ({ page }) => {
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
    });

    test('should create a new expense transaction', async ({ page }) => {
      const transaction = generateTestTransaction('Expense');
      
      // Open create dialog
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      // Fill in form
      await fillFormField(page, 'Date', transaction.date);
      await selectRadio(page, 'Expense');
      await fillFormField(page, 'Description', transaction.description);
      await fillFormField(page, 'Amount', transaction.amount.toString());
      await fillFormField(page, 'Notes', transaction.notes);
      
      // Submit form
      await clickButton(page, 'Create');
      
      // Wait for success toast
      await waitForToast(page, 'Transaction created successfully', 'success');
      
      // Dialog should close
      await expect(page.getByRole('dialog')).not.toBeVisible();
      
      // Transaction should appear in list
      await waitForPageLoad(page);
      await expect(page.getByText(transaction.description)).toBeVisible();
    });

    test('should create a new income transaction', async ({ page }) => {
      const transaction = generateTestTransaction('Income');
      
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      await fillFormField(page, 'Date', transaction.date);
      await selectRadio(page, 'Income');
      await fillFormField(page, 'Description', transaction.description);
      await fillFormField(page, 'Amount', transaction.amount.toString());
      
      await clickButton(page, 'Create');
      await waitForToast(page, 'Transaction created successfully', 'success');
      
      await waitForPageLoad(page);
      await expect(page.getByText(transaction.description)).toBeVisible();
    });

    test('should validate required fields', async ({ page }) => {
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      // Try to submit without filling required fields
      await clickButton(page, 'Create');
      
      // Should show validation errors
      await expect(page.getByText(expectedValidationMessages.descriptionRequired)).toBeVisible();
      await expect(page.getByText(expectedValidationMessages.amountRequired)).toBeVisible();
    });

    test('should validate description length', async ({ page }) => {
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      // Enter short description
      await fillFormField(page, 'Description', invalidTransactions.shortDescription.description);
      await fillFormField(page, 'Amount', '100');
      
      await clickButton(page, 'Create');
      
      // Should show validation error
      await expect(page.getByText(expectedValidationMessages.descriptionTooShort)).toBeVisible();
    });

    test('should validate amount is greater than zero', async ({ page }) => {
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      await fillFormField(page, 'Description', 'Test Transaction');
      await fillFormField(page, 'Amount', '0');
      
      await clickButton(page, 'Create');
      
      // Should show validation error
      await expect(page.getByText(expectedValidationMessages.amountTooSmall)).toBeVisible();
    });

    test('should cancel transaction creation', async ({ page }) => {
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      // Fill in some data
      await fillFormField(page, 'Description', 'Test Transaction');
      
      // Click cancel
      await clickButton(page, 'Cancel');
      
      // Dialog should close
      await expect(page.getByRole('dialog')).not.toBeVisible();
    });
  });

  test.describe('Read Transaction', () => {
    test('should view transaction details', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        // Click first transaction
        await clickDataGridRow(page, 0);
        
        // Detail dialog should open
        await waitForDialog(page, 'Transaction Details');
        
        // Should show transaction information
        await expect(page.getByText('Description')).toBeVisible();
        await expect(page.getByText('Amount')).toBeVisible();
        await expect(page.getByText('Date')).toBeVisible();
      }
    });

    test('should display transaction type badge', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        // Should show Income or Expense chip
        const chip = page.locator('.MuiChip-root').filter({ hasText: /Income|Expense/ });
        await expect(chip).toBeVisible();
      }
    });

    test('should show edit and delete buttons', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await expect(page.getByRole('button', { name: 'Edit' })).toBeVisible();
        await expect(page.getByRole('button', { name: 'Delete' })).toBeVisible();
      }
    });

    test('should close detail dialog', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Close');
        await expect(page.getByRole('dialog')).not.toBeVisible();
      }
    });
  });

  test.describe('Update Transaction', () => {
    test('should open edit dialog from detail view', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Edit');
        await waitForDialog(page, 'Edit Transaction');
      }
    });

    test('should update transaction description', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Edit');
        await waitForDialog(page, 'Edit Transaction');
        
        // Update description
        const newDescription = `Updated ${Date.now()}`;
        await fillFormField(page, 'Description', newDescription);
        
        await clickButton(page, 'Update');
        await waitForToast(page, 'Transaction updated successfully', 'success');
        
        // Verify update
        await waitForPageLoad(page);
        await expect(page.getByText(newDescription)).toBeVisible();
      }
    });

    test('should update transaction amount', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Edit');
        await waitForDialog(page, 'Edit Transaction');
        
        // Update amount
        await fillFormField(page, 'Amount', '999.99');
        
        await clickButton(page, 'Update');
        await waitForToast(page, 'Transaction updated successfully', 'success');
      }
    });

    test('should validate updated fields', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Edit');
        await waitForDialog(page, 'Edit Transaction');
        
        // Clear description
        await fillFormField(page, 'Description', '');
        
        await clickButton(page, 'Update');
        
        // Should show validation error
        await expect(page.getByText(expectedValidationMessages.descriptionRequired)).toBeVisible();
      }
    });

    test('should cancel transaction update', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Edit');
        await waitForDialog(page, 'Edit Transaction');
        
        // Make a change
        await fillFormField(page, 'Description', 'Changed');
        
        // Cancel
        await clickButton(page, 'Cancel');
        
        // Edit dialog should close
        await expect(page.getByText('Edit Transaction')).not.toBeVisible();
      }
    });
  });

  test.describe('Delete Transaction', () => {
    test('should show delete confirmation dialog', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Delete');
        
        // Confirmation dialog should appear
        await waitForDialog(page, 'Confirm Delete');
        await expect(page.getByText('Are you sure you want to delete this transaction?')).toBeVisible();
      }
    });

    test('should cancel delete operation', async ({ page }) => {
      const rowCount = await getDataGridRowCount(page);
      
      if (rowCount > 0) {
        await clickDataGridRow(page, 0);
        await waitForDialog(page, 'Transaction Details');
        
        await clickButton(page, 'Delete');
        await waitForDialog(page, 'Confirm Delete');
        
        // Click cancel
        await clickButton(page, 'Cancel');
        
        // Confirmation dialog should close
        await expect(page.getByText('Confirm Delete')).not.toBeVisible();
      }
    });

    test('should delete transaction successfully', async ({ page }) => {
      // First create a transaction to delete
      const transaction = generateTestTransaction('Expense');
      
      await clickButton(page, 'New Transaction');
      await waitForDialog(page, 'Add New Transaction');
      
      await fillFormField(page, 'Date', transaction.date);
      await fillFormField(page, 'Description', transaction.description);
      await fillFormField(page, 'Amount', transaction.amount.toString());
      
      await clickButton(page, 'Create');
      await waitForToast(page, 'Transaction created successfully', 'success');
      await waitForPageLoad(page);
      
      // Now find and delete it
      await expect(page.getByText(transaction.description)).toBeVisible();
      
      // Click on the transaction
      const transactionRow = page.locator('.MuiDataGrid-row').filter({ hasText: transaction.description });
      await transactionRow.click();
      
      await waitForDialog(page, 'Transaction Details');
      
      await clickButton(page, 'Delete');
      await waitForDialog(page, 'Confirm Delete');
      
      // Confirm delete
      const deleteButton = page.getByRole('dialog').getByRole('button', { name: 'Delete' });
      await deleteButton.click();
      
      await waitForToast(page, 'Transaction deleted successfully', 'success');
      
      // Transaction should be removed from list
      await waitForPageLoad(page);
      await expect(page.getByText(transaction.description)).not.toBeVisible();
    });
  });
});

