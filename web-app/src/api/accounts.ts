/**
 * API client functions for account management
 */

import { accountsApi } from "./sdk";
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
}): Promise<Account[]> => {
  const response = await accountsApi.listAccountsApiAccountsGet({
    isActive: params?.is_active,
    accountType: params?.account_type,
  });
  return (response.data as any[]).map(transformAccount);
};

export const createAccount = async (
  account: AccountCreate
): Promise<Account> => {
  const response = await accountsApi.createAccountApiAccountsPost(account);
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
  const response = await accountsApi.updateAccountApiAccountsAccountIdPut(
    accountId,
    account
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
  const response =
    await accountsApi.addBalanceSnapshotApiAccountsAccountIdBalancesPost(
      accountId,
      balance
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
  const response = await accountsApi.addHoldingApiAccountsAccountIdHoldingsPost(
    accountId,
    holding
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
  const response =
    await accountsApi.createReconciliationApiAccountsAccountIdReconcilePost(
      accountId,
      reconciliation
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
  const response =
    await accountsApi.completeReconciliationApiAccountsReconciliationsReconciliationIdCompletePut(
      reconciliationId,
      {
        reconciled_by: data.reconciled_by,
        cleared_transaction_ids: data.cleared_transaction_ids,
      }
    );
  return response.data as unknown as Reconciliation;
};

export const clearTransactions = async (
  transaction_ids: number[],
  cleared_date?: string
): Promise<{ message: string; cleared_count: number }> => {
  const response =
    await accountsApi.clearTransactionsApiAccountsTransactionsClearPost({
      transaction_ids,
      cleared_date,
    });
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
