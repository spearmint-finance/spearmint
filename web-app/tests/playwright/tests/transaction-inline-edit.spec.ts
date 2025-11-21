import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForPageLoad,
  waitForDataGrid,
} from "../../utils/test-helpers";

// Inline edit Category cell and verify it persists
// Assumes backend API is running at :8000 and frontend dev server is started by Playwright config

test.describe("Transactions – Inline Edit Category", () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, "/transactions");
    await waitForDataGrid(page);
  });

  test("should inline edit the category and persist the change", async ({
    page,
  }) => {
    // Find first row and the Category column cell (Date=0, Description=1, Category=2)
    const firstRow = page.locator(".MuiDataGrid-row").first();
    await expect(firstRow).toBeVisible();

    const categoryCell = firstRow.locator(".MuiDataGrid-cell").nth(2);
    const originalText = (await categoryCell.textContent())?.trim() || "";

    // Enter edit mode on the category cell
    await categoryCell.dblclick();

    // Open the singleSelect dropdown (role=combobox)
    const combo = firstRow.locator('[role="combobox"]');
    await combo.click();

    // Select a different option from the list
    const options = page.locator('[role="option"]');
    const count = await options.count();
    expect(count).toBeGreaterThan(0);

    // Choose the first option with different text than the original (if possible)
    let chosenIndex = 0;
    for (let i = 0; i < count; i++) {
      const text = (await options.nth(i).textContent())?.trim() || "";
      if (text && text !== originalText) {
        chosenIndex = i;
        break;
      }
    }

    const chosen = options.nth(chosenIndex);
    const chosenText = (await chosen.textContent())?.trim() || "";
    await chosen.click();

    // Commit the row edit (press Enter)
    await page.keyboard.press("Enter");

    // Expect success toast
    await page
      .getByText("Transaction updated successfully")
      .waitFor({ timeout: 10000 });

    // Wait for any refetch/render
    await waitForPageLoad(page);

    // Verify the Category cell now displays the chosen option text
    const updatedText = (await categoryCell.textContent())?.trim() || "";
    expect(updatedText).toBe(chosenText);
  });
});
