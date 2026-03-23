import { test, expect } from "@playwright/test";

test("check transactions page for errors", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (err) => errors.push(`${err.message}\n${err.stack?.substring(0, 300)}`));

  await page.goto("/transactions");
  await page.waitForTimeout(5000);

  console.log("Errors:", errors.length);
  for (const e of errors) console.log(e);

  await page.screenshot({ path: "tests/playwright/test-results/artifacts/page-load-check.png" });
});
