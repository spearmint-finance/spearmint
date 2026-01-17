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

// ==================== Account Management ====================

export const getAccounts = async (params?: {
  is_active?: boolean;
  account_type?: string;
}): Promise<Account[]> => {
  const response = await accountsApi.listAccountsApiAccountsGet({
    isActive: params?.is_active,
    accountType: params?.account_type,
  });
  return response.data as unknown as Account[];
};

export const createAccount = async (
  account: AccountCreate
): Promise<Account> => {
  const response = await accountsApi.createAccountApiAccountsPost(account);
  return response.data as unknown as Account;
};

export const getAccount = async (accountId: number): Promise<Account> => {
  const response = await accountsApi.getAccountApiAccountsAccountIdGet(
    accountId
  );
  return response.data as unknown as Account;
};

export const updateAccount = async (
  accountId: number,
  account: AccountUpdate
): Promise<Account> => {
  const response = await accountsApi.updateAccountApiAccountsAccountIdPut(
    accountId,
    account
  );
  return response.data as unknown as Account;
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
  return response.data as unknown as NetWorth;
};
