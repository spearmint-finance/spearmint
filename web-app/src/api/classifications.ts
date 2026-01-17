/**
 * API client for Classification Management
 */

import { classificationsApi } from "./sdk";
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
  const response =
    await classificationsApi.listClassificationsApiClassificationsGet({
      systemOnly,
    });
  return response.data as unknown as ClassificationListResponse;
};

/**
 * Get a single classification by ID
 */
export const getClassification = async (
  classificationId: number
): Promise<Classification> => {
  const response =
    await classificationsApi.getClassificationApiClassificationsClassificationIdGet(
      classificationId
    );
  return response.data as unknown as Classification;
};

/**
 * Create a new classification
 */
export const createClassification = async (
  data: ClassificationCreate
): Promise<Classification> => {
  const response =
    await classificationsApi.createClassificationApiClassificationsPost(data);
  return response.data as unknown as Classification;
};

/**
 * Update an existing classification
 */
export const updateClassification = async (
  classificationId: number,
  data: ClassificationUpdate
): Promise<Classification> => {
  const response =
    await classificationsApi.updateClassificationApiClassificationsClassificationIdPut(
      classificationId,
      data
    );
  return response.data as unknown as Classification;
};

/**
 * Delete a classification
 */
export const deleteClassification = async (
  classificationId: number
): Promise<void> => {
  await classificationsApi.deleteClassificationApiClassificationsClassificationIdDelete(
    classificationId
  );
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
  const response =
    await classificationsApi.listClassificationRulesApiClassificationRulesGet({
      activeOnly,
    });
  return response.data as unknown as ClassificationRuleListResponse;
};

/**
 * Get a single classification rule by ID
 */
export const getClassificationRule = async (
  ruleId: number
): Promise<ClassificationRule> => {
  const response =
    await classificationsApi.getClassificationRuleApiClassificationRulesRuleIdGet(
      ruleId
    );
  return response.data as unknown as ClassificationRule;
};

/**
 * Create a new classification rule
 */
export const createClassificationRule = async (
  data: ClassificationRuleCreate
): Promise<ClassificationRule> => {
  const response =
    await classificationsApi.createClassificationRuleApiClassificationRulesPost(
      data
    );
  return response.data as unknown as ClassificationRule;
};

/**
 * Update an existing classification rule
 */
export const updateClassificationRule = async (
  ruleId: number,
  data: ClassificationRuleUpdate
): Promise<ClassificationRule> => {
  const response =
    await classificationsApi.updateClassificationRuleApiClassificationRulesRuleIdPut(
      ruleId,
      data
    );
  return response.data as unknown as ClassificationRule;
};

/**
 * Delete a classification rule
 */
export const deleteClassificationRule = async (
  ruleId: number
): Promise<void> => {
  await classificationsApi.deleteClassificationRuleApiClassificationRulesRuleIdDelete(
    ruleId
  );
};

/**
 * Test a classification rule to see how many transactions it would match
 */
export const testClassificationRule = async (
  data: TestRuleRequest
): Promise<TestRuleResponse> => {
  const response =
    await classificationsApi.testClassificationRuleApiClassificationRulesTestPost(
      data
    );
  return response.data as unknown as TestRuleResponse;
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
  const response =
    await classificationsApi.classifyTransactionApiTransactionsTransactionIdClassifyPost(
      transactionId,
      data
    );
  return response.data as unknown as Classification;
};

/**
 * Bulk classify multiple transactions
 */
export const bulkClassifyTransactions = async (
  data: BulkClassifyRequest
): Promise<BulkClassifyResponse> => {
  const response =
    await classificationsApi.bulkClassifyTransactionsApiTransactionsClassifyBulkPost(
      data
    );
  return response.data as unknown as BulkClassifyResponse;
};

/**
 * Auto-classify transactions using rules
 */
export const autoClassifyTransactions = async (
  data: AutoClassifyRequest = {}
): Promise<AutoClassifyResponse> => {
  const response =
    await classificationsApi.autoClassifyTransactionsApiTransactionsAutoClassifyPost(
      data
    );
  return response.data as unknown as AutoClassifyResponse;
};

/**
 * Apply classification rules to existing transactions
 */
export const applyClassificationRules = async (
  data: ApplyRulesRequest = {}
): Promise<ApplyRulesResponse> => {
  const response =
    await classificationsApi.applyClassificationRulesApiClassificationRulesApplyPost(
      data
    );
  return response.data as unknown as ApplyRulesResponse;
};
