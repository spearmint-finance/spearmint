/**
 * React Query hooks for API Key Management
 */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createApiKey,
  listApiKeys,
  getApiKey,
  revokeApiKey,
} from "../api/auth";
import type { APIKeyCreate } from "../types/auth";

// Query keys
export const apiKeyKeys = {
  all: ["apiKeys"] as const,
  lists: () => [...apiKeyKeys.all, "list"] as const,
  list: (includeInactive?: boolean) =>
    [...apiKeyKeys.lists(), { includeInactive }] as const,
  details: () => [...apiKeyKeys.all, "detail"] as const,
  detail: (id: number) => [...apiKeyKeys.details(), id] as const,
};

/**
 * Hook to fetch all API keys
 * @param includeInactive - Whether to include revoked keys
 */
export function useApiKeys(includeInactive: boolean = false) {
  return useQuery({
    queryKey: apiKeyKeys.list(includeInactive),
    queryFn: () => listApiKeys(includeInactive),
  });
}

/**
 * Hook to fetch a single API key
 * @param keyId - The ID of the key to fetch
 */
export function useApiKey(keyId: number | null) {
  return useQuery({
    queryKey: apiKeyKeys.detail(keyId!),
    queryFn: () => getApiKey(keyId!),
    enabled: keyId !== null,
  });
}

/**
 * Hook to create a new API key
 * Returns the full key (only shown once at creation time)
 */
export function useCreateApiKey() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: APIKeyCreate) => createApiKey(data),
    onSuccess: () => {
      // Invalidate all API key lists
      queryClient.invalidateQueries({ queryKey: apiKeyKeys.lists() });
    },
  });
}

/**
 * Hook to revoke an API key
 * @param permanent - Whether to permanently delete the key
 */
export function useRevokeApiKey() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      keyId,
      permanent = false,
    }: {
      keyId: number;
      permanent?: boolean;
    }) => revokeApiKey(keyId, permanent),
    onSuccess: (_data, { keyId }) => {
      // Invalidate all API key lists
      queryClient.invalidateQueries({ queryKey: apiKeyKeys.lists() });
      // Remove the specific key from cache
      queryClient.removeQueries({
        queryKey: apiKeyKeys.detail(keyId),
      });
    },
  });
}
