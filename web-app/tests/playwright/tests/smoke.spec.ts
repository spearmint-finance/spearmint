import { test, expect } from "@playwright/test";

test("smoke test", async ({ page }) => {
  console.log("Navigating to app root...");
  try {
    await page.goto("/", { timeout: 10000 });

    // Take a screenshot of the initial state
    await page.screenshot({ path: "smoke-test-initial.png" });

    // Check if we are on the dashboard or login page
    const title = await page.title();
    console.log(`Page Title: ${title}`);

    // Check for common error text (Vite error overlay)
    const errorOverlay = await page.locator("vite-error-overlay").count();
    if (errorOverlay > 0) {
      console.error("Vite Error Overlay detected!");
    }
  } catch (e) {
    console.error("Navigation failed:", e);
    await page.screenshot({ path: "smoke-test-error.png" });
    throw e;
  }
});
