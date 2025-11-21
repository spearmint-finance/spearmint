import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForDataGrid,
  waitForPageLoad,
  searchDataGrid,
  waitForToast,
} from "../../utils/test-helpers";

// Reproduce the reported inline edit behavior and validate the correct flow

test.describe("Transactions – Inline Category Edit behavior", () => {
  test("double-click -> select category -> no navigation -> dropdown closes -> persists after refresh", async ({
    page,
  }) => {
    // Capture console errors and network issues
    const consoleErrors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });

    const failedApi: string[] = [];
    page.on("response", async (res) => {
      const url = res.url();
      if (
        url.includes("/transactions/") &&
        res.request().method() === "PUT" &&
        res.status() >= 400
      ) {
        failedApi.push(`${res.status()} ${url}`);
      }
    });

    await navigateTo(page, "/transactions");
    await waitForDataGrid(page);

    // Use the first row for editing
    const firstRow = page.locator(".MuiDataGrid-row").first();
    await expect(firstRow).toBeVisible();

    const descriptionCell = firstRow.locator(".MuiDataGrid-cell").nth(1);
    const descriptionText = (
      (await descriptionCell.textContent()) || ""
    ).trim();

    const categoryCell = firstRow.locator(".MuiDataGrid-cell").nth(2);
    const originalCategory = ((await categoryCell.textContent()) || "").trim();

    const initialUrl = page.url();

    // Enter edit mode and open dropdown
    await categoryCell.dblclick();
    const combo = firstRow.locator('[role="combobox"]');
    await expect(combo).toBeVisible();
    // Use keyboard to change selection to avoid overlay intercepts
    await page.keyboard.press("ArrowDown");
    await page.keyboard.press("Enter");
    await page.keyboard.press("Tab");

    // Success toast and no console/network errors
    await waitForToast(page, "Transaction updated successfully");

    // Expect we stayed on the same route and edit mode closed
    await waitForPageLoad(page);
    expect(page.url()).toBe(initialUrl);
    await expect(page.locator(".MuiDataGrid-cell--editing")).toHaveCount(0);

    // Read chosen text from the cell in view mode
    const chosenText = ((await categoryCell.textContent()) || "").trim();
    expect(chosenText).not.toEqual("");
    expect(chosenText).not.toEqual(originalCategory);
    expect(
      consoleErrors,
      `Console errors: ${consoleErrors.join(" | ")}`
    ).toEqual([]);
    expect(failedApi, `Failed API calls: ${failedApi.join(" | ")}`).toEqual([]);

    // Verify persistence after reload by searching for the row by its description
    await page.reload();
    await waitForDataGrid(page);

    if (descriptionText) {
      await searchDataGrid(
        page,
        descriptionText.slice(0, Math.min(20, descriptionText.length))
      );
      await waitForPageLoad(page);
    }

    const targetRow = page
      .locator(".MuiDataGrid-row", { hasText: descriptionText || "" })
      .first();
    await expect(targetRow).toBeVisible();
    const categoryCellAfter = targetRow.locator(".MuiDataGrid-cell").nth(2);
    const newCategory = ((await categoryCellAfter.textContent()) || "").trim();
    expect(newCategory).toBe(chosenText);
  });
});
