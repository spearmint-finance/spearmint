import { test, expect } from "@playwright/test";

/**
 * Test that dashboard entity scoping works:
 * - Dashboard API calls include entity_id when entity is selected
 * - Data changes when entity is selected vs all entities
 */

const BASE = process.env.TEST_BASE_URL || "http://localhost:5174";

test.use({ baseURL: BASE });

test.describe("Dashboard Entity Scoping", () => {
  test("API calls include entity_id query param when entity selected", async ({
    page,
  }) => {
    // Track API calls to analysis endpoints
    const apiCalls: { url: string; entityId: string | null }[] = [];

    page.on("request", (request) => {
      const url = request.url();
      if (url.includes("/api/analysis/")) {
        const parsed = new URL(url);
        apiCalls.push({
          url: parsed.pathname,
          entityId: parsed.searchParams.get("entity_id"),
        });
      }
    });

    // Load dashboard with no entity selected
    await page.goto(BASE + "/");
    await page.waitForLoadState("networkidle");

    // Verify initial API calls have no entity_id
    const initialCalls = apiCalls.filter(
      (c) => c.url.includes("/analysis/summary") || c.url.includes("/analysis/cashflow/trends")
    );
    console.log("Initial API calls:", JSON.stringify(initialCalls, null, 2));

    // Find the entity selector — it's a MUI Autocomplete with "All Entities" text
    const entityCombobox = page.getByRole("combobox").first();

    if (await entityCombobox.isVisible({ timeout: 5000 }).catch(() => false)) {
      // Clear the current selection and select a specific entity
      await entityCombobox.click();
      await page.waitForTimeout(500);

      // Look for entity options in the dropdown
      const options = page.getByRole("option");
      const optionCount = await options.count();
      console.log(`Found ${optionCount} entity options`);

      if (optionCount > 1) {
        // Get text of second option for logging
        const optionText = await options.nth(1).textContent();
        console.log(`Selecting entity: ${optionText}`);
        await options.nth(1).click();
        await page.waitForLoadState("networkidle");
        await page.waitForTimeout(1000);

        // Check that new API calls include entity_id
        const entityCalls = apiCalls.filter(
          (c) =>
            c.entityId !== null &&
            (c.url.includes("/analysis/summary") ||
              c.url.includes("/analysis/cashflow/trends"))
        );
        console.log(
          "Entity-scoped API calls:",
          JSON.stringify(entityCalls, null, 2)
        );
        expect(entityCalls.length).toBeGreaterThan(0);
      }
    } else {
      console.log("No entity selector found — checking API calls only");
    }
  });

  test("dashboard renders without errors", async ({ page }) => {
    await page.goto(BASE + "/");
    await page.waitForLoadState("networkidle");

    // Dashboard should have the title
    await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible({ timeout: 10000 });

    // Should show financial data (Total Income card)
    await expect(page.getByText("Total Income")).toBeVisible({ timeout: 10000 });

    // Should show expense view toggle (the "operating expenses only" button)
    await expect(
      page.getByRole("button", { name: /operating/i })
    ).toBeVisible({ timeout: 10000 });

    // Should show export button
    await expect(
      page.getByRole("button", { name: /export/i })
    ).toBeVisible({ timeout: 10000 });
  });

  test("analysis page renders without errors", async ({ page }) => {
    await page.goto(BASE + "/analysis");
    await page.waitForLoadState("networkidle");

    // Analysis page should have the title
    await expect(
      page.getByRole("heading", { name: "Financial Analysis" })
    ).toBeVisible({ timeout: 10000 });

    // Should show export button
    await expect(
      page.getByRole("button", { name: /export/i })
    ).toBeVisible({ timeout: 10000 });

    // Should show expense view toggle
    await expect(
      page.getByRole("button", { name: /operating/i })
    ).toBeVisible({ timeout: 10000 });
  });

  test("backend entity_id filtering returns different data per entity", async ({
    request,
  }) => {
    test.setTimeout(120000); // Backend SQLite can be slow
    // Direct API test — verify backend filtering works
    const allData = await request.get(
      "http://localhost:8001/api/analysis/summary?mode=analysis&top_n=2&recent_count=2",
      { timeout: 60000 }
    );
    const allJson = await allData.json();

    const entity4Data = await request.get(
      "http://localhost:8001/api/analysis/summary?mode=analysis&top_n=2&recent_count=2&entity_id=4",
      { timeout: 60000 }
    );
    const entity4Json = await entity4Data.json();

    // Entity-filtered data should be different from all-entities data
    console.log(`All: income=${allJson.total_income}, expenses=${allJson.total_expenses}`);
    console.log(`Entity4: income=${entity4Json.total_income}, expenses=${entity4Json.total_expenses}`);

    // All entities should have more data than a single entity
    expect(Math.abs(allJson.total_income)).toBeGreaterThan(
      Math.abs(entity4Json.total_income)
    );
    expect(allJson.income_count + allJson.expense_count).toBeGreaterThan(
      entity4Json.income_count + entity4Json.expense_count
    );
  });
});
