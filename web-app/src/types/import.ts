export interface ImportRequest {
  mode: "full" | "incremental" | "update";
  skip_duplicates: boolean;
}

export interface ImportError {
  row_number: number;
  error_type: string;
  error_message: string;
}

export interface ImportWarning {
  row_number: number;
  warning_type: string;
  warning_message: string;
}

export interface ImportResponse {
  success: boolean;
  message: string;
  total_rows: number;
  successful_rows: number;
  failed_rows: number;
  skipped_duplicates: number;
  classified_rows: number;
  accounts_created: number;
  accounts_skipped: number;
  errors: ImportError[];
  warnings: ImportWarning[];
}

export interface ImportHistoryItem {
  import_id: number;
  import_date: string;
  file_name: string;
  total_rows: number;
  successful_rows: number;
  failed_rows: number;
  classified_rows: number;
  import_mode: string;
  success_rate: number;
}

export interface ImportHistoryResponse {
  imports: ImportHistoryItem[];
  total: number;
}

export interface ImportHistoryDetail extends ImportHistoryItem {
  error_log: string | null;
  warning_log: string | null;
}

export interface ImportStatusResponse {
  import_id: number;
  status: "pending" | "processing" | "completed" | "failed";
  progress_percentage: number;
  current_row: number;
  total_rows: number;
  message: string;
}

