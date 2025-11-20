/**
 * TypeScript types for Classification Management
 */

// Base Classification Types
export interface Classification {
  classification_id: number;
  classification_name: string;
  classification_code: string;
  description: string | null;
  exclude_from_income_calc: boolean;
  exclude_from_expense_calc: boolean;
  exclude_from_cashflow_calc: boolean;
  is_system_classification: boolean;
  created_at: string;
  updated_at: string;
}

export interface ClassificationCreate {
  classification_name: string;
  classification_code: string;
  description?: string;
  exclude_from_income_calc?: boolean;
  exclude_from_expense_calc?: boolean;
  exclude_from_cashflow_calc?: boolean;
}

export interface ClassificationUpdate {
  classification_name?: string;
  description?: string;
  exclude_from_income_calc?: boolean;
  exclude_from_expense_calc?: boolean;
  exclude_from_cashflow_calc?: boolean;
}

export interface ClassificationListResponse {
  classifications: Classification[];
  total: number;
}

// Classification Rule Types
export interface ClassificationRule {
  rule_id: number;
  rule_name: string;
  rule_priority: number;
  classification_id: number;
  is_active: boolean;
  description_pattern: string | null;
  category_pattern: string | null;
  source_pattern: string | null;
  amount_min: number | null;
  amount_max: number | null;
  payment_method_pattern: string | null;
  created_at: string;
  updated_at: string;
}

export interface ClassificationRuleCreate {
  rule_name: string;
  rule_priority?: number;
  classification_id: number;
  is_active?: boolean;
  description_pattern?: string;
  category_pattern?: string;
  source_pattern?: string;
  amount_min?: number;
  amount_max?: number;
  payment_method_pattern?: string;
}

export interface ClassificationRuleUpdate {
  rule_name?: string;
  rule_priority?: number;
  classification_id?: number;
  is_active?: boolean;
  description_pattern?: string | null;
  category_pattern?: string | null;
  source_pattern?: string | null;
  amount_min?: number | null;
  amount_max?: number | null;
  payment_method_pattern?: string | null;
}

export interface ClassificationRuleListResponse {
  rules: ClassificationRule[];
  total: number;
}

// Transaction Classification Types
export interface ClassifyTransactionRequest {
  classification_id: number;
}

export interface BulkClassifyRequest {
  transaction_ids: number[];
  classification_id: number;
}

export interface BulkClassifyResponse {
  success_count: number;
  failed_count: number;
  failed_ids: number[];
}

export interface AutoClassifyRequest {
  transaction_ids?: number[];
  force_reclassify?: boolean;
}

export interface AutoClassifyResponse {
  total_processed: number;
  classified_count: number;
  skipped_count: number;
}

// Rule Testing Types
export interface TestRuleRequest {
  description_pattern?: string;
  category_pattern?: string;
  source_pattern?: string;
  amount_min?: number;
  amount_max?: number;
  payment_method_pattern?: string;
}

export interface TestRuleResponse {
  matching_transactions: number;
  sample_transaction_ids: number[];
}

// Apply Rules Types
export interface ApplyRulesRequest {
  dry_run?: boolean;
  rule_ids?: number[];
}

export interface ApplyRulesResponse {
  dry_run: boolean;
  total_rules_processed: number;
  total_transactions_updated: number;
  rules_applied: Array<{
    rule_id: number;
    rule_name: string;
    classification_name: string;
    transactions_matched: number;
  }>;
}

// UI Helper Types
export interface ClassificationRuleFormData {
  rule_name: string;
  rule_priority: number;
  classification_id: number | "";
  is_active: boolean;
  description_pattern: string;
  category_pattern: string;
  source_pattern: string;
  amount_min: string;
  amount_max: string;
  payment_method_pattern: string;
  transaction_type_filter: "income" | "expense" | "both";
}
