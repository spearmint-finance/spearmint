import { analysisApi } from "./sdk";
import { AnalysisModeEnum } from "@spearmint-money/sdk";

// Analysis API functions

export interface IncomeAnalysisResponse {
  total_income: number;
  transaction_count: number;
  average_transaction: number;
  breakdown_by_category: Record<string, CategoryBreakdown>;
  period_start: string | null;
  period_end: string | null;
  mode: "analysis" | "complete";
}

export interface ExpenseAnalysisResponse {
  total_expenses: number;
  transaction_count: number;
  average_transaction: number;
  breakdown_by_category: Record<string, CategoryBreakdown>;
  top_categories: TopCategory[];
  period_start: string | null;
  period_end: string | null;
  mode: "analysis" | "complete";
}

export interface CategoryBreakdown {
  total: number;
  count: number;
  average: number;
  percentage: number;
}

export interface TopCategory {
  category: string;
  amount: number;
  count: number;
  percentage: number;
}

export interface CashFlowResponse {
  total_income: number;
  total_expenses: number;
  net_cash_flow: number;
  income_count: number;
  expense_count: number;
  period_start: string | null;
  period_end: string | null;
  mode: "analysis" | "complete";
}

export interface FinancialHealthResponse {
  income_to_expense_ratio: number | null;
  savings_rate: number | null;
  average_daily_income: number;
  average_daily_expense: number;
  net_daily_cash_flow: number;
  period_start: string | null;
  period_end: string | null;
}

export interface FinancialSummaryResponse {
  total_income: number;
  total_expenses: number;
  net_cash_flow: number;
  income_count: number;
  expense_count: number;
  top_income_categories: TopCategory[];
  top_expense_categories: TopCategory[];
  recent_transactions: RecentTransaction[];
  financial_health: FinancialHealthResponse;
  period_start: string | null;
  period_end: string | null;
  mode: "analysis" | "complete";
}

export interface RecentTransaction {
  transaction_id: number;
  transaction_date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense";
  category: string | null;
}

export interface AnalysisParams {
  start_date?: string;
  end_date?: string;
  mode?: "analysis" | "with_capital" | "complete";
}

export interface CashFlowTrendPoint {
  period: string;
  income: number;
  expenses: number;
  net_cash_flow: number;
  income_count: number;
  expense_count: number;
}

export interface CashFlowTrendsResponse {
  trends: CashFlowTrendPoint[];
  period_type: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  mode: "analysis" | "complete";
}

// Helper to convert string mode to Enum
const toModeEnum = (mode?: string): AnalysisModeEnum | undefined => {
  if (mode === 'analysis') return AnalysisModeEnum.Analysis;
  if (mode === 'complete') return AnalysisModeEnum.Complete;
  // 'with_capital' might map to Analysis or custom handling in backend logic that might not be in Enum yet.
  // Assuming 'analysis' for now if undefined.
  return undefined;
};

/**
 * Get income analysis
 */
export const getIncomeAnalysis = async (
  params?: AnalysisParams
): Promise<IncomeAnalysisResponse> => {
  const response = await analysisApi.analyzeIncome({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode)
  });
  return response as unknown as IncomeAnalysisResponse;
};

/**
 * Get expense analysis
 */
export const getExpenseAnalysis = async (
  params?: AnalysisParams & { top_n?: number }
): Promise<ExpenseAnalysisResponse> => {
  const response = await analysisApi.analyzeExpenses({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
    topN: params?.top_n
  });
  return response as unknown as ExpenseAnalysisResponse;
};

/**
 * Get cash flow analysis
 */
export const getCashFlowAnalysis = async (
  params?: AnalysisParams
): Promise<CashFlowResponse> => {
  const response = await analysisApi.analyzeCashFlow({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode)
  });
  return response as unknown as CashFlowResponse;
};

/**
 * Get financial health indicators
 */
export const getFinancialHealth = async (
  params?: AnalysisParams
): Promise<FinancialHealthResponse> => {
  const response = await analysisApi.getFinancialHealth({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode)
  });
  return response as unknown as FinancialHealthResponse;
};

/**
 * Get financial summary (comprehensive dashboard data)
 */
export const getFinancialSummary = async (
  params?: AnalysisParams & { top_n?: number; recent_count?: number }
): Promise<FinancialSummaryResponse> => {
  const response = await analysisApi.getFinancialSummary({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
    topN: params?.top_n,
    recentCount: params?.recent_count
  });
  return response as unknown as FinancialSummaryResponse;
};

export const getCashFlowTrends = async (
  params?: AnalysisParams & {
    period?: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  }
): Promise<CashFlowTrendsResponse> => {
  const response = await analysisApi.getCashFlowTrends({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
    period: params?.period as any // Cast to TimePeriodEnum if available
  });
  return response as unknown as CashFlowTrendsResponse;
};

/**
 * Get expense category trends for stacked bar charts
 */
export interface CategoryTrendsParams {
  start_date?: string;
  end_date?: string;
  period?: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  mode?: "analysis" | "with_capital" | "complete";
  top_n?: number;
}

export interface CategoryTrendsResponse {
  periods: string[];
  categories: string[];
  data: Array<{
    period: string;
    [category: string]: string | number;
  }>;
  period_type: string;
  mode: string;
}

export const getExpenseCategoryTrends = async (
  params: CategoryTrendsParams
): Promise<CategoryTrendsResponse> => {
  // Check if this endpoint exists in SDK. 
  // It might be under AnalysisApi -> getExpenseCategoryTrends
  // Assuming naming convention holds.
  const response = await analysisApi.getExpenseCategoryTrends({
    startDate: params.start_date,
    endDate: params.end_date,
    period: params.period as any,
    mode: toModeEnum(params.mode),
    topN: params.top_n
  });
  return response as unknown as CategoryTrendsResponse;
};