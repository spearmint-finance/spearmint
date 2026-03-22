/**
 * Settings and configuration types
 */

// Category types
export interface Category {
  category_id: number;
  category_name: string;
  category_type: "Income" | "Expense" | "Both" | "Transfer";
  parent_category_id: number | null;
  description: string | null;
  entity_id: number | null;
  created_at: string;
  updated_at?: string;
  transaction_count?: number | null;
}

export interface CategoryCreate {
  category_name: string;
  category_type: "Income" | "Expense" | "Both" | "Transfer";
  parent_category_id?: number | null;
  description?: string | null;
  entity_id?: number | null;
}

export interface CategoryUpdate {
  category_name?: string;
  category_type?: "Income" | "Expense" | "Both" | "Transfer";
  parent_category_id?: number | null;
  description?: string | null;
  entity_id?: number | null;
}

export interface CategoriesResponse {
  categories: Category[];
  total: number;
}

// Category Rule types
export interface CategoryRule {
  rule_id: number;
  rule_name: string;
  rule_priority: number;
  category_id: number;
  is_active: boolean;
  description_pattern: string | null;
  source_pattern: string | null;
  amount_min: number | null;
  amount_max: number | null;
  payment_method_pattern: string | null;
  transaction_type_pattern: "Income" | "Expense" | null;
  created_at: string;
  updated_at: string;
}

export interface CategoryRuleCreate {
  rule_name: string;
  rule_priority?: number;
  category_id: number;
  is_active?: boolean;
  description_pattern?: string | null;
  source_pattern?: string | null;
  amount_min?: number | null;
  amount_max?: number | null;
  payment_method_pattern?: string | null;
  transaction_type_pattern?: "Income" | "Expense" | null;
}

export interface CategoryRuleUpdate {
  rule_name?: string;
  rule_priority?: number;
  category_id?: number;
  is_active?: boolean;
  description_pattern?: string | null;
  source_pattern?: string | null;
  amount_min?: number | null;
  amount_max?: number | null;
  payment_method_pattern?: string | null;
  transaction_type_pattern?: "Income" | "Expense" | null;
}

export interface CategoryRuleListResponse {
  rules: CategoryRule[];
  total: number;
}

export interface TestCategoryRuleRequest {
  description_pattern?: string | null;
  source_pattern?: string | null;
  amount_min?: number | null;
  amount_max?: number | null;
  payment_method_pattern?: string | null;
  transaction_type_pattern?: "Income" | "Expense" | null;
  limit?: number;
}

export interface TestCategoryRuleResponse {
  total_matches: number;
  sample_transactions: Array<{
    transaction_id: number;
    transaction_date: string;
    amount: number;
    transaction_type: string;
    description: string | null;
    source: string | null;
    payment_method: string | null;
    category_name: string | null;
  }>;
  has_more: boolean;
}

export interface ApplyCategoryRulesRequest {
  transaction_ids?: number[] | null;
  rule_ids?: number[] | null;
  force_recategorize?: boolean;
}

export interface ApplyCategoryRulesResponse {
  total_processed: number;
  categorized_count: number;
  skipped_count: number;
  rules_applied: number;
}

// User preferences types
export interface UserPreferences {
  defaultDateRange: "week" | "month" | "quarter" | "year" | "custom";
  defaultStartDate?: string;
  defaultEndDate?: string;
  currencySymbol: string;
  currencyPosition: "before" | "after";
  decimalPlaces: number;
  thousandsSeparator: "," | "." | " " | "";
  decimalSeparator: "." | ",";
  dateFormat: "MM/DD/YYYY" | "DD/MM/YYYY" | "YYYY-MM-DD";
  timeFormat: "12h" | "24h";
  firstDayOfWeek: 0 | 1; // 0 = Sunday, 1 = Monday
  enableNotifications: boolean;
  notificationEmail?: string;
}

// Theme types
export interface ThemeSettings {
  mode: "light" | "dark" | "system";
  primaryColor: string;
  secondaryColor: string;
  fontSize: "small" | "medium" | "large";
  fontFamily: string;
  compactMode: boolean;
}

// Export types
export interface ExportOptions {
  format: "csv" | "excel" | "pdf";
  dateRange: {
    start: string;
    end: string;
  };
  includeColumns: string[];
  filters?: {
    transactionType?: "Income" | "Expense";
    categories?: number[];
    minAmount?: number;
    maxAmount?: number;
  };
}

export interface ExportResponse {
  downloadUrl: string;
  filename: string;
  size: number;
  expiresAt: string;
}

// Settings tabs
export type SettingsTab = "categories" | "preferences" | "theme" | "export";
