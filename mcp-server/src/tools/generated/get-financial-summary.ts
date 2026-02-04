/**
 * get_financial_summary Tool (Auto-generated)
 *
 * Get a comprehensive financial summary including total income, total expenses, net cash flow, and key financial metrics. Use this when the user asks about their overall financial health, monthly overview, or wants to know how much they earned/spent.
 * 
 * Usage hint: "What's my financial summary for this month?"
 *
 * API Endpoint: GET /api/analysis/summary
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getFinancialSummaryTool: Tool = {
  name: "get_financial_summary",
  description: "Get a comprehensive financial summary including total income, total expenses, net cash flow, and key financial metrics. Use this when the user asks about their overall financial health, monthly overview, or wants to know how much they earned/spent.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Start date for the summary period (YYYY-MM-DD format). Defaults to beginning of current month."
      },
      end_date: {
        type: "string",
        description: "End date for the summary period (YYYY-MM-DD format). Defaults to today."
      }
    },
    required: []
  }
};

export interface GetFinancialSummaryInput {
  start_date?: string;
  end_date?: string;
}

/**
 * Execute the get_financial_summary tool
 */
export async function executeGetFinancialSummary(
  input: GetFinancialSummaryInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));

  const url = `${SPEARMINT_API_URL}/api/analysis/summary${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_financial_summary: ${response.statusText}`);
  }

  return await response.json();
}
