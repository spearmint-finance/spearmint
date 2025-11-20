import apiClient from "./client";
import type {
  ImportResponse,
  ImportHistoryResponse,
  ImportHistoryDetail,
  ImportStatusResponse,
} from "../types/import";

export const importApi = {
  /**
   * Upload and import a file
   */
  uploadFile: async (
    file: File,
    mode: "full" | "incremental" | "update" = "incremental",
    skipDuplicates: boolean = true
  ): Promise<ImportResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("mode", mode);
    formData.append("skip_duplicates", skipDuplicates.toString());

    const response = await apiClient.post<ImportResponse>(
      "/import",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 120000, // 2 minutes for file uploads
      }
    );
    return response.data;
  },

  /**
   * Get import history with pagination
   */
  getHistory: async (
    limit: number = 50,
    offset: number = 0
  ): Promise<ImportHistoryResponse> => {
    const response = await apiClient.get<ImportHistoryResponse>(
      "/import/history",
      {
        params: { limit, offset },
      }
    );
    return response.data;
  },

  /**
   * Get detailed information about a specific import
   */
  getImportDetail: async (importId: number): Promise<ImportHistoryDetail> => {
    const response = await apiClient.get<ImportHistoryDetail>(
      `/import/history/${importId}`
    );
    return response.data;
  },

  /**
   * Get import status for progress tracking
   */
  getImportStatus: async (importId: number): Promise<ImportStatusResponse> => {
    const response = await apiClient.get<ImportStatusResponse>(
      `/import/status/${importId}`
    );
    return response.data;
  },
};

