/**
 * API client functions for account management
 *
 * Uses the SDK for all API calls. The SDK uses camelCase; React components
 * use snake_case. We bridge with toCamelCase() / toSnakeCase() from
 * ../utils/caseConvert.
 */

import { accountsApi } from "./sdk";
import { toSnakeCase, toCamelCase } from "../utils/caseConvert";
import type {
  AccountCreate as SdkAccountCreate,
  AccountUpdate as SdkAccountUpdate,
  BalanceCreate as SdkBalanceCreate,
  HoldingCreate as SdkHoldingCreate,
  HoldingUpdate as SdkHoldingUpdate,
  ReconciliationCreate as SdkReconciliationCreate,
  ReconciliationComplete as SdkReconciliationComplete,
  TransactionClearRequest as SdkTransactionClearRequest,
} from "@spearmint-finance/sdk";
import {
  Account,
  AccountCreate,
  AccountUpdate,
  AccountSummary,
  Balance,
  BalanceCreate,
  BalanceHistory,
  InvestmentHolding,
  HoldingCreate,
  PortfolioSummary,
  Reconciliation,
  ReconciliationCreate,
  NetWorth,
} from "../types/account";

/**
 * Replace empty-string values with undefined so the SDK's Zod validators
 * don't reject them as invalid optional fields.
 */
function cleanEmptyStrings<T>(obj: Record<string, unknown>): T {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    result[key] = value === "" ? undefined : value;
  }
  return result as T;
}

// ==================== Account Management ====================

export const getAccounts = async (params?: {
  is_active?: boolean;
  account_type?: string;
  entity_id?: number;
}): Promise<Account[]> => {
  const sdkParams = params
    ? toCamelCase<{ isActive?: boolean; accountType?: string; entityId?: number }>(params)
    : undefined;
  const response = await accountsApi.listAccounts(sdkParams);
  return toSnakeCase<Account[]>(response.data);
};

export const createAccount = async (
  account: AccountCreate
): Promise<Account> => {
  const sdkPayload = cleanEmptyStrings<SdkAccountCreate>(toCamelCase(account));
  const response = await accountsApi.createAccount(sdkPayload);
  return toSnakeCase<Account>(response.data);
};

export const getAccount = async (accountId: number): Promise<Account> => {
  const response = await accountsApi.getAccount(accountId);
  return toSnakeCase<Account>(response.data);
};

export const updateAccount = async (
  accountId: number,
  account: AccountUpdate
): Promise<Account> => {
  const sdkPayload = cleanEmptyStrings<SdkAccountUpdate>(toCamelCase(account));
  const response = await accountsApi.updateAccount(accountId, sdkPayload);
  return toSnakeCase<Account>(response.data);
};

export const deleteAccount = async (accountId: number): Promise<void> => {
  await accountsApi.deleteAccount(accountId);
};

export const getAccountSummary = async (): Promise<AccountSummary[]> => {
  const response = await accountsApi.getAccountSummary();
  return toSnakeCase<AccountSummary[]>(response.data);
};

// ==================== Balance Management ====================

export const getBalanceHistory = async (
  accountId: number,
  params?: {
    start_date?: string;
    end_date?: string;
    balance_type?: string;
  }
): Promise<BalanceHistory> => {
  const sdkParams = params
    ? toCamelCase<{ startDate?: string; endDate?: string; balanceType?: string }>(params)
    : undefined;
  const response = await accountsApi.getBalanceHistory(accountId, sdkParams);
  return toSnakeCase<BalanceHistory>(response.data);
};

export const addBalanceSnapshot = async (
  accountId: number,
  balance: BalanceCreate
): Promise<Balance> => {
  const sdkPayload = cleanEmptyStrings<SdkBalanceCreate>(toCamelCase(balance));
  const response = await accountsApi.addBalanceSnapshot(accountId, sdkPayload);
  return toSnakeCase<Balance>(response.data);
};

export const getCurrentBalance = async (
  accountId: number
): Promise<Balance> => {
  const response = await accountsApi.getCurrentBalance(accountId);
  return toSnakeCase<Balance>(response.data);
};

export const getCalculatedBalance = async (
  accountId: number,
  as_of_date?: string
): Promise<{
  account_id: number;
  as_of_date: string;
  total: number;
  cash?: number;
  investments?: number;
  based_on_transactions: number;
}> => {
  const response = await accountsApi.getCalculatedBalance(accountId, {
    asOfDate: as_of_date,
  });
  return toSnakeCase(response.data);
};

// ==================== Investment Holdings ====================

export const getHoldings = async (
  accountId: number
): Promise<InvestmentHolding[]> => {
  const response = await accountsApi.getHoldings(accountId);
  return toSnakeCase<InvestmentHolding[]>(response.data);
};

export const addHolding = async (
  accountId: number,
  holding: HoldingCreate
): Promise<InvestmentHolding> => {
  const sdkPayload = cleanEmptyStrings<SdkHoldingCreate>(toCamelCase(holding));
  const response = await accountsApi.addHolding(accountId, sdkPayload);
  return toSnakeCase<InvestmentHolding>(response.data);
};

export const deleteHolding = async (
  holdingId: number
): Promise<{ message: string }> => {
  const response = await accountsApi.deleteHolding(holdingId);
  return response.data;
};

export const updateHolding = async (
  holdingId: number,
  updates: Record<string, unknown>
): Promise<InvestmentHolding> => {
  const sdkPayload = cleanEmptyStrings<SdkHoldingUpdate>(toCamelCase(updates));
  const response = await accountsApi.updateHolding(holdingId, sdkPayload);
  return toSnakeCase<InvestmentHolding>(response.data);
};

export const getPortfolioSummary = async (
  accountId: number
): Promise<PortfolioSummary> => {
  const response = await accountsApi.getPortfolioSummary(accountId);
  return toSnakeCase<PortfolioSummary>(response.data);
};

// ==================== Reconciliation ====================

export const createReconciliation = async (
  accountId: number,
  reconciliation: ReconciliationCreate
): Promise<Reconciliation> => {
  const sdkPayload = cleanEmptyStrings<SdkReconciliationCreate>(toCamelCase(reconciliation));
  const response = await accountsApi.createReconciliation(accountId, sdkPayload);
  return toSnakeCase<Reconciliation>(response.data);
};

export const getReconciliations = async (
  accountId: number,
  is_reconciled?: boolean
): Promise<Reconciliation[]> => {
  const response = await accountsApi.getReconciliations(accountId, {
    isReconciled: is_reconciled,
  });
  return toSnakeCase<Reconciliation[]>(response.data);
};

export const completeReconciliation = async (
  reconciliationId: number,
  data: {
    reconciled_by?: string;
    cleared_transaction_ids?: number[];
  }
): Promise<Reconciliation> => {
  const sdkPayload = cleanEmptyStrings<SdkReconciliationComplete>(toCamelCase(data));
  const response = await accountsApi.completeReconciliation(
    reconciliationId,
    sdkPayload
  );
  return toSnakeCase<Reconciliation>(response.data);
};

export const clearTransactions = async (
  transaction_ids: number[],
  cleared_date?: string
): Promise<{ message: string; cleared_count: number }> => {
  const sdkPayload: SdkTransactionClearRequest = {
    transactionIds: transaction_ids,
    clearedDate: cleared_date,
  };
  const response = await accountsApi.clearTransactions(sdkPayload);
  return toSnakeCase(response.data);
};

// ==================== Net Worth & Analytics ====================

export const getNetWorth = async (params?: {
  as_of_date?: string;
  entity_id?: number;
}): Promise<NetWorth> => {
  const sdkParams = params
    ? toCamelCase<{ asOfDate?: string; entityId?: number }>(params)
    : undefined;
  const response = await accountsApi.getNetWorth(sdkParams);
  return toSnakeCase<NetWorth>(response.data);
};
