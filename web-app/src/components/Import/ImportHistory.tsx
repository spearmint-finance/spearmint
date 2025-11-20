import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Chip,
  IconButton,
  Tooltip,
  CircularProgress,
  Alert,
} from "@mui/material";
import {
  Visibility as ViewIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
} from "@mui/icons-material";
import { useImportHistory } from "../../hooks/useImport";
import { format } from "date-fns";

interface ImportHistoryProps {
  onViewDetail?: (importId: number) => void;
}

export default function ImportHistory({ onViewDetail }: ImportHistoryProps) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const { data, isLoading, error } = useImportHistory(
    rowsPerPage,
    page * rowsPerPage
  );

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Failed to load import history: {(error as Error).message}
      </Alert>
    );
  }

  if (!data || data.imports.length === 0) {
    return (
      <Alert severity="info">
        No import history found. Upload a file to get started.
      </Alert>
    );
  }

  return (
    <Paper>
      <Box p={2}>
        <Typography variant="h6" gutterBottom>
          Import History
        </Typography>
        <Typography variant="body2" color="text.secondary">
          View past imports and their results
        </Typography>
      </Box>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              <TableCell>File Name</TableCell>
              <TableCell align="right">Total Rows</TableCell>
              <TableCell align="right">Successful</TableCell>
              <TableCell align="right">Failed</TableCell>
              <TableCell align="right">Success Rate</TableCell>
              <TableCell>Mode</TableCell>
              <TableCell align="center">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.imports.map((importItem) => (
              <TableRow key={importItem.import_id} hover>
                <TableCell>
                  {format(
                    new Date(importItem.import_date),
                    "MMM dd, yyyy HH:mm"
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                    {importItem.file_name}
                  </Typography>
                </TableCell>
                <TableCell align="right">{importItem.total_rows}</TableCell>
                <TableCell align="right">
                  <Box display="flex" alignItems="center" justifyContent="flex-end">
                    <SuccessIcon
                      fontSize="small"
                      color="success"
                      sx={{ mr: 0.5 }}
                    />
                    {importItem.successful_rows}
                  </Box>
                </TableCell>
                <TableCell align="right">
                  {importItem.failed_rows > 0 ? (
                    <Box display="flex" alignItems="center" justifyContent="flex-end">
                      <ErrorIcon
                        fontSize="small"
                        color="error"
                        sx={{ mr: 0.5 }}
                      />
                      {importItem.failed_rows}
                    </Box>
                  ) : (
                    importItem.failed_rows
                  )}
                </TableCell>
                <TableCell align="right">
                  <Chip
                    label={`${importItem.success_rate.toFixed(1)}%`}
                    size="small"
                    color={
                      importItem.success_rate >= 90
                        ? "success"
                        : importItem.success_rate >= 70
                        ? "warning"
                        : "error"
                    }
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={importItem.import_mode}
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell align="center">
                  <Tooltip title="View Details">
                    <IconButton
                      size="small"
                      onClick={() => onViewDetail?.(importItem.import_id)}
                    >
                      <ViewIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25, 50]}
        component="div"
        count={data.total}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}

