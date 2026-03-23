import { test, expect } from "@playwright/test";
import { API_BASE_URL } from '../../fixtures/env';
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TILLER_FILE = path.resolve(
  __dirname,
  "../../../../dev-tools/sample-data/Tiller-Foundation-Template.xlsx"
);

test.describe("Import with auto-account creation", () => {
  test("imports Tiller XLSX and creates accounts", async ({ page }) => {
    // Navigate to import page
    await page.goto("/");
    // Find and click Import nav link
    const importLink = page.locator('a[href*="import"], [role="tab"]:has-text("Import"), button:has-text("Import")').first();
    if (await importLink.isVisible({ timeout: 3000 }).catch(() => false)) {
      await importLink.click();
    } else {
      // Try direct navigation
      await page.goto("/import");
    }
    await page.waitForLoadState("networkidle");

    // Verify import page loaded
    await expect(page.locator("text=Import Transactions").first()).toBeVisible({ timeout: 5000 });

    // Upload the Tiller file
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(TILLER_FILE);

    // Wait for import to complete (may take a while for 9k rows)
    await page.waitForTimeout(15000);

    // Check for import summary
    const summary = page.locator("text=Import Summary").first();
    if (await summary.isVisible({ timeout: 5000 }).catch(() => false)) {
      // Verify accounts created message appears
      const accountsText = page.locator("text=/Accounts.*created/i").first();
      await expect(accountsText).toBeVisible({ timeout: 5000 });
    }

    // Verify accounts exist via API
    const response = await page.request.get(`${API_BASE_URL}/api/accounts`);
    const accounts = await response.json();
    const accountList = Array.isArray(accounts) ? accounts : accounts.accounts || accounts.data || [];
    // Should have at least the 19 Tiller accounts
    expect(accountList.length).toBeGreaterThanOrEqual(19);

    // Take screenshot for verification
    await page.screenshot({
      path: "tests/playwright/test-results/artifacts/import-accounts-result.png",
    });
  });

  test("accounts page shows imported accounts", async ({ page }) => {
    await page.goto("/accounts");
    await page.waitForLoadState("networkidle");

    // Verify some imported accounts are visible
    // Look for institution names from Tiller data
    const fidelityText = page.locator("text=Fidelity").first();
    const chaseText = page.locator("text=Chase").first();

    const fidelityVisible = await fidelityText.isVisible({ timeout: 5000 }).catch(() => false);
    const chaseVisible = await chaseText.isVisible({ timeout: 5000 }).catch(() => false);

    expect(fidelityVisible || chaseVisible).toBeTruthy();

    await page.screenshot({
      path: "tests/playwright/test-results/artifacts/accounts-after-import.png",
    });
  });
});
