import { categoriesApi as categoriesClient } from "./sdk";
import type {
  Category,
  CategoryCreate,
  CategoryUpdate,
  CategoriesResponse,
  CategoryRule,
  CategoryRuleCreate,
  CategoryRuleUpdate,
  CategoryRuleListResponse,
  TestCategoryRuleRequest,
  TestCategoryRuleResponse,
  ApplyCategoryRulesRequest,
  ApplyCategoryRulesResponse,
} from "../types/settings";

export const categoriesApi = {
  /**
   * Get all categories with optional filters
   */
  getAll: async (params?: {
    category_type?: "Income" | "Expense" | "Both";
    parent_category_id?: number | null;
    include_transfer_categories?: boolean;
    search_text?: string;
  }): Promise<CategoriesResponse> => {
    const response = await categoriesClient.listCategories({
      categoryType: params?.category_type,
      parentCategoryId: params?.parent_category_id,
      includeTransferCategories: params?.include_transfer_categories,
      searchText: params?.search_text
    });
    return response as unknown as CategoriesResponse;
  },

  /**
   * Get a single category by ID
   */
  getById: async (categoryId: number): Promise<Category> => {
    const response = await categoriesClient.getCategory({ categoryId });
    return response as unknown as Category;
  },

  /**
   * Get root categories (no parent)
   */
  getRootCategories: async (
    categoryType?: "Income" | "Expense" | "Both"
  ): Promise<CategoriesResponse> => {
    const response = await categoriesClient.listRootCategories({ categoryType });
    return response as unknown as CategoriesResponse;
  },

  /**
   * Get child categories of a parent
   */
  getChildren: async (categoryId: number): Promise<CategoriesResponse> => {
    const response = await categoriesClient.listCategoryChildren({ categoryId });
    return response as unknown as CategoriesResponse;
  },

  /**
   * Create a new category
   */
  create: async (category: CategoryCreate): Promise<Category> => {
    const response = await categoriesClient.createCategory({ categoryCreate: category });
    return response as unknown as Category;
  },

  /**
   * Update an existing category
   */
  update: async (
    categoryId: number,
    category: CategoryUpdate
  ): Promise<Category> => {
    const response = await categoriesClient.updateCategory({ categoryId, categoryUpdate: category });
    return response as unknown as Category;
  },

  /**
   * Delete a category
   */
  delete: async (
    categoryId: number,
    force: boolean = false
  ): Promise<{ message: string }> => {
    // openapi-generator usually returns void or the response body.
    // Assuming it returns void if 204, or object if 200.
    await categoriesClient.deleteCategory({ categoryId, force });
    return { message: "Category deleted" };
  },
};

/**
 * Category Rules API
 */
export const categoryRulesApi = {
  /**
   * Get all category rules with optional filters
   */
  getAll: async (params?: {
    active_only?: boolean;
    category_id?: number;
  }): Promise<CategoryRuleListResponse> => {
    const response = await categoriesClient.listCategoryRules({
      activeOnly: params?.active_only,
      categoryId: params?.category_id
    });
    return response as unknown as CategoryRuleListResponse;
  },

  /**
   * Get a single category rule by ID
   */
  getById: async (ruleId: number): Promise<CategoryRule> => {
    const response = await categoriesClient.getCategoryRule({ ruleId });
    return response as unknown as CategoryRule;
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    const response = await categoriesClient.createCategoryRule({ categoryRuleCreate: rule });
    return response as unknown as CategoryRule;
  },

  /**
   * Update an existing category rule
   */
  update: async (
    ruleId: number,
    rule: CategoryRuleUpdate
  ): Promise<CategoryRule> => {
    const response = await categoriesClient.updateCategoryRule({ ruleId, categoryRuleUpdate: rule });
    return response as unknown as CategoryRule;
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    await categoriesClient.deleteCategoryRule({ ruleId });
    return { message: "Rule deleted" };
  },

  /**
   * Test a category rule against existing transactions
   */
  test: async (
    request: TestCategoryRuleRequest
  ): Promise<TestCategoryRuleResponse> => {
    const response = await categoriesClient.testCategoryRule({ testCategoryRuleRequest: request });
    return response as unknown as TestCategoryRuleResponse;
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    const response = await categoriesClient.applyCategoryRules({ applyCategoryRulesRequest: request });
    return response as unknown as ApplyCategoryRulesResponse;
  },
};