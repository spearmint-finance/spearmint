/**
 * update-transaction Tool
 *
 * Update a transaction's category or entity assignment.
 * Use this when the user wants to recategorize a transaction or assign it to a different entity.
 *
 * API Endpoint: PUT /api/transactions/{transaction_id}
 */

import { Tool } from "@modelcontextprotocol/sdk/types.js";

const SPEARMINT_API_URL = process.env.SPEARMINT_API_URL || "http://localhost:8000";

export const updateTransactionTool: Tool = {
  name: "update-transaction",
  description:
    "Update a transaction's category or entity. Use this to recategorize a transaction or assign it to a different entity (personal, business, etc.).",
  inputSchema: {
    type: "object",
    properties: {
      transaction_id: {
        type: "number",
        description: "ID of the transaction to update",
      },
      category_id: {
        type: "number",
        description: "New category ID to assign",
      },
      entity_id: {
        type: "number",
        description: "New entity ID to assign (personal, business, etc.)",
      },
      notes: {
        type: "string",
        description: "Optional notes to add to the transaction",
      },
    },
    required: ["transaction_id"],
  },
};

export interface UpdateTransactionInput {
  transaction_id: number;
  category_id?: number;
  entity_id?: number;
  notes?: string;
}

/**
 * Execute the update-transaction tool
 */
export async function executeUpdateTransaction(
  input: UpdateTransactionInput
): Promise<unknown> {
  const { transaction_id, ...updates } = input;

  // Only send fields that were provided
  const body: Record<string, unknown> = {};
  if (updates.category_id !== undefined) body.category_id = updates.category_id;
  if (updates.entity_id !== undefined) body.entity_id = updates.entity_id;
  if (updates.notes !== undefined) body.notes = updates.notes;

  if (Object.keys(body).length === 0) {
    throw new Error("At least one field to update must be provided (category_id, entity_id, or notes)");
  }

  const url = `${SPEARMINT_API_URL}/api/transactions/${transaction_id}`;

  const response = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to update transaction ${transaction_id}: ${response.statusText} - ${errorText}`);
  }

  return await response.json();
}
