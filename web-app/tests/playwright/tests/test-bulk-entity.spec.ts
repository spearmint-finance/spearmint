import { test, expect } from "@playwright/test";

test("bulk assign entity to selected transactions", async ({ page }) => {
  // Get entity info
  const entRes = await page.request.get("http://localhost:8000/api/entities");
  const entities = await entRes.json();
  const entityList = Array.isArray(entities) ? entities : entities.entities || entities.data || [];
  const entity = entityList[0];
  const entityId = entity.entity_id ?? entity.entityId;
  const entityName = entity.entity_name ?? entity.entityName ?? entity.name;

  await page.goto("http://localhost:5173/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(3000);

  // Wait for data grid rows to appear
  await expect(page.locator('[role="row"][data-rowindex]').first()).toBeVisible({ timeout: 10000 });

  // Verify checkboxes are visible (MUI DataGrid uses input[type="checkbox"])
  const checkboxes = page.locator('input[type="checkbox"]');
  const checkboxCount = await checkboxes.count();
  console.log(`Checkboxes visible: ${checkboxCount}`);
  expect(checkboxCount).toBeGreaterThan(1); // header + at least 1 row

  // Select first 3 row checkboxes (skip header checkbox at index 0)
  for (let i = 1; i <= Math.min(3, checkboxCount - 1); i++) {
    await checkboxes.nth(i).click();
    await page.waitForTimeout(200);
  }

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/bulk-select.png",
  });

  // Verify bulk action bar appears
  const selectedText = page.locator('text=/\\d+ selected/');
  await expect(selectedText).toBeVisible({ timeout: 3000 });

  // Click "Assign Entity"
  const assignBtn = page.locator('button:has-text("Assign Entity")');
  await expect(assignBtn).toBeVisible({ timeout: 3000 });
  await assignBtn.click();
  await page.waitForTimeout(500);

  // Dialog should open
  const dialog = page.locator('[role="dialog"]');
  await expect(dialog).toBeVisible({ timeout: 3000 });

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/bulk-entity-dialog.png",
  });

  // Select entity from dropdown
  const entitySelect = dialog.locator('[role="combobox"]').first();
  await entitySelect.click();
  await page.waitForTimeout(300);
  const option = page.locator(`[role="option"]:has-text("${entityName}")`).first();
  await expect(option).toBeVisible({ timeout: 2000 });
  await option.click();
  await page.waitForTimeout(300);

  // Click Assign button
  const confirmBtn = dialog.locator('button:has-text("Assign")');
  await confirmBtn.click();
  await page.waitForTimeout(2000);

  // Verify success toast
  const toast = page.locator('text=Entity updated');
  const success = await toast.isVisible({ timeout: 3000 }).catch(() => false);
  console.log(`Bulk update success: ${success}`);

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/bulk-entity-result.png",
  });

  expect(success).toBe(true);
});

test("bulk update API works", async ({ page }) => {
  // Get some transaction IDs
  const txRes = await page.request.get("http://localhost:8000/api/transactions?limit=5&offset=30");
  const txData = await txRes.json();
  const ids = txData.transactions.map((t: any) => t.transaction_id);

  // Get entity
  const entRes = await page.request.get("http://localhost:8000/api/entities");
  const entities = await entRes.json();
  const entityList = Array.isArray(entities) ? entities : entities.entities || entities.data || [];
  const entityId = entityList[0].entity_id ?? entityList[0].entityId;

  // Bulk assign
  const res = await page.request.put("http://localhost:8000/api/transactions/bulk-update", {
    data: { transaction_ids: ids, updates: { entity_id: entityId } },
    headers: { "Content-Type": "application/json" },
  });
  expect(res.ok()).toBeTruthy();
  const result = await res.json();
  expect(result.updated).toBe(ids.length);

  // Verify
  for (const id of ids) {
    const txRes = await page.request.get(`http://localhost:8000/api/transactions/${id}`);
    const tx = await txRes.json();
    expect(tx.entity_id).toBe(entityId);
  }

  // Bulk clear
  const clearRes = await page.request.put("http://localhost:8000/api/transactions/bulk-update", {
    data: { transaction_ids: ids, updates: { entity_id: null } },
    headers: { "Content-Type": "application/json" },
  });
  expect(clearRes.ok()).toBeTruthy();
});
