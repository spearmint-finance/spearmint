import { test, expect } from "@playwright/test";

test.describe("Dashboard Debug", () => {
  test("should capture console and network activity", async ({ page }) => {
    const consoleMessages: string[] = [];
    const networkRequests: { url: string; status: number | null }[] = [];
    const networkErrors: string[] = [];

    // Capture console messages (especially errors and warnings)
    page.on("console", (msg) => {
      const type = msg.type();
      const text = msg.text();
      consoleMessages.push(`[${type}] ${text}`);

      // Also log errors immediately for visibility
      if (type === "error" || type === "warning") {
        console.log(`BROWSER ${type.toUpperCase()}: ${text}`);
      }
    });

    // Capture network requests
    page.on("request", (request) => {
      if (request.url().includes("/api/")) {
        networkRequests.push({ url: request.url(), status: null });
      }
    });

    page.on("response", async (response) => {
      if (response.url().includes("/api/")) {
        const req = networkRequests.find((r) => r.url === response.url());
        if (req) {
          req.status = response.status();
        }

        // Log response details for debugging
        console.log(
          `API Response: ${response.url()} - Status: ${response.status()}`
        );

        if (response.status() >= 400) {
          try {
            const body = await response.text();
            networkErrors.push(
              `${response.url()} - ${response.status()}: ${body}`
            );
          } catch (e) {
            networkErrors.push(
              `${response.url()} - ${response.status()}: Could not read body`
            );
          }
        }
      }
    });

    page.on("requestfailed", (request) => {
      if (request.url().includes("/api/")) {
        networkErrors.push(
          `Request failed: ${request.url()} - ${request.failure()?.errorText}`
        );
      }
    });

    // Navigate to dashboard with cache bypass
    console.log("Navigating to http://localhost:8080/ (bypassing cache)");
    await page.goto("http://localhost:8080/", {
      waitUntil: "domcontentloaded",
    });

    // Force a hard reload to bypass cache
    await page.reload({ waitUntil: "domcontentloaded" });

    // Check window.location.origin
    const origin = await page.evaluate(() => window.location.origin);
    console.log(`\n=== WINDOW ORIGIN === ${origin}`);

    // Wait a bit to see what happens
    await page.waitForTimeout(5000);

    // Log all captured information
    console.log("\n=== CONSOLE MESSAGES ===");
    consoleMessages.forEach((msg) => console.log(msg));

    console.log("\n=== NETWORK REQUESTS ===");
    networkRequests.forEach((req) =>
      console.log(`${req.url} - Status: ${req.status}`)
    );

    console.log("\n=== NETWORK ERRORS ===");
    networkErrors.forEach((err) => console.log(err));

    // Take a screenshot
    await page.screenshot({
      path: "tests/playwright/test-results/debug-dashboard.png",
      fullPage: true,
    });

    // Check page content
    const bodyText = await page.locator("body").textContent();
    console.log("\n=== PAGE CONTENT (first 500 chars) ===");
    console.log(bodyText?.substring(0, 500));

    // Fail the test with diagnostic info
    expect(networkErrors.length).toBe(0);
  });
});
