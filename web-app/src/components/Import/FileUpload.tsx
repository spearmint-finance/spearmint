import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import {
  Box,
  Paper,
  Typography,
  Button,
  LinearProgress,
  Alert,
} from "@mui/material";
import {
  CloudUpload as UploadIcon,
} from "@mui/icons-material";
import { useSnackbar } from "notistack";
import { useImportFile } from "../../hooks/useImport";
import type { ImportResponse } from "../../types/import";

interface FileUploadProps {
  mode?: "full" | "incremental" | "update";
  skipDuplicates?: boolean;
  onSuccess?: (result: ImportResponse) => void;
  onError?: (error: Error) => void;
}

export default function FileUpload({
  mode = "incremental",
  skipDuplicates = true,
  onSuccess,
  onError,
}: FileUploadProps) {
  const { enqueueSnackbar } = useSnackbar();
  const importMutation = useImportFile();

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) {
        return;
      }

      const file = acceptedFiles[0];

      // Validate file type
      if (!file.name.endsWith(".xlsx") && !file.name.endsWith(".xls")) {
        enqueueSnackbar("Please upload an Excel file (.xlsx or .xls)", {
          variant: "error",
        });
        return;
      }

      // Validate file size (10MB max)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        enqueueSnackbar("File size must be less than 10MB", {
          variant: "error",
        });
        return;
      }

      // Upload file
      importMutation.mutate(
        { file, mode, skipDuplicates },
        {
          onSuccess: (data) => {
            // Consider it successful if any rows were imported
            const isSuccess = data.successful_rows > 0;

            if (isSuccess) {
              let message = `Successfully imported ${data.successful_rows} of ${data.total_rows} transactions`;

              // Add duplicate information if any were skipped
              if (data.skipped_duplicates > 0) {
                message += ` (${data.skipped_duplicates} duplicates skipped)`;
              }

              enqueueSnackbar(message, { variant: "success" });
              onSuccess?.(data);
            } else if (data.skipped_duplicates > 0) {
              // All rows were duplicates
              enqueueSnackbar(
                `All ${data.skipped_duplicates} transactions were duplicates and were skipped`,
                { variant: "info" }
              );
              onSuccess?.(data);
            } else {
              // Complete failure
              enqueueSnackbar("Import failed - no transactions were imported", {
                variant: "error",
              });
              onError?.(new Error("No transactions were imported"));
            }
          },
          onError: (error: any) => {
            const message =
              error.response?.data?.detail ||
              error.message ||
              "Failed to import file";
            enqueueSnackbar(message, { variant: "error" });
            onError?.(error);
          },
        }
      );
    },
    [mode, skipDuplicates, importMutation, enqueueSnackbar, onSuccess, onError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
      "application/vnd.ms-excel": [".xls"],
    },
    multiple: false,
    disabled: importMutation.isPending,
  });

  return (
    <Box>
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          textAlign: "center",
          cursor: importMutation.isPending ? "not-allowed" : "pointer",
          border: "2px dashed",
          borderColor: isDragActive ? "primary.main" : "divider",
          bgcolor: isDragActive ? "action.hover" : "background.paper",
          transition: "all 0.2s",
          "&:hover": {
            borderColor: importMutation.isPending ? "divider" : "primary.main",
            bgcolor: importMutation.isPending
              ? "background.paper"
              : "action.hover",
          },
        }}
      >
        <input {...getInputProps()} />

        {importMutation.isPending ? (
          <Box>
            <Typography variant="h6" gutterBottom>
              Uploading and processing file...
            </Typography>
            <LinearProgress sx={{ mt: 2, mb: 2 }} />
            <Typography variant="body2" color="text.secondary">
              Please wait while we import your transactions
            </Typography>
          </Box>
        ) : (
          <Box>
            <UploadIcon
              sx={{ fontSize: 64, color: "primary.main", mb: 2 }}
            />
            <Typography variant="h6" gutterBottom>
              {isDragActive
                ? "Drop the file here"
                : "Drag & drop an Excel file here"}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              or
            </Typography>
            <Button variant="contained" sx={{ mt: 1 }}>
              Browse Files
            </Button>
            <Typography
              variant="caption"
              display="block"
              color="text.secondary"
              sx={{ mt: 2 }}
            >
              Supported formats: .xlsx, .xls (Max size: 10MB)
            </Typography>
          </Box>
        )}
      </Paper>

      {/* Import mode info */}
      <Alert severity="info" sx={{ mt: 2 }}>
        <Typography variant="body2">
          <strong>Import Mode:</strong>{" "}
          {mode === "full"
            ? "Full (replaces all existing data)"
            : mode === "incremental"
            ? "Incremental (adds new transactions)"
            : "Update (updates existing transactions)"}
        </Typography>
        <Typography variant="body2">
          <strong>Skip Duplicates:</strong> {skipDuplicates ? "Yes" : "No"}
        </Typography>
      </Alert>
    </Box>
  );
}

