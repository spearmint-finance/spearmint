/**
 * get_expense_breakdown Tool (Auto-generated)
 *
 * Get expenses broken down by category with amounts and percentages. Use this when the user asks where their money is going, wants to see spending by category, or asks about specific expense categories.
 * 
 * Usage hint: "Show me my expense breakdown by category"
 *
 * API Endpoint: GET /api/analysis/category-breakdown
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getExpenseBreakdownTool: Tool = {
  name: "get_expense_breakdown",
  description: "Get expenses broken down by category with amounts and percentages. Use this when the user asks where their money is going, wants to see spending by category, or asks about specific expense categories.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Start date for the breakdown period (YYYY-MM-DD format). Defaults to beginning of current month."
      },
      end_date: {
        type: "string",
        description: "End date for the breakdown period (YYYY-MM-DD format). Defaults to today."
      }
    },
    required: []
  }
};

export interface GetExpenseBreakdownInput {
  start_date?: string;
  end_date?: string;
}

/**
 * Execute the get_expense_breakdown tool
 */
export async function executeGetExpenseBreakdown(
  input: GetExpenseBreakdownInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));

  const url = `${SPEARMINT_API_URL}/api/analysis/category-breakdown${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_expense_breakdown: ${response.statusText}`);
  }

  return await response.json();
}
