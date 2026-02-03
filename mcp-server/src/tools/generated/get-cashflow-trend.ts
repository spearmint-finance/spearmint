/**
 * get_cashflow_trend Tool (Auto-generated)
 *
 * Get cash flow trends over time showing income and expenses by period. Use this when the user asks about cash flow patterns, spending trends over time, or wants to see how their finances have changed month-to-month.
 * 
 * Usage hint: "Show me my cash flow trend for the last 6 months"
 *
 * API Endpoint: GET /api/analysis/cashflow/trends
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getCashflowTrendTool: Tool = {
  name: "get_cashflow_trend",
  description: "Get cash flow trends over time showing income and expenses by period. Use this when the user asks about cash flow patterns, spending trends over time, or wants to see how their finances have changed month-to-month.",
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

export interface GetCashflowTrendInput {
  start_date?: string;
  end_date?: string;
  period?: string;
}

/**
 * Execute the get_cashflow_trend tool
 */
export async function executeGetCashflowTrend(
  input: GetCashflowTrendInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));
  if (input.period !== undefined) params.append("period", String(input.period));

  const url = `${SPEARMINT_API_URL}/api/analysis/cashflow/trends${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_cashflow_trend: ${response.statusText}`);
  }

  return await response.json();
}
