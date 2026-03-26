/**
 * create-category-rule Tool
 *
 * Create an auto-categorization rule that assigns a category to
 * future transactions matching a pattern.
 *
 * API Endpoint: POST /api/category-rules
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const createCategoryRuleTool: Tool = {
  name: "create-category-rule",
  description:
    "Create a rule to automatically categorize transactions matching a pattern. Rules match against the transaction source (merchant name). Use this when the user wants to set up automatic categorization for recurring merchants.",
  inputSchema: {
    type: "object",
    properties: {
      rule_name: {
        type: "string",
        description: "Human-readable name for the rule (e.g., 'Whole Foods → Groceries')",
      },
      category_id: {
        type: "number",
        description: "Category ID to assign when the rule matches",
      },
      source_pattern: {
        type: "string",
        description:
          "Pattern to match in the transaction source/merchant name. Use SQL LIKE syntax: '%pattern%' for contains, 'pattern%' for starts-with, '%pattern' for ends-with, or 'pattern' for exact match.",
      },
      description_pattern: {
        type: "string",
        description: "Optional pattern to match in the transaction description",
      },
      entity_id: {
        type: "number",
        description: "Optional entity ID to assign when the rule matches",
      },
      rule_priority: {
        type: "number",
        description: "Rule priority (lower = higher priority, default: 100)",
      },
    },
    required: ["rule_name", "category_id", "source_pattern"],
  },
};

export interface CreateCategoryRuleInput {
  rule_name: string;
  category_id: number;
  source_pattern: string;
  description_pattern?: string;
  entity_id?: number;
  rule_priority?: number;
}

/**
 * Execute the create-category-rule tool
 */
export async function executeCreateCategoryRule(
  input: CreateCategoryRuleInput
): Promise<unknown> {
  const body: Record<string, unknown> = {
    rule_name: input.rule_name,
    category_id: input.category_id,
    source_pattern: input.source_pattern,
  };

  if (input.description_pattern !== undefined) body.description_pattern = input.description_pattern;
  if (input.entity_id !== undefined) body.entity_id = input.entity_id;
  if (input.rule_priority !== undefined) body.rule_priority = input.rule_priority;

  const url = `${SPEARMINT_API_URL}/api/category-rules`;

  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to create category rule: ${response.statusText} - ${errorText}`);
  }

  return await response.json();
}
