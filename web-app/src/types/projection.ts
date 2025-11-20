/**
 * TypeScript types for financial projections
 * Matches backend API schemas from src/financial_analysis/api/schemas/projection.py
 */

export enum ProjectionMethod {
  LINEAR_REGRESSION = "linear_regression",
  MOVING_AVERAGE = "moving_average",
  EXPONENTIAL_SMOOTHING = "exponential_smoothing",
  WEIGHTED_AVERAGE = "weighted_average",
}

export enum ScenarioType {
  BEST_CASE = "best_case",
  EXPECTED = "expected",
  WORST_CASE = "worst_case",
}

export interface ProjectionRequest {
  start_date?: string;
  end_date?: string;
  projection_days: number;
  method: ProjectionMethod;
  confidence_level: number;
}

export interface CashflowProjectionRequest extends ProjectionRequest {
  include_scenarios: boolean;
}

export interface HistoricalPeriod {
  start_date: string;
  end_date: string;
  days: number;
  total_income?: number;
  total_expenses?: number;
  average_daily: number;
}

export interface ProjectionPeriod {
  start_date: string;
  end_date: string;
  days: number;
}

export interface ConfidenceInterval {
  lower: number;
  upper: number;
  range: number;
}

export interface DailyProjection {
  date: string;
  projected_value: number;
  lower_bound: number;
  upper_bound: number;
}

export interface CashflowDailyProjection {
  date: string;
  projected_income: number;
  projected_expenses: number;
  projected_cashflow: number;
  cashflow_lower: number;
  cashflow_upper: number;
}

export interface ModelMetrics {
  r_squared?: number;
  slope?: number;
  intercept?: number;
  std_error?: number;
  moving_average?: number;
  std_deviation?: number;
  window_size?: number;
  smoothed_value?: number;
  alpha?: number;
  weighted_average?: number;
  weighted_std?: number;
  sample_size?: number;
}

export interface IncomeProjectionResponse {
  projection_type: string;
  historical_period: HistoricalPeriod;
  projection_period: ProjectionPeriod;
  method: string;
  confidence_level: number;
  projected_total: number;
  confidence_interval: ConfidenceInterval;
  daily_projections: DailyProjection[];
  model_metrics: ModelMetrics;
}

export interface ExpenseProjectionResponse {
  projection_type: string;
  historical_period: HistoricalPeriod;
  projection_period: ProjectionPeriod;
  method: string;
  confidence_level: number;
  projected_total: number;
  confidence_interval: ConfidenceInterval;
  daily_projections: DailyProjection[];
  model_metrics: ModelMetrics;
}

export interface ScenarioData {
  income: number;
  expenses: number;
  cashflow: number;
  description: string;
}

export interface ScenarioRange {
  cashflow_range: number;
  income_range: number;
  expense_range: number;
}

export interface Scenarios {
  expected: ScenarioData;
  best_case: ScenarioData;
  worst_case: ScenarioData;
  range: ScenarioRange;
}

export interface CashflowProjectionResponse {
  projection_type: string;
  historical_period: HistoricalPeriod;
  projection_period: ProjectionPeriod;
  method: string;
  confidence_level: number;
  projected_income: number;
  projected_expenses: number;
  projected_cashflow: number;
  confidence_interval: ConfidenceInterval;
  daily_projections: CashflowDailyProjection[];
  scenarios?: Scenarios;
}

export interface AccuracyMetrics {
  mape: number;
  rmse: number;
  mae: number;
  r_squared: number;
  sample_size: number;
  accuracy_grade: string;
}

export interface ValidationRequest {
  actual_values: number[];
  predicted_values: number[];
}

// UI-specific types for projection controls
export interface ProjectionParams {
  projectionDays: number;
  method: ProjectionMethod;
  confidenceLevel: number;
  includeScenarios: boolean;
}

// Chart data types
export interface ProjectionChartData {
  date: string;
  projected: number;
  lowerBound: number;
  upperBound: number;
  income?: number;
  expenses?: number;
}

