/**
 * Search Transactions Tool
 *
 * Allows searching and filtering transactions with various criteria
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const searchTransactionsTool: Tool = {
  name: "search_transactions",
  description:
    "Search and filter transactions by date range, amount, category, description, or transaction type. Returns matching transactions with full details.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Filter transactions on or after this date (YYYY-MM-DD format).",
      },
      end_date: {
        type: "string",
        description: "Filter transactions on or before this date (YYYY-MM-DD format).",
      },
      transaction_type: {
        type: "string",
        enum: ["Income", "Expense"],
        description: "Filter by transaction type.",
      },
      category_id: {
        type: "number",
        description: "Filter by category ID.",
      },
      search: {
        type: "string",
        description:
          "Search term to match against transaction description or source.",
      },
      min_amount: {
        type: "number",
        description: "Minimum transaction amount.",
      },
      max_amount: {
        type: "number",
        description: "Maximum transaction amount.",
      },
      limit: {
        type: "number",
        description: "Maximum number of transactions to return. Defaults to 50.",
      },
      offset: {
        type: "number",
        description: "Number of transactions to skip for pagination. Defaults to 0.",
      },
    },
    required: [],
  },
};

export interface SearchTransactionsInput {
  start_date?: string;
  end_date?: string;
  transaction_type?: "Income" | "Expense";
  category_id?: number;
  search?: string;
  min_amount?: number;
  max_amount?: number;
  limit?: number;
  offset?: number;
}

export interface Transaction {
  transaction_id: number;
  transaction_date: string;
  amount: number;
  transaction_type: string;
  category_id: number;
  category_name?: string;
  source?: string;
  description?: string;
  payment_method?: string;
  is_transfer: boolean;
  notes?: string;
}

export interface SearchTransactionsResult {
  transactions: Transaction[];
  total: number;
  limit: number;
  offset: number;
}

/**
 * Execute the search transactions tool
 */
export async function executeSearchTransactions(
  input: SearchTransactionsInput
): Promise<SearchTransactionsResult> {
  const params = new URLSearchParams();
  if (input.start_date) params.append("start_date", input.start_date);
  if (input.end_date) params.append("end_date", input.end_date);
  if (input.transaction_type) params.append("transaction_type", input.transaction_type);
  if (input.category_id) params.append("category_id", input.category_id.toString());
  if (input.search) params.append("search", input.search);
  if (input.min_amount) params.append("min_amount", input.min_amount.toString());
  if (input.max_amount) params.append("max_amount", input.max_amount.toString());
  if (input.limit) params.append("limit", input.limit.toString());
  if (input.offset) params.append("offset", input.offset.toString());

  const url = `${SPEARMINT_API_URL}/api/transactions${
    params.toString() ? `?${params}` : ""
  }`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to search transactions: ${response.statusText}`);
  }

  return (await response.json()) as SearchTransactionsResult;
}
