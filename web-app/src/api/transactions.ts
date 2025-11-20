import { transactionsApi } from "./sdk";
import type {
  Transaction,
  TransactionCreate,
  TransactionUpdate,
} from "../types/transaction";
// Import SDK types if needed for mapping
import { Transaction as SdkTransaction } from "@spearmint-money/sdk";

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
  summary?: any; // Add summary to interface to match return type
}

/**
 * Transform backend transaction to frontend format
 */
const transformTransaction = (backendTransaction: any): Transaction => {
  // The SDK might return an object where properties are accessible directly
  return {
    id: backendTransaction.transaction_id,
    date: backendTransaction.transaction_date ? new Date(backendTransaction.transaction_date).toISOString().split('T')[0] : "",
    description: backendTransaction.description || "",
    amount: backendTransaction.amount,
    transaction_type: backendTransaction.transaction_type,
    is_transfer: backendTransaction.is_transfer,
    balance: backendTransaction.balance,
    category_id: backendTransaction.category_id,
    category_name: backendTransaction.category?.category_name,
    classification_id: backendTransaction.classification_id,
    classification_name: backendTransaction.classification?.classification_name,
    source: backendTransaction.source,
    payment_method: backendTransaction.payment_method,
    transfer_account_from: backendTransaction.transfer_account_from,
    transfer_account_to: backendTransaction.transfer_account_to,
    notes: backendTransaction.notes,
    tags: backendTransaction.tags?.map((tag: any) => tag.tag_name),
    created_at: backendTransaction.created_at ? new Date(backendTransaction.created_at).toISOString() : "",
    updated_at: backendTransaction.updated_at ? new Date(backendTransaction.updated_at).toISOString() : "",
  };
};

/**
 * Get list of transactions with optional filters
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  // Map frontend params to SDK params
  // Note: openapi-generator usually expects individual arguments or a request object
  // We'll assume it takes an object with keys matching the spec parameters
  
  const response = await transactionsApi.listTransactions({
    startDate: params?.start_date,
    endDate: params?.end_date,
    transactionType: params?.transaction_type,
    categoryId: params?.category_id,
    classificationId: params?.classification_id,
    includeInAnalysis: params?.include_in_analysis,
    isTransfer: params?.is_transfer,
    minAmount: params?.min_amount,
    maxAmount: params?.max_amount,
    search: params?.search_text, // "search" vs "search_text" - check spec
    limit: params?.limit,
    offset: params?.offset,
    sortBy: params?.sort_by,
    sortOrder: params?.sort_order
  });

  return {
    transactions: (response.transactions || []).map(transformTransaction),
    total: response.total,
    limit: response.limit,
    offset: response.offset,
    summary: (response as any).summary,
  };
};

/**
 * Get a single transaction by ID
 */
export const getTransaction = async (id: number): Promise<Transaction> => {
  const response = await transactionsApi.getTransaction({ transactionId: id });
  return transformTransaction(response);
};

/**
 * Create a new transaction
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const response = await transactionsApi.createTransaction({
    transactionCreate: {
      transaction_date: data.date, // SDK likely expects snake_case based on spec
      description: data.description,
      amount: data.amount,
      transaction_type: data.transaction_type,
      category_id: data.category_id,
      is_transfer: data.is_transfer || false,
      notes: data.notes,
    }
  });
  return transformTransaction(response);
};

/**
 * Update an existing transaction
 */
export const updateTransaction = async (
  id: number,
  data: TransactionUpdate
): Promise<Transaction> => {
  const response = await transactionsApi.updateTransaction({
    transactionId: id,
    transactionUpdate: {
      transaction_date: data.date,
      description: data.description,
      amount: data.amount,
      transaction_type: data.transaction_type,
      category_id: data.category_id,
      is_transfer: data.is_transfer,
      notes: data.notes,
      // reapply_rules: data.reapply_rules // Check if this exists in TransactionUpdate model
    }
  });
  return transformTransaction(response);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await transactionsApi.deleteTransaction({ transactionId: id });
};