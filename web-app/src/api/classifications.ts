/**
 * API client for Classification Management
 */

import apiClient from "./client";
import type {
  Classification,
  ClassificationCreate,
  ClassificationUpdate,
  ClassificationListResponse,
  ClassificationRule,
  ClassificationRuleCreate,
  ClassificationRuleUpdate,
  ClassificationRuleListResponse,
  ClassifyTransactionRequest,
  BulkClassifyRequest,
  BulkClassifyResponse,
  AutoClassifyRequest,
  AutoClassifyResponse,
  TestRuleRequest,
  TestRuleResponse,
  ApplyRulesRequest,
  ApplyRulesResponse,
} from "../types/classification";

// ============================================================================
// Classification CRUD Operations
// ============================================================================

/**
 * Get all classifications
 */
export const getClassifications = async (
  systemOnly: boolean = false
): Promise<ClassificationListResponse> => {
  const response = await apiClient.get<ClassificationListResponse>(
    "/classifications",
    {
      params: { system_only: systemOnly },
    }
  );
  return response.data;
};

/**
 * Get a single classification by ID
 */
export const getClassification = async (
  classificationId: number
): Promise<Classification> => {
  const response = await apiClient.get<Classification>(
    `/classifications/${classificationId}`
  );
  return response.data;
};

/**
 * Create a new classification
 */
export const createClassification = async (
  data: ClassificationCreate
): Promise<Classification> => {
  const response = await apiClient.post<Classification>(
    "/classifications",
    data
  );
  return response.data;
};

/**
 * Update an existing classification
 */
export const updateClassification = async (
  classificationId: number,
  data: ClassificationUpdate
): Promise<Classification> => {
  const response = await apiClient.put<Classification>(
    `/classifications/${classificationId}`,
    data
  );
  return response.data;
};

/**
 * Delete a classification
 */
export const deleteClassification = async (
  classificationId: number
): Promise<void> => {
  await apiClient.delete(`/classifications/${classificationId}`);
};

// ============================================================================
// Classification Rule CRUD Operations
// ============================================================================

/**
 * Get all classification rules
 */
export const getClassificationRules = async (
  activeOnly: boolean = false
): Promise<ClassificationRuleListResponse> => {
  const response = await apiClient.get<ClassificationRuleListResponse>(
    "/classification-rules",
    {
      params: { active_only: activeOnly },
    }
  );
  return response.data;
};

/**
 * Get a single classification rule by ID
 */
export const getClassificationRule = async (
  ruleId: number
): Promise<ClassificationRule> => {
  const response = await apiClient.get<ClassificationRule>(
    `/classification-rules/${ruleId}`
  );
  return response.data;
};

/**
 * Create a new classification rule
 */
export const createClassificationRule = async (
  data: ClassificationRuleCreate
): Promise<ClassificationRule> => {
  const response = await apiClient.post<ClassificationRule>(
    "/classification-rules",
    data
  );
  return response.data;
};

/**
 * Update an existing classification rule
 */
export const updateClassificationRule = async (
  ruleId: number,
  data: ClassificationRuleUpdate
): Promise<ClassificationRule> => {
  const response = await apiClient.put<ClassificationRule>(
    `/classification-rules/${ruleId}`,
    data
  );
  return response.data;
};

/**
 * Delete a classification rule
 */
export const deleteClassificationRule = async (
  ruleId: number
): Promise<void> => {
  await apiClient.delete(`/classification-rules/${ruleId}`);
};

/**
 * Test a classification rule to see how many transactions it would match
 */
export const testClassificationRule = async (
  data: TestRuleRequest
): Promise<TestRuleResponse> => {
  const response = await apiClient.post<TestRuleResponse>(
    "/classification-rules/test",
    data
  );
  return response.data;
};

// ============================================================================
// Transaction Classification Operations
// ============================================================================

/**
 * Classify a single transaction
 */
export const classifyTransaction = async (
  transactionId: number,
  data: ClassifyTransactionRequest
): Promise<Classification> => {
  const response = await apiClient.post<Classification>(
    `/transactions/${transactionId}/classify`,
    data
  );
  return response.data;
};

/**
 * Bulk classify multiple transactions
 */
export const bulkClassifyTransactions = async (
  data: BulkClassifyRequest
): Promise<BulkClassifyResponse> => {
  const response = await apiClient.post<BulkClassifyResponse>(
    "/transactions/bulk-classify",
    data
  );
  return response.data;
};

/**
 * Auto-classify transactions using rules
 */
export const autoClassifyTransactions = async (
  data: AutoClassifyRequest = {}
): Promise<AutoClassifyResponse> => {
  const response = await apiClient.post<AutoClassifyResponse>(
    "/classifications/auto-classify",
    data
  );
  return response.data;
};

/**
 * Apply classification rules to existing transactions
 */
export const applyClassificationRules = async (
  data: ApplyRulesRequest = {}
): Promise<ApplyRulesResponse> => {
  const response = await apiClient.post<ApplyRulesResponse>(
    "/classification-rules/apply",
    data
  );
  return response.data;
};

