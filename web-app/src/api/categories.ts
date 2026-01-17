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
    const response = await categoriesClient.listCategoriesApiCategoriesGet({
      categoryType: params?.category_type,
      parentCategoryId: params?.parent_category_id,
      includeTransferCategories: params?.include_transfer_categories,
      searchText: params?.search_text,
    });
    return response.data as unknown as CategoriesResponse;
  },

  /**
   * Get a single category by ID
   */
  getById: async (categoryId: number): Promise<Category> => {
    const response =
      await categoriesClient.getCategoryApiCategoriesCategoryIdGet(categoryId);
    return response.data as unknown as Category;
  },

  /**
   * Get root categories (no parent)
   */
  getRootCategories: async (
    categoryType?: "Income" | "Expense" | "Both"
  ): Promise<CategoriesResponse> => {
    const response =
      await categoriesClient.getRootCategoriesApiCategoriesRootGet({
        categoryType,
      });
    return response.data as unknown as CategoriesResponse;
  },

  /**
   * Get child categories of a parent
   */
  getChildren: async (categoryId: number): Promise<CategoriesResponse> => {
    const response =
      await categoriesClient.getChildCategoriesApiCategoriesCategoryIdChildrenGet(
        categoryId
      );
    return response.data as unknown as CategoriesResponse;
  },

  /**
   * Create a new category
   */
  create: async (category: CategoryCreate): Promise<Category> => {
    const response = await categoriesClient.createCategoryApiCategoriesPost(
      category
    );
    return response.data as unknown as Category;
  },

  /**
   * Update an existing category
   */
  update: async (
    categoryId: number,
    category: CategoryUpdate
  ): Promise<Category> => {
    const response =
      await categoriesClient.updateCategoryApiCategoriesCategoryIdPut(
        categoryId,
        category
      );
    return response.data as unknown as Category;
  },

  /**
   * Delete a category
   */
  delete: async (
    categoryId: number,
    force: boolean = false
  ): Promise<{ message: string }> => {
    await categoriesClient.deleteCategoryApiCategoriesCategoryIdDelete(
      categoryId,
      { force }
    );
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
    const response =
      await categoriesClient.listCategoryRulesApiCategoryRulesGet({
        activeOnly: params?.active_only,
        categoryId: params?.category_id,
      });
    return response.data as unknown as CategoryRuleListResponse;
  },

  /**
   * Get a single category rule by ID
   */
  getById: async (ruleId: number): Promise<CategoryRule> => {
    const response =
      await categoriesClient.getCategoryRuleApiCategoryRulesRuleIdGet(ruleId);
    return response.data as unknown as CategoryRule;
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    const response =
      await categoriesClient.createCategoryRuleApiCategoryRulesPost(rule);
    return response.data as unknown as CategoryRule;
  },

  /**
   * Update an existing category rule
   */
  update: async (
    ruleId: number,
    rule: CategoryRuleUpdate
  ): Promise<CategoryRule> => {
    const response =
      await categoriesClient.updateCategoryRuleApiCategoryRulesRuleIdPut(
        ruleId,
        rule
      );
    return response.data as unknown as CategoryRule;
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    await categoriesClient.deleteCategoryRuleApiCategoryRulesRuleIdDelete(
      ruleId
    );
    return { message: "Rule deleted" };
  },

  /**
   * Test a category rule against existing transactions
   */
  test: async (
    request: TestCategoryRuleRequest
  ): Promise<TestCategoryRuleResponse> => {
    const response =
      await categoriesClient.testCategoryRuleApiCategoryRulesTestPost(request);
    return response.data as unknown as TestCategoryRuleResponse;
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    const response =
      await categoriesClient.applyCategoryRulesApiCategoryRulesApplyPost(
        request
      );
    return response.data as unknown as ApplyCategoryRulesResponse;
  },
};
