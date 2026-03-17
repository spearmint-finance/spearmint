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
    entity_id: backendAccount.entityId ?? backendAccount.entity_id,
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
  const response = await fetch(url, );
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
    entityId: account.entity_id,
    notes: account.notes || undefined,
  };
  const response = await accountsApi.createAccountApiAccountsPost(sdkPayload as any);
  return transformAccount(response.data);
};

export const getAccount = async (accountId: number): Promise<Account> => {
  const response = await accountsApi.getAccountApiAccountsAccountIdGet(
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
  const response = await accountsApi.updateAccountApiAccountsAccountIdPut(
    accountId,
    sdkPayload as any
  );
  return transformAccount(response.data);
};

export const deleteAccount = async (accountId: number): Promise<void> => {
  await accountsApi.deleteAccountApiAccountsAccountIdDelete(accountId);
};

export const getAccountSummary = async (): Promise<AccountSummary[]> => {
  const response = await accountsApi.getAccountSummaryApiAccountsSummaryGet();
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
    await accountsApi.getBalanceHistoryApiAccountsAccountIdBalancesGet(
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
    await accountsApi.addBalanceSnapshotApiAccountsAccountIdBalancesPost(
      accountId,
      sdkPayload as any
    );
  return response.data as unknown as Balance;
};

export const getCurrentBalance = async (
  accountId: number
): Promise<Balance> => {
  const response =
    await accountsApi.getCurrentBalanceApiAccountsAccountIdCurrentBalanceGet(
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
    await accountsApi.getCalculatedBalanceApiAccountsAccountIdCalculatedBalanceGet(
      accountId,
      { asOfDate: as_of_date }
    );
  return response.data as unknown as any;
};

// ==================== Investment Holdings ====================

export const getHoldings = async (
  accountId: number
): Promise<InvestmentHolding[]> => {
  const response = await accountsApi.getHoldingsApiAccountsAccountIdHoldingsGet(
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
  const response = await accountsApi.addHoldingApiAccountsAccountIdHoldingsPost(
    accountId,
    sdkPayload as any
  );
  return response.data as unknown as InvestmentHolding;
};

export const getPortfolioSummary = async (
  accountId: number
): Promise<PortfolioSummary> => {
  const response =
    await accountsApi.getPortfolioSummaryApiAccountsAccountIdPortfolioGet(
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
    await accountsApi.createReconciliationApiAccountsAccountIdReconcilePost(
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
    await accountsApi.getReconciliationsApiAccountsAccountIdReconciliationsGet(
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
    await accountsApi.completeReconciliationApiAccountsReconciliationsReconciliationIdCompletePut(
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
    await accountsApi.clearTransactionsApiAccountsTransactionsClearPost(
      sdkPayload as any
    );
  return response.data as unknown as { message: string; cleared_count: number };
};

// ==================== Net Worth & Analytics ====================

export const getNetWorth = async (as_of_date?: string): Promise<NetWorth> => {
  const response = await accountsApi.getNetWorthApiAccountsNetWorthGet({
    asOfDate: as_of_date,
  });
  // SDK returns camelCase, map to our interface format
  const data = response.data as {
    assets: string;
    liabilities: string;
    netWorth: string;
    liquidAssets: string;
    investments: string;
    asOfDate: string;
    accountBreakdown?: Record<string, string>;
  };
  return {
    assets: data.assets,
    liabilities: data.liabilities,
    net_worth: data.netWorth,
    netWorth: data.netWorth,
    liquid_assets: data.liquidAssets,
    liquidAssets: data.liquidAssets,
    investments: data.investments,
    as_of_date: data.asOfDate,
    asOfDate: data.asOfDate,
    account_breakdown: data.accountBreakdown,
    accountBreakdown: data.accountBreakdown,
  };
};
