import { test, expect } from "@playwright/test";

test("split indicator shows in category column", async ({ page }) => {
  await page.goto("http://localhost:5173/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(2000);

  // Look for "splits" badge text in the grid
  const splitBadge = page.locator('[role="gridcell"]:has-text("splits")').first();
  const visible = await splitBadge.isVisible({ timeout: 5000 }).catch(() => false);
  console.log(`Split badge visible: ${visible}`);

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/split-indicator.png",
  });

  expect(visible).toBe(true);
});
