/**
 * Cash Flow Trend Tool
 *
 * Provides cash flow trends over time periods
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getCashflowTrendTool: Tool = {
  name: "get_cashflow_trend",
  description:
    "Get cash flow trends over time, showing income, expenses, and net cash flow for each period. Useful for understanding spending patterns and financial trajectory.",
  inputSchema: {
    type: "object",
    properties: {
      period: {
        type: "string",
        enum: ["daily", "weekly", "monthly", "quarterly", "yearly"],
        description: "Time period granularity for the trend data. Defaults to monthly.",
      },
      start_date: {
        type: "string",
        description:
          "Start date for the trend period (YYYY-MM-DD format). Defaults to 6 months ago.",
      },
      end_date: {
        type: "string",
        description:
          "End date for the trend period (YYYY-MM-DD format). Defaults to today.",
      },
    },
    required: [],
  },
};

export interface GetCashflowTrendInput {
  period?: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  start_date?: string;
  end_date?: string;
}

export interface CashflowPeriod {
  period_start: string;
  period_end: string;
  period_label: string;
  income: number;
  expenses: number;
  net_cash_flow: number;
  income_count: number;
  expense_count: number;
}

export interface CashflowTrendResult {
  period_type: string;
  date_range: {
    start: string;
    end: string;
  };
  periods: CashflowPeriod[];
  totals: {
    income: number;
    expenses: number;
    net_cash_flow: number;
  };
  averages: {
    income: number;
    expenses: number;
    net_cash_flow: number;
  };
}

/**
 * Execute the cash flow trend tool
 */
export async function executeGetCashflowTrend(
  input: GetCashflowTrendInput
): Promise<CashflowTrendResult> {
  const period = input.period || "monthly";
  const params = new URLSearchParams();
  if (input.start_date) params.append("start_date", input.start_date);
  if (input.end_date) params.append("end_date", input.end_date);

  const url = `${SPEARMINT_API_URL}/api/analysis/trends/${period}${
    params.toString() ? `?${params}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to fetch cash flow trends: ${response.statusText}`);
  }

  return (await response.json()) as CashflowTrendResult;
}
