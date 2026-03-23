import { test, expect } from "@playwright/test";
import { API_BASE_URL } from '../../fixtures/env';

test("FULL UI: entity filter + inline category change", async ({ page }) => {
  // Setup
  const entRes = await page.request.get(`${API_BASE_URL}/api/entities`);
  const entities = await entRes.json();
  const entityList = Array.isArray(entities) ? entities : entities.entities || entities.data || [];
  const entityName = entityList[0].entity_name ?? entityList[0].entityName;
  const entityId = entityList[0].entity_id ?? entityList[0].entityId;

  // Ensure we have transactions with this entity
  const txRes = await page.request.get(`${API_BASE_URL}/api/transactions?limit=5&offset=300`);
  for (const tx of (await txRes.json()).transactions) {
    await page.request.put(`${API_BASE_URL}/api/transactions/${tx.transaction_id}`, {
      data: { entity_id: entityId },
      headers: { "Content-Type": "application/json" },
    });
  }

  // Track PUT requests
  const putBodies: { url: string; body: string }[] = [];
  page.on("request", (req) => {
    if (req.method() === "PUT" && req.url().includes("/api/transactions/")) {
      putBodies.push({ url: req.url(), body: req.postData() || "" });
    }
  });

  // 1. Navigate
  await page.goto("/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(3000);

  // 2. Select entity filter
  await page.locator('text=All Entities').first().click();
  await page.waitForTimeout(500);
  await page.locator(`[role="option"]:has-text("${entityName}")`).first().click();
  await page.waitForTimeout(3000);

  const rowsBefore = await page.locator('[role="row"][data-rowindex]').count();
  console.log(`Rows before inline edit: ${rowsBefore}`);
  await page.screenshot({ path: "tests/playwright/test-results/artifacts/fullui-before.png" });

  // 3. Double-click a category cell for inline editing
  const catCells = page.locator('[data-field="category_id"][role="gridcell"]');
  const cellCount = await catCells.count();
  console.log(`Category cells: ${cellCount}`);
  expect(cellCount).toBeGreaterThan(0);

  await catCells.first().dblclick();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: "tests/playwright/test-results/artifacts/fullui-editing.png" });

  // 4. Find and interact with the inline select
  // MUI DataGrid renders a Select component in edit mode
  const inlineSelect = page.locator('.MuiSelect-select, [role="combobox"]').last();
  const isEditing = await inlineSelect.isVisible({ timeout: 3000 }).catch(() => false);
  console.log(`Inline select visible: ${isEditing}`);

  if (isEditing) {
    await inlineSelect.click();
    await page.waitForTimeout(500);

    // Pick a different category (third option to avoid selecting current)
    const options = page.locator('[role="option"]');
    const optCount = await options.count();
    console.log(`Options available: ${optCount}`);

    if (optCount > 3) {
      await options.nth(3).click();
    } else if (optCount > 0) {
      await options.first().click();
    }

    // Wait for the mutation + refetch
    await page.waitForTimeout(5000);

    // 5. Log what was sent
    console.log(`\nPUT requests captured: ${putBodies.length}`);
    for (const { url, body } of putBodies) {
      const txIdMatch = url.match(/\/transactions\/(\d+)/);
      const parsed = JSON.parse(body);
      const keys = Object.keys(parsed);
      console.log(`  TX ${txIdMatch?.[1]}: keys=${keys.join(',')}`);
      if ('entity_id' in parsed) {
        console.log(`    entity_id = ${parsed.entity_id} ${parsed.entity_id === null ? '*** BUG: CLEARED! ***' : '(ok)'}`);
      } else {
        console.log(`    entity_id NOT in body (correct - preserved)`);
      }
    }
  }

  await page.screenshot({ path: "tests/playwright/test-results/artifacts/fullui-after.png" });

  // 6. Count rows after
  const rowsAfter = await page.locator('[role="row"][data-rowindex]').count();
  console.log(`\nRows after: ${rowsAfter} (was: ${rowsBefore})`);
  if (rowsAfter < rowsBefore) {
    console.log("*** BUG: Transaction disappeared! ***");
  }
  expect(rowsAfter).toBe(rowsBefore);
});
