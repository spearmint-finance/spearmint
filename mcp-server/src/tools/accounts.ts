/**
 * Account Balances Tool
 *
 * Provides current balances and summaries for all financial accounts
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL =
  process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const getAccountBalancesTool: Tool = {
  name: "get_account_balances",
  description:
    "Get current balances for all financial accounts including checking, savings, credit cards, and investment accounts. Shows account names, types, and current balance amounts.",
  inputSchema: {
    type: "object",
    properties: {
      account_type: {
        type: "string",
        enum: [
          "checking",
          "savings",
          "brokerage",
          "investment",
          "credit_card",
          "loan",
          "401k",
          "ira",
          "other",
        ],
        description: "Filter by account type.",
      },
      active_only: {
        type: "boolean",
        description: "Only return active accounts. Defaults to true.",
      },
    },
    required: [],
  },
};

export interface GetAccountBalancesInput {
  account_type?: string;
  active_only?: boolean;
}

export interface AccountSummary {
  account_id: number;
  account_name: string;
  account_type: string;
  institution?: string;
  current_balance: number;
  balance_date?: string;
  has_cash: boolean;
  has_investments: boolean;
  cash_balance?: number;
  investment_value?: number;
}

export interface AccountBalancesResult {
  accounts: AccountSummary[];
  total_assets: number;
  total_liabilities: number;
  net_worth: number;
}

/**
 * Execute the account balances tool
 */
export async function executeGetAccountBalances(
  input: GetAccountBalancesInput
): Promise<AccountBalancesResult> {
  // Get account summary
  const summaryResponse = await fetch(
    `${SPEARMINT_API_URL}/api/accounts/summary`
  );

  if (!summaryResponse.ok) {
    throw new Error(`Failed to fetch account summary: ${summaryResponse.statusText}`);
  }

  const accounts = (await summaryResponse.json()) as AccountSummary[];

  // Filter by account type if specified
  let filteredAccounts = accounts;
  if (input.account_type) {
    filteredAccounts = accounts.filter(
      (a) => a.account_type === input.account_type
    );
  }

  // Calculate totals
  const assetTypes = ["checking", "savings", "brokerage", "investment", "401k", "ira"];
  const liabilityTypes = ["credit_card", "loan"];

  let totalAssets = 0;
  let totalLiabilities = 0;

  for (const account of filteredAccounts) {
    if (assetTypes.includes(account.account_type)) {
      totalAssets += account.current_balance;
    } else if (liabilityTypes.includes(account.account_type)) {
      totalLiabilities += Math.abs(account.current_balance);
    }
  }

  return {
    accounts: filteredAccounts,
    total_assets: totalAssets,
    total_liabilities: totalLiabilities,
    net_worth: totalAssets - totalLiabilities,
  };
}
