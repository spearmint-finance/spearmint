import sdk, { transactionsApi } from "./sdk";
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
  account_id?: number;
  entity_id?: number;
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
  const accountId =
    backendTransaction.accountId ?? backendTransaction.account_id;
  const createdAt =
    backendTransaction.createdAt ?? backendTransaction.created_at;
  const updatedAt =
    backendTransaction.updatedAt ?? backendTransaction.updated_at;

  // Handle nested category object (supports both camelCase and snake_case)
  // Normalize "nan" (from pandas NaN serialization during import) to undefined
  const rawCategoryName =
    backendTransaction.category?.categoryName ??
    backendTransaction.category?.category_name;
  const categoryName =
    rawCategoryName && rawCategoryName !== "nan" && rawCategoryName.trim() !== ""
      ? rawCategoryName
      : undefined;

  // Handle nested classification object (supports both camelCase and snake_case)
  const rawClassificationName =
    backendTransaction.classification?.classificationName ??
    backendTransaction.classification?.classification_name;
  const classificationName =
    rawClassificationName && rawClassificationName !== "nan" && rawClassificationName.trim() !== ""
      ? rawClassificationName
      : undefined;

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
    account_id: accountId,
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
 * Get list of transactions with optional filters.
 *
 * Uses direct fetch instead of SDK to support account_id filtering
 * (SDK v0.0.15 predates the account_id query param).
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  // Reuse the same base URL the SDK uses (configured in sdk.ts)
  const sdkConfig = (sdk as any).config ?? {};
  const baseUrl = sdkConfig.baseUrl || sdkConfig.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined"
      ? window.location.origin
      : "http://localhost:8080");

  const queryParams = new URLSearchParams();
  if (params?.start_date) queryParams.set("start_date", params.start_date);
  if (params?.end_date) queryParams.set("end_date", params.end_date);
  if (params?.transaction_type)
    queryParams.set("transaction_type", params.transaction_type);
  if (params?.category_id != null)
    queryParams.set("category_id", String(params.category_id));
  if (params?.classification_id != null)
    queryParams.set("classification_id", String(params.classification_id));
  if (params?.include_in_analysis != null)
    queryParams.set("include_in_analysis", String(params.include_in_analysis));
  if (params?.is_transfer != null)
    queryParams.set("is_transfer", String(params.is_transfer));
  if (params?.min_amount != null)
    queryParams.set("min_amount", String(params.min_amount));
  if (params?.max_amount != null)
    queryParams.set("max_amount", String(params.max_amount));
  if (params?.search_text) queryParams.set("search_text", params.search_text);
  if (params?.account_id != null)
    queryParams.set("account_id", String(params.account_id));
  if (params?.entity_id != null)
    queryParams.set("entity_id", String(params.entity_id));
  if (params?.include_capital_expenses != null)
    queryParams.set(
      "include_capital_expenses",
      String(params.include_capital_expenses)
    );
  if (params?.include_transfers != null)
    queryParams.set("include_transfers", String(params.include_transfers));
  if (params?.limit != null) queryParams.set("limit", String(params.limit));
  if (params?.offset != null) queryParams.set("offset", String(params.offset));
  if (params?.sort_by) queryParams.set("sort_by", params.sort_by);
  if (params?.sort_order) queryParams.set("sort_order", params.sort_order);

  const url = `${baseUrl}/api/transactions?${queryParams.toString()}`;
  const response = await fetch(url);
  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(
      errorBody?.detail || `Failed to fetch transactions: ${response.statusText}`
    );
  }
  const data = await response.json();

  return {
    transactions: (data.transactions || []).map(transformTransaction),
    total: data.total ?? 0,
    limit: data.limit ?? params?.limit ?? 100,
    offset: data.offset ?? params?.offset ?? 0,
    summary: data.summary,
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
    accountId: data.account_id,
    notes: data.notes,
  } as any);
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
      accountId: data.account_id,
      notes: data.notes,
    } as any);
  return transformTransaction(response.data);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await transactionsApi.deleteTransactionApiTransactionsTransactionIdDelete(id);
};
