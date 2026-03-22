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
/**
 * List transactions — uses direct fetch to preserve entity_id, boolean
 * properties, and splits that the SDK's Zod strict mode strips.
 */
export const getTransactions = async (
  params?: TransactionListParams
): Promise<TransactionListResponse> => {
  const query = new URLSearchParams();
  if (params?.start_date) query.set('start_date', params.start_date);
  if (params?.end_date) query.set('end_date', params.end_date);
  if (params?.transaction_type) query.set('transaction_type', params.transaction_type);
  if (params?.category_id != null) query.set('category_id', String(params.category_id));
  if (params?.include_in_analysis != null) query.set('include_in_analysis', String(params.include_in_analysis));
  if (params?.is_transfer != null) query.set('is_transfer', String(params.is_transfer));
  if (params?.min_amount != null) query.set('min_amount', String(params.min_amount));
  if (params?.max_amount != null) query.set('max_amount', String(params.max_amount));
  if (params?.search_text) query.set('search_text', params.search_text);
  if (params?.account_id != null) query.set('account_id', String(params.account_id));
  if (params?.entity_id != null) query.set('entity_id', String(params.entity_id));
  if (params?.include_capital_expenses != null) query.set('include_capital_expenses', String(params.include_capital_expenses));
  if (params?.include_transfers != null) query.set('include_transfers', String(params.include_transfers));
  if (params?.limit != null) query.set('limit', String(params.limit));
  if (params?.offset != null) query.set('offset', String(params.offset));
  if (params?.sort_by) query.set('sort_by', params.sort_by);
  if (params?.sort_order) query.set('sort_order', params.sort_order);

  const response = await fetch(`/api/transactions?${query.toString()}`);
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Failed to load transactions' }));
    throw new Error(err.detail || 'Failed to load transactions');
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
 * Get a single transaction by ID — uses direct fetch to preserve all fields.
 */
export const getTransaction = async (id: number): Promise<Transaction> => {
  const response = await fetch(`/api/transactions/${id}`);
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Transaction not found' }));
    throw new Error(err.detail || 'Transaction not found');
  }
  const data = await response.json();
  return transformTransaction(data);
};

/**
 * Create a new transaction
 * Uses direct fetch — the SDK schema strips fields it doesn't know about
 * (entity_id, boolean properties), so we bypass it here.
 */
export const createTransaction = async (
  data: TransactionCreate
): Promise<Transaction> => {
  const body: Record<string, unknown> = {
    transaction_date: data.date,
    description: data.description,
    amount: data.amount,
    transaction_type: data.transaction_type,
    category_id: data.category_id,
  };
  if (data.account_id != null) body.account_id = data.account_id;
  if (data.entity_id != null) body.entity_id = data.entity_id;
  if (data.notes != null) body.notes = data.notes;
  if (data.tag_names != null) body.tag_names = data.tag_names;
  if (data.is_capital_expense != null) body.is_capital_expense = data.is_capital_expense;
  if (data.is_tax_deductible != null) body.is_tax_deductible = data.is_tax_deductible;
  if (data.is_recurring != null) body.is_recurring = data.is_recurring;
  if (data.is_reimbursable != null) body.is_reimbursable = data.is_reimbursable;
  if (data.exclude_from_income != null) body.exclude_from_income = data.exclude_from_income;
  if (data.exclude_from_expenses != null) body.exclude_from_expenses = data.exclude_from_expenses;

  const response = await fetch('/api/transactions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Failed to create transaction');
  }
  return transformTransaction(await response.json());
};

/**
 * Update an existing transaction
 * Uses direct fetch — the SDK schema strips entity_id and boolean properties.
 */
export const updateTransaction = async (
  id: number,
  data: TransactionUpdate
): Promise<Transaction> => {
  const body: Record<string, unknown> = {};
  if (data.date != null) body.transaction_date = data.date;
  if (data.description != null) body.description = data.description;
  if (data.amount != null) body.amount = data.amount;
  if (data.transaction_type != null) body.transaction_type = data.transaction_type;
  if (data.category_id != null) body.category_id = data.category_id;
  if (data.account_id != null) body.account_id = data.account_id;
  // Only include entity_id when explicitly provided (undefined = don't change, null = clear)
  if (data.entity_id !== undefined) body.entity_id = data.entity_id;
  if (data.notes != null) body.notes = data.notes;
  if (data.tag_names != null) body.tag_names = data.tag_names;
  if (data.is_capital_expense != null) body.is_capital_expense = data.is_capital_expense;
  if (data.is_tax_deductible != null) body.is_tax_deductible = data.is_tax_deductible;
  if (data.is_recurring != null) body.is_recurring = data.is_recurring;
  if (data.is_reimbursable != null) body.is_reimbursable = data.is_reimbursable;
  if (data.exclude_from_income != null) body.exclude_from_income = data.exclude_from_income;
  if (data.exclude_from_expenses != null) body.exclude_from_expenses = data.exclude_from_expenses;

  const response = await fetch(`/api/transactions/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Failed to update transaction');
  }
  return transformTransaction(await response.json());
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
  const response = await fetch(`/api/transactions/${transactionId}/splits`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(splits.map(s => ({
      amount: s.amount,
      category_id: s.category_id,
      entity_id: s.entity_id ?? null,
      description: s.description ?? null,
      notes: s.notes ?? null,
    }))),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(err.detail || 'Failed to set splits');
  }
};
