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
  const isCapitalExpense =
    backendTransaction.isCapitalExpense ?? backendTransaction.is_capital_expense ?? false;
  const isTaxDeductible =
    backendTransaction.isTaxDeductible ?? backendTransaction.is_tax_deductible ?? false;
  const isRecurring =
    backendTransaction.isRecurring ?? backendTransaction.is_recurring ?? false;
  const isReimbursable =
    backendTransaction.isReimbursable ?? backendTransaction.is_reimbursable ?? false;
  const excludeFromIncome =
    backendTransaction.excludeFromIncome ?? backendTransaction.exclude_from_income ?? false;
  const excludeFromExpenses =
    backendTransaction.excludeFromExpenses ?? backendTransaction.exclude_from_expenses ?? false;

  // Handle nested category object (supports both camelCase and snake_case)
  // Normalize "nan" (from pandas NaN serialization during import) to undefined
  const rawCategoryName =
    backendTransaction.category?.categoryName ??
    backendTransaction.category?.category_name;
  const categoryName =
    rawCategoryName && rawCategoryName !== "nan" && rawCategoryName.trim() !== ""
      ? rawCategoryName
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
    is_capital_expense: isCapitalExpense,
    is_tax_deductible: isTaxDeductible,
    is_recurring: isRecurring,
    is_reimbursable: isReimbursable,
    exclude_from_income: excludeFromIncome,
    exclude_from_expenses: excludeFromExpenses,
    created_at: createdAt ? new Date(createdAt).toISOString() : "",
    updated_at: updatedAt ? new Date(updatedAt).toISOString() : "",
  };
};

/**
 * Get list of transactions with optional filters.
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  const response = await transactionsApi.listTransactions({
    startDate: params?.start_date,
    endDate: params?.end_date,
    transactionType: params?.transaction_type,
    categoryId: params?.category_id,
    includeInAnalysis: params?.include_in_analysis,
    isTransfer: params?.is_transfer,
    minAmount: params?.min_amount,
    maxAmount: params?.max_amount,
    searchText: params?.search_text,
    accountId: params?.account_id,
    entityId: params?.entity_id,
    includeCapitalExpenses: params?.include_capital_expenses,
    includeTransfers: params?.include_transfers,
    limit: params?.limit,
    offset: params?.offset,
    sortBy: params?.sort_by,
    sortOrder: params?.sort_order,
  });
  const data = response.data!;

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
    await transactionsApi.getTransaction(id);
  return transformTransaction(response.data);
};

/**
 * Create a new transaction
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const response = await transactionsApi.createTransaction({
    transactionDate: data.date,
    description: data.description,
    amount: data.amount,
    transactionType: data.transaction_type,
    categoryId: data.category_id,
    accountId: data.account_id,
    notes: data.notes,
    tagNames: data.tag_names,
    isCapitalExpense: data.is_capital_expense,
    isTaxDeductible: data.is_tax_deductible,
    isRecurring: data.is_recurring,
    isReimbursable: data.is_reimbursable,
    excludeFromIncome: data.exclude_from_income,
    excludeFromExpenses: data.exclude_from_expenses,
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
    await transactionsApi.updateTransaction(id, {
      transactionDate: data.date,
      description: data.description,
      amount: data.amount,
      transactionType: data.transaction_type,
      categoryId: data.category_id,
      accountId: data.account_id,
      notes: data.notes,
      tagNames: data.tag_names,
      isCapitalExpense: data.is_capital_expense,
      isTaxDeductible: data.is_tax_deductible,
      isRecurring: data.is_recurring,
      isReimbursable: data.is_reimbursable,
      excludeFromIncome: data.exclude_from_income,
      excludeFromExpenses: data.exclude_from_expenses,
    } as any);
  return transformTransaction(response.data);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await transactionsApi.deleteTransaction(id);
};
