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
    const response = await importClient.importTransactions({
      file,
      mode,
      skipDuplicates,
    });
    const data = response.data as any;
    return {
      success: (data.successfulRows ?? data.successful_rows ?? 0) > 0,
      message: "",
      total_rows: data.totalRows ?? data.total_rows ?? 0,
      successful_rows: data.successfulRows ?? data.successful_rows ?? 0,
      failed_rows: data.failedRows ?? data.failed_rows ?? 0,
      skipped_duplicates: data.skippedDuplicates ?? data.skipped_duplicates ?? 0,
      classified_rows: data.classifiedRows ?? data.classified_rows ?? 0,
      errors: data.errors ?? [],
      warnings: data.warnings ?? [],
    };
  },

  /**
   * Get import history with pagination
   */
  getHistory: async (
    limit: number = 50,
    offset: number = 0
  ): Promise<ImportHistoryResponse> => {
    const response = await importClient.getImportHistory({
      limit,
      offset,
    });
    const data = response.data as any;
    return {
      imports: (data.imports || []).map((item: any) => ({
        import_id: item.importId ?? item.import_id,
        import_date: item.importDate ?? item.import_date,
        file_name: item.fileName ?? item.file_name,
        total_rows: item.totalRows ?? item.total_rows,
        successful_rows: item.successfulRows ?? item.successful_rows,
        failed_rows: item.failedRows ?? item.failed_rows,
        classified_rows: item.classifiedRows ?? item.classified_rows,
        import_mode: item.importMode ?? item.import_mode,
        success_rate: item.successRate ?? item.success_rate,
      })),
      total: data.total,
    };
  },

  /**
   * Get detailed information about a specific import
   */
  getImportDetail: async (importId: number): Promise<ImportHistoryDetail> => {
    const response =
      await importClient.getImportDetail(importId);
    const item = response.data as any;
    return {
      import_id: item.importId ?? item.import_id,
      import_date: item.importDate ?? item.import_date,
      file_name: item.fileName ?? item.file_name,
      total_rows: item.totalRows ?? item.total_rows,
      successful_rows: item.successfulRows ?? item.successful_rows,
      failed_rows: item.failedRows ?? item.failed_rows,
      classified_rows: item.classifiedRows ?? item.classified_rows,
      import_mode: item.importMode ?? item.import_mode,
      success_rate: item.successRate ?? item.success_rate,
      error_log: item.errorLog ?? item.error_log ?? null,
      warning_log: item.warningLog ?? item.warning_log ?? null,
    };
  },

  /**
   * Get import status for progress tracking
   */
  getImportStatus: async (importId: number): Promise<ImportStatusResponse> => {
    const response =
      await importClient.getImportStatus(importId);
    const item = response.data as any;
    return {
      import_id: item.importId ?? item.import_id,
      status: item.status,
      progress_percentage: item.progressPercentage ?? item.progress_percentage ?? item.progress,
      current_row: item.currentRow ?? item.current_row,
      total_rows: item.totalRows ?? item.total_rows,
      message: item.message,
    };
  },
};
