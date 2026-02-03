/**
 * Expense Breakdown Tool
 *
 * Provides detailed breakdown of expenses by category
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getExpenseBreakdownTool: Tool = {
  name: "get_expense_breakdown",
  description:
    "Get a breakdown of expenses organized by category. Shows how much was spent in each category, the number of transactions, and percentage of total spending.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description:
          "Start date for the analysis period (YYYY-MM-DD format). Defaults to beginning of current month.",
      },
      end_date: {
        type: "string",
        description:
          "End date for the analysis period (YYYY-MM-DD format). Defaults to today.",
      },
      limit: {
        type: "number",
        description: "Maximum number of categories to return. Defaults to 10.",
      },
    },
    required: [],
  },
};

export interface ExpenseBreakdownInput {
  start_date?: string;
  end_date?: string;
  limit?: number;
}

export interface CategoryExpense {
  category_id: number;
  category_name: string;
  total_amount: number;
  transaction_count: number;
  percentage: number;
  average_transaction: number;
}

export interface ExpenseBreakdownResult {
  period: {
    start_date: string;
    end_date: string;
  };
  total_expenses: number;
  categories: CategoryExpense[];
}

/**
 * Execute the expense breakdown tool
 */
export async function executeExpenseBreakdown(
  input: ExpenseBreakdownInput
): Promise<ExpenseBreakdownResult> {
  const params = new URLSearchParams();
  if (input.start_date) params.append("start_date", input.start_date);
  if (input.end_date) params.append("end_date", input.end_date);
  if (input.limit) params.append("limit", input.limit.toString());

  const url = `${SPEARMINT_API_URL}/api/analysis/expenses${
    params.toString() ? `?${params}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch expense breakdown: ${response.statusText}`);
  }

  return (await response.json()) as ExpenseBreakdownResult;
}
