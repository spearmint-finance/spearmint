/**
 * MCP Tool Registry
 *
 * Re-exports from generated tools for backward compatibility.
 * The generated tools are the source of truth.
 *
 * Run `npm run generate:tools` to regenerate after API changes.
 */

// Re-export everything from generated tools
export * from "./generated/index.js";

// Legacy exports for backward compatibility with hand-written tools
// These can be removed once all code migrates to generated tools
export { getFinancialSummaryTool } from "./financial.js";
export { getExpenseBreakdownTool } from "./expenses.js";
export { searchTransactionsTool } from "./transactions.js";
export { getAccountBalancesTool } from "./accounts.js";
export { getCashflowTrendTool } from "./cashflow.js";

// Legacy tool names (use GENERATED_TOOL_NAMES from generated/index.js instead)
export const TOOL_NAMES = {
  FINANCIAL_SUMMARY: "get_financial_summary",
  EXPENSE_BREAKDOWN: "get_expense_breakdown",
  SEARCH_TRANSACTIONS: "search_transactions",
  ACCOUNT_BALANCES: "get_account_balances",
  CASHFLOW_TREND: "get_cashflow_trend",
} as const;
