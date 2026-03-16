import { useQuery } from "@tanstack/react-query";
import {
  getIncomeAnalysis,
  getExpenseAnalysis,
  getCashFlowAnalysis,
  getFinancialHealth,
  getFinancialSummary,
  getCashFlowTrends,
  getExpenseCategoryTrends,
  type AnalysisParams,
  type CategoryTrendsParams,
} from "../api/analysis";

/**
 * Hook to fetch income analysis
 */
export const useIncomeAnalysis = (params?: AnalysisParams) => {
  return useQuery({
    queryKey: ["income-analysis", params],
    queryFn: () => getIncomeAnalysis(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch expense analysis
 */
export const useExpenseAnalysis = (
  params?: AnalysisParams & { top_n?: number }
) => {
  return useQuery({
    queryKey: ["expense-analysis", params],
    queryFn: () => getExpenseAnalysis(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch cash flow analysis
 */
export const useCashFlowAnalysis = (params?: AnalysisParams) => {
  return useQuery({
    queryKey: ["cash-flow-analysis", params],
    queryFn: () => getCashFlowAnalysis(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch financial health indicators
 */
export const useFinancialHealth = (params?: AnalysisParams) => {
  return useQuery({
    queryKey: ["financial-health", params],
    queryFn: () => getFinancialHealth(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

/**
 * Hook to fetch financial summary (comprehensive dashboard data)
 */
export const useFinancialSummary = (
  params?: AnalysisParams & { top_n?: number; recent_count?: number }
) => {
  return useQuery({
    queryKey: ["financial-summary", params],
    queryFn: () => getFinancialSummary(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    placeholderData: (previousData: any) => previousData,
  });
};

/**
 * Hook to fetch cash flow trends over time
 */
export const useCashFlowTrends = (
  params?: AnalysisParams & {
    period?: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  }
) => {
  return useQuery({
    queryKey: ["cash-flow-trends", params],
    queryFn: () => getCashFlowTrends(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    placeholderData: (previousData: any) => previousData,
  });
};

/**
 * Hook to fetch expense category trends over time
 */
export const useExpenseCategoryTrends = (params?: CategoryTrendsParams) => {
  return useQuery({
    queryKey: ["expense-category-trends", params],
    queryFn: () => getExpenseCategoryTrends(params!),
    enabled: !!params,
    staleTime: 5 * 60 * 1000, // 5 minutes
    placeholderData: (previousData: any) => previousData,
  });
};
