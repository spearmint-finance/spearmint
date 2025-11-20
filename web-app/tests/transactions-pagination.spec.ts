import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForPageLoad,
  waitForDataGrid,
  getDataGridRowCount,
} from "./utils/test-helpers";

/**
 * Helpers local to this spec
 */
async function getDisplayedRowsText(page) {
  const locator = page.locator(".MuiTablePagination-displayedRows").first();
  await locator.waitFor({ state: "visible" });
  await expect(locator).toContainText("of");
  const text = await locator.textContent();
  return (text || "").trim();
}

function parseDisplayedRange(text) {
  // Formats like: "1–25 of 5,515" or "0–0 of 0"
  const match = text.match(/(\d+)[^\d]+(\d+)[^\d]+(\d[\d,]*)/);
  if (!match) return null;
  const start = parseInt(match[1], 10);
  const end = parseInt(match[2], 10);
  const total = parseInt(match[3].replace(/,/g, ""), 10);
  return { start, end, total };
}
async function getFirstRowSignature(page) {
  // Prefer a stable attribute if present
  const row = page.locator(".MuiDataGrid-row").first();
  await row.waitFor({ state: "visible" });
  // data-id is present on MUI rows in v6; fall back to text content
  const dataId = await row.getAttribute("data-id");
  if (dataId) return `id:${dataId}`;
  const text = await row.textContent();
  return (text || "").slice(0, 100);
}

async function setRowsPerPage(page, size) {
  const combo = page.getByRole("combobox", { name: "Rows per page:" });
  if (await combo.count()) {
    await combo.click();
  } else {
    // Fallback to aria-label selector (older MUI versions)
    await page.locator('[aria-label="Rows per page:"]').click();
  }
  await page.getByRole("option", { name: new RegExp(`^${size}$`) }).click();
  await waitForPageLoad(page);
}

async function openFilters(page) {
  await page.getByRole("button", { name: "More Filters" }).click();
}

async function applyFilters(page) {
  await page.getByRole("button", { name: "Apply Filters" }).click();
  await waitForPageLoad(page);
}

async function clearAllFilters(page) {
  const clear = page.getByRole("button", { name: /Clear All/i });
  if (await clear.isVisible()) {
    await clear.click();
    await waitForPageLoad(page);
  }
}

async function waitForTransactionsRequest(page, predicate) {
  // Wait for a /api/transactions request that matches a predicate on the URL
  const response = await page.waitForResponse((resp) => {
    const url = resp.url();
    if (!url.includes("/api/transactions")) return false;
    if (predicate) return predicate(url, resp);
    return resp.ok();
  });
  return response;
}

/**
 * Transactions Pagination Suite
 */
test.describe("Transactions pagination", () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, "/transactions");
    await waitForDataGrid(page);
  });

  test("basic pagination: next/previous/first/last", async ({ page }) => {
    // Ensure data has loaded and default page is populated
    await expect
      .poll(async () => await getDataGridRowCount(page), { timeout: 15000 })
      .toBeGreaterThan(0);
    const initialText = await getDisplayedRowsText(page);
    const initial = parseDisplayedRange(initialText)!;
    expect(initial).toBeTruthy();
    expect(initial.start).toBeGreaterThanOrEqual(0);

    const prevBtn = page.getByRole("button", { name: "Go to previous page" });
    const nextBtn = page.getByRole("button", { name: "Go to next page" });
    const firstBtn = page
      .getByRole("button", { name: "Go to first page" })
      .first();
    const lastBtn = page
      .getByRole("button", { name: "Go to last page" })
      .first();

    // On first page: prev should be disabled; first may not exist depending on component
    await expect(prevBtn).toBeDisabled();
    if ((await firstBtn.count()) > 0) {
      await expect(firstBtn).toBeDisabled();
    }

    // Go to next page
    if (await nextBtn.isEnabled()) {
      const beforeSig = await getFirstRowSignature(page);
      const targetOffset = initial.end; // next page should request offset=end
      const waitReq = waitForTransactionsRequest(
        page,
        (url) =>
          url.includes("/api/transactions") &&
          url.includes(`offset=${targetOffset}`)
      );
      await nextBtn.click();
      await waitReq;
      // Accept either the displayed range moves or the first row changes
      const moved = await expect
        .poll(
          async () => {
            const t = await getDisplayedRowsText(page);
            const r = parseDisplayedRange(t);
            return r?.start || 0;
          },
          { timeout: 15000 }
        )
        .toBeGreaterThan(initial.start)
        .catch(() => false);
      if (moved === false) {
        await expect
          .poll(async () => await getFirstRowSignature(page), {
            timeout: 15000,
          })
          .not.toEqual(beforeSig);
      }
    }

    // Go to last page then back to first
    if ((await lastBtn.count()) > 0 && (await lastBtn.isEnabled())) {
      await lastBtn.click();
      await waitForPageLoad(page);
      await expect(nextBtn).toBeDisabled();

      await firstBtn.click();
      await waitForPageLoad(page);
      await expect(prevBtn).toBeDisabled();
    }
  });

  test("page size changes update ranges correctly", async ({ page }) => {
    // 10 per page
    await setRowsPerPage(page, 10);
    await expect
      .poll(
        async () =>
          parseDisplayedRange(await getDisplayedRowsText(page))?.end || 0
      )
      .toBeGreaterThan(0);
    let text = await getDisplayedRowsText(page);
    let r = parseDisplayedRange(text)!;
    expect(r.start).toBe(1);
    expect(r.end - r.start + 1).toBeLessThanOrEqual(10);

    // 50 per page
    await setRowsPerPage(page, 50);
    await expect
      .poll(
        async () =>
          parseDisplayedRange(await getDisplayedRowsText(page))?.end || 0
      )
      .toBeGreaterThan(0);
    text = await getDisplayedRowsText(page);
    r = parseDisplayedRange(text)!;
    expect(r.start).toBe(1);
    expect(r.end - r.start + 1).toBeLessThanOrEqual(50);
  });

  test("filters + pagination: transaction type remains applied when paging", async ({
    page,
  }) => {
    // Open filters and select Income
    await openFilters(page);
    await page.getByRole("dialog").waitFor({ state: "visible" });
    // Open the 'Transaction Type' select using test id to avoid fragile role matching
    await page
      .locator(
        '[data-testid="filter-transaction-type"] [aria-haspopup="listbox"]'
      )
      .click();
    await page.getByRole("option", { name: /^Income$/ }).click();

    const waitApplyReq = waitForTransactionsRequest(
      page,
      (url) =>
        url.includes("transaction_type=Income") && url.includes("offset=0")
    );
    await applyFilters(page);
    await waitApplyReq;

    // Navigate to next page and verify param persists
    const nextBtn = page.getByRole("button", { name: "Go to next page" });
    if (await nextBtn.isEnabled()) {
      const waitNextReq = waitForTransactionsRequest(
        page,
        (url) =>
          url.includes("transaction_type=Income") && url.includes("offset=")
      );
      await nextBtn.click();
      await waitNextReq;
      const text2 = await getDisplayedRowsText(page);
      const r2 = parseDisplayedRange(text2)!;
      expect(r2.start).toBeGreaterThan(1);
    }

    await clearAllFilters(page);
  });

  test("edge case: empty results show no rows and controls disabled", async ({
    page,
  }) => {
    await openFilters(page);
    // Choose a far-future date range
    await page.getByLabel("Start Date").fill("2099-01-01");
    await page.getByLabel("End Date").fill("2099-01-02");
    const waitEmptyReq = waitForTransactionsRequest(
      page,
      (url) =>
        url.includes("start_date=2099-01-01") &&
        url.includes("end_date=2099-01-02")
    );
    await applyFilters(page);
    await waitEmptyReq;

    // Prefer checking the displayed count and overlay rather than DOM rows
    const text = await getDisplayedRowsText(page);
    const r = parseDisplayedRange(text);
    if (r) {
      expect(r.total).toBe(0);
    }
    // 'No rows' overlay appears for empty datasets
    const overlay = page.locator(".MuiDataGrid-overlay");
    await expect(overlay).toBeVisible();

    const prevBtn = page.getByRole("button", { name: "Go to previous page" });
    const nextBtn = page.getByRole("button", { name: "Go to next page" });
    await expect(prevBtn).toBeDisabled();
    await expect(nextBtn).toBeDisabled();

    await clearAllFilters(page);
  });

  test("single-page results: next is disabled and start resets to 1 when filtering with unique search", async ({
    page,
  }) => {
    // Grab a description from first row
    const firstDesc = await page
      .locator(".MuiDataGrid-row >> .MuiDataGrid-cell")
      .nth(1)
      .textContent()
      .catch(() => "");
    if (!firstDesc) test.skip();

    // Search with that exact text to narrow results
    const search = page.getByPlaceholder("Search transactions...");
    await search.fill(firstDesc.trim());
    await waitForPageLoad(page);

    await setRowsPerPage(page, 100);
    const text = await getDisplayedRowsText(page);
    const r = parseDisplayedRange(text)!;
    expect(r.start).toBe(1);
    // In a highly filtered search, total should fit in one page; if not, skip assertions
    if (r.total <= 100) {
      const nextBtn = page.getByRole("button", { name: "Go to next page" });
      await expect(nextBtn).toBeDisabled();
    }

    // Clear search
    await clearAllFilters(page);
  });
});
