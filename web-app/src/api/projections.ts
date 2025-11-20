/**
 * API client for financial projections
 */

import { projectionsApi } from "./sdk";
import {
  IncomeProjectionResponse,
  ExpenseProjectionResponse,
  CashflowProjectionResponse,
  AccuracyMetrics,
  ValidationRequest,
  ProjectionMethodEnum,
} from "../types/projection";

export interface ProjectionQueryParams {
  start_date?: string;
  end_date?: string;
  projection_days?: number;
  method?: ProjectionMethodEnum;
  confidence_level?: number;
  include_scenarios?: boolean;
}

/**
 * Get income projections
 */
export const getIncomeProjection = async (
  params: ProjectionQueryParams = {}
): Promise<IncomeProjectionResponse> => {
  const response = await projectionsApi.projectIncome({
    startDate: params.start_date,
    endDate: params.end_date,
    projectionDays: params.projection_days,
    method: params.method as any, // Cast enum
    confidenceLevel: params.confidence_level
  });
  return response as unknown as IncomeProjectionResponse;
};

/**
 * Get expense projections
 */
export const getExpenseProjection = async (
  params: ProjectionQueryParams = {}
): Promise<ExpenseProjectionResponse> => {
  const response = await projectionsApi.projectExpenses({
    startDate: params.start_date,
    endDate: params.end_date,
    projectionDays: params.projection_days,
    method: params.method as any,
    confidenceLevel: params.confidence_level
  });
  return response as unknown as ExpenseProjectionResponse;
};

/**
 * Get cash flow projections with optional scenario analysis
 */
export const getCashflowProjection = async (
  params: ProjectionQueryParams = {}
): Promise<CashflowProjectionResponse> => {
  const response = await projectionsApi.projectCashFlow({
    startDate: params.start_date,
    endDate: params.end_date,
    projectionDays: params.projection_days,
    method: params.method as any,
    confidenceLevel: params.confidence_level,
    includeScenarios: params.include_scenarios
  });
  return response as unknown as CashflowProjectionResponse;
};

/**
 * Get scenario analysis (always includes scenarios)
 */
export const getScenarios = async (
  params: Omit<ProjectionQueryParams, "include_scenarios"> = {}
): Promise<CashflowProjectionResponse> => {
  const response = await projectionsApi.projectCashFlow({
    startDate: params.start_date,
    endDate: params.end_date,
    projectionDays: params.projection_days,
    method: params.method as any,
    confidenceLevel: params.confidence_level,
    includeScenarios: true
  });
  return response as unknown as CashflowProjectionResponse;
};

/**
 * Validate projection accuracy
 */
export const validateProjection = async (
  data: ValidationRequest
): Promise<AccuracyMetrics> => {
  const response = await projectionsApi.validateProjections({ validationRequest: data });
  return response as unknown as AccuracyMetrics;
};

/**
 * Get all projections (income, expenses, and cashflow) in one call
 */
export const getAllProjections = async (
  params: ProjectionQueryParams = {}
) => {
  const [income, expenses, cashflow] = await Promise.all([
    getIncomeProjection(params),
    getExpenseProjection(params),
    getCashflowProjection({ ...params, include_scenarios: true }),
  ]);

  return {
    income,
    expenses,
    cashflow,
  };
};