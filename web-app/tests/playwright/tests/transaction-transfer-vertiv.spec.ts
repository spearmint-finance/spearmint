import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForDataGrid,
  searchDataGrid,
  waitForPageLoad,
} from "../../utils/test-helpers";

// Verify that the "VERTIV HOLDINGS" reinvestment transaction is treated as a Transfer

test.describe("Transactions – VERTIV HOLDINGS reinvestment should be Transfer", () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, "/transactions");
    await waitForDataGrid(page);
  });

  test("should display Transfer chip for VERTIV HOLDINGS reinvestment", async ({
    page,
  }) => {
    await searchDataGrid(page, "VERTIV HOLDINGS");
    await waitForPageLoad(page);

    // Find the row containing VERTIV HOLDINGS
    const row = page
      .locator(".MuiDataGrid-row", { hasText: /VERTIV HOLDINGS/i })
      .first();
    await expect(row).toBeVisible({ timeout: 10000 });

    // Within that row, expect the Type chip to say "Transfer"
    const transferChip = row.locator(".MuiChip-label", { hasText: "Transfer" });
    await expect(transferChip).toBeVisible({ timeout: 10000 });
  });
});
