/**
 * Custom hooks for category rules API
 */

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { categoryRulesApi } from "../api/categories";
import type {
  CategoryRuleCreate,
  CategoryRuleUpdate,
  TestCategoryRuleRequest,
  ApplyCategoryRulesRequest,
} from "../types/settings";

// Query keys
export const categoryRuleKeys = {
  all: ["categoryRules"] as const,
  lists: () => [...categoryRuleKeys.all, "list"] as const,
  list: (filters: Record<string, any>) =>
    [...categoryRuleKeys.lists(), filters] as const,
  details: () => [...categoryRuleKeys.all, "detail"] as const,
  detail: (id: number) => [...categoryRuleKeys.details(), id] as const,
};

/**
 * Hook to fetch all category rules
 */
export function useCategoryRules(params?: {
  active_only?: boolean;
  category_id?: number;
}) {
  return useQuery({
    queryKey: categoryRuleKeys.list(params || {}),
    queryFn: () => categoryRulesApi.getAll(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to fetch a single category rule
 */
export function useCategoryRule(ruleId: number) {
  return useQuery({
    queryKey: categoryRuleKeys.detail(ruleId),
    queryFn: () => categoryRulesApi.getById(ruleId),
    enabled: !!ruleId,
  });
}

/**
 * Hook to create a category rule
 */
export function useCreateCategoryRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CategoryRuleCreate) => categoryRulesApi.create(data),
    onSuccess: () => {
      // Invalidate and refetch category rules
      queryClient.invalidateQueries({ queryKey: categoryRuleKeys.lists() });
    },
  });
}

/**
 * Hook to update a category rule
 */
export function useUpdateCategoryRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: CategoryRuleUpdate }) =>
      categoryRulesApi.update(id, data),
    onSuccess: (_, variables) => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: categoryRuleKeys.lists() });
      queryClient.invalidateQueries({
        queryKey: categoryRuleKeys.detail(variables.id),
      });
    },
  });
}

/**
 * Hook to delete a category rule
 */
export function useDeleteCategoryRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ruleId: number) => categoryRulesApi.delete(ruleId),
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries({ queryKey: categoryRuleKeys.lists() });
    },
  });
}

/**
 * Hook to test a category rule
 */
export function useTestCategoryRule() {
  return useMutation({
    mutationFn: (request: TestCategoryRuleRequest) =>
      categoryRulesApi.test(request),
  });
}

/**
 * Hook to apply category rules
 */
export function useApplyCategoryRules() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: ApplyCategoryRulesRequest) =>
      categoryRulesApi.apply(request),
    onSuccess: () => {
      // Invalidate transactions since they may have been updated
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
}
