import { defineConfig, devices } from "@playwright/test";
import { BASE_URL } from "./tests/fixtures/env";

/**
 * Playwright configuration for Financial Analysis Tool E2E tests
 *
 * See https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: "./tests/playwright/tests",

  // Put all Playwright artifacts (screenshots, videos, traces, etc.) here:
  outputDir: "tests/playwright/test-results/artifacts",

  /* Run tests in files in parallel */
  fullyParallel: true,

  /* Fail the build on CI if you accidentally left test.only in the source code */
  forbidOnly: !!process.env.CI,

  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,

  /* Opt out of parallel tests on CI */
  workers: process.env.CI ? 1 : undefined,

  /* Reporter to use */
  reporter: [
    [
      "html",
      {
        outputFolder: "./tests/playwright/test-results/playwright-report",
        open: "never",
      },
    ],
    ["list"],
    ["json", { outputFile: "./tests/playwright/test-results/results.json" }],
  ],

  /* Shared settings for all the projects below */
  use: {
    /* Base URL to use in actions like `await page.goto('/')` */
    baseURL: BASE_URL,

    /* Disable cache to ensure fresh content */
    serviceWorkers: "block",

    /* Collect trace when retrying the failed test */
    trace: "on-first-retry",

    /* Screenshot on failure */
    screenshot: "only-on-failure",

    /* Video on failure */
    video: "retain-on-failure",

    /* Maximum time each action can take */
    actionTimeout: 10000,

    /* Navigation timeout */
    navigationTimeout: 30000,
  },

  /* Screenshot comparison settings for visual regression tests */
  expect: {
    toHaveScreenshot: {
      /* Maximum pixel difference threshold (0-1) */
      maxDiffPixelRatio: 0.02,

      /* Maximum number of pixels that can differ */
      maxDiffPixels: 100,

      /* Threshold for pixel color difference (0-1) */
      threshold: 0.2,

      /* Animation handling */
      animations: "disabled",

      /* Scale for retina displays */
      scale: "css",
    },
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },

    // Uncomment to test on other browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },

    /* Test against mobile viewports */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'Mobile Safari',
    //   use: { ...devices['iPhone 12'] },
    // },
  ],

  /* Run your local dev server before starting the tests 
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
    stdout: "ignore",
    stderr: "pipe",
  },*/
});
