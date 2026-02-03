/**
 * API client functions for authentication and API key management
 *
 * Note: Using axios directly since auth endpoints are not yet in the SDK.
 * Once the SDK is regenerated, this can be migrated to use SDK methods.
 */

import axios from "axios";
import {
  APIKey,
  APIKeyCreate,
  APIKeyCreated,
  APIKeyListResponse,
  APIKeyValidateRequest,
  APIKeyValidateResponse,
} from "../types/auth";

// Get base URL from environment or use origin (same as SDK)
const baseUrl =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined"
    ? window.location.origin
    : "http://localhost:8080");

// Create axios instance for auth API
const authClient = axios.create({
  baseURL: `${baseUrl}/api/auth`,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Create a new API key
 * @param data - Name and optional expiration for the key
 * @returns The created API key with the full key (only shown once)
 */
export const createApiKey = async (
  data: APIKeyCreate
): Promise<APIKeyCreated> => {
  const response = await authClient.post<APIKeyCreated>("/api-keys", data);
  return response.data;
};

/**
 * List all API keys
 * @param includeInactive - Whether to include revoked keys
 * @returns List of API keys (masked)
 */
export const listApiKeys = async (
  includeInactive: boolean = false
): Promise<APIKeyListResponse> => {
  const response = await authClient.get<APIKeyListResponse>("/api-keys", {
    params: { include_inactive: includeInactive },
  });
  return response.data;
};

/**
 * Get a specific API key by ID
 * @param keyId - The ID of the key to retrieve
 * @returns The API key (masked)
 */
export const getApiKey = async (keyId: number): Promise<APIKey> => {
  const response = await authClient.get<APIKey>(`/api-keys/${keyId}`);
  return response.data;
};

/**
 * Revoke an API key
 * @param keyId - The ID of the key to revoke
 * @param permanent - Whether to permanently delete the key
 */
export const revokeApiKey = async (
  keyId: number,
  permanent: boolean = false
): Promise<{ message: string; key_id: number }> => {
  const response = await authClient.delete<{ message: string; key_id: number }>(
    `/api-keys/${keyId}`,
    {
      params: { permanent },
    }
  );
  return response.data;
};

/**
 * Validate an API key
 * @param key - The full API key to validate
 * @returns Validation result
 */
export const validateApiKey = async (
  key: string
): Promise<APIKeyValidateResponse> => {
  const request: APIKeyValidateRequest = { key };
  const response = await authClient.post<APIKeyValidateResponse>(
    "/api-keys/validate",
    request
  );
  return response.data;
};
