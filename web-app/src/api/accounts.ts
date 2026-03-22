/**
 * API client functions for account management
 */

import sdk, { accountsApi } from "./sdk";
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
 * Transform backend account to frontend format
 * Handles both snake_case (direct API) and camelCase (SDK) field names
 */
const transformAccount = (backendAccount: any): Account => {
  const accountId =
    backendAccount.accountId ?? backendAccount.account_id;
  const accountName =
    backendAccount.accountName ?? backendAccount.account_name;
  const accountType =
    backendAccount.accountType ?? backendAccount.account_type;
  const accountSubtype =
    backendAccount.accountSubtype ?? backendAccount.account_subtype;
  const institutionName =
    backendAccount.institutionName ?? backendAccount.institution_name;
  const accountNumberLast4 =
    backendAccount.accountNumberLast4 ?? backendAccount.account_number_last4;
  const isActive =
    backendAccount.isActive ?? backendAccount.is_active;
  const hasCashComponent =
    backendAccount.hasCashComponent ?? backendAccount.has_cash_component;
  const hasInvestmentComponent =
    backendAccount.hasInvestmentComponent ?? backendAccount.has_investment_component;
  const openingBalance =
    backendAccount.openingBalance ?? backendAccount.opening_balance;
  const openingBalanceDate =
    backendAccount.openingBalanceDate ?? backendAccount.opening_balance_date;
  const createdAt =
    backendAccount.createdAt ?? backendAccount.created_at;
  const updatedAt =
    backendAccount.updatedAt ?? backendAccount.updated_at;
  const currentBalance =
    backendAccount.currentBalance ?? backendAccount.current_balance;
  const currentBalanceDate =
    backendAccount.currentBalanceDate ?? backendAccount.current_balance_date;
  const cashBalance =
    backendAccount.cashBalance ?? backendAccount.cash_balance;
  const investmentValue =
    backendAccount.investmentValue ?? backendAccount.investment_value;

  return {
    account_id: accountId,
    account_name: accountName,
    account_type: accountType,
    account_subtype: accountSubtype,
    institution_name: institutionName,
    account_number_last4: accountNumberLast4,
    currency: backendAccount.currency || "USD",
    is_active: isActive ?? true,
    has_cash_component: hasCashComponent ?? false,
    has_investment_component: hasInvestmentComponent ?? false,
    opening_balance: parseFloat(openingBalance) || 0,
    opening_balance_date: openingBalanceDate,
    entity_ids: backendAccount.entityIds ?? backendAccount.entity_ids ?? [],
    notes: backendAccount.notes,
    created_at: createdAt,
    updated_at: updatedAt,
    current_balance: currentBalance != null ? parseFloat(currentBalance) : undefined,
    current_balance_date: currentBalanceDate,
    cash_balance: cashBalance != null ? parseFloat(cashBalance) : undefined,
    investment_value: investmentValue != null ? parseFloat(investmentValue) : undefined,
  };
};

// ==================== Account Management ====================

export const getAccounts = async (params?: {
  is_active?: boolean;
  account_type?: string;
  entity_id?: number;
}): Promise<Account[]> => {
  // Use direct fetch to support entity_id (SDK predates this param)
  const sdkConfig = (sdk as any).config ?? {};
  const baseUrl = sdkConfig.baseUrl || sdkConfig.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined" ? window.location.origin : "http://localhost:8080");

  const queryParams = new URLSearchParams();
  if (params?.is_active != null) queryParams.set("is_active", String(params.is_active));
  if (params?.account_type) queryParams.set("account_type", params.account_type);
  if (params?.entity_id != null) queryParams.set("entity_id", String(params.entity_id));

  const url = `${baseUrl}/api/accounts?${queryParams.toString()}`;
  const response = await fetch(url);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail || `Failed to fetch accounts: ${response.statusText}`);
  }
  const data = await response.json();
  return (data as any[]).map(transformAccount);
};

export const createAccount = async (
  account: AccountCreate
): Promise<Account> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    accountName: account.account_name,
    accountType: account.account_type,
    accountSubtype: account.account_subtype || undefined,
    institutionName: account.institution_name || undefined,
    accountNumberLast4: account.account_number_last4 || undefined,
    currency: account.currency || undefined,
    openingBalance: account.opening_balance,
    openingBalanceDate: account.opening_balance_date,
    entityIds: account.entity_ids,
    notes: account.notes || undefined,
  };
  const response = await accountsApi.createAccount(sdkPayload as any);
  return transformAccount(response.data);
};

export const getAccount = async (accountId: number): Promise<Account> => {
  const response = await accountsApi.getAccount(
    accountId
  );
  return transformAccount(response.data);
};

export const updateAccount = async (
  accountId: number,
  account: AccountUpdate
): Promise<Account> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    accountName: account.account_name || undefined,
    accountSubtype: account.account_subtype || undefined,
    institutionName: account.institution_name || undefined,
    accountNumberLast4: account.account_number_last4 || undefined,
    isActive: account.is_active,
    notes: account.notes || undefined,
  };
  const response = await accountsApi.updateAccount(
    accountId,
    sdkPayload as any
  );
  return transformAccount(response.data);
};

export const deleteAccount = async (accountId: number): Promise<void> => {
  await accountsApi.deleteAccount(accountId);
};

export const getAccountSummary = async (): Promise<AccountSummary[]> => {
  const response = await accountsApi.getAccountSummary();
  return response.data as unknown as AccountSummary[];
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
  const response =
    await accountsApi.getBalanceHistory(
      accountId,
      {
        startDate: params?.start_date,
        endDate: params?.end_date,
        balanceType: params?.balance_type,
      }
    );
  return response.data as unknown as BalanceHistory;
};

export const addBalanceSnapshot = async (
  accountId: number,
  balance: BalanceCreate
): Promise<Balance> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    balanceDate: balance.balance_date,
    totalBalance: balance.total_balance,
    balanceType: balance.balance_type || undefined,
    cashBalance: balance.cash_balance,
    investmentValue: balance.investment_value,
    notes: balance.notes || undefined,
  };
  const response =
    await accountsApi.addBalanceSnapshot(
      accountId,
      sdkPayload as any
    );
  return response.data as unknown as Balance;
};

export const getCurrentBalance = async (
  accountId: number
): Promise<Balance> => {
  const response =
    await accountsApi.getCurrentBalance(
      accountId
    );
  return response.data as unknown as Balance;
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
  const response =
    await accountsApi.getCalculatedBalance(
      accountId,
      { asOfDate: as_of_date }
    );
  return response.data as unknown as any;
};

// ==================== Investment Holdings ====================

export const getHoldings = async (
  accountId: number
): Promise<InvestmentHolding[]> => {
  const response = await accountsApi.getHoldings(
    accountId
  );
  return response.data as unknown as InvestmentHolding[];
};

export const addHolding = async (
  accountId: number,
  holding: HoldingCreate
): Promise<InvestmentHolding> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    symbol: holding.symbol,
    quantity: holding.quantity,
    asOfDate: holding.as_of_date,
    description: holding.description || undefined,
    costBasis: holding.cost_basis,
    currentValue: holding.current_value,
    assetClass: holding.asset_class || undefined,
    sector: holding.sector || undefined,
  };
  const response = await accountsApi.addHolding(
    accountId,
    sdkPayload as any
  );
  return response.data as unknown as InvestmentHolding;
};

export const deleteHolding = async (
  holdingId: number
): Promise<{ message: string }> => {
  const sdkConfig = (sdk as any).config ?? {};
  const baseUrl = sdkConfig.baseUrl || sdkConfig.environment ||
    (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8080');
  const response = await fetch(`${baseUrl}/api/accounts/holdings/${holdingId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Delete failed' }));
    throw new Error(err.detail || 'Failed to delete holding');
  }
  return response.json();
};

export const getPortfolioSummary = async (
  accountId: number
): Promise<PortfolioSummary> => {
  const response =
    await accountsApi.getPortfolioSummary(
      accountId
    );
  return response.data as unknown as PortfolioSummary;
};

// ==================== Reconciliation ====================

export const createReconciliation = async (
  accountId: number,
  reconciliation: ReconciliationCreate
): Promise<Reconciliation> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    statementDate: reconciliation.statement_date,
    statementBalance: reconciliation.statement_balance,
    statementCashBalance: reconciliation.statement_cash_balance,
    statementInvestmentValue: reconciliation.statement_investment_value,
    notes: reconciliation.notes || undefined,
  };
  const response =
    await accountsApi.createReconciliation(
      accountId,
      sdkPayload as any
    );
  return response.data as unknown as Reconciliation;
};

export const getReconciliations = async (
  accountId: number,
  is_reconciled?: boolean
): Promise<Reconciliation[]> => {
  const response =
    await accountsApi.getReconciliations(
      accountId,
      { isReconciled: is_reconciled }
    );
  return response.data as unknown as Reconciliation[];
};

export const completeReconciliation = async (
  reconciliationId: number,
  data: {
    reconciled_by?: string;
    cleared_transaction_ids?: number[];
  }
): Promise<Reconciliation> => {
  // Transform snake_case frontend format to camelCase SDK format
  // SDK validates optional fields - empty strings must be converted to undefined
  const sdkPayload = {
    reconciledBy: data.reconciled_by || undefined,
    clearedTransactionIds: data.cleared_transaction_ids,
  };
  const response =
    await accountsApi.completeReconciliation(
      reconciliationId,
      sdkPayload as any
    );
  return response.data as unknown as Reconciliation;
};

export const clearTransactions = async (
  transaction_ids: number[],
  cleared_date?: string
): Promise<{ message: string; cleared_count: number }> => {
  // Transform snake_case frontend format to camelCase SDK format
  const sdkPayload = {
    transactionIds: transaction_ids,
    clearedDate: cleared_date,
  };
  const response =
    await accountsApi.clearTransactions(
      sdkPayload as any
    );
  return response.data as unknown as { message: string; cleared_count: number };
};

// ==================== Net Worth & Analytics ====================

export const getNetWorth = async (params?: { as_of_date?: string; entity_id?: number }): Promise<NetWorth> => {
  const sdkConfig = (sdk as any).config ?? {};
  const baseUrl = sdkConfig.baseUrl || sdkConfig.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined" ? window.location.origin : "http://localhost:8080");

  const queryParams = new URLSearchParams();
  if (params?.as_of_date) queryParams.set("as_of_date", params.as_of_date);
  if (params?.entity_id != null) queryParams.set("entity_id", String(params.entity_id));

  const url = `${baseUrl}/api/accounts/net-worth?${queryParams.toString()}`;
  const response = await fetch(url);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail || `Failed to fetch net worth: ${response.statusText}`);
  }
  const data = await response.json();
  return {
    assets: data.assets,
    liabilities: data.liabilities,
    net_worth: data.net_worth ?? data.netWorth,
    netWorth: data.net_worth ?? data.netWorth,
    liquid_assets: data.liquid_assets ?? data.liquidAssets,
    liquidAssets: data.liquid_assets ?? data.liquidAssets,
    investments: data.investments,
    as_of_date: data.as_of_date ?? data.asOfDate,
    asOfDate: data.as_of_date ?? data.asOfDate,
    account_breakdown: data.account_breakdown ?? data.accountBreakdown,
    accountBreakdown: data.account_breakdown ?? data.accountBreakdown,
  };
};
