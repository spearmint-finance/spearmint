/**
 * React Query hooks for category management
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { categoriesApi } from "../api/categories";
import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
} from "../types/settings";

/**
 * Query key factory for categories
 */
export const categoryKeys = {
  all: ["categories"] as const,
  lists: () => [...categoryKeys.all, "list"] as const,
  list: (filters?: Record<string, unknown>) =>
    [...categoryKeys.lists(), filters] as const,
  details: () => [...categoryKeys.all, "detail"] as const,
  detail: (id: number) => [...categoryKeys.details(), id] as const,
  roots: (type?: string) => [...categoryKeys.all, "roots", type] as const,
  children: (id: number) => [...categoryKeys.all, "children", id] as const,
};

/**
 * Hook to fetch all categories with optional filters
 */
export function useCategories(params?: {
  category_type?: "Income" | "Expense" | "Both" | "Transfer";
  parent_category_id?: number | null;
  search_text?: string;
}) {
  return useQuery({
    queryKey: categoryKeys.list(params),
    queryFn: () => categoriesApi.getAll(params),
    staleTime: 5 * 60 * 1000, // 5 minutes - categories don't change often
  });
}

/**
 * Hook to fetch a single category by ID
 */
export function useCategory(categoryId: number) {
  return useQuery({
    queryKey: categoryKeys.detail(categoryId),
    queryFn: () => categoriesApi.getById(categoryId),
    enabled: !!categoryId,
  });
}

/**
 * Hook to fetch root categories
 */
export function useRootCategories(
  categoryType?: "Income" | "Expense" | "Both" | "Transfer"
) {
  return useQuery({
    queryKey: categoryKeys.roots(categoryType),
    queryFn: () => categoriesApi.getRootCategories(categoryType),
    staleTime: 5 * 60 * 1000,
  });
}

/**
 * Hook to fetch child categories
 */
export function useChildCategories(categoryId: number) {
  return useQuery({
    queryKey: categoryKeys.children(categoryId),
    queryFn: () => categoriesApi.getChildren(categoryId),
    enabled: !!categoryId,
  });
}

/**
 * Hook to create a new category
 */
export function useCreateCategory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (category: CategoryCreate) => categoriesApi.create(category),
    onSuccess: () => {
      // Invalidate all category queries to refetch
      queryClient.invalidateQueries({ queryKey: categoryKeys.all });
    },
  });
}

/**
 * Hook to update a category
 */
export function useUpdateCategory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      categoryId,
      category,
    }: {
      categoryId: number;
      category: CategoryUpdate;
    }) => categoriesApi.update(categoryId, category),
    onSuccess: (data) => {
      // Invalidate all category queries
      queryClient.invalidateQueries({ queryKey: categoryKeys.all });
      // Update the specific category in cache
      queryClient.setQueryData(categoryKeys.detail(data.category_id), data);
    },
  });
}

/**
 * Hook to delete a category
 */
export function useDeleteCategory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      categoryId,
      force,
    }: {
      categoryId: number;
      force?: boolean;
    }) => categoriesApi.delete(categoryId, force),
    onSuccess: () => {
      // Invalidate all category queries to refetch
      queryClient.invalidateQueries({ queryKey: categoryKeys.all });
    },
  });
}
