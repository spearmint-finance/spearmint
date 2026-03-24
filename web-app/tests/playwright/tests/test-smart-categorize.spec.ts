import { test, expect } from "@playwright/test";

test.describe("Smart Categorize", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/transactions");
    await page.waitForSelector(".MuiDataGrid-row", { timeout: 15000 });
  });

  test("Smart Categorize button exists and opens dialog", async ({ page }) => {
    // Find the Smart Categorize button
    const button = page.getByRole("button", { name: "Smart Categorize" });
    await expect(button).toBeVisible();

    // Click it
    await button.click();

    // Dialog should open
    const dialog = page.locator('[role="dialog"]').filter({ hasText: "Smart Categorization" });
    await expect(dialog).toBeVisible({ timeout: 10000 });

    // Should show loading or results (depending on API key)
    // Either "Analyzing transactions..." spinner or results/warning
    await page.waitForSelector('[role="dialog"] .MuiCircularProgress-root, [role="dialog"] .MuiAlert-root, [role="dialog"] [class*="subtitle2"]', { timeout: 30000 });

    // Close button should be visible
    const closeButton = dialog.locator('button[aria-label="Close"]');
    await expect(closeButton).toBeVisible();

    // Close the dialog
    await closeButton.click();
    await expect(dialog).not.toBeVisible();
  });
});
