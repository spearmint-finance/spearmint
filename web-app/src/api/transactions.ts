import apiClient from "./client";
import type {
  Transaction,
  TransactionCreate,
  TransactionUpdate,
} from "../types/transaction";

export interface TransactionListParams {
  start_date?: string;
  end_date?: string;
  transaction_type?: "Income" | "Expense";
  category_id?: number;
  classification_id?: number;
  include_in_analysis?: boolean;
  is_transfer?: boolean;
  min_amount?: number;
  max_amount?: number;
  search_text?: string;
  include_capital_expenses?: boolean;
  include_transfers?: boolean;
  limit?: number;
  offset?: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}

export interface TransactionListResponse {
  transactions: Transaction[];
  total: number;
  limit: number;
  offset: number;
}

/**
 * Transform backend transaction to frontend format
 */
const transformTransaction = (backendTransaction: any): Transaction => {
  return {
    id: backendTransaction.transaction_id,
    date: backendTransaction.transaction_date,
    description: backendTransaction.description || "",
    amount: backendTransaction.amount,
    transaction_type: backendTransaction.transaction_type,
    is_transfer: backendTransaction.is_transfer,
    balance: backendTransaction.balance,
    // Prefer top-level IDs if present; fallback to nested relation
    category_id:
      backendTransaction.category_id ??
      backendTransaction.category?.category_id,
    category_name: backendTransaction.category?.category_name,
    classification_id:
      backendTransaction.classification_id ??
      backendTransaction.classification?.classification_id,
    classification_name: backendTransaction.classification?.classification_name,
    source: backendTransaction.source,
    payment_method: backendTransaction.payment_method,
    transfer_account_from: backendTransaction.transfer_account_from,
    transfer_account_to: backendTransaction.transfer_account_to,
    notes: backendTransaction.notes,
    tags: backendTransaction.tags?.map((tag: any) => tag.tag_name),
    created_at: backendTransaction.created_at,
    updated_at: backendTransaction.updated_at,
  };
};

/**
 * Get list of transactions with optional filters
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  const response = await apiClient.get("/transactions", { params });
  return {
    transactions: response.data.transactions.map(transformTransaction),
    total: response.data.total,
    limit: response.data.limit,
    offset: response.data.offset,
    summary: response.data.summary,
  };
};

/**
 * Get a single transaction by ID
 */
export const getTransaction = async (id: number): Promise<Transaction> => {
  const response = await apiClient.get(`/transactions/${id}`);
  return transformTransaction(response.data);
};

/**
 * Transform frontend transaction create data to backend format
 */
const transformTransactionCreate = (frontendData: TransactionCreate): any => {
  return {
    transaction_date: frontendData.date,
    description: frontendData.description,
    amount: frontendData.amount,
    transaction_type: frontendData.transaction_type,
    category_id: frontendData.category_id,
    is_transfer: frontendData.is_transfer || false,
    notes: frontendData.notes,
  };
};

/**
 * Transform frontend transaction update data to backend format
 */
const transformTransactionUpdate = (frontendData: TransactionUpdate): any => {
  const backendData: any = {};
  if (frontendData.date !== undefined)
    backendData.transaction_date = frontendData.date;
  if (frontendData.description !== undefined)
    backendData.description = frontendData.description;
  if (frontendData.amount !== undefined)
    backendData.amount = frontendData.amount;
  if (frontendData.transaction_type !== undefined)
    backendData.transaction_type = frontendData.transaction_type;
  if (frontendData.category_id !== undefined)
    backendData.category_id = frontendData.category_id;
  if (frontendData.is_transfer !== undefined)
    backendData.is_transfer = frontendData.is_transfer;
  if (frontendData.notes !== undefined) backendData.notes = frontendData.notes;
  if (frontendData.reapply_rules !== undefined)
    backendData.reapply_rules = frontendData.reapply_rules;
  return backendData;
};

/**
 * Create a new transaction
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const backendData = transformTransactionCreate(data);
  const response = await apiClient.post("/transactions", backendData);
  return transformTransaction(response.data);
};

/**
 * Update an existing transaction
 */
export const updateTransaction = async (
  id: number,
  data: TransactionUpdate
): Promise<Transaction> => {
  const backendData = transformTransactionUpdate(data);
  const response = await apiClient.put(`/transactions/${id}`, backendData);
  return transformTransaction(response.data);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await apiClient.delete(`/transactions/${id}`);
};
