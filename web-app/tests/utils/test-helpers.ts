import { Page, expect } from '@playwright/test';

/**
 * Wait for the page to finish loading (no loading spinners)
 */
export async function waitForPageLoad(page: Page) {
  // Wait for any loading spinners to disappear
  await page.waitForSelector('text=Loading', { state: 'hidden', timeout: 10000 }).catch(() => {
    // Ignore if no loading spinner found
  });
  
  // Wait for network to be idle
  await page.waitForLoadState('networkidle');
}

/**
 * Navigate to a specific page and wait for it to load
 */
export async function navigateTo(page: Page, path: string) {
  await page.goto(path);
  await waitForPageLoad(page);
}

/**
 * Click on a sidebar menu item
 */
export async function clickSidebarItem(page: Page, itemName: string) {
  await page.getByRole('button', { name: itemName }).click();
  await waitForPageLoad(page);
}

/**
 * Wait for a toast notification to appear
 */
export async function waitForToast(page: Page, message: string, type: 'success' | 'error' = 'success') {
  const toastSelector = `.notistack-SnackbarContainer`;
  await page.waitForSelector(toastSelector, { timeout: 5000 });
  
  // Verify the message appears
  await expect(page.locator(toastSelector)).toContainText(message, { timeout: 5000 });
}

/**
 * Fill in a form field by label
 */
export async function fillFormField(page: Page, label: string, value: string) {
  const field = page.getByLabel(label, { exact: false });
  await field.clear();
  await field.fill(value);
}

/**
 * Select a radio button by label
 */
export async function selectRadio(page: Page, value: string) {
  await page.getByRole('radio', { name: value }).click();
}

/**
 * Click a button by text
 */
export async function clickButton(page: Page, text: string) {
  await page.getByRole('button', { name: text, exact: false }).click();
}

/**
 * Wait for a dialog to open
 */
export async function waitForDialog(page: Page, title: string) {
  await page.getByRole('dialog').waitFor({ state: 'visible' });
  await expect(page.getByRole('dialog')).toContainText(title);
}

/**
 * Close a dialog
 */
export async function closeDialog(page: Page) {
  // Try clicking the close button or Cancel button
  const closeButton = page.getByRole('button', { name: /close|cancel/i });
  if (await closeButton.isVisible()) {
    await closeButton.click();
  }
  await page.getByRole('dialog').waitFor({ state: 'hidden' });
}

/**
 * Format currency for comparison
 */
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * Get current date in YYYY-MM-DD format
 */
export function getCurrentDate(): string {
  return new Date().toISOString().split('T')[0];
}

/**
 * Wait for DataGrid to load
 */
export async function waitForDataGrid(page: Page) {
  await page.waitForSelector('.MuiDataGrid-root', { timeout: 10000 });
  await page.waitForSelector('.MuiDataGrid-row', { timeout: 10000 }).catch(() => {
    // Ignore if no rows (empty state)
  });
}

/**
 * Get row count from DataGrid
 */
export async function getDataGridRowCount(page: Page): Promise<number> {
  const rows = await page.locator('.MuiDataGrid-row').count();
  return rows;
}

/**
 * Click a DataGrid row by index
 */
export async function clickDataGridRow(page: Page, index: number) {
  await page.locator('.MuiDataGrid-row').nth(index).click();
}

/**
 * Search in DataGrid
 */
export async function searchDataGrid(page: Page, searchText: string) {
  const searchInput = page.getByPlaceholder('Search transactions...');
  await searchInput.clear();
  await searchInput.fill(searchText);
  await page.waitForTimeout(500); // Debounce
  await waitForPageLoad(page);
}

/**
 * Check if element contains text
 */
export async function expectTextContent(page: Page, selector: string, text: string) {
  await expect(page.locator(selector)).toContainText(text);
}

/**
 * Verify error message is displayed
 */
export async function expectErrorMessage(page: Page, message: string) {
  await expect(page.getByText(message)).toBeVisible();
}

/**
 * Verify success state
 */
export async function expectSuccess(page: Page) {
  // Check for absence of error messages
  await expect(page.getByText(/failed|error/i)).not.toBeVisible();
}

