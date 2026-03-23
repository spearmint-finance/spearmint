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

const baseUrl =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined"
    ? window.location.origin
    : "http://localhost:8080");

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
      await categoriesClient.updateCategory(
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
    const response = await fetch(
      `${baseUrl}/api/categories/${sourceCategoryId}/merge`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target_category_id: targetCategoryId }),
      }
    );
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: "Merge failed" }));
      throw new Error(err.detail || "Failed to merge category");
    }
    return response.json();
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
      await categoriesClient.listCategoryRules({
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
      await categoriesClient.getCategoryRule(ruleId);
    return response.data as unknown as CategoryRule;
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    const response =
      await categoriesClient.createCategoryRule(rule as any);
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
      await categoriesClient.updateCategoryRule(
        ruleId,
        rule as any
      );
    return response.data as unknown as CategoryRule;
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    await categoriesClient.deleteCategoryRule(
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
      await categoriesClient.testCategoryRule(request);
    return response.data as unknown as TestCategoryRuleResponse;
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    const response =
      await categoriesClient.applyCategoryRules(
        request
      );
    return response.data as unknown as ApplyCategoryRulesResponse;
  },
};
