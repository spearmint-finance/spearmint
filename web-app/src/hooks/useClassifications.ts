/**
 * React Query hooks for Classification Management
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getClassifications,
  getClassification,
  createClassification,
  updateClassification,
  deleteClassification,
  getClassificationRules,
  getClassificationRule,
  createClassificationRule,
  updateClassificationRule,
  deleteClassificationRule,
  testClassificationRule,
  bulkClassifyTransactions,
  autoClassifyTransactions,
  applyClassificationRules,
} from "../api/classifications";
import type {
  Classification,
  ClassificationCreate,
  ClassificationUpdate,
  ClassificationRule,
  ClassificationRuleCreate,
  ClassificationRuleUpdate,
  TestRuleRequest,
  BulkClassifyRequest,
  AutoClassifyRequest,
  ApplyRulesRequest,
} from "../types/classification";

// Query keys
export const classificationKeys = {
  all: ["classifications"] as const,
  lists: () => [...classificationKeys.all, "list"] as const,
  list: (systemOnly?: boolean) =>
    [...classificationKeys.lists(), { systemOnly }] as const,
  details: () => [...classificationKeys.all, "detail"] as const,
  detail: (id: number) => [...classificationKeys.details(), id] as const,
};

export const classificationRuleKeys = {
  all: ["classificationRules"] as const,
  lists: () => [...classificationRuleKeys.all, "list"] as const,
  list: (activeOnly?: boolean) =>
    [...classificationRuleKeys.lists(), { activeOnly }] as const,
  details: () => [...classificationRuleKeys.all, "detail"] as const,
  detail: (id: number) => [...classificationRuleKeys.details(), id] as const,
};

/**
 * Hook to fetch all classifications
 */
export function useClassifications(systemOnly: boolean = false) {
  return useQuery({
    queryKey: classificationKeys.list(systemOnly),
    queryFn: () => getClassifications(systemOnly),
  });
}

/**
 * Hook to fetch a single classification
 */
export function useClassification(classificationId: number | null) {
  return useQuery({
    queryKey: classificationKeys.detail(classificationId!),
    queryFn: () => getClassification(classificationId!),
    enabled: classificationId !== null,
  });
}

/**
 * Hook to create a new classification
 */
export function useCreateClassification() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ClassificationCreate) => createClassification(data),
    onSuccess: () => {
      // Invalidate all classification lists
      queryClient.invalidateQueries({ queryKey: classificationKeys.lists() });
    },
  });
}

/**
 * Hook to update an existing classification
 */
export function useUpdateClassification() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: ClassificationUpdate;
    }) => updateClassification(id, data),
    onSuccess: (updatedClassification: Classification) => {
      // Invalidate all classification lists
      queryClient.invalidateQueries({ queryKey: classificationKeys.lists() });
      // Update the specific classification in cache
      queryClient.setQueryData(
        classificationKeys.detail(updatedClassification.classification_id),
        updatedClassification
      );
    },
  });
}

/**
 * Hook to delete a classification
 */
export function useDeleteClassification() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (classificationId: number) =>
      deleteClassification(classificationId),
    onSuccess: (_data, classificationId) => {
      // Invalidate all classification lists
      queryClient.invalidateQueries({ queryKey: classificationKeys.lists() });
      // Remove the specific classification from cache
      queryClient.removeQueries({
        queryKey: classificationKeys.detail(classificationId),
      });
    },
  });
}

// ============================================================================
// Classification Rule Hooks
// ============================================================================

/**
 * Hook to fetch all classification rules
 */
export function useClassificationRules(activeOnly: boolean = false) {
  return useQuery({
    queryKey: classificationRuleKeys.list(activeOnly),
    queryFn: () => getClassificationRules(activeOnly),
  });
}

/**
 * Hook to fetch a single classification rule
 */
export function useClassificationRule(ruleId: number | null) {
  return useQuery({
    queryKey: classificationRuleKeys.detail(ruleId!),
    queryFn: () => getClassificationRule(ruleId!),
    enabled: ruleId !== null,
  });
}

/**
 * Hook to create a new classification rule
 */
export function useCreateClassificationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ClassificationRuleCreate) =>
      createClassificationRule(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: classificationRuleKeys.lists() });
    },
  });
}

/**
 * Hook to update an existing classification rule
 */
export function useUpdateClassificationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      id,
      data,
    }: {
      id: number;
      data: ClassificationRuleUpdate;
    }) => updateClassificationRule(id, data),
    onSuccess: (updatedRule: ClassificationRule) => {
      queryClient.invalidateQueries({ queryKey: classificationRuleKeys.lists() });
      queryClient.setQueryData(
        classificationRuleKeys.detail(updatedRule.rule_id),
        updatedRule
      );
    },
  });
}

/**
 * Hook to delete a classification rule
 */
export function useDeleteClassificationRule() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (ruleId: number) => deleteClassificationRule(ruleId),
    onSuccess: (_data, ruleId) => {
      queryClient.invalidateQueries({ queryKey: classificationRuleKeys.lists() });
      queryClient.removeQueries({
        queryKey: classificationRuleKeys.detail(ruleId),
      });
    },
  });
}

/**
 * Hook to test a classification rule
 */
export function useTestClassificationRule() {
  return useMutation({
    mutationFn: (data: TestRuleRequest) => testClassificationRule(data),
  });
}

// ============================================================================
// Transaction Classification Hooks
// ============================================================================

/**
 * Hook to bulk classify multiple transactions
 */
export function useBulkClassifyTransactions() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: BulkClassifyRequest) => bulkClassifyTransactions(data),
    onSuccess: () => {
      // Invalidate transaction queries to refresh the data
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
}

/**
 * Hook to auto-classify transactions using rules
 */
export function useAutoClassifyTransactions() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: AutoClassifyRequest = {}) =>
      autoClassifyTransactions(data),
    onSuccess: () => {
      // Invalidate transaction queries to refresh the data
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
}

/**
 * Hook to apply classification rules to existing transactions
 */
export function useApplyClassificationRules() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ApplyRulesRequest = {}) =>
      applyClassificationRules(data),
    onSuccess: () => {
      // Invalidate transaction queries to refresh the data
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
}
