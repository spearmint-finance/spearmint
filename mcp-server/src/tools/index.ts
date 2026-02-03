/**
 * MCP Tool Registry
 *
 * Exports all available MCP tools for registration with the server
 */

export { getFinancialSummaryTool } from "./financial.js";
export { getExpenseBreakdownTool } from "./expenses.js";
export { searchTransactionsTool } from "./transactions.js";
export { getAccountBalancesTool } from "./accounts.js";
export { getCashflowTrendTool } from "./cashflow.js";

// Tool names for reference
export const TOOL_NAMES = {
  FINANCIAL_SUMMARY: "get_financial_summary",
  EXPENSE_BREAKDOWN: "get_expense_breakdown",
  SEARCH_TRANSACTIONS: "search_transactions",
  ACCOUNT_BALANCES: "get_account_balances",
  CASHFLOW_TREND: "get_cashflow_trend",
} as const;
