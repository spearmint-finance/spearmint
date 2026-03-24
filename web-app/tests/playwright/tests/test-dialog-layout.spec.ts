import { test, expect } from "@playwright/test";

test.describe("Transaction Dialog Layout", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/transactions");
    await page.waitForSelector(".MuiDataGrid-row", { timeout: 15000 });
  });

  test("new transaction dialog has X close button and sticky actions", async ({ page }) => {
    // Click the "New Transaction" button
    await page.getByRole("button", { name: "New Transaction" }).click();

    // Dialog should open
    const dialog = page.locator('[role="dialog"]').filter({ hasText: "Add New Transaction" });
    await expect(dialog).toBeVisible({ timeout: 5000 });

    // Should have X close button in title bar
    const closeButton = dialog.locator('button[aria-label="Close"]');
    await expect(closeButton).toBeVisible();

    // Should have Create button
    await expect(dialog.getByRole("button", { name: "Create" })).toBeVisible();

    // Should have Cancel button
    await expect(dialog.getByRole("button", { name: "Cancel" })).toBeVisible();

    // Close via X button
    await closeButton.click();
    await expect(dialog).not.toBeVisible();
  });
});
