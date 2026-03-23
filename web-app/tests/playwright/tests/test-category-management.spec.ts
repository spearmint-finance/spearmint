import { test, expect } from "@playwright/test";


test.describe("Category Management", () => {
  test("edit button opens edit dialog for existing category", async ({ page }) => {
    await page.goto("/settings");

    // Wait for the Categories tab to load with the DataGrid
    await expect(page.getByText("Category Management")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });

    // Wait for rows to load
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Find the first edit button (pencil icon) in the grid
    const editButton = page.locator(".MuiDataGrid-row").first().locator('button[title="Edit category"]');
    await expect(editButton).toBeVisible();
    await editButton.click();

    // The edit dialog should open with "Edit Category" title
    await expect(page.getByText("Edit Category")).toBeVisible({ timeout: 5000 });

    // The dialog should contain a Category Name field pre-filled
    const dialog = page.locator('[role="dialog"]');
    const nameField = dialog.getByLabel("Category Name");
    const nameValue = await nameField.inputValue();
    expect(nameValue.length).toBeGreaterThan(0);

    // Should have an Entity dropdown in the dialog
    await expect(dialog.getByText("Global categories are shared across all entities")).toBeVisible();

    // Should have Update button (not Create)
    await expect(page.getByRole("button", { name: "Update" })).toBeVisible();

    // Close dialog
    await page.getByRole("button", { name: "Cancel" }).click();
    await expect(page.getByText("Edit Category")).not.toBeVisible();
  });

  test("delete button shows confirmation dialog", async ({ page }) => {
    await page.goto("/settings");

    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Find the delete button in the first row
    const deleteButton = page.locator(".MuiDataGrid-row").first().locator('button[title="Delete category"]');
    await expect(deleteButton).toBeVisible();
    await deleteButton.click();

    // Should show confirmation dialog
    await expect(page.getByText("Delete Category")).toBeVisible({ timeout: 5000 });
    await expect(page.getByText("Are you sure you want to delete")).toBeVisible();

    // Cancel
    await page.getByRole("button", { name: "Cancel" }).click();
    await expect(page.getByText("Are you sure you want to delete")).not.toBeVisible();
  });

  test("add category button opens create dialog", async ({ page }) => {
    await page.goto("/settings");

    await expect(page.getByText("Category Management")).toBeVisible({ timeout: 10000 });

    // Click Add Category button
    await page.getByRole("button", { name: "Add Category" }).click();

    // Should open Create dialog (not Edit)
    await expect(page.getByText("Create Category")).toBeVisible({ timeout: 5000 });

    // Name field should be empty
    const nameField = page.getByLabel("Category Name");
    await expect(nameField).toBeVisible();
    const nameValue = await nameField.inputValue();
    expect(nameValue).toBe("");

    // Should have Create button (not Update)
    await expect(page.getByRole("button", { name: "Create" })).toBeVisible();

    // Close
    await page.getByRole("button", { name: "Cancel" }).click();
  });

  test("search filters categories by name", async ({ page }) => {
    await page.goto("/settings");
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Type a search term to filter categories
    const searchField = page.getByPlaceholder("Search categories...");
    await searchField.fill("rent");
    await page.waitForTimeout(500);

    // After filtering, the grid should show fewer rows than total
    // The count text shows "X of Y" where X is filtered count
    const filteredCountText = page.locator('p.MuiTypography-body2:has-text(" of ")');
    await expect(filteredCountText).toBeVisible({ timeout: 5000 });
    const filteredText = await filteredCountText.textContent();
    expect(filteredText).toMatch(/\d+ of \d+/);

    // The filtered count should be less than total
    const parts = filteredText!.match(/(\d+) of (\d+)/);
    const filtered = parseInt(parts![1]);
    const total = parseInt(parts![2]);
    expect(filtered).toBeLessThan(total);
    expect(filtered).toBeGreaterThan(0); // "rent" should match some categories

    // Clear search — count should restore
    await searchField.clear();
    await page.waitForTimeout(500);
    const restoredText = await filteredCountText.textContent();
    const restoredParts = restoredText!.match(/(\d+) of (\d+)/);
    expect(parseInt(restoredParts![1])).toBe(total);
  });

  test("type filter filters categories", async ({ page }) => {
    await page.goto("/settings");
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Get initial count
    const countText = page.locator('p.MuiTypography-body2:has-text(" of ")');
    await expect(countText).toBeVisible({ timeout: 5000 });
    const initialText = await countText.textContent();
    const totalMatch = initialText!.match(/(\d+) of (\d+)/);
    const total = parseInt(totalMatch![2]);

    // Click the type filter dropdown (not the DataGrid column)
    const typeFilter = page.getByRole("combobox", { name: /Type.*All Types/i });
    await typeFilter.click();
    await page.getByRole("option", { name: "Income" }).click();
    await page.waitForTimeout(500);

    // Count should be less than total
    const filteredText = await countText.textContent();
    const filteredMatch = filteredText!.match(/(\d+) of (\d+)/);
    const filtered = parseInt(filteredMatch![1]);
    expect(filtered).toBeLessThan(total);
    expect(filtered).toBeGreaterThan(0);
  });

  test("category grid shows entity column with Global/entity chips", async ({ page }) => {
    await page.goto("/settings");

    await expect(page.locator(".MuiDataGrid-root")).toBeVisible({ timeout: 10000 });
    await expect(page.locator(".MuiDataGrid-row").first()).toBeVisible({ timeout: 10000 });

    // Should have an Entity column header in the grid
    await expect(page.locator('.MuiDataGrid-columnHeaderTitle:has-text("Entity")')).toBeVisible();

    // Should have at least one "Global" chip for categories without entity
    const globalChips = page.locator('.MuiChip-root:has-text("Global")');
    await expect(globalChips.first()).toBeVisible({ timeout: 5000 });
  });
});
