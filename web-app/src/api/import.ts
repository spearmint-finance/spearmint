import { importApi as importClient } from "./sdk";
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
    // The SDK should handle multipart/form-data if spec is correct
    // Assuming the method is named importFile or uploadFile
    // We pass the file object directly
    const response = await importClient.importTransactions({
      file,
      mode,
      skipDuplicates
    });
    return response as unknown as ImportResponse;
  },

  /**
   * Get import history with pagination
   */
  getHistory: async (
    limit: number = 50,
    offset: number = 0
  ): Promise<ImportHistoryResponse> => {
    const response = await importClient.getImportHistory({ limit, offset });
    return response as unknown as ImportHistoryResponse;
  },

  /**
   * Get detailed information about a specific import
   */
  getImportDetail: async (importId: number): Promise<ImportHistoryDetail> => {
    const response = await importClient.getImportDetail({ importId });
    return response as unknown as ImportHistoryDetail;
  },

  /**
   * Get import status for progress tracking
   */
  getImportStatus: async (importId: number): Promise<ImportStatusResponse> => {
    const response = await importClient.getImportStatus({ importId });
    return response as unknown as ImportStatusResponse;
  },
};