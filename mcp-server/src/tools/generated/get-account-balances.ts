/**
 * get_account_balances Tool (Auto-generated)
 *
 * Get current balances for all financial accounts including total assets, liabilities, and net worth. Use this when the user asks about their account balances, net worth, or wants to see all their accounts.
 * 
 * Usage hint: "What are my current account balances?"
 *
 * API Endpoint: GET /api/accounts/summary
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getAccountBalancesTool: Tool = {
  name: "get_account_balances",
  description: "Get current balances for all financial accounts including total assets, liabilities, and net worth. Use this when the user asks about their account balances, net worth, or wants to see all their accounts.",
  inputSchema: {
    type: "object",
    properties: {

    },
    required: []
  }
};

export interface GetAccountBalancesInput {
  // No parameters
}

/**
 * Execute the get_account_balances tool
 */
export async function executeGetAccountBalances(
  input: GetAccountBalancesInput
): Promise<unknown> {
  const params = new URLSearchParams();


  const url = `${SPEARMINT_API_URL}/api/accounts/summary${params.toString() ? `?${params}` : ""}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to execute get_account_balances: ${response.statusText}`);
  }

  return await response.json();
}
