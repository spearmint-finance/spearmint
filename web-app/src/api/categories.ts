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
    // Bypass SDK — returns camelCase but components expect snake_case
    const searchParams = new URLSearchParams();
    if (params?.active_only !== undefined) searchParams.set("active_only", String(params.active_only));
    if (params?.category_id !== undefined) searchParams.set("category_id", String(params.category_id));
    const qs = searchParams.toString();
    const response = await fetch(`${baseUrl}/api/category-rules${qs ? `?${qs}` : ""}`);
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },

  /**
   * Get a single category rule by ID
   */
  getById: async (ruleId: number): Promise<CategoryRule> => {
    // Bypass SDK — returns camelCase but components expect snake_case
    const response = await fetch(`${baseUrl}/api/category-rules/${ruleId}`);
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },

  /**
   * Create a new category rule
   */
  create: async (rule: CategoryRuleCreate): Promise<CategoryRule> => {
    // Bypass SDK — its schema requires categoryId and lacks entityId
    const response = await fetch(`${baseUrl}/api/category-rules`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(rule),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },

  /**
   * Update an existing category rule
   */
  update: async (
    ruleId: number,
    rule: CategoryRuleUpdate
  ): Promise<CategoryRule> => {
    // Bypass SDK — its schema requires categoryId and lacks entityId
    const response = await fetch(`${baseUrl}/api/category-rules/${ruleId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(rule),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },

  /**
   * Delete a category rule
   */
  delete: async (ruleId: number): Promise<{ message: string }> => {
    const response = await fetch(`${baseUrl}/api/category-rules/${ruleId}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return { message: "Rule deleted" };
  },

  /**
   * Test a category rule against existing transactions
   */
  test: async (
    request: TestCategoryRuleRequest
  ): Promise<TestCategoryRuleResponse> => {
    // Bypass SDK for consistency with create/update
    const response = await fetch(`${baseUrl}/api/category-rules/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },

  /**
   * Apply category rules to transactions
   */
  apply: async (
    request: ApplyCategoryRulesRequest
  ): Promise<ApplyCategoryRulesResponse> => {
    // Bypass SDK for consistency with create/update
    const response = await fetch(`${baseUrl}/api/category-rules/apply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(detail);
    }
    return response.json();
  },
};
