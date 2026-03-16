/**
 * search-transactions Tool (Auto-generated)
 *
 * Search and filter transactions by various criteria. Use this when the user wants to find specific transactions, search by merchant name, filter by date range, or look up purchases.
 * 
 * Usage hint: "Find all Amazon transactions over $50"
 *
 * API Endpoint: GET /api/transactions
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const searchTransactionsTool: Tool = {
  name: "search-transactions",
  description: "Search and filter transactions by various criteria. Use this when the user wants to find specific transactions, search by merchant name, filter by date range, or look up purchases.",
  inputSchema: {
    type: "object",
    properties: {
      start_date: {
        type: "string",
        description: "Start date filter"
      },
      end_date: {
        type: "string",
        description: "End date filter"
      },
      transaction_type: {
        type: "string",
        description: "Filter by transaction type: 'Income' or 'Expense'"
      },
      category_id: {
        type: "number",
        description: "Filter by category ID"
      },
      is_transfer: {
        type: "boolean",
        description: "Filter by transfer status: true for transfers only, false to exclude transfers"
      },
      min_amount: {
        type: "number",
        description: "Minimum transaction amount to include in results"
      },
      max_amount: {
        type: "number",
        description: "Maximum transaction amount to include in results"
      },
      search_text: {
        type: "string",
        description: "Search in description, source, notes"
      },
      tag_ids: {
        type: "array",
        description: "Filter by tag IDs (transactions matching any of the given tags)"
      },
      include_capital_expenses: {
        type: "boolean",
        description: "Include non-operating expenses (capital, refunds, reimbursements, etc.) in results"
      },
      include_transfers: {
        type: "boolean",
        description: "Include transfers in results"
      },
      limit: {
        type: "number",
        description: "Maximum number of transactions to return (default: 20, max: 100)"
      }
    },
    required: []
  }
};

export interface SearchTransactionsInput {
  start_date?: string;
  end_date?: string;
  transaction_type?: string;
  category_id?: number;
  is_transfer?: boolean;
  min_amount?: number;
  max_amount?: number;
  search_text?: string;
  tag_ids?: string;
  include_capital_expenses?: boolean;
  include_transfers?: boolean;
  limit?: number;
}

/**
 * Execute the search-transactions tool
 */
export async function executeSearchTransactions(
  input: SearchTransactionsInput
): Promise<unknown> {
  const params = new URLSearchParams();
  if (input.start_date !== undefined) params.append("start_date", String(input.start_date));
  if (input.end_date !== undefined) params.append("end_date", String(input.end_date));
  if (input.transaction_type !== undefined) params.append("transaction_type", String(input.transaction_type));
  if (input.category_id !== undefined) params.append("category_id", String(input.category_id));
  if (input.is_transfer !== undefined) params.append("is_transfer", String(input.is_transfer));
  if (input.min_amount !== undefined) params.append("min_amount", String(input.min_amount));
  if (input.max_amount !== undefined) params.append("max_amount", String(input.max_amount));
  if (input.search_text !== undefined) params.append("search_text", String(input.search_text));
  if (input.tag_ids !== undefined) params.append("tag_ids", String(input.tag_ids));
  if (input.include_capital_expenses !== undefined) params.append("include_capital_expenses", String(input.include_capital_expenses));
  if (input.include_transfers !== undefined) params.append("include_transfers", String(input.include_transfers));
  if (input.limit !== undefined) params.append("limit", String(input.limit));

  const url = `${SPEARMINT_API_URL}/api/transactions${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute search-transactions: ${response.statusText}`);
  }

  return await response.json();
}
