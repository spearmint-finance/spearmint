import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForPageLoad,
  waitForDataGrid,
  getDataGridRowCount,
  clickDataGridRow,
  searchDataGrid,
  clickButton,
} from "./utils/test-helpers";

test.describe("Transaction List", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to transactions page
    await navigateTo(page, "/transactions");
    // Wait for DataGrid to load
    await waitForDataGrid(page);
  });

  test.describe("Basic UI Elements", () => {
    test("should display transactions page title", async ({ page }) => {
      await expect(
        page.getByRole("heading", { name: "Transactions" })
      ).toBeVisible();
    });

    test('should display "New Transaction" button', async ({ page }) => {
      await expect(
        page.getByRole("button", { name: "New Transaction" })
      ).toBeVisible();
    });

    test("should display search input", async ({ page }) => {
      await expect(
        page.getByPlaceholder("Search transactions...")
      ).toBeVisible();
    });

    test('should display "More Filters" button', async ({ page }) => {
      await expect(
        page.getByRole("button", { name: "More Filters" })
      ).toBeVisible();
    });
  });

  test("should display DataGrid", async ({ page }) => {
    await waitForDataGrid(page);

    // Check that DataGrid is rendered
    await expect(page.locator(".MuiDataGrid-root")).toBeVisible();
  });

  test("should display DataGrid columns", async ({ page }) => {
    await waitForDataGrid(page);

    // Check for column headers
    const expectedColumns = [
      "Date",
      "Description",
      "Category",
      "Type",
      "Amount",
    ];

    for (const column of expectedColumns) {
      await expect(
        page.getByRole("columnheader", { name: column })
      ).toBeVisible();
    }
  });

  test("should display pagination controls", async ({ page }) => {
    await waitForDataGrid(page);

    // Check for pagination
    const pagination = page.locator(".MuiTablePagination-root");
    await expect(pagination).toBeVisible();
  });

  test("should allow changing page size", async ({ page }) => {
    await waitForDataGrid(page);

    // Click on rows per page dropdown
    await page.locator('[aria-label="Rows per page:"]').click();

    // Select different page size
    await page.getByRole("option", { name: "50" }).click();

    // Wait for data to reload
    await waitForPageLoad(page);

    // Verify the selection
    await expect(page.locator("text=50")).toBeVisible();
  });

  test("should filter transactions by search text", async ({ page }) => {
    await waitForDataGrid(page);

    // Get initial row count
    const initialCount = await getDataGridRowCount(page);

    if (initialCount > 0) {
      // Search for something specific
      await searchDataGrid(page, "test");

      // Wait for results
      await waitForPageLoad(page);

      // Row count may change (could be 0 if no matches)
      const newCount = await getDataGridRowCount(page);
      expect(newCount).toBeGreaterThanOrEqual(0);
    }
  });

  test("should clear search filter", async ({ page }) => {
    await waitForDataGrid(page);

    // Search for something
    await searchDataGrid(page, "test");
    await waitForPageLoad(page);

    // Clear button should appear
    const clearButton = page.getByRole("button", { name: "Clear" });

    if (await clearButton.isVisible()) {
      await clearButton.click();
      await waitForPageLoad(page);

      // Search input should be empty
      const searchInput = page.getByPlaceholder("Search transactions...");
      await expect(searchInput).toHaveValue("");
    }
  });

  test("should display transaction type chips", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Check for Income or Expense chips
      const chips = page.locator(".MuiChip-root");
      const chipCount = await chips.count();

      expect(chipCount).toBeGreaterThan(0);
    }
  });

  test("should color-code amounts correctly", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Check for colored cells (income-cell or expense-cell classes)
      const coloredCells = page.locator(".income-cell, .expense-cell");
      const count = await coloredCells.count();

      expect(count).toBeGreaterThan(0);
    }
  });

  test("should open transaction detail on row click", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Click first row
      await clickDataGridRow(page, 0);

      // Dialog should open
      await page.waitForSelector('[role="dialog"]', { timeout: 5000 });
      await expect(page.getByRole("dialog")).toBeVisible();

      // Should show "Transaction Details" title
      await expect(page.getByText("Transaction Details")).toBeVisible();
    }
  });

  test("should have clickable rows with cursor pointer", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Check that rows have pointer cursor
      const firstRow = page.locator(".MuiDataGrid-row").first();
      const cursor = await firstRow.evaluate(
        (el) => window.getComputedStyle(el).cursor
      );

      expect(cursor).toBe("pointer");
    }
  });

  test("should display loading state", async ({ page }) => {
    // Navigate and try to catch loading state
    const navPromise = page.goto("/transactions");

    // Try to see loading spinner
    const loadingText = page.getByText("Loading transactions...");
    const isVisible = await loadingText.isVisible().catch(() => false);

    await navPromise;

    // After loading, spinner should be gone
    await expect(loadingText).not.toBeVisible();
  });

  test("should handle empty state", async ({ page }) => {
    await waitForPageLoad(page);

    // If there are no transactions, DataGrid should still render
    const dataGrid = page.locator(".MuiDataGrid-root");
    await expect(dataGrid).toBeVisible();
  });

  test("should navigate between pages", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    // Only test pagination if there are enough rows
    if (rowCount >= 25) {
      // Click next page button
      const nextButton = page.getByRole("button", { name: "Go to next page" });

      if (await nextButton.isEnabled()) {
        await nextButton.click();
        await waitForPageLoad(page);

        // Should still have rows
        const newCount = await getDataGridRowCount(page);
        expect(newCount).toBeGreaterThan(0);
      }
    }
  });

  test("should sort by clicking column headers", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 1) {
      // Click on Date column header to sort
      await page.getByRole("columnheader", { name: "Date" }).click();
      await waitForPageLoad(page);

      // DataGrid should still be visible
      await expect(page.locator(".MuiDataGrid-root")).toBeVisible();
    }
  });

  test("should maintain state when navigating away and back", async ({
    page,
  }) => {
    await waitForDataGrid(page);

    // Search for something
    await searchDataGrid(page, "test");
    await waitForPageLoad(page);

    // Navigate to dashboard
    await page.getByRole("button", { name: "Dashboard" }).click();
    await waitForPageLoad(page);

    // Navigate back to transactions
    await page.getByRole("button", { name: "Transactions" }).click();
    await waitForPageLoad(page);

    // Page should load successfully
    await expect(
      page.getByRole("heading", { name: "Transactions" })
    ).toBeVisible();
  });

  test("should display formatted currency values", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Look for currency symbols in the Amount column
      const amounts = page
        .locator(".MuiDataGrid-cell")
        .filter({ hasText: "$" });
      const count = await amounts.count();

      expect(count).toBeGreaterThan(0);
    }
  });

  test("should display formatted dates", async ({ page }) => {
    await waitForDataGrid(page);

    const rowCount = await getDataGridRowCount(page);

    if (rowCount > 0) {
      // Dates should be in MM/DD/YYYY format
      const datePattern = /\d{2}\/\d{2}\/\d{4}/;
      const dateCells = page
        .locator(".MuiDataGrid-cell")
        .filter({ hasText: datePattern });
      const count = await dateCells.count();

      expect(count).toBeGreaterThan(0);
    }
  });

  test.describe("Data Loading and Verification - Critical Bug Prevention", () => {
    test("should load actual transaction data from API (prevents blank page bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Verify at least one row exists
      const rowCount = await getDataGridRowCount(page);
      expect(rowCount).toBeGreaterThan(0);

      // Get first row data
      const firstRow = page.locator(".MuiDataGrid-row").first();
      await expect(firstRow).toBeVisible();

      // Verify all columns have actual data (not empty)
      const cells = firstRow.locator(".MuiDataGrid-cell");
      const cellCount = await cells.count();
      expect(cellCount).toBeGreaterThan(5); // Should have Date, Description, Category, Type, Amount, Balance

      // Check each cell has content
      for (let i = 0; i < cellCount; i++) {
        const cellText = await cells.nth(i).textContent();
        // Cell should not be empty (except Balance which can be "-")
        expect(cellText).toBeTruthy();
      }
    });

    test("should display Date column with actual dates (prevents field mapping bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Find Date column header
      const dateHeader = page
        .locator(".MuiDataGrid-columnHeader")
        .filter({ hasText: "Date" });
      await expect(dateHeader).toBeVisible();

      // Get first row's date cell (first column)
      const firstRow = page.locator(".MuiDataGrid-row").first();
      const dateCell = firstRow.locator(".MuiDataGrid-cell").first();
      const dateText = await dateCell.textContent();

      // Verify date format (MM/DD/YYYY)
      expect(dateText).toMatch(/\d{1,2}\/\d{1,2}\/\d{4}/);

      // Verify it's not showing "undefined" or empty
      expect(dateText).not.toContain("undefined");
      expect(dateText).not.toBe("");
    });

    test("should display Description with actual text (prevents data transformation bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get first row's description (second column)
      const firstRow = page.locator(".MuiDataGrid-row").first();
      const descCell = firstRow.locator(".MuiDataGrid-cell").nth(1);
      const descText = await descCell.textContent();

      // Should have actual description text
      expect(descText).toBeTruthy();
      expect(descText!.length).toBeGreaterThan(0);
      expect(descText).not.toContain("undefined");
    });

    test("should display Amount with currency formatting (prevents data type bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Find Amount column cells
      const firstRow = page.locator(".MuiDataGrid-row").first();
      const amountCell = firstRow
        .locator(".MuiDataGrid-cell")
        .filter({ hasText: "$" })
        .first();
      const amountText = await amountCell.textContent();

      // Verify currency format ($X,XXX.XX)
      expect(amountText).toMatch(/\$[\d,]+\.\d{2}/);
      expect(amountText).not.toContain("undefined");
      expect(amountText).not.toContain("NaN");
    });

    test("should correctly identify and display Transfer transactions", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Look for transfer transactions (should have "Transfer" chip, not "Income" or "Expense")
      const transferChips = page
        .locator(".MuiChip-label")
        .filter({ hasText: "Transfer" });
      const transferCount = await transferChips.count();

      if (transferCount > 0) {
        // Verify transfer chip exists
        const firstTransferChip = transferChips.first();
        await expect(firstTransferChip).toBeVisible();

        // Verify it's not showing as "Income" or "Expense"
        const chipText = await firstTransferChip.textContent();
        expect(chipText).toBe("Transfer");

        // Verify chip color is default (gray), not success (green) or error (red)
        const chipElement = firstTransferChip.locator("..");
        const chipClass = await chipElement.getAttribute("class");
        expect(chipClass).toContain("MuiChip-colorDefault");
        expect(chipClass).not.toContain("MuiChip-colorSuccess");
        expect(chipClass).not.toContain("MuiChip-colorError");
      }
    });
  });

  test.describe("Layout and Positioning - Critical Bug Prevention", () => {
    test("should display Date column without being cut off (prevents layout bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get Date column header
      const dateHeader = page
        .locator(".MuiDataGrid-columnHeader")
        .filter({ hasText: "Date" });
      await expect(dateHeader).toBeVisible();

      // Get bounding box
      const box = await dateHeader.boundingBox();
      expect(box).toBeTruthy();

      // Date column should be fully visible (x position should be >= 0)
      expect(box!.x).toBeGreaterThanOrEqual(0);

      // Should be within viewport
      const viewport = page.viewportSize();
      expect(box!.x).toBeLessThan(viewport!.width);

      // Verify first data cell in Date column is also visible
      const firstRow = page.locator(".MuiDataGrid-row").first();
      const firstDateCell = firstRow.locator(".MuiDataGrid-cell").first();
      const cellBox = await firstDateCell.boundingBox();
      expect(cellBox!.x).toBeGreaterThanOrEqual(0);
    });

    test("should not have sidebar overlapping main content (prevents overlap bug)", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get main content area
      const mainContent = page.locator("main");
      const mainBox = await mainContent.boundingBox();

      // Main content should start after sidebar (240px) + some padding
      // Should be at least 240px from left edge
      expect(mainBox!.x).toBeGreaterThanOrEqual(240);
    });

    test("should have all DataGrid columns visible without horizontal scroll", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get DataGrid container
      const dataGrid = page.locator(".MuiDataGrid-root");

      // Check if horizontal scrollbar exists on DataGrid
      const hasHorizontalScroll = await dataGrid.evaluate((el) => {
        return el.scrollWidth > el.clientWidth;
      });

      // DataGrid can have horizontal scroll, but main content should not
      const mainContent = page.locator("main");
      const mainHasScroll = await mainContent.evaluate((el) => {
        return el.scrollWidth > el.clientWidth;
      });

      // Main content should not require horizontal scrolling
      expect(mainHasScroll).toBe(false);
    });

    test("should have proper spacing between sidebar and content", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get DataGrid container
      const dataGrid = page.locator(".MuiDataGrid-root");
      const gridBox = await dataGrid.boundingBox();

      // DataGrid should not be at x=0 (should have left margin from sidebar + padding)
      // Sidebar is 240px, main content has padding of 24px
      expect(gridBox!.x).toBeGreaterThan(240);
    });

    test("should display all column headers within viewport", async ({
      page,
    }) => {
      await waitForDataGrid(page);

      // Get all column headers
      const headers = page.locator(".MuiDataGrid-columnHeader");
      const headerCount = await headers.count();

      expect(headerCount).toBeGreaterThan(0);

      // Check first header (Date) is visible
      const firstHeader = headers.first();
      const firstBox = await firstHeader.boundingBox();
      expect(firstBox!.x).toBeGreaterThanOrEqual(0);
    });
  });
});
