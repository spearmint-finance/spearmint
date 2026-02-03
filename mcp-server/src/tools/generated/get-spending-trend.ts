/**
 * get_spending_trend Tool (Auto-generated)
 *
 * Get spending trends over time for expenses. Use this when the user asks how their spending has changed, wants to see expense patterns, or track spending over multiple months.
 * 
 * Usage hint: "How has my spending changed over the last 3 months?"
 *
 * API Endpoint: GET /api/analysis/expenses/trends
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getSpendingTrendTool: Tool = {
  name: "get_spending_trend",
  description: "Get spending trends over time for expenses. Use this when the user asks how their spending has changed, wants to see expense patterns, or track spending over multiple months.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Start date for analysis"
      },
      end_date: {
        type: "string",
        description: "End date for analysis"
      },
      period: {
        type: "string",
        description: "Time period for grouping: 'monthly', 'weekly', 'daily', 'quarterly', or 'yearly'"
      }
    },
    required: []
  }
};

export interface GetSpendingTrendInput {
  start_date?: string;
  end_date?: string;
  period?: string;
}

/**
 * Execute the get_spending_trend tool
 */
export async function executeGetSpendingTrend(
  input: GetSpendingTrendInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));
  if (input.period !== undefined) params.append("period", String(input.period));

  const url = `${SPEARMINT_API_URL}/api/analysis/expenses/trends${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_spending_trend: ${response.statusText}`);
  }

  return await response.json();
}
