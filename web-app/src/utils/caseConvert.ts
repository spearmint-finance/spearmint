/**
 * Utility functions to convert object keys between camelCase and snake_case.
 * Used as adapters between the SDK (camelCase) and React components (snake_case).
 */

function camelToSnake(key: string): string {
  return key.replace(/([A-Z])/g, (match, char, index) => {
    // Don't add underscore at the start
    return index > 0 ? `_${char.toLowerCase()}` : char.toLowerCase();
  });
}

function snakeToCamel(key: string): string {
  return key.replace(/_([a-z])/g, (_, char) => char.toUpperCase());
}

/**
 * Recursively converts all camelCase keys in an object to snake_case.
 * Handles nested objects, arrays, and primitives.
 */
export function toSnakeCase<T = Record<string, unknown>>(obj: unknown): T {
  if (obj === null || obj === undefined || typeof obj !== "object") {
    return obj as T;
  }

  if (Array.isArray(obj)) {
    return obj.map((item) => toSnakeCase(item)) as T;
  }

  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const snakeKey = camelToSnake(key);
    result[snakeKey] = toSnakeCase(value);
  }
  return result as T;
}

/**
 * Recursively converts all snake_case keys in an object to camelCase.
 * Handles nested objects, arrays, and primitives.
 */
export function toCamelCase<T = Record<string, unknown>>(obj: unknown): T {
  if (obj === null || obj === undefined || typeof obj !== "object") {
    return obj as T;
  }

  if (Array.isArray(obj)) {
    return obj.map((item) => toCamelCase(item)) as T;
  }

  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    const camelKey = snakeToCamel(key);
    result[camelKey] = toCamelCase(value);
  }
  return result as T;
}
