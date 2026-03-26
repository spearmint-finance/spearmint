import { useQuery, useMutation, useQueryClient, keepPreviousData } from "@tanstack/react-query";
import {
  getTransactions,
  getTransaction,
  createTransaction,
  updateTransaction,
  deleteTransaction,
  setTransactionSplits,
  type TransactionListParams,
} from "../api/transactions";
import type {
  TransactionCreate,
  TransactionUpdate,
} from "../types/transaction";

/**
 * Hook to fetch list of transactions
 */
export const useTransactions = (params?: TransactionListParams) => {
  return useQuery({
    queryKey: ["transactions", params],
    queryFn: () => getTransactions(params),
    placeholderData: keepPreviousData, // keep rows/rowCount while fetching next page to avoid UI reset
  });
};

/**
 * Hook to fetch a single transaction
 */
export const useTransaction = (id: number) => {
  return useQuery({
    queryKey: ["transaction", id],
    queryFn: () => getTransaction(id),
    enabled: !!id,
  });
};

/**
 * Hook to create a new transaction
 */
export const useCreateTransaction = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: TransactionCreate) => createTransaction(data),
    onSuccess: () => {
      // Invalidate and refetch transactions list
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      // Also invalidate analysis data since it depends on transactions
      queryClient.invalidateQueries({ queryKey: ["income-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["expense-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["cash-flow-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["financial-health"] });
    },
  });
};

/**
 * Hook to update an existing transaction
 */
export const useUpdateTransaction = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: TransactionUpdate }) =>
      updateTransaction(id, data),
    onSuccess: (_, variables) => {
      // Invalidate the specific transaction
      queryClient.invalidateQueries({
        queryKey: ["transaction", variables.id],
      });
      // Invalidate transactions list
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      // Invalidate analysis data
      queryClient.invalidateQueries({ queryKey: ["income-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["expense-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["cash-flow-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["financial-health"] });
    },
  });
};

/**
 * Hook to delete a transaction
 */
export const useDeleteTransaction = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteTransaction(id),
    onSuccess: () => {
      // Invalidate transactions list
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      // Invalidate analysis data
      queryClient.invalidateQueries({ queryKey: ["income-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["expense-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["cash-flow-analysis"] });
      queryClient.invalidateQueries({ queryKey: ["financial-health"] });
    },
  });
};

/**
 * Hook to set splits for a transaction
 */
export const useSetTransactionSplits = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, splits }: { id: number; splits: Parameters<typeof setTransactionSplits>[1] }) =>
      setTransactionSplits(id, splits),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["transaction", variables.id] });
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
};
