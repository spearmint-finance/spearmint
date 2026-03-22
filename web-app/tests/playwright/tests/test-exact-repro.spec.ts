import { test, expect } from "@playwright/test";

test("EXACT REPRO: assign MemNexus, scope, edit category, observe disappearance", async ({ page }) => {
  // Track all PUT requests
  const puts: { url: string; body: string }[] = [];
  page.on("request", (req) => {
    if (req.method() === "PUT" && req.url().includes("/api/transactions/")) {
      puts.push({ url: req.url(), body: req.postData() || "" });
    }
  });

  // Track all GET requests for transactions (to see the refetch query)
  const gets: string[] = [];
  page.on("request", (req) => {
    if (req.method() === "GET" && req.url().includes("/api/transactions?")) {
      gets.push(req.url());
    }
  });

  // Step 1: View all transactions
  await page.goto("http://localhost:5173/transactions");
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(3000);

  // Ensure "All Entities" is selected
  await page.screenshot({ path: "tests/playwright/test-results/artifacts/repro-01-all.png" });
  const allRows = await page.locator('[role="row"][data-rowindex]').count();
  console.log(`Step 1: All transactions visible, rows=${allRows}`);

  // Step 2: Choose one and assign to MemNexus
  // Click on the first transaction's amount cell to open edit dialog
  const amountCell = page.locator('[role="gridcell"]').filter({ hasText: /^\$|^-\$/ }).first();
  await amountCell.click();
  await page.waitForTimeout(1000);

  let dialog = page.locator('[role="dialog"]');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  // Find the entity dropdown in the form and select "MemNexus"
  const entityField = dialog.getByRole('combobox', { name: 'Entity' }).first();
  await entityField.click();
  await page.waitForTimeout(300);
  const memnexusOption = page.locator('[role="option"]:has-text("MemNexus")');
  await expect(memnexusOption).toBeVisible({ timeout: 3000 });
  await memnexusOption.click();
  await page.waitForTimeout(500);

  // Save the form
  const saveBtn = dialog.locator('button:has-text("Save"), button:has-text("Update"), button[type="submit"]').first();
  await saveBtn.click();
  await page.waitForTimeout(3000);

  console.log("\nStep 2: Assigned MemNexus entity");
  console.log(`PUT requests: ${puts.length}`);
  for (const p of puts) {
    const parsed = JSON.parse(p.body);
    console.log(`  entity_id sent: ${parsed.entity_id}`);
  }

  await page.screenshot({ path: "tests/playwright/test-results/artifacts/repro-02-assigned.png" });

  // Step 3: Change scope to MemNexus
  puts.length = 0;
  gets.length = 0;

  const entitySelect = page.locator('text=All Entities').first();
  await entitySelect.click();
  await page.waitForTimeout(500);
  const mnOption = page.locator('[role="option"]:has-text("MemNexus")').first();
  await expect(mnOption).toBeVisible({ timeout: 3000 });
  await mnOption.click();
  await page.waitForTimeout(3000);

  const mnRows = await page.locator('[role="row"][data-rowindex]').count();
  console.log(`\nStep 3: MemNexus scope, rows=${mnRows}`);
  await page.screenshot({ path: "tests/playwright/test-results/artifacts/repro-03-scoped.png" });

  // Step 4: Click on that transaction to open edit dialog
  const scopedAmountCell = page.locator('[role="gridcell"]').filter({ hasText: /^\$|^-\$/ }).first();
  await scopedAmountCell.click();
  await page.waitForTimeout(1000);

  dialog = page.locator('[role="dialog"]');
  await expect(dialog).toBeVisible({ timeout: 5000 });

  // Check what entity the form shows
  const entityDisplay = dialog.getByRole('combobox', { name: 'Entity' }).first();
  const entityText = await entityDisplay.textContent().catch(() => "?");
  console.log(`\nStep 4: Form entity field shows: "${entityText}"`);

  await page.screenshot({ path: "tests/playwright/test-results/artifacts/repro-04-form.png" });

  // Step 5: Change the category
  const catSelect = dialog.locator('label:has-text("Category")').locator('..').locator('[role="combobox"]').first();
  await catSelect.click();
  await page.waitForTimeout(300);
  const catOptions = page.locator('[role="option"]');
  const catCount = await catOptions.count();
  console.log(`Category options: ${catCount}`);
  if (catCount > 3) {
    await catOptions.nth(3).click();
  } else {
    await catOptions.first().click();
  }
  await page.waitForTimeout(500);

  // Step 6: Save
  puts.length = 0;
  gets.length = 0;

  const saveBtn2 = dialog.locator('button:has-text("Save"), button:has-text("Update"), button[type="submit"]').first();
  await saveBtn2.click();
  await page.waitForTimeout(5000);

  console.log(`\nStep 6: Saved`);
  console.log(`PUT requests: ${puts.length}`);
  for (const p of puts) {
    const parsed = JSON.parse(p.body);
    console.log(`  Full body keys: ${Object.keys(parsed).join(', ')}`);
    console.log(`  entity_id: ${JSON.stringify(parsed.entity_id)}`);
    if (parsed.entity_id === null) {
      console.log(`  *** BUG: entity_id was set to null! ***`);
    }
  }

  console.log(`\nGET refetch URLs:`);
  for (const g of gets) {
    const url = new URL(g);
    console.log(`  entity_id param: ${url.searchParams.get('entity_id')}`);
  }

  await page.screenshot({ path: "tests/playwright/test-results/artifacts/repro-05-after-save.png" });

  // Step 7: Check if transaction disappeared
  const rowsAfter = await page.locator('[role="row"][data-rowindex]').count();
  console.log(`\nStep 7: Rows after save: ${rowsAfter} (was: ${mnRows})`);

  if (rowsAfter < mnRows) {
    console.log("*** BUG CONFIRMED: Transaction disappeared! ***");
  } else {
    console.log("Transaction still visible - no bug");
  }
});
