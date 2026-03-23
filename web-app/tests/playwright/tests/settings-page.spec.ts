import { test, expect } from "@playwright/test";


test.describe("Settings Page", () => {
  test("settings page loads without crashing", async ({ page }) => {
    await page.goto("/settings");

    // Should see the Settings page with tabs
    await expect(page.getByText("Categories")).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("API Keys")).toBeVisible();

    // The Categories tab (default) should load the DataGrid without errors
    // Check that the category management content is visible (not a blank page)
    await expect(page.getByText("Category Management")).toBeVisible({ timeout: 10000 });
    await expect(page.getByText("Add Category")).toBeVisible();

    // Verify no uncaught errors by checking the page didn't crash
    // The DataGrid should be present
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
  });

  test("API Keys tab loads and shows key management", async ({ page }) => {
    await page.goto("/settings");

    // Click the API Keys tab
    await page.getByText("API Keys").click();

    // Should show API key management content (either keys list or empty state)
    // Wait for loading to complete (no spinner)
    await expect(page.locator("text=CircularProgress")).not.toBeVisible({ timeout: 10000 }).catch(() => {});

    // Should see either existing keys or the "Generate New Key" button
    const hasKeys = await page.getByText("Generate New Key").isVisible().catch(() => false);
    const hasTable = await page.locator("table").isVisible().catch(() => false);
    const hasEmptyState = await page.getByText("No API keys").isVisible().catch(() => false);

    expect(hasKeys || hasTable || hasEmptyState).toBeTruthy();
  });

  test("can switch between all settings tabs", async ({ page }) => {
    await page.goto("/settings");

    // Categories tab (default)
    await expect(page.getByText("Category Management")).toBeVisible({ timeout: 10000 });

    // Preferences tab
    await page.getByRole("tab", { name: /preferences/i }).click();
    await expect(page.getByRole("tabpanel")).toBeVisible();

    // Theme tab
    await page.getByRole("tab", { name: /theme/i }).click();
    await expect(page.getByRole("tabpanel")).toBeVisible();

    // API Keys tab
    await page.getByRole("tab", { name: /api keys/i }).click();
    await expect(page.getByRole("tabpanel")).toBeVisible();
  });
});
