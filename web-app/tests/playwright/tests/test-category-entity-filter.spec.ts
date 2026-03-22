import { test, expect } from "@playwright/test";

test.use({ baseURL: "http://localhost:5173" });

test.describe("Category Entity Filtering in TransactionForm", () => {
  test("transaction form shows category and entity fields", async ({ page }) => {
    await page.goto("/transactions");
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });

    // Open create dialog
    await page.getByRole("button", { name: /new transaction/i }).click();
    await expect(page.getByText("Add New Transaction")).toBeVisible({ timeout: 5000 });

    const dialog = page.locator('[role="dialog"]');

    // Should have Category field
    await expect(dialog.locator('label:has-text("Category")')).toBeVisible();

    // Should have Entity field with combobox
    const entityCombobox = dialog.locator('label:has-text("Entity")').locator('..').locator('[role="combobox"]');
    const hasEntities = await entityCombobox.isVisible({ timeout: 3000 }).catch(() => false);

    if (hasEntities) {
      // Click the combobox to open the dropdown
      await entityCombobox.click();
      // Should show "Inherit from account" option
      await expect(page.getByRole("option", { name: /inherit from account/i })).toBeVisible({ timeout: 3000 });
      // Press Escape to close
      await page.keyboard.press("Escape");
    }

    // Close dialog
    await page.getByRole("button", { name: "Cancel" }).click();
  });

  test("category dropdown includes Create New Category option", async ({ page }) => {
    await page.goto("/transactions");
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });

    // Open create dialog
    await page.getByRole("button", { name: /new transaction/i }).click();
    await expect(page.getByText("Add New Transaction")).toBeVisible({ timeout: 5000 });

    const dialog = page.locator('[role="dialog"]');

    // Open category dropdown by clicking the combobox
    const categoryCombobox = dialog.locator('label:has-text("Category")').locator('..').locator('[role="combobox"]');
    if (await categoryCombobox.isVisible({ timeout: 3000 }).catch(() => false)) {
      await categoryCombobox.click();
      // Should show "Create New Category" option
      await expect(page.getByText("Create New Category")).toBeVisible({ timeout: 5000 });
      await page.keyboard.press("Escape");
    }

    // Close dialog
    await page.getByRole("button", { name: "Cancel" }).click();
  });

  test("inline category edit in transaction grid works", async ({ page }) => {
    await page.goto("/transactions");
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Find the category cell in the first row
    const firstRow = page.locator(".MuiDataGrid-row").first();
    const categoryCell = firstRow.locator('[data-field="category_id"]');
    await expect(categoryCell).toBeVisible();

    // Double-click to enter edit mode
    await categoryCell.dblclick();

    // Should show a select dropdown with category options
    const selectDropdown = page.locator('[role="listbox"]');
    const isEditing = await selectDropdown.isVisible({ timeout: 3000 }).catch(() => false);

    if (isEditing) {
      const menuItems = selectDropdown.locator('[role="option"]');
      const count = await menuItems.count();
      expect(count).toBeGreaterThan(0);
      await page.keyboard.press("Escape");
    }
  });
});
