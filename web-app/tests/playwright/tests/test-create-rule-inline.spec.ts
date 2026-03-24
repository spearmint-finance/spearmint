import { test, expect } from "@playwright/test";

test.describe("Transactions – Create Rule Inline", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/transactions");
    await page.waitForSelector(".MuiDataGrid-row", { timeout: 15000 });
  });

  test("rule icon button opens create rule dialog pre-filled with transaction description", async ({
    page,
  }) => {
    const firstRow = page.locator(".MuiDataGrid-row").first();
    await expect(firstRow).toBeVisible();

    // Get the transaction description for verification
    const descCell = firstRow.locator('[data-field="description"]');
    const description = (await descCell.textContent())?.trim() || "";

    // Click the rule icon button (last cell action)
    const ruleButton = firstRow.locator('button').filter({ has: page.locator('svg[data-testid="RuleIcon"]') });
    await expect(ruleButton).toBeVisible();
    await ruleButton.click();

    // The Create Rule dialog should open
    const dialog = page.locator('[role="dialog"]').filter({ hasText: "Create Transaction Rule" });
    await expect(dialog).toBeVisible({ timeout: 5000 });

    // The description pattern field should be pre-filled
    const patternInput = dialog.locator('input').nth(1); // Second input (after rule name)
    const patternValue = await patternInput.inputValue();
    expect(patternValue).toContain(description.slice(0, 20)); // At least partial match

    // Rule name should also be pre-filled
    const nameInput = dialog.locator('input').first();
    const nameValue = await nameInput.inputValue();
    expect(nameValue.length).toBeGreaterThan(0);

    // Cancel should close the dialog
    await dialog.getByRole("button", { name: "Cancel" }).click();
    await expect(dialog).not.toBeVisible();
  });
});
