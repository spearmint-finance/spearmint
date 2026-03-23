import { test, expect } from "@playwright/test";

test("Add Split auto-fills remaining amount and Split Evenly works", async ({ page }) => {
  // Use a transaction without existing splits — offset to find one
  const txRes = await page.request.get("http://localhost:8000/api/transactions?limit=1&offset=20");
  const txData = await txRes.json();
  const tx = txData.transactions[0];
  const txId = tx.transaction_id;
  const amount = Math.abs(parseFloat(tx.amount));

  // Clear any existing splits
  await page.request.put(`http://localhost:8000/api/transactions/${txId}/splits`, {
    data: [], headers: { "Content-Type": "application/json" },
  });

  await page.goto("/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(2000);

  // Find and click this specific transaction's amount cell
  // Just click the first amount cell and work with whatever opens
  const amountCell = page.locator('[role="gridcell"]').filter({ hasText: /^\$/ }).first();
  await amountCell.click();
  await page.waitForTimeout(1000);

  const dialog = page.locator('[role="dialog"]');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  const mainInput = dialog.locator('input[name="amount"]');
  const mainAmt = Math.abs(parseFloat(await mainInput.inputValue() || "0"));

  // Scroll to bottom
  const dialogContent = dialog.locator('[class*="MuiDialogContent"]').first();
  if (await dialogContent.isVisible().catch(() => false)) {
    await dialogContent.evaluate((el) => el.scrollTop = el.scrollHeight);
  }
  await page.waitForTimeout(300);

  // Clear existing splits by removing them
  const removeButtons = dialog.locator('button:has-text("✕")');
  let removeCount = await removeButtons.count();
  while (removeCount > 0) {
    await removeButtons.first().click();
    await page.waitForTimeout(200);
    removeCount = await removeButtons.count();
  }

  // Add first split — should auto-fill with full amount
  const addSplit = dialog.locator('button:has-text("Add Split")');
  await addSplit.click();
  await page.waitForTimeout(500);

  const allAmountInputs = dialog.locator('label:has-text("Amount")').locator('..').locator('input');
  const firstSplitValue = parseFloat(await allAmountInputs.nth(1).inputValue() || "0");
  console.log(`Main: ${mainAmt}, First split auto-fill: ${firstSplitValue}`);
  expect(firstSplitValue).toBeCloseTo(mainAmt, 1);

  // Add second split — remaining should be 0
  await addSplit.click();
  await page.waitForTimeout(500);
  const secondSplitValue = parseFloat(await allAmountInputs.nth(2).inputValue() || "0");
  console.log(`Second split auto-fill: ${secondSplitValue}`);
  expect(secondSplitValue).toBe(0);

  // "Split Evenly" should appear with 2+ splits
  const splitEvenly = dialog.locator('button:has-text("Split Evenly")');
  await expect(splitEvenly).toBeVisible({ timeout: 3000 });
  await splitEvenly.click();
  await page.waitForTimeout(500);

  const s1 = parseFloat(await allAmountInputs.nth(1).inputValue() || "0");
  const s2 = parseFloat(await allAmountInputs.nth(2).inputValue() || "0");
  console.log(`After Split Evenly: ${s1} + ${s2} = ${s1 + s2} (target: ${mainAmt})`);
  expect(s1 + s2).toBeCloseTo(mainAmt, 1);
  expect(Math.abs(s1 - s2)).toBeLessThan(0.02);

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/split-evenly.png",
  });

  // Close without saving
  const cancelBtn = dialog.locator('button:has-text("Cancel")').first();
  if (await cancelBtn.isVisible().catch(() => false)) await cancelBtn.click();
});
