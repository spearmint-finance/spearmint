/**
 * Entity assignment end-to-end test.
 */
import { test, expect, Page } from "@playwright/test";

async function waitForGrid(page: Page) {
  await page.waitForSelector(".MuiDataGrid-row", { timeout: 15000 });
}

test.describe("Entity Assignment", () => {
  test("assign entity to transaction and verify it persists", async ({ page }) => {
    // Capture all API requests/responses
    const apiCalls: { method: string; url: string; body: string; status: number; response: string }[] = [];
    page.on("request", async (req) => {
      if (req.url().includes("/api/transactions/") && req.method() === "PUT") {
        apiCalls.push({ method: req.method(), url: req.url(), body: req.postData() || "", status: 0, response: "" });
      }
    });
    page.on("response", async (res) => {
      if (res.url().includes("/api/transactions/") && res.request().method() === "PUT") {
        const idx = apiCalls.findLastIndex(c => c.url === res.url());
        if (idx >= 0) {
          apiCalls[idx].status = res.status();
          apiCalls[idx].response = await res.text().catch(() => "");
        }
      }
    });

    // Step 1: Navigate to transactions
    await page.goto("/transactions");
    await waitForGrid(page);

    // Step 2: Click on the amount cell of first row (triggers dialog)
    const firstRow = page.locator(".MuiDataGrid-row").first();
    const desc = await firstRow.locator('[data-field="description"]').textContent();
    console.log(`Transaction: "${desc}"`);

    // Click a cell that opens the dialog (not description/category/boolean fields)
    await firstRow.locator('[data-field="amount"]').click();
    await page.waitForSelector('[role="dialog"]', { timeout: 10000 });
    await page.screenshot({ path: "tests/playwright/test-results/01-edit-dialog.png" });

    // Step 3: Find the Entity select — it's one of the MuiSelect-select elements
    const selectElements = await page.locator('[role="dialog"] .MuiSelect-select').all();
    console.log(`Select elements in dialog: ${selectElements.length}`);
    for (let i = 0; i < selectElements.length; i++) {
      console.log(`  select[${i}]: "${await selectElements[i].textContent()}"`);
    }

    // Entity is the 3rd MuiSelect-select (index 2): Category=0, Account=1, Entity=2
    const entitySelect = page.locator('[role="dialog"] .MuiSelect-select').nth(2);
    const entitySelectText = await entitySelect.textContent();
    console.log(`Entity select current value: "${entitySelectText}"`);

    // Click to open the dropdown
    await entitySelect.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: "tests/playwright/test-results/02-entity-dropdown.png" });

    // Pick "Personal" from the dropdown
    const options = await page.getByRole("option").all();
    console.log(`Options in dropdown:`);
    for (const opt of options) {
      console.log(`  "${await opt.textContent()}"`);
    }

    await page.getByRole("option", { name: "Personal" }).click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: "tests/playwright/test-results/03-entity-selected.png" });

    // Step 4: Click Update
    await page.getByRole("button", { name: /update/i }).click();
    await page.waitForTimeout(2000);
    await page.screenshot({ path: "tests/playwright/test-results/04-after-save.png" });

    // Step 5: Show captured API call details
    console.log(`\nAPI calls intercepted: ${apiCalls.length}`);
    for (const call of apiCalls) {
      console.log(`  ${call.method} ${call.url}`);
      console.log(`  Request body: ${call.body}`);
      console.log(`  Response status: ${call.status}`);
      console.log(`  Response body: ${call.response.substring(0, 300)}`);
    }

    // Check for error/success toast
    const errorToast = await page.getByText(/failed to update/i).isVisible({ timeout: 2000 }).catch(() => false);
    const successToast = await page.getByText(/updated successfully/i).isVisible({ timeout: 2000 }).catch(() => false);
    console.log(`\nError toast: ${errorToast}, Success toast: ${successToast}`);

    if (errorToast) {
      // Print what the API returned
      const errDetail = apiCalls[0]?.response || "no response captured";
      throw new Error(`Save failed. API response: ${errDetail}`);
    }

    // Step 6: Verify via API that entity_id is persisted
    await page.waitForTimeout(500);
    const verifyResponse = await page.evaluate(async () => {
      const r = await fetch("/api/transactions?limit=100&sort_by=updated_at&sort_order=desc");
      return r.json();
    });

    const txWithEntity = verifyResponse.transactions?.find((t: any) => t.entity_id !== null && t.entity_id !== undefined);
    console.log(`\nTransaction with entity_id: ${JSON.stringify(txWithEntity ? {
      id: txWithEntity.transaction_id,
      entity_id: txWithEntity.entity_id,
      desc: txWithEntity.description,
    } : null)}`);

    expect(txWithEntity, "No transaction has entity_id set — assignment failed").toBeTruthy();
    expect(txWithEntity.entity_id).toBe(1);

    // Step 7: Verify entity scope filter via API
    const filteredResponse = await page.evaluate(async (eid: number) => {
      const r = await fetch(`/api/transactions?entity_id=${eid}&limit=100`);
      return r.json();
    }, 1);
    console.log(`Transactions returned for entity_id=1: ${filteredResponse.total}`);
    expect(filteredResponse.total).toBeGreaterThan(0);

    console.log("\nPASS: Entity assignment and scope filter work end-to-end");
  });

  test("new transaction form has Entity field and boolean flags", async ({ page }) => {
    await page.goto("/transactions");
    await waitForGrid(page);

    await page.getByRole("button", { name: /new transaction/i }).click();
    await page.waitForSelector('[role="dialog"]', { timeout: 10000 });

    const dialogContent = await page.locator('[role="dialog"]').textContent();
    expect(dialogContent).toContain("Entity");
    expect(dialogContent?.toLowerCase()).toContain("capital expense");
    expect(dialogContent?.toLowerCase()).toContain("tax deductible");

    console.log("PASS: New transaction form has Entity and boolean flag fields");
  });
});
