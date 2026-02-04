/**
 * get_financial_health Tool (Auto-generated)
 *
 * Get financial health indicators and scores. Use this when the user asks about their financial health, wants a financial checkup, or asks how they're doing financially.
 * 
 * Usage hint: "How healthy are my finances?"
 *
 * API Endpoint: GET /api/analysis/health
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getFinancialHealthTool: Tool = {
  name: "get_financial_health",
  description: "Get financial health indicators and scores. Use this when the user asks about their financial health, wants a financial checkup, or asks how they're doing financially.",
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
      }
    },
    required: []
  }
};

export interface GetFinancialHealthInput {
  start_date?: string;
  end_date?: string;
}

/**
 * Execute the get_financial_health tool
 */
export async function executeGetFinancialHealth(
  input: GetFinancialHealthInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));

  const url = `${SPEARMINT_API_URL}/api/analysis/health${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_financial_health: ${response.statusText}`);
  }

  return await response.json();
}
