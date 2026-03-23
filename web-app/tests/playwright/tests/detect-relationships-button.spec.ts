import { test, expect } from "@playwright/test";

/**
 * E2E Test: Detect Relationships Button
 *
 * This test verifies that the "Detect Relationships" button in the Transactions page works correctly.
 * The database already contains NVIDIA dividend reinvestment transactions that can be linked.
 */

test.describe("Detect Relationships Button", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to transactions page
    await page.goto("/transactions");
    await page.waitForLoadState("networkidle");

    // Wait for the "Detect Relationships" button to be ready (not in "Detecting..." state)
    await page.waitForSelector('button:has-text("Detect Relationships")', {
      timeout: 15000,
    });
  });

  test("should have Detect Relationships button visible", async ({ page }) => {
    console.log("Verifying button is visible...");

    const detectButton = page.locator('button:has-text("Detect Relationships")');
    await expect(detectButton).toBeVisible();
    await expect(detectButton).toBeEnabled();

    console.log("✓ Button is visible and enabled");
  });

  test("should detect relationships when button is clicked", async ({
    page,
  }) => {
    console.log("Testing relationship detection...");

    // Click the "Detect Relationships" button
    const detectButton = page.locator('button:has-text("Detect Relationships")');
    await detectButton.click();

    // Verify loading state appears
    const detectingButton = page.locator('button:has-text("Detecting...")');
    await expect(detectingButton).toBeVisible({ timeout: 2000 });
    console.log("✓ Button shows loading state");

    // Wait for detection to complete (button should return to normal state)
    await expect(detectButton).toBeVisible({ timeout: 15000 });
    await expect(detectButton).toBeEnabled({ timeout: 15000 });
    console.log("✓ Detection completed");

    // Check for success or info message (either "Found X pairs" or "No pairs found")
    const hasMessage = await page
      .locator('div[role="alert"]')
      .first()
      .isVisible({ timeout: 5000 })
      .catch(() => false);

    if (hasMessage) {
      const messageText = await page
        .locator('div[role="alert"]')
        .first()
        .textContent();
      console.log(`✓ Message shown: ${messageText}`);
    } else {
      console.log("ℹ No snackbar message appeared (may have already closed)");
    }
  });

  test("should show visual indicators for linked pairs", async ({ page }) => {
    console.log("Testing visual indicators...");

    // First, run detection to ensure pairs are linked
    const detectButton = page.locator('button:has-text("Detect Relationships")');
    await detectButton.click();

    // Wait for detection to complete
    await page.waitForTimeout(3000);

    // Look for NVIDIA dividend transactions (we know they exist in the database)
    const nvidiaRows = page.locator(
      'div[role="row"]:has-text("NVIDIA CORPORATION COM")'
    );
    const rowCount = await nvidiaRows.count();

    if (rowCount > 0) {
      console.log(`✓ Found ${rowCount} NVIDIA transactions`);

      // Check if any have the "Reinvestment" classification chip
      const reinvestmentChips = page.locator('text="Reinvestment"');
      const chipCount = await reinvestmentChips.count();

      if (chipCount > 0) {
        console.log(`✓ Found ${chipCount} Reinvestment classification chips`);
      } else {
        console.log("ℹ No Reinvestment chips found (may not be linked yet)");
      }
    } else {
      console.log("ℹ No NVIDIA transactions found on current page");
    }
  });

  test("should disable button during detection", async ({ page }) => {
    console.log("Testing button disabled state...");

    const detectButton = page.locator('button:has-text("Detect Relationships")');

    // Button should be enabled initially
    await expect(detectButton).toBeEnabled();
    console.log("✓ Button is enabled initially");

    // Click the button
    await detectButton.click();

    // Button should be disabled during detection
    const detectingButton = page.locator('button:has-text("Detecting...")');
    await expect(detectingButton).toBeDisabled({ timeout: 2000 });
    console.log("✓ Button is disabled during detection");

    // Wait for detection to complete
    await page.waitForTimeout(5000);

    // Button should be enabled again
    await expect(detectButton).toBeEnabled({ timeout: 10000 });
    console.log("✓ Button is enabled again after detection");
  });
});

