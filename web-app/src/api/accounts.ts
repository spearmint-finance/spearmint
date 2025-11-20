/**
 * API client functions for account management
 */

import axios from 'axios';
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
} from '../types/account';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// ==================== Account Management ====================

export const getAccounts = async (params?: {
  is_active?: boolean;
  account_type?: string;
}): Promise<Account[]> => {
  const response = await axios.get(`${API_BASE_URL}/accounts`, { params });
  return response.data;
};

export const createAccount = async (account: AccountCreate): Promise<Account> => {
  const response = await axios.post(`${API_BASE_URL}/accounts`, account);
  return response.data;
};

export const getAccount = async (accountId: number): Promise<Account> => {
  const response = await axios.get(`${API_BASE_URL}/accounts/${accountId}`);
  return response.data;
};

export const updateAccount = async (
  accountId: number,
  account: AccountUpdate
): Promise<Account> => {
  const response = await axios.put(`${API_BASE_URL}/accounts/${accountId}`, account);
  return response.data;
};

export const deleteAccount = async (accountId: number): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/accounts/${accountId}`);
};

export const getAccountSummary = async (): Promise<AccountSummary[]> => {
  const response = await axios.get(`${API_BASE_URL}/accounts/summary`);
  return response.data;
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
  const response = await axios.get(
    `${API_BASE_URL}/accounts/${accountId}/balances`,
    { params }
  );
  return response.data;
};

export const addBalanceSnapshot = async (
  accountId: number,
  balance: BalanceCreate
): Promise<Balance> => {
  const response = await axios.post(
    `${API_BASE_URL}/accounts/${accountId}/balances`,
    balance
  );
  return response.data;
};

export const getCurrentBalance = async (accountId: number): Promise<Balance> => {
  const response = await axios.get(
    `${API_BASE_URL}/accounts/${accountId}/current-balance`
  );
  return response.data;
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
  const params = as_of_date ? { as_of_date } : {};
  const response = await axios.get(
    `${API_BASE_URL}/accounts/${accountId}/calculated-balance`,
    { params }
  );
  return response.data;
};

// ==================== Investment Holdings ====================

export const getHoldings = async (accountId: number): Promise<InvestmentHolding[]> => {
  const response = await axios.get(`${API_BASE_URL}/accounts/${accountId}/holdings`);
  return response.data;
};

export const addHolding = async (
  accountId: number,
  holding: HoldingCreate
): Promise<InvestmentHolding> => {
  const response = await axios.post(
    `${API_BASE_URL}/accounts/${accountId}/holdings`,
    holding
  );
  return response.data;
};

export const getPortfolioSummary = async (
  accountId: number
): Promise<PortfolioSummary> => {
  const response = await axios.get(`${API_BASE_URL}/accounts/${accountId}/portfolio`);
  return response.data;
};

// ==================== Reconciliation ====================

export const createReconciliation = async (
  accountId: number,
  reconciliation: ReconciliationCreate
): Promise<Reconciliation> => {
  const response = await axios.post(
    `${API_BASE_URL}/accounts/${accountId}/reconcile`,
    reconciliation
  );
  return response.data;
};

export const getReconciliations = async (
  accountId: number,
  is_reconciled?: boolean
): Promise<Reconciliation[]> => {
  const params = is_reconciled !== undefined ? { is_reconciled } : {};
  const response = await axios.get(
    `${API_BASE_URL}/accounts/${accountId}/reconciliations`,
    { params }
  );
  return response.data;
};

export const completeReconciliation = async (
  reconciliationId: number,
  data: {
    reconciled_by?: string;
    cleared_transaction_ids?: number[];
  }
): Promise<Reconciliation> => {
  const response = await axios.put(
    `${API_BASE_URL}/accounts/reconciliations/${reconciliationId}/complete`,
    data
  );
  return response.data;
};

export const clearTransactions = async (
  transaction_ids: number[],
  cleared_date?: string
): Promise<{ message: string; cleared_count: number }> => {
  const response = await axios.post(`${API_BASE_URL}/accounts/transactions/clear`, {
    transaction_ids,
    cleared_date,
  });
  return response.data;
};

// ==================== Net Worth & Analytics ====================

export const getNetWorth = async (as_of_date?: string): Promise<NetWorth> => {
  const params = as_of_date ? { as_of_date } : {};
  const response = await axios.get(`${API_BASE_URL}/accounts/net-worth`, { params });
  return response.data;
};