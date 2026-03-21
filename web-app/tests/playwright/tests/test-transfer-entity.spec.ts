import { test, expect } from "@playwright/test";

test("debug transfer disappearing from entity scope", async ({ page }) => {
  // Capture API requests
  page.on("request", async (req) => {
    if (req.url().includes("/api/transactions") && req.method() === "GET" && !req.url().includes(".ts")) {
      console.log(`GET ${req.url()}`);
    }
  });
  page.on("response", async (res) => {
    if (res.url().includes("/api/transactions") && res.request().method() === "GET" && !res.url().includes(".ts")) {
      const data = await res.json().catch(() => null);
      if (data?.total !== undefined) {
        console.log(`  → ${data.total} results`);
      }
    }
  });

  await page.goto("http://localhost:8080/transactions");
  await page.waitForSelector(".MuiDataGrid-row", { timeout: 15000 });

  // Click "All Entities" dropdown in sidebar
  const entityDropdown = page.getByText("All Entities").first();
  await entityDropdown.click();
  await page.waitForTimeout(500);

  // Click "Personal" to scope to that entity
  const personalItem = page.getByText("Personal").first();
  await personalItem.click();
  await page.waitForTimeout(3000);
  await page.screenshot({ path: "tests/playwright/test-results/debug-entity-scoped.png" });

  // Check how many rows are visible
  const rows = await page.locator(".MuiDataGrid-row").count();
  console.log(`Rows visible after entity scope: ${rows}`);

  // Check the grid content
  if (rows > 0) {
    for (let i = 0; i < Math.min(rows, 5); i++) {
      const row = page.locator(".MuiDataGrid-row").nth(i);
      const desc = await row.locator('[data-field="description"]').textContent();
      const cat = await row.locator('[data-field="category_id"]').textContent();
      console.log(`  row[${i}]: desc="${desc}" cat="${cat}"`);
    }
  }
});
