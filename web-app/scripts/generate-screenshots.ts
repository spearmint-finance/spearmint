/**
 * Generate product screenshots for the marketing site.
 * Uses Playwright to mock API responses and capture populated pages.
 *
 * Usage: npx playwright test scripts/generate-screenshots.ts
 */
import { test } from "@playwright/test";

const OUTPUT_DIR = "../marketing-site/public/screenshots";

// --------------- Mock Data ---------------

const mockCategories = [
  { id: 1, name: "Salary", parent_id: null, is_active: true },
  { id: 2, name: "Freelance", parent_id: null, is_active: true },
  { id: 3, name: "Dining", parent_id: null, is_active: true },
  { id: 4, name: "Groceries", parent_id: null, is_active: true },
  { id: 5, name: "Rent", parent_id: null, is_active: true },
  { id: 6, name: "Utilities", parent_id: null, is_active: true },
  { id: 7, name: "Transportation", parent_id: null, is_active: true },
  { id: 8, name: "Entertainment", parent_id: null, is_active: true },
  { id: 9, name: "Healthcare", parent_id: null, is_active: true },
  { id: 10, name: "Shopping", parent_id: null, is_active: true },
  { id: 11, name: "Investment Income", parent_id: null, is_active: true },
  { id: 12, name: "Insurance", parent_id: null, is_active: true },
];

const mockClassifications = [
  { classification_id: 1, classification_name: "Operating Expense", classification_code: "OPEX", description: "Day-to-day expenses", exclude_from_income_calc: false, exclude_from_expense_calc: false, exclude_from_cashflow_calc: false, is_system_classification: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { classification_id: 2, classification_name: "Capital Investment", classification_code: "CAPEX", description: "Capital expenditure", exclude_from_income_calc: false, exclude_from_expense_calc: true, exclude_from_cashflow_calc: false, is_system_classification: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { classification_id: 3, classification_name: "Income", classification_code: "INC", description: "Income", exclude_from_income_calc: false, exclude_from_expense_calc: true, exclude_from_cashflow_calc: false, is_system_classification: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
  { classification_id: 4, classification_name: "Transfer", classification_code: "XFER", description: "Transfer between accounts", exclude_from_income_calc: true, exclude_from_expense_calc: true, exclude_from_cashflow_calc: true, is_system_classification: true, created_at: "2025-01-01", updated_at: "2025-01-01" },
];

const mockAccounts = [
  { account_id: 1, account_name: "Chase Checking", account_type: "checking", institution_name: "Chase", currency: "USD", is_active: true, has_cash_component: true, has_investment_component: false, opening_balance: 5000, current_balance: 12847.32, current_balance_date: "2026-03-14" },
  { account_id: 2, account_name: "Ally Savings", account_type: "savings", institution_name: "Ally Bank", currency: "USD", is_active: true, has_cash_component: true, has_investment_component: false, opening_balance: 20000, current_balance: 34250.00, current_balance_date: "2026-03-14" },
  { account_id: 3, account_name: "Fidelity Brokerage", account_type: "brokerage", institution_name: "Fidelity", currency: "USD", is_active: true, has_cash_component: true, has_investment_component: true, opening_balance: 50000, current_balance: 187432.15, current_balance_date: "2026-03-14", cash_balance: 8432.15, investment_value: 179000.00 },
  { account_id: 4, account_name: "Amex Platinum", account_type: "credit_card", institution_name: "American Express", currency: "USD", is_active: true, has_cash_component: true, has_investment_component: false, opening_balance: 0, current_balance: -2341.87, current_balance_date: "2026-03-14" },
  { account_id: 5, account_name: "Vanguard 401k", account_type: "401k", institution_name: "Vanguard", currency: "USD", is_active: true, has_cash_component: false, has_investment_component: true, opening_balance: 85000, current_balance: 142890.50, current_balance_date: "2026-03-14", investment_value: 142890.50 },
];

const mockNetWorth = {
  assets: 377419.97,
  liabilities: 2341.87,
  investments: 321890.50,
  net_worth: 375078.10,
  netWorth: 375078.10,
  liquid_assets: 47097.32,
  liquidAssets: 47097.32,
  as_of_date: "2026-03-14",
  asOfDate: "2026-03-14",
  account_breakdown: {
    "Chase Checking": 12847.32,
    "Ally Savings": 34250.00,
    "Fidelity Brokerage": 187432.15,
    "Amex Platinum": -2341.87,
    "Vanguard 401k": 142890.50,
  },
};

function generateTransactions() {
  const txns = [];
  const descriptions: [string, number, string, string][] = [
    ["Payroll - Acme Corp", 8450.00, "Income", "Salary"],
    ["Freelance — Logo Design", 1200.00, "Income", "Freelance"],
    ["Whole Foods Market", -127.43, "Expense", "Groceries"],
    ["Chipotle Mexican Grill", -14.85, "Expense", "Dining"],
    ["Monthly Rent — Apt 4B", -2200.00, "Expense", "Rent"],
    ["Con Edison Electric", -142.30, "Expense", "Utilities"],
    ["MTA MetroCard", -33.00, "Expense", "Transportation"],
    ["Netflix Subscription", -15.99, "Expense", "Entertainment"],
    ["Blue Cross Blue Shield", -385.00, "Expense", "Healthcare"],
    ["Amazon.com", -67.42, "Expense", "Shopping"],
    ["Dividend — VTI", 245.80, "Income", "Investment Income"],
    ["Trader Joe's", -89.12, "Expense", "Groceries"],
    ["Uber Ride", -24.50, "Expense", "Transportation"],
    ["State Farm Insurance", -165.00, "Expense", "Insurance"],
    ["Target", -53.28, "Expense", "Shopping"],
    ["Starbucks", -6.75, "Expense", "Dining"],
    ["Gym Membership", -49.99, "Expense", "Healthcare"],
    ["AT&T Wireless", -85.00, "Expense", "Utilities"],
    ["Interest — Ally Savings", 42.15, "Income", "Investment Income"],
    ["Costco Wholesale", -234.67, "Expense", "Groceries"],
    ["Payroll - Acme Corp", 8450.00, "Income", "Salary"],
    ["Restaurant — Nobu", -186.00, "Expense", "Dining"],
    ["Spotify Premium", -10.99, "Expense", "Entertainment"],
    ["Lyft Ride", -18.75, "Expense", "Transportation"],
    ["CVS Pharmacy", -32.40, "Expense", "Healthcare"],
  ];

  let balance = 12847.32;
  for (let i = 0; i < descriptions.length; i++) {
    const [desc, amount, type, cat] = descriptions[i];
    const day = Math.max(1, 14 - Math.floor(i / 2));
    balance -= amount;
    txns.push({
      id: i + 1,
      date: `2026-03-${String(day).padStart(2, "0")}`,
      description: desc,
      amount: Math.abs(amount),
      transaction_type: type,
      category_name: cat,
      classification_name: type === "Income" ? "Income" : "Operating Expense",
      balance: Math.round(balance * 100) / 100,
      source: "Chase Bank",
    });
  }
  return txns;
}

const mockTransactions = generateTransactions();

const mockFinancialSummary = {
  total_income: 18387.95,
  total_expenses: 4182.44,
  net_cash_flow: 14205.51,
  income_count: 5,
  expense_count: 20,
  top_income_categories: [
    { category: "Salary", amount: 16900.00, count: 2, percentage: 91.9 },
    { category: "Freelance", amount: 1200.00, count: 1, percentage: 6.5 },
    { category: "Investment Income", amount: 287.95, count: 2, percentage: 1.6 },
  ],
  top_expense_categories: [
    { category: "Rent", amount: 2200.00, count: 1, percentage: 52.6 },
    { category: "Groceries", amount: 451.22, count: 3, percentage: 10.8 },
    { category: "Healthcare", amount: 467.39, count: 3, percentage: 11.2 },
    { category: "Utilities", amount: 227.30, count: 2, percentage: 5.4 },
    { category: "Dining", amount: 207.60, count: 3, percentage: 5.0 },
  ],
  recent_transactions: mockTransactions.slice(0, 5).map((t) => ({
    transaction_id: t.id,
    transaction_date: t.date,
    description: t.description,
    amount: t.amount,
    transaction_type: t.transaction_type,
    category: t.category_name,
  })),
  financial_health: {
    income_to_expense_ratio: 4.4,
    savings_rate: 77.3,
    average_daily_income: 612.93,
    average_daily_expense: 139.41,
    net_daily_cash_flow: 473.52,
    period_start: "2026-03-01",
    period_end: "2026-03-31",
  },
  period_start: "2026-03-01",
  period_end: "2026-03-31",
  mode: "analysis",
};

const mockCashFlowTrends = {
  trends: [
    { period: "2025-10", income: 9850, expenses: 4320, net_cash_flow: 5530, income_count: 3, expense_count: 18 },
    { period: "2025-11", income: 10200, expenses: 4580, net_cash_flow: 5620, income_count: 4, expense_count: 21 },
    { period: "2025-12", income: 11400, expenses: 5100, net_cash_flow: 6300, income_count: 4, expense_count: 24 },
    { period: "2026-01", income: 9650, expenses: 4150, net_cash_flow: 5500, income_count: 3, expense_count: 19 },
    { period: "2026-02", income: 10800, expenses: 4380, net_cash_flow: 6420, income_count: 4, expense_count: 20 },
    { period: "2026-03", income: 18388, expenses: 4182, net_cash_flow: 14206, income_count: 5, expense_count: 20 },
  ],
  period_type: "monthly",
  mode: "analysis",
};

function generateProjections(type: "income" | "expenses" | "cashflow") {
  const days: { date: string; projected_value?: number; projected_income?: number; projected_expenses?: number; projected_cashflow?: number; lower_bound?: number; upper_bound?: number; cashflow_lower?: number; cashflow_upper?: number }[] = [];
  const baseIncome = 340;
  const baseExpense = 145;

  for (let i = 0; i < 90; i++) {
    const d = new Date(2026, 2, 15 + i);
    const dateStr = d.toISOString().split("T")[0];
    const noise = Math.sin(i * 0.3) * 20 + Math.random() * 10;

    if (type === "cashflow") {
      const inc = baseIncome + noise;
      const exp = baseExpense + noise * 0.5;
      days.push({
        date: dateStr,
        projected_income: Math.round(inc * 100) / 100,
        projected_expenses: Math.round(exp * 100) / 100,
        projected_cashflow: Math.round((inc - exp) * 100) / 100,
        cashflow_lower: Math.round((inc - exp - 80) * 100) / 100,
        cashflow_upper: Math.round((inc - exp + 80) * 100) / 100,
      });
    } else {
      const base = type === "income" ? baseIncome : baseExpense;
      const val = base + noise;
      days.push({
        date: dateStr,
        projected_value: Math.round(val * 100) / 100,
        lower_bound: Math.round((val - 60) * 100) / 100,
        upper_bound: Math.round((val + 60) * 100) / 100,
      });
    }
  }

  const base = {
    historical_period: { start_date: "2025-09-15", end_date: "2026-03-14", days: 181 },
    projection_period: { start_date: "2026-03-15", end_date: "2026-06-13", days: 90 },
    method: "linear_regression",
    confidence_level: 0.95,
    model_metrics: { r_squared: 0.87, mae: 42.5, rmse: 58.3, mape: 8.2 },
  };

  if (type === "cashflow") {
    return {
      ...base,
      projection_type: "cashflow",
      projected_income: 30600,
      projected_expenses: 13050,
      projected_cashflow: 17550,
      confidence_interval: { lower: 15200, upper: 19900, range: 4700 },
      daily_projections: days,
      scenarios: {
        expected: { income: 30600, expenses: 13050, cashflow: 17550, description: "Based on current trends" },
        best_case: { income: 34200, expenses: 11500, cashflow: 22700, description: "Income up 12%, expenses down 12%" },
        worst_case: { income: 27000, expenses: 15200, cashflow: 11800, description: "Income down 12%, expenses up 16%" },
        range: { min_cashflow: 11800, max_cashflow: 22700, range: 10900 },
      },
    };
  }

  return {
    ...base,
    projection_type: type,
    projected_total: type === "income" ? 30600 : 13050,
    confidence_interval: type === "income" ? { lower: 28200, upper: 33000, range: 4800 } : { lower: 11500, upper: 14600, range: 3100 },
    daily_projections: days,
  };
}

// --------------- Route Handler ---------------

async function setupMocks(page: import("@playwright/test").Page) {
  // Categories
  await page.route("**/api/categories*", (route) =>
    route.fulfill({ json: mockCategories })
  );

  // Classifications
  await page.route("**/api/classifications*", (route) =>
    route.fulfill({ json: mockClassifications })
  );

  // Accounts
  await page.route("**/api/accounts/net-worth*", (route) =>
    route.fulfill({ json: mockNetWorth })
  );
  await page.route("**/api/accounts/summary*", (route) =>
    route.fulfill({ json: mockAccounts })
  );
  await page.route("**/api/accounts*", (route) => {
    if (route.request().url().includes("/summary") || route.request().url().includes("/net-worth")) return;
    route.fulfill({ json: mockAccounts });
  });

  // Transactions
  await page.route("**/api/transactions*", (route) =>
    route.fulfill({
      json: {
        transactions: mockTransactions,
        total: mockTransactions.length,
        limit: 25,
        offset: 0,
        summary: {
          total_income: 18387.95,
          total_expenses: 4182.44,
          net_income: 14205.51,
          transaction_count: mockTransactions.length,
        },
      },
    })
  );

  // Analysis
  await page.route("**/api/analysis/summary*", (route) =>
    route.fulfill({ json: mockFinancialSummary })
  );
  await page.route("**/api/analysis/cashflow/trends*", (route) =>
    route.fulfill({ json: mockCashFlowTrends })
  );
  await page.route("**/api/analysis/health*", (route) =>
    route.fulfill({ json: mockFinancialSummary.financial_health })
  );
  await page.route("**/api/analysis/cashflow*", (route) => {
    if (route.request().url().includes("/trends")) return;
    route.fulfill({
      json: {
        total_income: 18387.95,
        total_expenses: 4182.44,
        net_cash_flow: 14205.51,
        period_start: "2026-03-01",
        period_end: "2026-03-31",
      },
    });
  });
  await page.route("**/api/analysis/income*", (route) =>
    route.fulfill({
      json: {
        total_income: 18387.95,
        categories: mockFinancialSummary.top_income_categories,
        period_start: "2026-03-01",
        period_end: "2026-03-31",
      },
    })
  );
  await page.route("**/api/analysis/expenses*", (route) => {
    if (route.request().url().includes("/category-trends")) {
      route.fulfill({ json: { trends: [], period_type: "monthly" } });
      return;
    }
    route.fulfill({
      json: {
        total_expenses: 4182.44,
        categories: mockFinancialSummary.top_expense_categories,
        period_start: "2026-03-01",
        period_end: "2026-03-31",
      },
    });
  });

  // Projections
  await page.route("**/api/projections/income*", (route) =>
    route.fulfill({ json: generateProjections("income") })
  );
  await page.route("**/api/projections/expenses*", (route) =>
    route.fulfill({ json: generateProjections("expenses") })
  );
  await page.route("**/api/projections/cashflow*", (route) =>
    route.fulfill({ json: generateProjections("cashflow") })
  );

  // Catch-all for any other API calls
  await page.route("**/api/**", (route) => {
    console.log(`[mock] Unhandled API: ${route.request().url()}`);
    route.fulfill({ json: {} });
  });
}

// --------------- Screenshots ---------------

test.describe("Product Screenshots", () => {
  test.use({ viewport: { width: 1440, height: 900 } });

  test("capture all product pages", async ({ page }) => {
    await setupMocks(page);

    // Dashboard
    await page.goto("/dashboard");
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: `${OUTPUT_DIR}/dashboard.png`,
      fullPage: false,
    });

    // Transactions
    await page.goto("/transactions");
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: `${OUTPUT_DIR}/transactions.png`,
      fullPage: false,
    });

    // Analysis
    await page.goto("/analysis");
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: `${OUTPUT_DIR}/analysis.png`,
      fullPage: false,
    });

    // Projections
    await page.goto("/projections");
    await page.waitForTimeout(2000);
    await page.screenshot({
      path: `${OUTPUT_DIR}/projections.png`,
      fullPage: false,
    });

    // Accounts
    await page.goto("/accounts");
    await page.waitForTimeout(1500);
    await page.screenshot({
      path: `${OUTPUT_DIR}/accounts.png`,
      fullPage: false,
    });
  });
});
