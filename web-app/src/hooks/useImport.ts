import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { importApi } from "../api/import";

/**
 * Hook for uploading and importing a file
 */
export const useImportFile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      file,
      mode = "incremental",
      skipDuplicates = true,
    }: {
      file: File;
      mode?: "full" | "incremental" | "update";
      skipDuplicates?: boolean;
    }) => importApi.uploadFile(file, mode, skipDuplicates),
    onSuccess: () => {
      // Invalidate import history to refresh the list
      queryClient.invalidateQueries({ queryKey: ["import", "history"] });
      // Invalidate transactions to show newly imported data
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      // Invalidate dashboard data
      queryClient.invalidateQueries({ queryKey: ["financial-summary"] });
    },
  });
};

/**
 * Hook for fetching import history
 */
export const useImportHistory = (limit: number = 50, offset: number = 0) => {
  return useQuery({
    queryKey: ["import", "history", limit, offset],
    queryFn: () => importApi.getHistory(limit, offset),
    staleTime: 30 * 1000, // 30 seconds
  });
};

/**
 * Hook for fetching import detail
 */
export const useImportDetail = (importId: number | null) => {
  return useQuery({
    queryKey: ["import", "detail", importId],
    queryFn: () => importApi.getImportDetail(importId!),
    enabled: importId !== null,
    staleTime: 60 * 1000, // 1 minute
  });
};

/**
 * Hook for fetching import status (for progress tracking)
 */
export const useImportStatus = (
  importId: number | null,
  enabled: boolean = true
) => {
  return useQuery({
    queryKey: ["import", "status", importId],
    queryFn: () => importApi.getImportStatus(importId!),
    enabled: enabled && importId !== null,
    refetchInterval: (query) => {
      // Stop polling if import is completed or failed
      if (
        query.state.data?.status === "completed" ||
        query.state.data?.status === "failed"
      ) {
        return false;
      }
      // Poll every 1 second while processing
      return 1000;
    },
    staleTime: 0, // Always fetch fresh data for status
  });
};

