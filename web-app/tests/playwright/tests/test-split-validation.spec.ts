import { test, expect } from "@playwright/test";

test("split validation blocks save when amounts don't match", async ({ page }) => {
  await page.goto("http://localhost:5173/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(2000);

  // Open edit dialog
  const amountCell = page.locator('[role="gridcell"]').filter({ hasText: /^\$/ }).first();
  await amountCell.click();
  await page.waitForTimeout(1000);

  const dialog = page.locator('[role="dialog"]');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  // Scroll down and add a split with wrong amount
  const dialogContent = dialog.locator('[class*="MuiDialogContent"]').first();
  if (await dialogContent.isVisible().catch(() => false)) {
    await dialogContent.evaluate((el) => el.scrollTop = el.scrollHeight);
  }

  const addSplit = dialog.locator('button:has-text("Add Split")');
  await addSplit.click();
  await page.waitForTimeout(300);

  // Set split amount to something wrong (half the actual amount)
  const allAmountInputs = dialog.locator('label:has-text("Amount")').locator('..').locator('input');
  const mainAmt = Math.abs(parseFloat(await allAmountInputs.nth(0).inputValue() || "100"));
  await allAmountInputs.nth(1).fill(String(mainAmt / 2));

  // Select a category for the split
  const catSelects = dialog.locator('label:has-text("Category")').locator('..').locator('[role="combobox"]');
  if (await catSelects.nth(1).isVisible().catch(() => false)) {
    await catSelects.nth(1).click();
    await page.waitForTimeout(200);
    const opt = page.locator('[role="option"]').first();
    if (await opt.isVisible().catch(() => false)) await opt.click();
    await page.waitForTimeout(200);
  }

  // Try to save
  const saveBtn = dialog.locator('button:has-text("Save"), button:has-text("Update"), button[type="submit"]').first();
  await saveBtn.click();
  await page.waitForTimeout(2000);

  // Should show validation error (either snackbar or inline)
  const errorSnack = page.locator("text=/Splits sum.*doesn.*match/i");
  const errorInline = page.locator("text=/Splits sum.*≠/i");
  const hasSnackError = await errorSnack.isVisible({ timeout: 3000 }).catch(() => false);
  const hasInlineError = await errorInline.isVisible({ timeout: 1000 }).catch(() => false);
  const hasError = hasSnackError || hasInlineError;
  console.log(`Split validation error shown: ${hasError} (snack: ${hasSnackError}, inline: ${hasInlineError})`);

  // Dialog should still be open (save was blocked)
  const dialogStillOpen = await dialog.isVisible().catch(() => false);
  console.log(`Dialog still open (blocked): ${dialogStillOpen}`);

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/split-validation-error.png",
  });

  expect(hasError).toBe(true);
  expect(dialogStillOpen).toBe(true);

  // Close dialog
  const cancelBtn = dialog.locator('button:has-text("Cancel")').first();
  if (await cancelBtn.isVisible().catch(() => false)) await cancelBtn.click();
});
