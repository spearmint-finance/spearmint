import { analysisApi } from "./sdk";
import { GetIncomeAnalysisApiAnalysisIncomeGetMode } from "@spearmint-finance/sdk";

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
const toModeEnum = (
  mode?: string
): GetIncomeAnalysisApiAnalysisIncomeGetMode | undefined => {
  if (mode === "analysis")
    return GetIncomeAnalysisApiAnalysisIncomeGetMode.ANALYSIS;
  if (mode === "complete")
    return GetIncomeAnalysisApiAnalysisIncomeGetMode.COMPLETE;
  if (mode === "with_capital")
    return GetIncomeAnalysisApiAnalysisIncomeGetMode.WITH_CAPITAL;
  return undefined;
};

/**
 * Get income analysis
 */
export const getIncomeAnalysis = async (
  params?: AnalysisParams
): Promise<IncomeAnalysisResponse> => {
  const { data } = await analysisApi.getIncomeAnalysisApiAnalysisIncomeGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
  });
  if (!data) {
    throw new Error("Empty response from income analysis API");
  }
  return {
    total_income: Number(data.totalIncome),
    transaction_count: data.transactionCount,
    average_transaction: Number(data.averageTransaction),
    breakdown_by_category: Object.fromEntries(
      Object.entries(data.breakdownByCategory ?? {}).map(
        ([key, value]: any) => [
          key,
          {
            total: Number(value.total),
            count: value.count,
            average: Number(value.average),
            percentage: value.percentage,
          },
        ]
      )
    ),
    period_start: data.periodStart ?? null,
    period_end: data.periodEnd ?? null,
    mode: (data.mode as "analysis" | "complete") ?? "analysis",
  };
};

/**
 * Get expense analysis
 */
export const getExpenseAnalysis = async (
  params?: AnalysisParams & { top_n?: number }
): Promise<ExpenseAnalysisResponse> => {
  const { data } = await analysisApi.getExpenseAnalysisApiAnalysisExpensesGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
    topN: params?.top_n,
  });
  if (!data) {
    throw new Error("Empty response from expense analysis API");
  }
  return {
    total_expenses: Number(data.totalExpenses),
    transaction_count: data.transactionCount,
    average_transaction: Number(data.averageTransaction),
    breakdown_by_category: Object.fromEntries(
      Object.entries(data.breakdownByCategory ?? {}).map(
        ([key, value]: any) => [
          key,
          {
            total: Number(value.total),
            count: value.count,
            average: Number(value.average),
            percentage: value.percentage,
          },
        ]
      )
    ),
    top_categories: (data.topCategories ?? []).map((cat) => ({
      category: cat.category,
      amount: Number(cat.amount),
      count: cat.count,
      percentage: cat.percentage,
    })),
    period_start: data.periodStart ?? null,
    period_end: data.periodEnd ?? null,
    mode: (data.mode as "analysis" | "complete") ?? "analysis",
  };
};

/**
 * Get cash flow analysis
 */
export const getCashFlowAnalysis = async (
  params?: AnalysisParams
): Promise<CashFlowResponse> => {
  const { data } = await analysisApi.getCashFlowAnalysisApiAnalysisCashflowGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
  });
  if (!data) {
    throw new Error("Empty response from cash flow analysis API");
  }
  return {
    total_income: Number(data.totalIncome),
    total_expenses: Number(data.totalExpenses),
    net_cash_flow: Number(data.netCashFlow),
    income_count: data.incomeCount,
    expense_count: data.expenseCount,
    period_start: data.periodStart ?? null,
    period_end: data.periodEnd ?? null,
    mode: (data.mode as "analysis" | "complete") ?? "analysis",
  };
};

/**
 * Get financial health indicators
 */
export const getFinancialHealth = async (
  params?: AnalysisParams
): Promise<FinancialHealthResponse> => {
  const { data } = await analysisApi.getFinancialHealthApiAnalysisHealthGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
  });
  if (!data) {
    throw new Error("Empty response from financial health API");
  }
  return {
    income_to_expense_ratio: data.incomeToExpenseRatio ?? null,
    savings_rate: data.savingsRate ?? null,
    average_daily_income: Number(data.averageDailyIncome),
    average_daily_expense: Number(data.averageDailyExpense),
    net_daily_cash_flow: Number(data.netDailyCashFlow),
    period_start: data.periodStart ?? null,
    period_end: data.periodEnd ?? null,
  };
};

/**
 * Get financial summary (comprehensive dashboard data)
 */
export const getFinancialSummary = async (
  params?: AnalysisParams & { top_n?: number; recent_count?: number }
): Promise<FinancialSummaryResponse> => {
  const { data } = await analysisApi.getFinancialSummaryApiAnalysisSummaryGet({
    startDate: params?.start_date,
    endDate: params?.end_date,
    mode: toModeEnum(params?.mode),
    topN: params?.top_n,
    recentCount: params?.recent_count,
  });
  if (!data) {
    throw new Error("Empty response from financial summary API");
  }
  return {
    total_income: Number(data.totalIncome),
    total_expenses: Number(data.totalExpenses),
    net_cash_flow: Number(data.netCashFlow),
    income_count: data.incomeCount,
    expense_count: data.expenseCount,
    top_income_categories: (data.topIncomeCategories ?? []).map((cat) => ({
      category: cat.category,
      amount: Number(cat.amount),
      count: cat.count,
      percentage: cat.percentage,
    })),
    top_expense_categories: (data.topExpenseCategories ?? []).map((cat) => ({
      category: cat.category,
      amount: Number(cat.amount),
      count: cat.count,
      percentage: cat.percentage,
    })),
    recent_transactions: (data.recentTransactions ?? []).map((txn) => ({
      transaction_id: txn.transactionId,
      transaction_date: txn.transactionDate,
      description: txn.description,
      amount: Number(txn.amount),
      transaction_type: txn.transactionType as "Income" | "Expense",
      category: txn.category ?? null,
    })),
    financial_health: {
      income_to_expense_ratio:
        data.financialHealth.incomeToExpenseRatio ?? null,
      savings_rate: data.financialHealth.savingsRate ?? null,
      average_daily_income: Number(data.financialHealth.averageDailyIncome),
      average_daily_expense: Number(data.financialHealth.averageDailyExpense),
      net_daily_cash_flow: Number(data.financialHealth.netDailyCashFlow),
      period_start: data.financialHealth.periodStart ?? null,
      period_end: data.financialHealth.periodEnd ?? null,
    },
    period_start: data.periodStart ?? null,
    period_end: data.periodEnd ?? null,
    mode: (data.mode as "analysis" | "complete") ?? "analysis",
  };
};

export const getCashFlowTrends = async (
  params?: AnalysisParams & {
    period?: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  }
): Promise<CashFlowTrendsResponse> => {
  const { data } =
    await analysisApi.getCashFlowTrendsApiAnalysisCashflowTrendsGet({
      startDate: params?.start_date,
      endDate: params?.end_date,
      mode: toModeEnum(params?.mode),
      period: params?.period as any, // Cast to TimePeriodEnum if available
    });
  if (!data) {
    throw new Error("Empty response from cash flow trends API");
  }
  return {
    trends: (data.trends ?? []).map((t) => ({
      period: t.period,
      income: Number(t.income),
      expenses: Number(t.expenses),
      net_cash_flow: Number(t.netCashFlow),
      income_count: t.incomeCount,
      expense_count: t.expenseCount,
    })),
    period_type: data.periodType as any,
    mode: (data.mode as "analysis" | "complete") ?? "analysis",
  };
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
  const { data } =
    await analysisApi.getExpenseCategoryTrendsApiAnalysisExpensesCategoryTrendsGet(
      {
        startDate: params.start_date,
        endDate: params.end_date,
        period: params.period as any,
        mode: toModeEnum(params.mode),
        topN: params.top_n,
      }
    );
  if (!data) {
    throw new Error("Empty response from expense category trends API");
  }
  return data as CategoryTrendsResponse;
};
