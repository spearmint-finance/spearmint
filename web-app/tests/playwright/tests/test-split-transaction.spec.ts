import { test, expect } from "@playwright/test";

test.describe("Transaction splitting", () => {
  test("split endpoint creates and clears splits via API", async ({ page }) => {
    // Get a transaction
    const txRes = await page.request.get(
      "http://localhost:8000/api/transactions?limit=1"
    );
    const txData = await txRes.json();
    const transactions = txData.transactions || txData.data || [];
    expect(transactions.length).toBeGreaterThan(0);

    const tx = transactions[0];
    const txId = tx.transaction_id ?? tx.transactionId;
    const amount = parseFloat(tx.amount);
    const catId = tx.category_id ?? tx.categoryId;

    // Split 70/30
    const amt1 = Math.round(amount * 0.7 * 100) / 100;
    const amt2 = Math.round((amount - amt1) * 100) / 100;

    const splitRes = await page.request.put(
      `http://localhost:8000/api/transactions/${txId}/splits`,
      {
        data: [
          { amount: amt1, category_id: catId, description: "Split A" },
          { amount: amt2, category_id: catId, description: "Split B" },
        ],
        headers: { "Content-Type": "application/json" },
      }
    );
    expect(splitRes.ok()).toBeTruthy();

    const result = await splitRes.json();
    const splits = result.splits || [];
    expect(splits.length).toBe(2);
    expect(parseFloat(splits[0].amount)).toBeCloseTo(amt1, 1);
    expect(parseFloat(splits[1].amount)).toBeCloseTo(amt2, 1);

    // Verify splits persist on re-fetch
    const refetchRes = await page.request.get(
      `http://localhost:8000/api/transactions/${txId}`
    );
    const refetched = await refetchRes.json();
    expect(refetched.splits?.length ?? 0).toBe(2);

    // Clear splits
    const clearRes = await page.request.put(
      `http://localhost:8000/api/transactions/${txId}/splits`,
      {
        data: [],
        headers: { "Content-Type": "application/json" },
      }
    );
    expect(clearRes.ok()).toBeTruthy();

    const cleared = await clearRes.json();
    expect(cleared.splits?.length ?? 0).toBe(0);
  });

  test("splits with different categories", async ({ page }) => {
    // Get categories
    const catRes = await page.request.get("http://localhost:8000/api/categories");
    const catData = await catRes.json();
    const categories = Array.isArray(catData)
      ? catData
      : catData.categories || catData.data || [];
    expect(categories.length).toBeGreaterThanOrEqual(2);

    const cat1Id = categories[0].category_id ?? categories[0].categoryId;
    const cat2Id = categories[1].category_id ?? categories[1].categoryId;

    // Get a transaction
    const txRes = await page.request.get(
      "http://localhost:8000/api/transactions?limit=1&offset=10"
    );
    const txData = await txRes.json();
    const tx = (txData.transactions || [])[0];
    const txId = tx.transaction_id ?? tx.transactionId;
    const amount = parseFloat(tx.amount);

    // Split across two categories
    const half = Math.round(amount * 50) / 100;
    const other = Math.round((amount - half) * 100) / 100;

    const splitRes = await page.request.put(
      `http://localhost:8000/api/transactions/${txId}/splits`,
      {
        data: [
          { amount: half, category_id: cat1Id },
          { amount: other, category_id: cat2Id },
        ],
        headers: { "Content-Type": "application/json" },
      }
    );
    expect(splitRes.ok()).toBeTruthy();

    const result = await splitRes.json();
    expect(result.splits.length).toBe(2);
    expect(result.splits[0].category_id ?? result.splits[0].categoryId).toBe(cat1Id);
    expect(result.splits[1].category_id ?? result.splits[1].categoryId).toBe(cat2Id);

    // Clean up
    await page.request.put(
      `http://localhost:8000/api/transactions/${txId}/splits`,
      { data: [], headers: { "Content-Type": "application/json" } }
    );
  });
});
