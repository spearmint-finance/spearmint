/**
 * API client for financial projections
 */

import apiClient from "./client";
import {
  IncomeProjectionResponse,
  ExpenseProjectionResponse,
  CashflowProjectionResponse,
  AccuracyMetrics,
  ValidationRequest,
  ProjectionMethod,
} from "../types/projection";

export interface ProjectionQueryParams {
  start_date?: string;
  end_date?: string;
  projection_days?: number;
  method?: ProjectionMethod;
  confidence_level?: number;
  include_scenarios?: boolean;
}

/**
 * Get income projections
 */
export const getIncomeProjection = async (
  params: ProjectionQueryParams = {}
): Promise<IncomeProjectionResponse> => {
  const response = await apiClient.get<IncomeProjectionResponse>(
    "/projections/income",
    { params }
  );
  return response.data;
};

/**
 * Get expense projections
 */
export const getExpenseProjection = async (
  params: ProjectionQueryParams = {}
): Promise<ExpenseProjectionResponse> => {
  const response = await apiClient.get<ExpenseProjectionResponse>(
    "/projections/expenses",
    { params }
  );
  return response.data;
};

/**
 * Get cash flow projections with optional scenario analysis
 */
export const getCashflowProjection = async (
  params: ProjectionQueryParams = {}
): Promise<CashflowProjectionResponse> => {
  const response = await apiClient.get<CashflowProjectionResponse>(
    "/projections/cashflow",
    { params }
  );
  return response.data;
};

/**
 * Get scenario analysis (always includes scenarios)
 */
export const getScenarios = async (
  params: Omit<ProjectionQueryParams, "include_scenarios"> = {}
): Promise<CashflowProjectionResponse> => {
  const response = await apiClient.get<CashflowProjectionResponse>(
    "/projections/scenarios",
    { params }
  );
  return response.data;
};

/**
 * Validate projection accuracy
 */
export const validateProjection = async (
  data: ValidationRequest
): Promise<AccuracyMetrics> => {
  const response = await apiClient.post<AccuracyMetrics>(
    "/projections/validate",
    data
  );
  return response.data;
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

