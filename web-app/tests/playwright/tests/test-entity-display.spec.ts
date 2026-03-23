import { test, expect } from "@playwright/test";
import { API_BASE_URL } from '../../fixtures/env';

test("entity values display in transaction list", async ({ page }) => {
  // First ensure a transaction has an entity assigned via API
  const txRes = await page.request.get(`${API_BASE_URL}/api/transactions?limit=1`);
  const txData = await txRes.json();
  const tx = txData.transactions[0];
  const txId = tx.transaction_id;

  const entRes = await page.request.get(`${API_BASE_URL}/api/entities`);
  const entities = await entRes.json();
  const entity = (Array.isArray(entities) ? entities : entities.entities || entities.data || [])[0];
  const entityId = entity.entity_id ?? entity.entityId;
  const entityName = entity.entity_name ?? entity.entityName ?? entity.name;

  // Assign entity to transaction
  await page.request.put(`${API_BASE_URL}/api/transactions/${txId}`, {
    data: { entity_id: entityId },
    headers: { "Content-Type": "application/json" },
  });

  // Load transactions page
  await page.goto("/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(3000);

  await page.screenshot({
    path: "tests/playwright/test-results/artifacts/entity-display.png",
  });

  // Check that the entity name appears in the grid
  const entityCell = page.locator(`[role="gridcell"]:has-text("${entityName}")`).first();
  const visible = await entityCell.isVisible({ timeout: 5000 }).catch(() => false);
  console.log(`Entity "${entityName}" visible in grid: ${visible}`);

  expect(visible).toBe(true);
});
