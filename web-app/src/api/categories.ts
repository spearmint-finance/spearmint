import { categoriesApi as categoriesClient } from "./sdk";
import { toSnakeCase, toCamelCase } from "../utils/caseConvert";
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
    category_type?: "Income" | "Expense" | "Both" | "Transfer";
    parent_category_id?: number | null;
    search_text?: string;
    entity_id?: number;
  }): Promise<CategoriesResponse> => {
    const response = await categoriesClient.listCategories({
      categoryType: params?.category_type,
      parentCategoryId: params?.parent_category_id,
      searchText: params?.search_text,
      entityId: params?.entity_id,
    } as any);
    const raw = response.data as Record<string, unknown>;
    const categories = ((raw.categories ?? raw) as Record<string, unknown>[]).map(
      (c) => ({
        category_id: c.category_id ?? c.categoryId,
        category_name: c.category_name ?? c.categoryName,
        category_type: c.category_type ?? c.categoryType,
        parent_category_id: c.parent_category_id ?? c.parentCategoryId ?? null,
        description: c.description ?? null,
        entity_id: c.entity_id ?? c.entityId ?? null,
        created_at: c.created_at ?? c.createdAt ?? "",
        transaction_count: c.transaction_count ?? c.transactionCount ?? null,
      })
    ) as Category[];
    return { categories, total: categories.length };
  },

  /**
   * Get a single category by ID
   */
  getById: async (categoryId: number): Promise<Category> => {
    const response =
      await categoriesClient.getCategory(categoryId);
    return response.data as unknown as Category;
  },

  /**
   * Get root categories (no parent)
   */
  getRootCategories: async (
    categoryType?: "Income" | "Expense" | "Both" | "Transfer"
  ): Promise<CategoriesResponse> => {
    const response =
      await categoriesClient.getRootCategories({
        categoryType,
      });
    return response.data as unknown as CategoriesResponse;
  },

  /**
   * Get child categories of a parent
   */
  getChildren: async (categoryId: number): Promise<CategoriesResponse> => {
    const response =
      await categoriesClient.getChildCategories(
        categoryId
      );
    return response.data as unknown as CategoriesResponse;
  },

  /**
   * Create a new category
   */
  create: async (category: CategoryCreate): Promise<Category> => {
    const response = await categoriesClient.createCategory({
      categoryName: category.category_name,
      categoryType: category.category_type,
      parentCategoryId: category.parent_category_id ?? undefined,
      description: category.description ?? undefined,
      entityId: category.entity_id ?? undefined,
    } as any);
    // SDK transforms API snake_case → camelCase; normalize back to snake_case for consistency
    const c = response.data as Record<string, unknown>;
    return {
      category_id: (c.category_id ?? c.categoryId) as number,
      category_name: (c.category_name ?? c.categoryName) as string,
      category_type: (c.category_type ?? c.categoryType) as string,
      parent_category_id: (c.parent_category_id ?? c.parentCategoryId ?? null) as number | null,
      description: (c.description ?? null) as string | null,
      entity_id: (c.entity_id ?? c.entityId ?? null) as number | null,
      created_at: (c.created_at ?? c.createdAt ?? "") as string,
      transaction_count: (c.transaction_count ?? c.transactionCount ?? null) as number | null,
    } as Category;
  },

  /**
   * Update an existing category
   */
  update: async (
    categoryId: number,
    category: CategoryUpdate
  ): Promise<Category> => {
    const response =
      await categoriesClient.updateCategory(
        categoryId,
        {
          categoryName: category.category_name,
          categoryType: category.category_type,
          parentCategoryId: category.parent_category_id,
          description: category.description,
          entityId: category.entity_id,
        } as any
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
    await categoriesClient.deleteCategory(
      categoryId,
      { force }
    );
    return { message: "Category deleted" };
  },

  /**
   * Merge source category into target. Reassigns all transactions, splits,
   * rules, budgets, and children, then deletes the source.
   */
  merge: async (
    sourceCategoryId: number,
    targetCategoryId: number
  ): Promise<{
    message: string;
    transactions: number;
    splits: number;
    rules: number;
    budgets: number;
    children: number;
  }> => {
    const response = await categoriesClient.mergeCategory(
      sourceCategoryId,
      { targetCategoryId }
    );
    return toSnakeCase(response.data);
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
      categoryId: params?.category_id,
    });
    return toSnakeCase<CategoryRuleListResponse>(response.data);
  },

  /**
   * Get a single category rule by ID
   */
  getById: async (ruleId: number): Promise<CategoryRule> => {
    const response = await categoriesClient.getCategoryRule(ruleId);
    return toSnakeCase<CategoryRule>(response.data);
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    const camelRule = toCamelCase(rule);
    const response = await categoriesClient.createCategoryRule(camelRule as any);
    return toSnakeCase<CategoryRule>(response.data);
  },

  /**
   * Update an existing category rule
   */
  update: async (
    ruleId: number,
    rule: CategoryRuleUpdate
  ): Promise<CategoryRule> => {
    const camelRule = toCamelCase(rule);
    const response = await categoriesClient.updateCategoryRule(ruleId, camelRule as any);
    return toSnakeCase<CategoryRule>(response.data);
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    await categoriesClient.deleteCategoryRule(ruleId);
    return { message: "Rule deleted" };
  },

  /**
   * Test a category rule against existing transactions
   */
  test: async (
    request: TestCategoryRuleRequest
  ): Promise<TestCategoryRuleResponse> => {
    const camelRequest = toCamelCase(request);
    const response = await categoriesClient.testCategoryRule(camelRequest as any);
    return toSnakeCase<TestCategoryRuleResponse>(response.data);
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    const camelRequest = toCamelCase(request);
    const response = await categoriesClient.applyCategoryRules(camelRequest as any);
    return toSnakeCase<ApplyCategoryRulesResponse>(response.data);
  },
};
