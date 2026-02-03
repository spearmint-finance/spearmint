/**
 * Financial Summary Tool
 *
 * Provides an overview of financial health including income, expenses, and net cash flow
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getFinancialSummaryTool: Tool = {
  name: "get_financial_summary",
  description:
    "Get a comprehensive financial summary including total income, total expenses, net cash flow, and key financial metrics. Use this to understand overall financial health.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description:
          "Start date for the summary period (YYYY-MM-DD format). Defaults to beginning of current month.",
      },
      end_date: {
        type: "string",
        description:
          "End date for the summary period (YYYY-MM-DD format). Defaults to today.",
      },
    },
    required: [],
  },
};

export interface FinancialSummaryInput {
  start_date?: string;
  end_date?: string;
}

export interface FinancialSummaryResult {
  period: {
    start_date: string;
    end_date: string;
  };
  income: {
    total: number;
    transaction_count: number;
  };
  expenses: {
    total: number;
    transaction_count: number;
  };
  net_cash_flow: number;
  savings_rate: number;
}

/**
 * Execute the financial summary tool
 */
export async function executeFinancialSummary(
  input: FinancialSummaryInput
): Promise<FinancialSummaryResult> {
  const params = new URLSearchParams();
  if (input.start_date) params.append("start_date", input.start_date);
  if (input.end_date) params.append("end_date", input.end_date);

  const url = `${SPEARMINT_API_URL}/api/analysis/summary${
    params.toString() ? `?${params}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch financial summary: ${response.statusText}`);
  }

  return (await response.json()) as FinancialSummaryResult;
}
