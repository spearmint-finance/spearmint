import { test, expect } from "@playwright/test";
import {
  navigateTo,
  waitForPageLoad,
  waitForDataGrid,
} from "./utils/test-helpers";

/**
 * Visual Regression Tests
 *
 * These tests capture screenshots and verify layout consistency to prevent
 * visual bugs like:
 * - Content being cut off or hidden
 * - Overlapping elements
 * - Incorrect positioning
 * - Missing or misaligned components
 */

test.describe("Visual Regression - Critical Bug Prevention", () => {
  test.describe("Transaction List Page", () => {
    test("should render transaction list without layout issues", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Take full page screenshot
      await expect(page).toHaveScreenshot("transaction-list-full-page.png", {
        fullPage: true,
        animations: "disabled",
      });
    });

    test("should display Date column in viewport (prevents cut-off bug)", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Take screenshot of DataGrid area
      const dataGrid = page.locator(".MuiDataGrid-root");
      await expect(dataGrid).toHaveScreenshot("transaction-list-datagrid.png", {
        animations: "disabled",
      });

      // Verify Date column header is visible
      const dateHeader = page
        .locator(".MuiDataGrid-columnHeader")
        .filter({ hasText: "Date" });
      await expect(dateHeader).toBeVisible();

      // Get position
      const box = await dateHeader.boundingBox();
      expect(box!.x).toBeGreaterThanOrEqual(0);
    });

    test("should have proper sidebar and content layout", async ({ page }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Take screenshot showing sidebar and main content
      await expect(page).toHaveScreenshot("transaction-list-with-sidebar.png", {
        fullPage: false,
        animations: "disabled",
      });

      // Verify no overlap
      const mainContent = page.locator("main");
      const mainBox = await mainContent.boundingBox();
      expect(mainBox!.x).toBeGreaterThanOrEqual(240); // Sidebar width
    });

    test("should display transfer chips correctly (prevents display bug)", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Look for Transfer chips
      const transferChips = page
        .locator(".MuiChip-label")
        .filter({ hasText: "Transfer" });
      const count = await transferChips.count();

      if (count > 0) {
        // Take screenshot of first transfer row
        const firstChip = transferChips.first();
        const row = firstChip.locator("..").locator("..").locator("..");

        await expect(row).toHaveScreenshot("transfer-transaction-row.png", {
          animations: "disabled",
        });

        // Verify chip is gray (default color), not green or red
        const chipElement = firstChip.locator("..");
        const chipClass = await chipElement.getAttribute("class");
        expect(chipClass).toContain("MuiChip-colorDefault");
      }
    });

    test("should render correctly at different viewport sizes", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Desktop view (1920x1080)
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.waitForTimeout(500); // Wait for layout to settle
      await expect(page).toHaveScreenshot("transaction-list-desktop.png", {
        fullPage: false,
        animations: "disabled",
      });

      // Tablet view (768x1024)
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.waitForTimeout(500);
      await expect(page).toHaveScreenshot("transaction-list-tablet.png", {
        fullPage: false,
        animations: "disabled",
      });

      // Verify no horizontal scroll on tablet
      const mainContent = page.locator("main");
      const hasScroll = await mainContent.evaluate((el) => {
        return el.scrollWidth > el.clientWidth;
      });
      expect(hasScroll).toBe(false);
    });
  });

  test.describe("Dashboard Page", () => {
    test("should render dashboard without layout issues", async ({ page }) => {
      await navigateTo(page, "/");
      await waitForPageLoad(page);

      // Take full page screenshot
      await expect(page).toHaveScreenshot("dashboard-full-page.png", {
        fullPage: true,
        animations: "disabled",
      });
    });

    test("should display all financial cards within viewport", async ({
      page,
    }) => {
      await navigateTo(page, "/");
      await waitForPageLoad(page);

      // Take screenshot of overview cards section
      const cardsSection = page.locator("main").first();
      await expect(cardsSection).toHaveScreenshot(
        "dashboard-overview-cards.png",
        {
          animations: "disabled",
        }
      );

      // Verify all cards are visible
      await expect(page.getByText("Total Income")).toBeVisible();
      await expect(page.getByText("Total Expenses")).toBeVisible();
      await expect(page.getByText("Net Cash Flow")).toBeVisible();
    });

    test("should have proper sidebar and content layout", async ({ page }) => {
      await navigateTo(page, "/");
      await waitForPageLoad(page);

      // Verify no overlap
      const mainContent = page.locator("main");
      const mainBox = await mainContent.boundingBox();
      expect(mainBox!.x).toBeGreaterThanOrEqual(240); // Sidebar width

      // Take screenshot
      await expect(page).toHaveScreenshot("dashboard-with-sidebar.png", {
        fullPage: false,
        animations: "disabled",
      });
    });

    test("should render correctly at different viewport sizes", async ({
      page,
    }) => {
      await navigateTo(page, "/");
      await waitForPageLoad(page);

      // Desktop view
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.waitForTimeout(500);
      await expect(page).toHaveScreenshot("dashboard-desktop.png", {
        fullPage: false,
        animations: "disabled",
      });

      // Tablet view
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.waitForTimeout(500);
      await expect(page).toHaveScreenshot("dashboard-tablet.png", {
        fullPage: false,
        animations: "disabled",
      });
    });
  });

  test.describe("Layout Consistency Across Pages", () => {
    test("should have consistent sidebar across all pages", async ({
      page,
    }) => {
      // Dashboard
      await navigateTo(page, "/");
      await waitForPageLoad(page);
      const dashboardSidebar = page.locator(".MuiDrawer-root").first();
      const dashboardBox = await dashboardSidebar.boundingBox();

      // Transactions
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);
      const transactionsSidebar = page.locator(".MuiDrawer-root").first();
      const transactionsBox = await transactionsSidebar.boundingBox();

      // Sidebar should have same width on both pages
      expect(dashboardBox!.width).toBe(transactionsBox!.width);
      expect(dashboardBox!.x).toBe(transactionsBox!.x);
    });

    test("should have consistent main content positioning across pages", async ({
      page,
    }) => {
      // Dashboard
      await navigateTo(page, "/");
      await waitForPageLoad(page);
      const dashboardMain = page.locator("main");
      const dashboardBox = await dashboardMain.boundingBox();

      // Transactions
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);
      const transactionsMain = page.locator("main");
      const transactionsBox = await transactionsMain.boundingBox();

      // Main content should start at same x position on both pages
      expect(dashboardBox!.x).toBe(transactionsBox!.x);

      // Both should be after sidebar (240px)
      expect(dashboardBox!.x).toBeGreaterThanOrEqual(240);
      expect(transactionsBox!.x).toBeGreaterThanOrEqual(240);
    });

    test("should not have content overflow on any page", async ({ page }) => {
      const pages = ["/", "/transactions"];

      for (const pagePath of pages) {
        await navigateTo(page, pagePath);
        await waitForPageLoad(page);

        if (pagePath === "/transactions") {
          await waitForDataGrid(page);
        }

        // Check for horizontal overflow
        const mainContent = page.locator("main");
        const hasOverflow = await mainContent.evaluate((el) => {
          return el.scrollWidth > el.clientWidth;
        });

        expect(hasOverflow).toBe(false);
      }
    });
  });

  test.describe("Component Rendering", () => {
    test("should render DataGrid with all columns visible", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Get all column headers
      const headers = page.locator(".MuiDataGrid-columnHeader");
      const headerCount = await headers.count();

      // Should have 6 columns: Date, Description, Category, Type, Amount, Balance
      expect(headerCount).toBe(6);

      // Take screenshot of header row
      const headerRow = page.locator(".MuiDataGrid-columnHeaders");
      await expect(headerRow).toHaveScreenshot("datagrid-headers.png", {
        animations: "disabled",
      });
    });

    test("should render transaction type chips with correct colors", async ({
      page,
    }) => {
      await navigateTo(page, "/transactions");
      await waitForDataGrid(page);

      // Look for different chip types
      const incomeChips = page.locator(".MuiChip-colorSuccess");
      const expenseChips = page.locator(".MuiChip-colorError");
      const transferChips = page.locator(".MuiChip-colorDefault");

      const incomeCount = await incomeChips.count();
      const expenseCount = await expenseChips.count();
      const transferCount = await transferChips.count();

      // Should have at least one type of chip
      const totalChips = incomeCount + expenseCount + transferCount;
      expect(totalChips).toBeGreaterThan(0);

      // If we have transfers, verify they're not green or red
      if (transferCount > 0) {
        const firstTransfer = transferChips.first();
        const chipText = await firstTransfer
          .locator(".MuiChip-label")
          .textContent();
        expect(chipText).toBe("Transfer");
      }
    });
  });
});

test.describe("Projections Visual Regression", () => {
  test.beforeEach(async ({ page }) => {
    await navigateTo(page, "/projections");
  });

  test("should match projections page desktop layout", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await waitForPageLoad(page);

    // Take full page screenshot
    await expect(page).toHaveScreenshot("projections-desktop.png", {
      fullPage: true,
    });
  });

  test("should match projections page tablet layout", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await waitForPageLoad(page);

    // Take full page screenshot
    await expect(page).toHaveScreenshot("projections-tablet.png", {
      fullPage: true,
    });
  });

  test("should match cash flow forecast chart", async ({ page }) => {
    await waitForPageLoad(page);

    // Ensure Cash Flow Forecast tab is active
    const cashFlowTab = page.getByRole("tab", { name: "Cash Flow Forecast" });
    await cashFlowTab.click();
    await page.waitForTimeout(500);

    // Screenshot the chart
    const chart = page.locator(".recharts-wrapper").first();
    await expect(chart).toHaveScreenshot("cash-flow-forecast-chart.png");
  });

  test("should match income and expense charts", async ({ page }) => {
    await waitForPageLoad(page);

    // Switch to Income & Expenses tab
    await page.getByRole("tab", { name: "Income & Expenses" }).click();
    await page.waitForTimeout(500);

    // Screenshot both charts
    const mainContent = page.locator("main");
    await expect(mainContent).toHaveScreenshot("income-expense-charts.png");
  });

  test("should match scenario analysis cards", async ({ page }) => {
    await waitForPageLoad(page);

    // Switch to Scenario Analysis tab
    await page.getByRole("tab", { name: "Scenario Analysis" }).click();
    await page.waitForTimeout(500);

    // Screenshot scenario cards
    const mainContent = page.locator("main");
    await expect(mainContent).toHaveScreenshot("scenario-analysis-cards.png");
  });

  test("should match projection controls", async ({ page }) => {
    await waitForPageLoad(page);

    // Screenshot the controls section
    const controls = page.locator("text=Projection Settings").locator("..");
    await expect(controls).toHaveScreenshot("projection-controls.png");
  });

  test("should match summary cards", async ({ page }) => {
    await waitForPageLoad(page);

    // Screenshot the summary cards section
    const summaryCards = page
      .locator(".MuiCard-root")
      .filter({ hasText: "Projected Income" })
      .locator("../..");
    await expect(summaryCards).toHaveScreenshot("projection-summary-cards.png");
  });

  test("should match model information panel", async ({ page }) => {
    await waitForPageLoad(page);

    // Scroll to model information
    const modelInfo = page.getByRole("heading", { name: "Model Information" });
    await modelInfo.scrollIntoViewIfNeeded();

    // Screenshot the panel
    const panel = modelInfo.locator("..");
    await expect(panel).toHaveScreenshot("model-information-panel.png");
  });
});
