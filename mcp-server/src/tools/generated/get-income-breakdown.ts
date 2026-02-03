/**
 * get_income_breakdown Tool (Auto-generated)
 *
 * Get income broken down by source/category with amounts and percentages. Use this when the user asks about their income sources, where their money comes from, or wants to analyze their earnings.
 * 
 * Usage hint: "Where does my income come from?"
 *
 * API Endpoint: GET /api/analysis/income
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getIncomeBreakdownTool: Tool = {
  name: "get_income_breakdown",
  description: "Get income broken down by source/category with amounts and percentages. Use this when the user asks about their income sources, where their money comes from, or wants to analyze their earnings.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Start date for the income analysis (YYYY-MM-DD format). Defaults to beginning of current month."
      },
      end_date: {
        type: "string",
        description: "End date for the income analysis (YYYY-MM-DD format). Defaults to today."
      }
    },
    required: []
  }
};

export interface GetIncomeBreakdownInput {
  start_date?: string;
  end_date?: string;
}

/**
 * Execute the get_income_breakdown tool
 */
export async function executeGetIncomeBreakdown(
  input: GetIncomeBreakdownInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));

  const url = `${SPEARMINT_API_URL}/api/analysis/income${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_income_breakdown: ${response.statusText}`);
  }

  return await response.json();
}
