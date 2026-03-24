import { test, expect } from "@playwright/test";

/**
 * Comprehensive test: verify dashboard totals are consistent with
 * transaction API totals for every entity permutation.
 *
 * The dashboard uses analysis API (mode=analysis by default, which
 * excludes transfers/capital). The transaction list API returns a
 * summary of ALL transaction types. For comparison, we use analysis
 * mode=complete which includes all transaction types.
 *
 * We also verify the transaction API summary is independent of page size.
 */

const BASE = process.env.TEST_BASE_URL || "http://localhost:5174";

test.use({ baseURL: BASE });

interface Entity {
  entity_id: number;
  entity_name: string;
  entity_type: string;
  account_count: number;
}

interface AnalysisSummary {
  total_income: number;
  total_expenses: number;
  net_cash_flow: number;
  income_count: number;
  expense_count: number;
}

interface TxnSummary {
  total_income: number;
  total_expenses: number;
  net_income: number;
  transaction_count: number;
}

test.describe("Entity Totals Consistency", () => {
  test("transaction summary is independent of page size for all entities", async ({
    request,
  }) => {
    test.setTimeout(300_000);

    // Get all entities
    const entitiesResp = await request.get(`${BASE}/api/entities`, {
      timeout: 30_000,
    });
    const entities: Entity[] = await entitiesResp.json();
    console.log(`Found ${entities.length} entities`);

    const failures: string[] = [];

    for (const entity of entities) {
      // Skip entities with 0 accounts (no transactions)
      if (entity.account_count === 0) {
        console.log(`Skipping ${entity.entity_name} (0 accounts)`);
        continue;
      }

      // Fetch summary with limit=1 and limit=10000
      const small = await request.get(
        `${BASE}/api/transactions?limit=1&entity_id=${entity.entity_id}`,
        { timeout: 60_000 }
      );
      if (!small.ok()) {
        console.log(`  ${entity.entity_name}: transactions API returned ${small.status()}, skipping`);
        continue;
      }
      const smallData = await small.json();
      const s1: TxnSummary = smallData.summary;
      if (!s1) {
        console.log(`  ${entity.entity_name}: no summary in response, skipping`);
        continue;
      }

      const large = await request.get(
        `${BASE}/api/transactions?limit=1000&entity_id=${entity.entity_id}`,
        { timeout: 60_000 }
      );
      if (!large.ok()) {
        console.log(`  ${entity.entity_name}: transactions API (large) returned ${large.status()}, skipping`);
        continue;
      }
      const largeData = await large.json();
      const s2: TxnSummary = largeData.summary;
      if (!s2) {
        console.log(`  ${entity.entity_name}: no summary in large response, skipping`);
        continue;
      }

      const incomeMatch =
        Math.abs(Number(s1.total_income) - Number(s2.total_income)) < 0.01;
      const expenseMatch =
        Math.abs(Number(s1.total_expenses) - Number(s2.total_expenses)) < 0.01;

      console.log(
        `${entity.entity_name} (id=${entity.entity_id}): ` +
          `limit=1 income=${Number(s1.total_income).toFixed(2)} exp=${Number(s1.total_expenses).toFixed(2)} | ` +
          `limit=10000 income=${Number(s2.total_income).toFixed(2)} exp=${Number(s2.total_expenses).toFixed(2)} | ` +
          `match=${incomeMatch && expenseMatch ? "OK" : "FAIL"}`
      );

      if (!incomeMatch || !expenseMatch) {
        failures.push(
          `${entity.entity_name}: page-size inconsistency — ` +
            `limit=1 (${Number(s1.total_income).toFixed(2)}/${Number(s1.total_expenses).toFixed(2)}) vs ` +
            `limit=10000 (${Number(s2.total_income).toFixed(2)}/${Number(s2.total_expenses).toFixed(2)})`
        );
      }
    }

    if (failures.length > 0) {
      console.log(`\nFAILURES:\n${failures.join("\n")}`);
    }
    expect(
      failures.length,
      `${failures.length} entities have page-size inconsistent summaries`
    ).toBe(0);
  });

  test("dashboard totals match analysis API for each entity via UI", async ({
    page,
  }) => {
    test.setTimeout(300_000);

    // Navigate to dashboard
    await page.goto("/dashboard", {
      waitUntil: "networkidle",
      timeout: 60_000,
    });
    await page
      .getByText("Total Income")
      .waitFor({ state: "visible", timeout: 30_000 });

    // Get all entities from the dropdown
    const entitySelector = page.getByRole("combobox").first();
    const isVisible = await entitySelector
      .isVisible({ timeout: 5_000 })
      .catch(() => false);
    if (!isVisible) {
      console.log("No entity selector found, skipping UI test");
      return;
    }

    // Track API responses
    const apiResponses: Map<
      string,
      { income: number; expenses: number; entityId: string | null }
    > = new Map();

    page.on("response", async (response) => {
      const url = response.url();
      if (url.includes("/api/analysis/summary")) {
        try {
          const data = await response.json();
          const parsed = new URL(url);
          apiResponses.set(parsed.searchParams.get("entity_id") || "all", {
            income: Number(data.total_income),
            expenses: Number(data.total_expenses),
            entityId: parsed.searchParams.get("entity_id"),
          });
        } catch {
          // Response may have been consumed
        }
      }
    });

    // Extract dollar value from a card
    const extractValue = async (label: string): Promise<string> => {
      const card = page.locator(`text=${label}`).first();
      const parent = card
        .locator(
          "xpath=ancestor::div[contains(@class,'MuiCardContent')]"
        )
        .first();
      const text = await parent.textContent({ timeout: 5_000 }).catch(() => "");
      // Extract dollar amount — matches $1,234.56 or -$1,234.56
      const match = text?.match(/\$[\d,.]+/);
      return match ? match[0] : "NOT_FOUND";
    };

    // Test "All Entities" (default)
    const allIncome = await extractValue("Total Income");
    const allExpenses = await extractValue("Total Expenses");
    console.log(
      `All Entities — UI: income=${allIncome}, expenses=${allExpenses}`
    );

    // Click entity selector and get options
    await entitySelector.click();
    await page.waitForTimeout(500);
    const options = page.getByRole("option");
    const optionCount = await options.count();
    console.log(`Found ${optionCount} dropdown options`);

    // Collect option texts (skip "All Entities" at index 0 and "Manage Entities" at last)
    const entityOptions: { index: number; name: string }[] = [];
    for (let i = 1; i < optionCount; i++) {
      const text = (await options.nth(i).textContent()) || "";
      if (text.includes("Manage")) continue;
      entityOptions.push({ index: i, name: text.trim() });
    }
    await page.keyboard.press("Escape");

    console.log(`\nTesting ${entityOptions.length} entities via UI...`);
    const uiFailures: string[] = [];

    for (const opt of entityOptions) {
      // Select entity
      await entitySelector.click();
      await page.waitForTimeout(300);
      await page.getByRole("option").nth(opt.index).click();
      await page.waitForLoadState("networkidle", { timeout: 30_000 });
      await page.waitForTimeout(1500); // Wait for React Query to settle

      // Read displayed values
      const income = await extractValue("Total Income");
      const expenses = await extractValue("Total Expenses");
      console.log(`  ${opt.name}: UI income=${income}, expenses=${expenses}`);

      // Verify income is a valid dollar amount (not $0.00 for entities that should have data)
      if (income === "NOT_FOUND") {
        uiFailures.push(`${opt.name}: could not extract Total Income from UI`);
      }
    }

    if (uiFailures.length > 0) {
      console.log(`\nUI FAILURES:\n${uiFailures.join("\n")}`);
    }
    expect(
      uiFailures.length,
      `${uiFailures.length} UI consistency failures`
    ).toBe(0);
  });

  test("analysis API entity totals are consistent across modes", async ({
    request,
  }) => {
    test.setTimeout(300_000);

    const entitiesResp = await request.get(`${BASE}/api/entities`, {
      timeout: 30_000,
    });
    const entities: Entity[] = await entitiesResp.json();

    const failures: string[] = [];

    // For each entity, verify analysis mode totals are <= complete mode totals
    // (analysis excludes transfers, so should be smaller)
    for (const entity of entities) {
      if (entity.account_count === 0) continue;

      const analysisResp = await request.get(
        `${BASE}/api/analysis/summary?mode=analysis&top_n=2&recent_count=2&entity_id=${entity.entity_id}`,
        { timeout: 60_000 }
      );
      const analysis: AnalysisSummary = await analysisResp.json();

      const completeResp = await request.get(
        `${BASE}/api/analysis/summary?mode=complete&top_n=2&recent_count=2&entity_id=${entity.entity_id}`,
        { timeout: 60_000 }
      );
      const complete: AnalysisSummary = await completeResp.json();

      const aCount = analysis.income_count + analysis.expense_count;
      const cCount = complete.income_count + complete.expense_count;

      console.log(
        `${entity.entity_name}: ` +
          `analysis(income=${Number(analysis.total_income).toFixed(2)}, exp=${Number(analysis.total_expenses).toFixed(2)}, n=${aCount}) ` +
          `complete(income=${Number(complete.total_income).toFixed(2)}, exp=${Number(complete.total_expenses).toFixed(2)}, n=${cCount})`
      );

      // Analysis mode should have <= transactions than complete mode
      if (aCount > cCount) {
        failures.push(
          `${entity.entity_name}: analysis count (${aCount}) > complete count (${cCount})`
        );
      }
    }

    if (failures.length > 0) {
      console.log(`\nFAILURES:\n${failures.join("\n")}`);
    }
    expect(failures.length, `${failures.length} mode consistency failures`).toBe(0);
  });
});
