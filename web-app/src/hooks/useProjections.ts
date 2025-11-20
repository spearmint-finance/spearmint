/**
 * React Query hooks for financial projections
 */

import { useQuery, useMutation, UseQueryOptions } from "@tanstack/react-query";
import {
  getIncomeProjection,
  getExpenseProjection,
  getCashflowProjection,
  getScenarios,
  validateProjection,
  getAllProjections,
  ProjectionQueryParams,
} from "../api/projections";
import {
  IncomeProjectionResponse,
  ExpenseProjectionResponse,
  CashflowProjectionResponse,
  AccuracyMetrics,
  ValidationRequest,
} from "../types/projection";

/**
 * Hook to fetch income projections
 */
export const useIncomeProjection = (
  params: ProjectionQueryParams = {},
  options?: Omit<
    UseQueryOptions<IncomeProjectionResponse, Error>,
    "queryKey" | "queryFn"
  >
) => {
  return useQuery<IncomeProjectionResponse, Error>({
    queryKey: ["projections", "income", params],
    queryFn: () => getIncomeProjection(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    ...options,
  });
};

/**
 * Hook to fetch expense projections
 */
export const useExpenseProjection = (
  params: ProjectionQueryParams = {},
  options?: Omit<
    UseQueryOptions<ExpenseProjectionResponse, Error>,
    "queryKey" | "queryFn"
  >
) => {
  return useQuery<ExpenseProjectionResponse, Error>({
    queryKey: ["projections", "expenses", params],
    queryFn: () => getExpenseProjection(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    ...options,
  });
};

/**
 * Hook to fetch cash flow projections
 */
export const useCashflowProjection = (
  params: ProjectionQueryParams = {},
  options?: Omit<
    UseQueryOptions<CashflowProjectionResponse, Error>,
    "queryKey" | "queryFn"
  >
) => {
  return useQuery<CashflowProjectionResponse, Error>({
    queryKey: ["projections", "cashflow", params],
    queryFn: () => getCashflowProjection(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    ...options,
  });
};

/**
 * Hook to fetch scenario analysis
 */
export const useScenarios = (
  params: Omit<ProjectionQueryParams, "include_scenarios"> = {},
  options?: Omit<
    UseQueryOptions<CashflowProjectionResponse, Error>,
    "queryKey" | "queryFn"
  >
) => {
  return useQuery<CashflowProjectionResponse, Error>({
    queryKey: ["projections", "scenarios", params],
    queryFn: () => getScenarios(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    ...options,
  });
};

/**
 * Hook to fetch all projections at once
 */
export const useAllProjections = (
  params: ProjectionQueryParams = {},
  options?: Omit<
    UseQueryOptions<
      {
        income: IncomeProjectionResponse;
        expenses: ExpenseProjectionResponse;
        cashflow: CashflowProjectionResponse;
      },
      Error
    >,
    "queryKey" | "queryFn"
  >
) => {
  return useQuery({
    queryKey: ["projections", "all", params],
    queryFn: () => getAllProjections(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    ...options,
  });
};

/**
 * Hook to validate projection accuracy
 */
export const useValidateProjection = () => {
  return useMutation<AccuracyMetrics, Error, ValidationRequest>({
    mutationFn: validateProjection,
  });
};

