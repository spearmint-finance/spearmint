import { transactionsApi, splitsApi } from "./sdk";
import { toCamelCase } from "../utils/caseConvert";
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
    entity_id: backendTransaction.entityId ?? backendTransaction.entity_id ?? null,
    splits: (backendTransaction.splits || []).map((s: any) => ({
      split_id: s.splitId ?? s.split_id,
      transaction_id: s.transactionId ?? s.transaction_id,
      amount: s.amount,
      category_id: s.categoryId ?? s.category_id,
      category_name: s.categoryName ?? s.category_name,
      entity_id: s.entityId ?? s.entity_id ?? null,
      description: s.description,
      notes: s.notes,
    })),
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
  // Convert snake_case params to camelCase for SDK
  const sdkParams = params ? toCamelCase<Record<string, any>>(params) : undefined;
  const response = await transactionsApi.listTransactions(sdkParams);
  const data = response.data as any;

  return {
    transactions: (data.transactions || []).map(transformTransaction),
    total: data.total ?? 0,
    limit: data.limit ?? params?.limit ?? 100,
    offset: data.offset ?? params?.offset ?? 0,
    summary: data.summary,
  };
};

/**
 * Get a single transaction by ID.
 */
export const getTransaction = async (id: number): Promise<Transaction> => {
  const response = await transactionsApi.getTransaction(id);
  return transformTransaction(response.data);
};

/**
 * Create a new transaction
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const body: Record<string, unknown> = {
    transactionDate: data.date,
    description: data.description,
    amount: data.amount,
    transactionType: data.transaction_type,
    categoryId: data.category_id,
  };
  if (data.account_id != null) body.accountId = data.account_id;
  if (data.entity_id != null) body.entityId = data.entity_id;
  if (data.notes != null) body.notes = data.notes;
  if (data.tag_names != null) body.tagNames = data.tag_names;
  if (data.is_capital_expense != null) body.isCapitalExpense = data.is_capital_expense;
  if (data.is_tax_deductible != null) body.isTaxDeductible = data.is_tax_deductible;
  if (data.is_recurring != null) body.isRecurring = data.is_recurring;
  if (data.is_reimbursable != null) body.isReimbursable = data.is_reimbursable;
  if (data.exclude_from_income != null) body.excludeFromIncome = data.exclude_from_income;
  if (data.exclude_from_expenses != null) body.excludeFromExpenses = data.exclude_from_expenses;

  const response = await transactionsApi.createTransaction(body as any);
  return transformTransaction(response.data);
};

/**
 * Update an existing transaction
 */
export const updateTransaction = async (
  id: number,
  data: TransactionUpdate
): Promise<Transaction> => {
  const body: Record<string, unknown> = {};
  if (data.date != null) body.transactionDate = data.date;
  if (data.description != null) body.description = data.description;
  if (data.amount != null) body.amount = data.amount;
  if (data.transaction_type != null) body.transactionType = data.transaction_type;
  if (data.category_id != null) body.categoryId = data.category_id;
  if (data.account_id != null) body.accountId = data.account_id;
  // Only include entityId when explicitly provided (undefined = don't change, null = clear)
  if (data.entity_id !== undefined) body.entityId = data.entity_id;
  if (data.notes != null) body.notes = data.notes;
  if (data.tag_names != null) body.tagNames = data.tag_names;
  if (data.is_capital_expense != null) body.isCapitalExpense = data.is_capital_expense;
  if (data.is_tax_deductible != null) body.isTaxDeductible = data.is_tax_deductible;
  if (data.is_recurring != null) body.isRecurring = data.is_recurring;
  if (data.is_reimbursable != null) body.isReimbursable = data.is_reimbursable;
  if (data.exclude_from_income != null) body.excludeFromIncome = data.exclude_from_income;
  if (data.exclude_from_expenses != null) body.excludeFromExpenses = data.exclude_from_expenses;

  const response = await transactionsApi.updateTransaction(id, body as any);
  return transformTransaction(response.data);
};

/**
 * Delete a transaction
 */
export const deleteTransaction = async (id: number): Promise<void> => {
  await transactionsApi.deleteTransaction(id);
};

/**
 * Set splits for a transaction (replaces all existing splits)
 */
export const setTransactionSplits = async (
  transactionId: number,
  splits: { amount: number; category_id: number; entity_id?: number | null; description?: string; notes?: string }[]
): Promise<void> => {
  const sdkSplits = splits.map(s => ({
    amount: s.amount,
    categoryId: s.category_id,
    entityId: s.entity_id ?? null,
    description: s.description ?? null,
    notes: s.notes ?? null,
  }));
  await splitsApi.setTransactionSplits(transactionId, sdkSplits as any);
};
