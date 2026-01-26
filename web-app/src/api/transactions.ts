import { transactionsApi } from "./sdk";
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
  summary?: any; // Add summary to interface to match return type
}

/**
 * Transform backend transaction to frontend format
 * Handles both snake_case (direct API) and camelCase (SDK) field names
 */
const transformTransaction = (backendTransaction: any): Transaction => {
  // Get values supporting both camelCase (SDK) and snake_case (direct API)
  const transactionId =
    backendTransaction.transactionId ?? backendTransaction.transaction_id ?? backendTransaction.id;
  const transactionDate =
    backendTransaction.transactionDate ?? backendTransaction.transaction_date ?? backendTransaction.date;
  const transactionType =
    backendTransaction.transactionType ?? backendTransaction.transaction_type;
  const isTransfer =
    backendTransaction.isTransfer ?? backendTransaction.is_transfer;
  const categoryId =
    backendTransaction.categoryId ?? backendTransaction.category_id;
  const classificationId =
    backendTransaction.classificationId ?? backendTransaction.classification_id;
  const paymentMethod =
    backendTransaction.paymentMethod ?? backendTransaction.payment_method;
  const transferAccountFrom =
    backendTransaction.transferAccountFrom ??
    backendTransaction.transfer_account_from;
  const transferAccountTo =
    backendTransaction.transferAccountTo ??
    backendTransaction.transfer_account_to;
  const relatedTransactionId =
    backendTransaction.relatedTransactionId ??
    backendTransaction.related_transaction_id;
  const createdAt =
    backendTransaction.createdAt ?? backendTransaction.created_at;
  const updatedAt =
    backendTransaction.updatedAt ?? backendTransaction.updated_at;

  // Handle nested category object (supports both camelCase and snake_case)
  const categoryName =
    backendTransaction.category?.categoryName ??
    backendTransaction.category?.category_name;

  // Handle nested classification object (supports both camelCase and snake_case)
  const classificationName =
    backendTransaction.classification?.classificationName ??
    backendTransaction.classification?.classification_name;

  return {
    id: transactionId,
    date: transactionDate
      ? new Date(transactionDate).toISOString().split("T")[0]
      : "",
    description: backendTransaction.description || "",
    amount: backendTransaction.amount,
    transaction_type: transactionType,
    is_transfer: isTransfer,
    balance: backendTransaction.balance,
    category_id: categoryId,
    category_name: categoryName,
    classification_id: classificationId,
    classification_name: classificationName,
    related_transaction_id: relatedTransactionId,
    source: backendTransaction.source,
    payment_method: paymentMethod,
    transfer_account_from: transferAccountFrom,
    transfer_account_to: transferAccountTo,
    notes: backendTransaction.notes,
    tags: backendTransaction.tags?.map(
      (tag: any) => tag.tagName ?? tag.tag_name
    ),
    created_at: createdAt ? new Date(createdAt).toISOString() : "",
    updated_at: updatedAt ? new Date(updatedAt).toISOString() : "",
  };
};

/**
 * Get list of transactions with optional filters
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  const response = await transactionsApi.listTransactionsApiTransactionsGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    transactionType: params?.transaction_type,
    categoryId: params?.category_id,
    classificationId: params?.classification_id,
    includeInAnalysis: params?.include_in_analysis,
    isTransfer: params?.is_transfer,
    minAmount: params?.min_amount,
    maxAmount: params?.max_amount,
    searchText: params?.search_text,
    limit: params?.limit,
    offset: params?.offset,
    sortBy: params?.sort_by,
    sortOrder: params?.sort_order,
  });

  const data = response.data ?? {};
  return {
    transactions: (data.transactions || []).map(transformTransaction),
    total: data.total ?? 0,
    limit: data.limit ?? params?.limit ?? 100,
    offset: data.offset ?? params?.offset ?? 0,
    summary: (data as any).summary,
  };
};

/**
 * Get a single transaction by ID
 */
export const getTransaction = async (id: number): Promise<Transaction> => {
  const response =
    await transactionsApi.getTransactionApiTransactionsTransactionIdGet(id);
  return transformTransaction(response.data);
};

/**
 * Create a new transaction
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const response = await transactionsApi.createTransactionApiTransactionsPost({
    transactionDate: data.date,
    description: data.description,
    amount: data.amount,
    transactionType: data.transaction_type,
    categoryId: data.category_id,
    isTransfer: data.is_transfer || false,
    notes: data.notes,
  });
  return transformTransaction(response.data);
};

/**
 * Update an existing transaction
 */
export const updateTransaction = async (
  id: number,
  data: TransactionUpdate
): Promise<Transaction> => {
  const response =
    await transactionsApi.updateTransactionApiTransactionsTransactionIdPut(id, {
      transactionDate: data.date,
      description: data.description,
      amount: data.amount,
      transactionType: data.transaction_type,
      categoryId: data.category_id,
      isTransfer: data.is_transfer,
      notes: data.notes,
    });
  return transformTransaction(response.data);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await transactionsApi.deleteTransactionApiTransactionsTransactionIdDelete(id);
};
