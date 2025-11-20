import apiClient from "./client";
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
    const response = await apiClient.get<CategoriesResponse>("/categories", {
      params,
    });
    return response.data;
  },

  /**
   * Get a single category by ID
   */
  getById: async (categoryId: number): Promise<Category> => {
    const response = await apiClient.get<Category>(`/categories/${categoryId}`);
    return response.data;
  },

  /**
   * Get root categories (no parent)
   */
  getRootCategories: async (
    categoryType?: "Income" | "Expense" | "Both"
  ): Promise<CategoriesResponse> => {
    const response = await apiClient.get<CategoriesResponse>(
      "/categories/root",
      {
        params: { category_type: categoryType },
      }
    );
    return response.data;
  },

  /**
   * Get child categories of a parent
   */
  getChildren: async (categoryId: number): Promise<CategoriesResponse> => {
    const response = await apiClient.get<CategoriesResponse>(
      `/categories/${categoryId}/children`
    );
    return response.data;
  },

  /**
   * Create a new category
   */
  create: async (category: CategoryCreate): Promise<Category> => {
    const response = await apiClient.post<Category>("/categories", category);
    return response.data;
  },

  /**
   * Update an existing category
   */
  update: async (
    categoryId: number,
    category: CategoryUpdate
  ): Promise<Category> => {
    const response = await apiClient.put<Category>(
      `/categories/${categoryId}`,
      category
    );
    return response.data;
  },

  /**
   * Delete a category
   */
  delete: async (
    categoryId: number,
    force: boolean = false
  ): Promise<{ message: string }> => {
    const response = await apiClient.delete<{ message: string }>(
      `/categories/${categoryId}`,
      {
        params: { force },
      }
    );
    return response.data;
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
    const response = await apiClient.get<CategoryRuleListResponse>(
      "/category-rules",
      {
        params,
      }
    );
    return response.data;
  },

  /**
   * Get a single category rule by ID
   */
  getById: async (ruleId: number): Promise<CategoryRule> => {
    const response = await apiClient.get<CategoryRule>(
      `/category-rules/${ruleId}`
    );
    return response.data;
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    const response = await apiClient.post<CategoryRule>(
      "/category-rules",
      rule
    );
    return response.data;
  },

  /**
   * Update an existing category rule
   */
  update: async (
    ruleId: number,
    rule: CategoryRuleUpdate
  ): Promise<CategoryRule> => {
    const response = await apiClient.put<CategoryRule>(
      `/category-rules/${ruleId}`,
      rule
    );
    return response.data;
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    const response = await apiClient.delete<{ message: string }>(
      `/category-rules/${ruleId}`
    );
    return response.data;
  },

  /**
   * Test a category rule against existing transactions
   */
  test: async (
    request: TestCategoryRuleRequest
  ): Promise<TestCategoryRuleResponse> => {
    const response = await apiClient.post<TestCategoryRuleResponse>(
      "/category-rules/test",
      request
    );
    return response.data;
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    const response = await apiClient.post<ApplyCategoryRulesResponse>(
      "/category-rules/apply",
      request
    );
    return response.data;
  },
};
