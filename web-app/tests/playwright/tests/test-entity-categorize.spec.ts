import { test, expect } from "@playwright/test";
import { API_BASE_URL } from '../../fixtures/env';

test.describe("Entity filter + category change", () => {
  test("categorizing a transaction preserves its entity assignment", async ({
    page,
  }) => {
    // Step 1: Create a transaction with entity assignment via API
    // First get available entities
    const entitiesRes = await page.request.get(`${API_BASE_URL}/api/entities`);
    const entities = await entitiesRes.json();
    const entityList = Array.isArray(entities) ? entities : entities.entities || entities.data || [];

    if (entityList.length === 0) {
      test.skip(true, "No entities available");
      return;
    }

    const entity = entityList[0];
    const entityId = entity.entityId ?? entity.entity_id ?? entity.id;
    const entityName = entity.entityName ?? entity.entity_name ?? entity.name;

    // Get a transaction to work with
    const txRes = await page.request.get(`${API_BASE_URL}/api/transactions?limit=5`);
    const txData = await txRes.json();
    const transactions = Array.isArray(txData) ? txData : txData.transactions || txData.data || [];

    if (transactions.length === 0) {
      test.skip(true, "No transactions available");
      return;
    }

    const tx = transactions[0];
    const txId = tx.transactionId ?? tx.transaction_id ?? tx.id;

    // Assign entity to this transaction via direct API
    const assignRes = await page.request.put(
      `${API_BASE_URL}/api/transactions/${txId}`,
      {
        data: { entity_id: entityId },
        headers: { "Content-Type": "application/json" },
      }
    );
    expect(assignRes.ok()).toBeTruthy();

    // Verify entity_id is set
    const verifyRes = await page.request.get(
      `${API_BASE_URL}/api/transactions/${txId}`
    );
    const verifiedTx = await verifyRes.json();
    const verifiedEntityId = verifiedTx.entityId ?? verifiedTx.entity_id;
    expect(verifiedEntityId).toBe(entityId);

    // Step 2: Get a category to change to
    const catRes = await page.request.get(`${API_BASE_URL}/api/categories`);
    const catData = await catRes.json();
    const categories = Array.isArray(catData) ? catData : catData.categories || catData.data || [];
    const currentCatId = verifiedTx.categoryId ?? verifiedTx.category_id;
    const newCategory = categories.find(
      (c: any) => (c.categoryId ?? c.category_id ?? c.id) !== currentCatId
    );

    if (!newCategory) {
      test.skip(true, "Need at least 2 categories");
      return;
    }

    const newCatId = newCategory.categoryId ?? newCategory.category_id ?? newCategory.id;

    // Step 3: Update category via the frontend API function (simulating what the UI does)
    // This is the critical test — updating only category_id should NOT clear entity_id
    await page.goto("/transactions");
    await page.waitForLoadState("networkidle");

    // Use the frontend's updateTransaction path by calling fetch from the page context
    const updateResult = await page.evaluate(
      async ({ txId, newCatId }) => {
        const res = await fetch(`/api/transactions/${txId}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category_id: newCatId }),
        });
        return { ok: res.ok, status: res.status, data: await res.json() };
      },
      { txId, newCatId }
    );
    expect(updateResult.ok).toBeTruthy();

    // Step 4: Verify entity_id is STILL set after category change
    const afterRes = await page.request.get(
      `${API_BASE_URL}/api/transactions/${txId}`
    );
    const afterTx = await afterRes.json();
    const afterEntityId = afterTx.entityId ?? afterTx.entity_id;

    expect(afterEntityId).toBe(entityId);

    await page.screenshot({
      path: "tests/playwright/test-results/artifacts/entity-categorize-preserved.png",
    });
  });
});
