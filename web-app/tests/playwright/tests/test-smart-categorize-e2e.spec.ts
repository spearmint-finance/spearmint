import { test, expect } from "@playwright/test";

const API = "http://localhost:8000/api";

test.describe("Smart Categorize E2E", () => {
  test("apply-categories endpoint updates DUNKIN transactions in DB", async ({ page }) => {
    // Use page.evaluate to make API calls (avoids request fixture issues)
    const result = await page.evaluate(async (apiBase) => {
      const log: string[] = [];

      // Step 1: Get uncategorized descriptions
      const descsResp = await fetch(`${apiBase}/transactions/uncategorized-descriptions?offset=0&limit=3000`);
      const descsData = await descsResp.json();
      log.push(`Total uncategorized: ${descsData.total}`);

      const dunkin = descsData.descriptions?.find((d: any) => d.description.includes("DUNKIN"));
      if (!dunkin) {
        log.push("No DUNKIN found - skipping");
        return { log, dunkinAfterCount: 0, updated: 0, skipped: true };
      }
      log.push(`Found: "${dunkin.description}" with ${dunkin.count} txns`);

      // Step 2: Ensure Coffee & Cafes category exists
      const catsResp = await fetch(`${apiBase}/categories`);
      const catsData = await catsResp.json();
      let coffeeCatId = catsData.categories?.find((c: any) => c.category_name === "Coffee & Cafes")?.category_id;

      if (!coffeeCatId) {
        const createResp = await fetch(`${apiBase}/categories`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category_name: "Coffee & Cafes", category_type: "Expense" }),
        });
        const created = await createResp.json();
        coffeeCatId = created.category_id;
        log.push(`Created category ID: ${coffeeCatId}`);
      }

      // Step 3: Apply
      const applyResp = await fetch(`${apiBase}/transactions/apply-categories`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          assignments: [{
            description: dunkin.description,
            category_id: coffeeCatId,
            suggested_pattern: "DUNKIN",
            rule_name: "Auto: Dunkin Donuts",
          }],
          create_rules: true,
        }),
      });
      const applyData = await applyResp.json();
      log.push(`Apply: total_updated=${applyData.total_updated}, rules=${applyData.rules_created}`);

      // Step 4: Verify
      const afterResp = await fetch(`${apiBase}/transactions/uncategorized-descriptions?offset=0&limit=3000`);
      const afterData = await afterResp.json();
      const dunkinAfter = afterData.descriptions?.filter((d: any) => d.description.includes("DUNKIN")) || [];
      log.push(`DUNKIN still uncategorized: ${dunkinAfter.length}`);
      dunkinAfter.forEach((d: any) => log.push(`  BUG: "${d.description}" - ${d.count} txns`));

      return { log, dunkinAfterCount: dunkinAfter.length, updated: applyData.total_updated, skipped: false };
    }, API);

    // Print all logs
    for (const line of result.log) {
      console.log(line);
    }

    if (result.skipped) return;

    expect(result.updated).toBeGreaterThan(0);
    expect(result.dunkinAfterCount).toBe(0);
  });
});
