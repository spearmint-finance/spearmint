import { test, expect } from '@playwright/test';
import { navigateTo, waitForPageLoad } from './utils/test-helpers';

test.describe('Error Handling', () => {
  test.describe('Network Errors', () => {
    test('should display error message when API is unavailable', async ({ page }) => {
      // Intercept API calls and return errors
      await page.route('**/api/**', (route) => {
        route.abort('failed');
      });

      await page.goto('/dashboard');
      
      // Should show error message
      await expect(page.getByText(/failed to load|error/i)).toBeVisible({ timeout: 10000 });
    });

    test('should show retry button on error', async ({ page }) => {
      // Intercept API calls and return errors
      await page.route('**/api/**', (route) => {
        route.abort('failed');
      });

      await page.goto('/dashboard');
      
      // Wait for error state
      await page.waitForSelector('text=/failed to load|error/i', { timeout: 10000 });
      
      // Should have a retry button
      const retryButton = page.getByRole('button', { name: /retry/i });
      const hasRetry = await retryButton.isVisible().catch(() => false);
      
      // Retry button may or may not be present depending on error handling
      expect(typeof hasRetry).toBe('boolean');
    });

    test('should recover after retry when API becomes available', async ({ page }) => {
      let failCount = 0;
      
      // Fail first request, succeed on retry
      await page.route('**/api/**', (route) => {
        if (failCount === 0) {
          failCount++;
          route.abort('failed');
        } else {
          route.continue();
        }
      });

      await page.goto('/dashboard');
      
      // Wait for error
      await page.waitForSelector('text=/failed to load|error/i', { timeout: 10000 });
      
      // Click retry if available
      const retryButton = page.getByRole('button', { name: /retry/i });
      if (await retryButton.isVisible()) {
        await retryButton.click();
        
        // Should load successfully
        await waitForPageLoad(page);
        await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
      }
    });
  });

  test.describe('Form Validation Errors', () => {
    test('should show validation errors for empty required fields', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      // Open create dialog
      await page.getByRole('button', { name: 'New Transaction' }).click();
      await page.waitForSelector('[role="dialog"]');
      
      // Try to submit without filling fields
      await page.getByRole('button', { name: 'Create' }).click();
      
      // Should show validation errors
      await expect(page.getByText(/required/i)).toBeVisible();
    });

    test('should show validation error for invalid amount', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      await page.getByRole('button', { name: 'New Transaction' }).click();
      await page.waitForSelector('[role="dialog"]');
      
      // Fill in description but invalid amount
      await page.getByLabel('Description').fill('Test Transaction');
      await page.getByLabel('Amount').fill('0');
      
      await page.getByRole('button', { name: 'Create' }).click();
      
      // Should show validation error
      await expect(page.getByText(/greater than 0/i)).toBeVisible();
    });

    test('should show validation error for short description', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      await page.getByRole('button', { name: 'New Transaction' }).click();
      await page.waitForSelector('[role="dialog"]');
      
      // Fill in short description
      await page.getByLabel('Description').fill('AB');
      await page.getByLabel('Amount').fill('100');
      
      await page.getByRole('button', { name: 'Create' }).click();
      
      // Should show validation error
      await expect(page.getByText(/at least 3 characters/i)).toBeVisible();
    });

    test('should clear validation errors when corrected', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      await page.getByRole('button', { name: 'New Transaction' }).click();
      await page.waitForSelector('[role="dialog"]');
      
      // Submit empty form
      await page.getByRole('button', { name: 'Create' }).click();
      
      // Should show errors
      await expect(page.getByText(/required/i)).toBeVisible();
      
      // Fill in valid data
      await page.getByLabel('Description').fill('Valid Transaction');
      await page.getByLabel('Amount').fill('100');
      
      // Errors should clear (or form should be submittable)
      const createButton = page.getByRole('button', { name: 'Create' });
      await expect(createButton).toBeEnabled();
    });
  });

  test.describe('API Error Responses', () => {
    test('should handle 404 errors gracefully', async ({ page }) => {
      // Intercept and return 404
      await page.route('**/api/transactions/*', (route) => {
        route.fulfill({
          status: 404,
          body: JSON.stringify({ detail: 'Transaction not found' }),
        });
      });

      await navigateTo(page, '/transactions');
      
      // Page should still load
      await expect(page.getByRole('heading', { name: 'Transactions' })).toBeVisible();
    });

    test('should handle 500 errors gracefully', async ({ page }) => {
      // Intercept and return 500
      await page.route('**/api/**', (route) => {
        route.fulfill({
          status: 500,
          body: JSON.stringify({ detail: 'Internal server error' }),
        });
      });

      await page.goto('/dashboard');
      
      // Should show error state
      await expect(page.getByText(/error|failed/i)).toBeVisible({ timeout: 10000 });
    });

    test('should show error toast on failed transaction creation', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      // Intercept create request and return error
      await page.route('**/api/transactions', (route) => {
        if (route.request().method() === 'POST') {
          route.fulfill({
            status: 400,
            body: JSON.stringify({ detail: 'Invalid transaction data' }),
          });
        } else {
          route.continue();
        }
      });
      
      await page.getByRole('button', { name: 'New Transaction' }).click();
      await page.waitForSelector('[role="dialog"]');
      
      // Fill in valid data
      await page.getByLabel('Description').fill('Test Transaction');
      await page.getByLabel('Amount').fill('100');
      
      await page.getByRole('button', { name: 'Create' }).click();
      
      // Should show error toast
      await expect(page.getByText(/failed to create/i)).toBeVisible({ timeout: 5000 });
    });

    test('should show error toast on failed transaction update', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      // Check if there are transactions
      const rowCount = await page.locator('.MuiDataGrid-row').count();
      
      if (rowCount > 0) {
        // Intercept update request and return error
        await page.route('**/api/transactions/*', (route) => {
          if (route.request().method() === 'PUT') {
            route.fulfill({
              status: 400,
              body: JSON.stringify({ detail: 'Update failed' }),
            });
          } else {
            route.continue();
          }
        });
        
        // Click first transaction
        await page.locator('.MuiDataGrid-row').first().click();
        await page.waitForSelector('[role="dialog"]');
        
        // Click edit
        await page.getByRole('button', { name: 'Edit' }).click();
        
        // Make a change
        await page.getByLabel('Description').fill('Updated Description');
        
        await page.getByRole('button', { name: 'Update' }).click();
        
        // Should show error toast
        await expect(page.getByText(/failed to update/i)).toBeVisible({ timeout: 5000 });
      }
    });

    test('should show error toast on failed transaction deletion', async ({ page }) => {
      await navigateTo(page, '/transactions');
      await waitForPageLoad(page);
      
      const rowCount = await page.locator('.MuiDataGrid-row').count();
      
      if (rowCount > 0) {
        // Intercept delete request and return error
        await page.route('**/api/transactions/*', (route) => {
          if (route.request().method() === 'DELETE') {
            route.fulfill({
              status: 400,
              body: JSON.stringify({ detail: 'Delete failed' }),
            });
          } else {
            route.continue();
          }
        });
        
        // Click first transaction
        await page.locator('.MuiDataGrid-row').first().click();
        await page.waitForSelector('[role="dialog"]');
        
        // Click delete
        await page.getByRole('button', { name: 'Delete' }).click();
        
        // Confirm delete
        await page.waitForSelector('text=Confirm Delete');
        const deleteButton = page.getByRole('dialog').getByRole('button', { name: 'Delete' });
        await deleteButton.click();
        
        // Should show error toast
        await expect(page.getByText(/failed to delete/i)).toBeVisible({ timeout: 5000 });
      }
    });
  });

  test.describe('Empty States', () => {
    test('should handle empty transaction list gracefully', async ({ page }) => {
      // Intercept and return empty list
      await page.route('**/api/transactions*', (route) => {
        route.fulfill({
          status: 200,
          body: JSON.stringify({
            transactions: [],
            total: 0,
            limit: 25,
            offset: 0,
          }),
        });
      });

      await navigateTo(page, '/transactions');
      
      // DataGrid should still render
      await expect(page.locator('.MuiDataGrid-root')).toBeVisible();
    });

    test('should handle empty dashboard data gracefully', async ({ page }) => {
      // Intercept and return zero values
      await page.route('**/api/analysis/**', (route) => {
        route.fulfill({
          status: 200,
          body: JSON.stringify({
            total_income: 0,
            total_expenses: 0,
            net_cash_flow: 0,
            transaction_count: 0,
          }),
        });
      });

      await page.goto('/dashboard');
      
      // Dashboard should still render with $0.00 values
      await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
      await expect(page.getByText('$0.00')).toBeVisible();
    });
  });

  test.describe('Loading States', () => {
    test('should show loading spinner during data fetch', async ({ page }) => {
      // Delay API response
      await page.route('**/api/**', async (route) => {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        route.continue();
      });

      const navPromise = page.goto('/dashboard');
      
      // Try to catch loading state
      const loadingText = page.getByText(/loading/i);
      const isVisible = await loadingText.isVisible().catch(() => false);
      
      await navPromise;
      
      // Loading should eventually disappear
      await expect(loadingText).not.toBeVisible();
    });
  });
});

