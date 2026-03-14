import { test, expect } from "@playwright/test";

test.describe("Marketing Site — Core Pages", () => {
  test("homepage loads with hero, value props, features, and CTA", async ({
    page,
  }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/Spearmint/);

    // Hero section
    await expect(
      page.getByRole("heading", { name: /Business-Grade/i })
    ).toBeVisible();
    await expect(
      page.getByText("Personal Finance", { exact: true })
    ).toBeVisible();
    await expect(page.getByText(/Your personal CFO/i)).toBeVisible();
    await expect(
      page.getByRole("link", { name: /Get Started/i }).first()
    ).toBeVisible();

    // Value props table
    await expect(
      page.getByRole("heading", { name: /Not another expense tracker/i })
    ).toBeVisible();
    await expect(page.getByText("$15k kitchen renovation")).toBeVisible();
    await expect(
      page.getByText("Separated as Capital Investment")
    ).toBeVisible();

    // Features section
    await expect(
      page.getByRole("heading", { name: /Everything you need/i })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Smart Classification" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Statistical Forecasting" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Self-Hosted & Private" })
    ).toBeVisible();

    // CTA section
    await expect(
      page.getByRole("heading", { name: /Take control/i })
    ).toBeVisible();
  });

  test("features page loads", async ({ page }) => {
    await page.goto("/features");
    await expect(page).toHaveTitle(/Features/);
    await expect(
      page.getByRole("heading", { name: "Features", level: 1 })
    ).toBeVisible();
  });

  test("how-it-works page loads with all 4 steps", async ({ page }) => {
    await page.goto("/how-it-works");
    await expect(page).toHaveTitle(/How It Works/);
    await expect(
      page.getByRole("heading", { name: "Export your bank data" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Import & classify" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Analyze & forecast" })
    ).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Stay in control" })
    ).toBeVisible();
  });

  test("pricing page loads with free tier", async ({ page }) => {
    await page.goto("/pricing");
    await expect(page).toHaveTitle(/Pricing/);
    await expect(page.getByText("$0")).toBeVisible();
    await expect(page.getByText("forever")).toBeVisible();
    await expect(page.getByText("All features included")).toBeVisible();
  });
});

test.describe("Marketing Site — Agents Page", () => {
  test("agents page loads with all sections", async ({ page }) => {
    await page.goto("/agents");
    await expect(page).toHaveTitle(/Autonomous Financial Agents/);

    // Hero
    await expect(
      page.getByRole("heading", { name: /AI that watches/i })
    ).toBeVisible();
    await expect(
      page.getByText(/your finances for you/i).first()
    ).toBeVisible();
  });

  test("agents page — Why Agents section", async ({ page }) => {
    await page.goto("/agents");
    await expect(
      page.getByRole("heading", { name: /Why autonomous agents/i })
    ).toBeVisible();
    await expect(
      page.getByText(/You only check your spending when it's too late/i)
    ).toBeVisible();
    await expect(
      page.getByText(/Agents monitor continuously/i)
    ).toBeVisible();
  });

  test("agents page — Meet the Agents section with all 5 agents", async ({
    page,
  }) => {
    await page.goto("/agents");
    await expect(
      page.getByRole("heading", { name: /Meet the agents/i })
    ).toBeVisible();

    // All 5 agents present
    await expect(page.getByText("Minty").first()).toBeVisible();
    await expect(page.getByText("Budget Advisor").first()).toBeVisible();
    await expect(page.getByText("Subscription Auditor").first()).toBeVisible();
    await expect(page.getByText("Bill Negotiator").first()).toBeVisible();
    await expect(page.getByText("Tax Optimizer").first()).toBeVisible();

    // Agent descriptions
    await expect(
      page.getByText(/AI Financial Assistant/i).first()
    ).toBeVisible();
    await expect(
      page.getByText(/Autonomous Spending Analyst/i).first()
    ).toBeVisible();

    // Example content rendered
    await expect(
      page.getByText(/How much did I spend on dining/i)
    ).toBeVisible();
    await expect(
      page.getByText(/dining spending is up 40%/i)
    ).toBeVisible();
  });

  test("agents page — Hybrid Architecture section", async ({ page }) => {
    await page.goto("/agents");
    await expect(
      page.getByRole("heading", { name: /Hybrid architecture/i })
    ).toBeVisible();
    await expect(
      page.getByText("Deterministic Layer").first()
    ).toBeVisible();
    await expect(page.getByText("LLM Reasoning Layer").first()).toBeVisible();
    await expect(
      page.getByRole("heading", { name: /Why does this matter/i })
    ).toBeVisible();
  });

  test("agents page — A2A Protocol section", async ({ page }) => {
    await page.goto("/agents");
    await expect(
      page.getByRole("heading", { name: /Agent-to-Agent protocol/i })
    ).toBeVisible();

    // Flow diagram steps
    await expect(page.getByText("You ask Minty")).toBeVisible();
    await expect(page.getByText("Minty delegates")).toBeVisible();
    await expect(page.getByText("Advisor orchestrates")).toBeVisible();
    await expect(page.getByText("Results synthesized")).toBeVisible();
    await expect(page.getByText("You get answers")).toBeVisible();

    // Capability cards
    await expect(page.getByText("Proactive").first()).toBeVisible();
    await expect(page.getByText("Orchestrating").first()).toBeVisible();
    await expect(page.getByText("Extensible").first()).toBeVisible();
  });

  test("agents page — CTA section", async ({ page }) => {
    await page.goto("/agents");
    await expect(
      page.getByRole("heading", { name: /Stop checking. Start knowing/i })
    ).toBeVisible();
    await expect(
      page.getByRole("link", { name: /Get Started on GitHub/i })
    ).toBeVisible();
  });
});

test.describe("Navigation", () => {
  test("header nav links work including Agents", async ({ page }) => {
    await page.goto("/");

    // Agents link is in the nav
    const agentsLink = page.getByRole("link", { name: "Agents" }).first();
    await expect(agentsLink).toBeVisible();

    // Click through to agents page
    await agentsLink.click();
    await expect(page).toHaveURL(/\/agents/);
    await expect(
      page.getByRole("heading", { name: /AI that watches/i })
    ).toBeVisible();
  });

  test("mobile menu contains Agents link", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/");

    // Open mobile menu
    await page.getByRole("button", { name: /Open menu/i }).click();

    // Agents link visible in mobile menu
    const agentsLink = page.getByRole("link", { name: "Agents" }).first();
    await expect(agentsLink).toBeVisible();
  });
});
