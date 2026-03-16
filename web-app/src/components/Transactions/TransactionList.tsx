import { useState, useEffect, useCallback, useRef } from "react";
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Chip,
  InputAdornment,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
} from "@mui/material";
import IconButton from "@mui/material/IconButton";
import AutorenewRoundedIcon from "@mui/icons-material/AutorenewRounded";

import {
  DataGrid,
  GridColDef,
  GridPaginationModel,
  GridColumnVisibilityModel,
  GridRowModel,
  GridRowModes,
  GridRowModesModel,
  GridEventListener,
  GridRowEditStopReasons,
  GridFilterModel,
  useGridApiRef,
} from "@mui/x-data-grid";
import SearchIcon from "@mui/icons-material/Search";
import FilterListIcon from "@mui/icons-material/FilterList";
import AddIcon from "@mui/icons-material/Add";
import LinkIcon from "@mui/icons-material/Link";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import {
  useTransactions,
  useUpdateTransaction,
} from "../../hooks/useTransactions";
import { useCategories } from "../../hooks/useCategories";
import { useClassifications } from "../../hooks/useClassifications";
import { formatCurrency, formatDate } from "../../utils/formatters";
import TransactionDetail from "./TransactionDetail";
import TransactionForm from "./TransactionForm";
import type { Transaction } from "../../types/transaction";
import { useSnackbar } from "notistack";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { detectAllRelationships } from "../../api/relationships";
import CircularProgress from "@mui/material/CircularProgress";
import { getAccounts } from "../../api/accounts";

function TransactionList() {
  // State for filters
  const [searchInput, setSearchInput] = useState(""); // Local input value
  const [searchText, setSearchText] = useState(""); // Debounced search value for API
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: 25,
  });

  // Sorting state
  const [sortModel, setSortModel] = useState([
    { field: "date", sort: "desc" as const },
  ]);

  // Map frontend column field names to backend API field names
  const fieldToApiFieldMap: Record<string, string> = {
    date: "transaction_date",
    // Add other mappings if needed
  };

  // Column visibility state
  const [columnVisibilityModel, setColumnVisibilityModel] =
    useState<GridColumnVisibilityModel>({});
  // Grid API ref to control edit mode programmatically
  const apiRef = useGridApiRef();

  // Row editing state
  const [rowModesModel, setRowModesModel] = useState<GridRowModesModel>({});

  // Hooks for data
  const updateTransaction = useUpdateTransaction();
  const { data: categoriesData } = useCategories();
  const { data: classificationsData } = useClassifications();
  const { data: accountsData } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts(),
  });
  const { enqueueSnackbar } = useSnackbar();

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearchText(searchInput);
      // Reset to first page when search changes
      setPaginationModel((prev) => ({ ...prev, page: 0 }));
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [searchInput]);

  // State for dialogs
  const [selectedTransaction, setSelectedTransaction] =
    useState<Transaction | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [filtersDialogOpen, setFiltersDialogOpen] = useState(false);

  // State for advanced filters
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    transaction_type: "",
    category_id: "",
    classification_id: "",
    account_id: "",
    include_in_analysis: "",
    is_transfer: "",
    include_capital_expenses: true,
    include_transfers: true,
  });

  // State for dividend reinvestment filter
  const [showDividendReinvestments, setShowDividendReinvestments] =
    useState(true);

  // Fetch transactions with filters
  const { data, isLoading, error, refetch } = useTransactions({
    search_text: searchText || undefined,
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
    transaction_type: filters.transaction_type || undefined,
    category_id: filters.category_id ? Number(filters.category_id) : undefined,
    classification_id: filters.classification_id
      ? Number(filters.classification_id)
      : undefined,
    account_id: filters.account_id ? Number(filters.account_id) : undefined,
    include_in_analysis: filters.include_in_analysis
      ? filters.include_in_analysis === "true"
      : undefined,
    is_transfer: filters.is_transfer
      ? filters.is_transfer === "true"
      : undefined,
    include_capital_expenses: filters.include_capital_expenses,
    include_transfers: filters.include_transfers,
    limit: paginationModel.pageSize,
    offset: paginationModel.page * paginationModel.pageSize,
    sort_by: sortModel[0]?.field
      ? fieldToApiFieldMap[sortModel[0].field] || sortModel[0].field
      : "transaction_date",
    sort_order: sortModel[0]?.sort || "desc",
  });

  // Keep stable total row count across page transitions to avoid UI resets
  const prevTotalRef = useRef<number>(0);
  useEffect(() => {
    const d: any = data as any;
    if (d?.total != null) prevTotalRef.current = d.total as number;
  }, [data]);
  const totalCount = (data as any)?.total ?? prevTotalRef.current;

  // Relationship detection mutation
  const queryClient = useQueryClient();
  const detectRelationshipsMutation = useMutation({
    mutationFn: detectAllRelationships,
    onSuccess: (data) => {
      const totalDetected = data.total_detected;
      const autoLinked = data.auto_linked;

      if (totalDetected === 0) {
        enqueueSnackbar("No relationship pairs found", { variant: "info" });
      } else {
        const message = autoLinked
          ? `Found ${totalDetected} relationship pair${
              totalDetected > 1 ? "s" : ""
            } and linked them automatically`
          : `Found ${totalDetected} relationship pair${
              totalDetected > 1 ? "s" : ""
            }`;
        enqueueSnackbar(message, { variant: "success" });

        // Refetch transactions to show updated visual indicators
        queryClient.invalidateQueries({ queryKey: ["transactions"] });
      }
    },
    onError: (error: any) => {
      enqueueSnackbar(
        error.response?.data?.detail || "Failed to detect relationships",
        { variant: "error" }
      );
    },
  });

  const handleDetectRelationships = () => {
    detectRelationshipsMutation.mutate({ auto_link: true });
  };

  // Handle pagination model change
  const handlePaginationModelChange = useCallback(
    (newModel: GridPaginationModel) => {
      setPaginationModel(newModel);
    },
    []
  );

  // Handle row edit stop
  const handleRowEditStop: GridEventListener<"rowEditStop"> = () => {
    // Allow default behavior so edits commit and the editor closes
  };

  // Process row update
  const processRowUpdate = async (newRow: GridRowModel) => {
    try {
      const updates: any = {};

      // Map changes to API format
      if (newRow.description !== undefined)
        updates.description = newRow.description;
      if (newRow.category_id !== undefined) {
        updates.category_id = newRow.category_id;
        // Also update the human-readable name immediately for a responsive UI
        const matched = categoriesData?.categories?.find(
          (c) => c.category_id === newRow.category_id
        );
        if (matched) {
          (newRow as any).category_name = matched.category_name;
        }
      }
      if (newRow.notes !== undefined) updates.notes = newRow.notes;

      await updateTransaction.mutateAsync({
        id: newRow.id,
        data: updates,
      });

      enqueueSnackbar("Transaction updated successfully", {
        variant: "success",
      });
      return newRow;
    } catch (error) {
      enqueueSnackbar("Failed to update transaction", { variant: "error" });
      throw error;
    }
  };

  // Prepare category options for select
  const categoryOptions =
    categoriesData?.categories?.map((cat) => ({
      value: cat.category_id,
      label: cat.category_name,
    })) || [];

  // Define columns for DataGrid
  const columns: GridColDef[] = [
    {
      field: "date",
      headerName: "Date",
      width: 120,
      valueFormatter: (value) => formatDate(value),
      filterable: false,
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1,
      minWidth: 200,
      editable: true,
      filterable: false,
      renderCell: (params) => {
        const hasRelationship = params.row.related_transaction_id;
        const isDividendReinvestment =
          params.row.classification_name === "Dividend Reinvestment" ||
          params.row.classification_name?.includes("Investment Distribution");

        return (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              width: "100%",
            }}
          >
            {hasRelationship && isDividendReinvestment && (
              <Tooltip title="Part of dividend reinvestment pair - Click row to view related transaction">
                <LinkIcon fontSize="small" color="primary" />
              </Tooltip>
            )}
            <Typography variant="body2" sx={{ flex: 1 }}>
              {params.value}
            </Typography>
          </Box>
        );
      },
    },
    {
      field: "category_id",
      headerName: "Category",
      width: 180,
      editable: true,
      filterable: false,
      renderCell: (params) => {
        const categoryName = params.row.category_name;
        const isUncategorized =
          !categoryName || categoryName === "nan" || categoryName.trim() === "";

        if (isUncategorized) {
          return (
            <Tooltip title="Click to categorize this transaction">
              <Chip
                label="Uncategorized"
                size="small"
                color="warning"
                variant="outlined"
                icon={<span style={{ fontSize: "16px" }}>⚠️</span>}
              />
            </Tooltip>
          );
        }

        return categoryName;
      },
      renderEditCell: (params) => {
        const id = params.id as number;
        const currentValue =
          (params.value as number) ?? params.row.category_id ?? "";
        return (
          <Select
            autoFocus
            fullWidth
            size="small"
            value={currentValue}
            onClick={(e) => e.stopPropagation()}
            onKeyDown={(e) => e.stopPropagation()}
            onChange={async (e) => {
              e.stopPropagation();
              const newVal = Number((e.target as HTMLInputElement).value);
              try {
                await updateTransaction.mutateAsync({
                  id: Number(id),
                  data: { category_id: newVal },
                });
                // Optimistically update displayed name to reduce flicker
                const matched = categoriesData?.categories?.find(
                  (c) => c.category_id === newVal
                );
                if (matched) {
                  (params.api as any).setEditCellValue?.(
                    {
                      id,
                      field: "category_name",
                      value: matched.category_name,
                    },
                    e
                  );
                }
                enqueueSnackbar("Transaction updated successfully", {
                  variant: "success",
                });
              } catch (err) {
                console.error("Category update failed", err);
                enqueueSnackbar("Failed to update transaction", {
                  variant: "error",
                });
              } finally {
                apiRef.current.stopCellEditMode({ id, field: "category_id" });
              }
            }}
          >
            {categoryOptions.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </Select>
        );
      },
    },
    {
      field: "classification_name",
      headerName: "Classification",
      width: 180,
      filterable: false,
      renderCell: (params) => {
        const classificationName = params.value;

        const onReapply = async (e: any) => {
          e.stopPropagation();
          try {
            await updateTransaction.mutateAsync({
              id: params.row.id,
              data: { reapply_rules: true },
            });
            enqueueSnackbar("Classification rules re-applied", {
              variant: "success",
            });
          } catch (err) {
            enqueueSnackbar("Failed to re-apply rules", { variant: "error" });
          }
        };

        if (!classificationName) {
          return (
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <Tooltip title="No classification rule has been applied to this transaction">
                <Chip
                  label="Unclassified"
                  size="small"
                  variant="outlined"
                  color="default"
                />
              </Tooltip>
              <Tooltip title="Reapply rules">
                <IconButton
                  size="small"
                  aria-label="Reapply rules"
                  onClick={onReapply}
                  onMouseDown={(e) => e.stopPropagation()}
                  sx={{ p: 0.5 }}
                >
                  <AutorenewRoundedIcon fontSize="inherit" />
                </IconButton>
              </Tooltip>
            </Box>
          );
        }

        // Color code and tooltips based on classification type
        let color: "default" | "primary" | "secondary" | "info" | "warning" =
          "primary";
        let tooltip = "Classification applied via rules";
        const hasRelationship = params.row.related_transaction_id;

        if (classificationName.includes("Dividend Reinvestment")) {
          color = "secondary";
          tooltip = hasRelationship
            ? "Dividend reinvestment - linked to dividend income"
            : "Dividend reinvestment - excluded from expense calculations";
        } else if (classificationName.includes("Investment Distribution")) {
          color = "success";
          tooltip = hasRelationship
            ? "Dividend income - linked to reinvestment"
            : "Dividend or investment distribution income";
        } else if (classificationName.includes("Transfer")) {
          color = "info";
          tooltip = "Transfer between accounts - may be excluded from analysis";
        } else if (
          classificationName.includes("Refund") ||
          classificationName.includes("Reimbursement")
        ) {
          color = "warning";
          tooltip =
            "Refund or reimbursement - handled specially in calculations";
        } else if (classificationName.includes("Regular")) {
          color = "default";
          tooltip = "Regular transaction - included in standard analysis";
        } else if (classificationName.includes("Loan")) {
          color = "secondary";
          tooltip = "Loan-related transaction";
        } else if (classificationName.includes("Credit Card")) {
          color = "info";
          tooltip = "Credit card transaction";
        }

        return (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Tooltip title={tooltip}>
              <Chip
                label={classificationName}
                size="small"
                color={color}
                variant="filled"
              />
            </Tooltip>
            <Tooltip title="Reapply rules">
              <IconButton
                size="small"
                aria-label="Reapply rules"
                onClick={onReapply}
                onMouseDown={(e) => e.stopPropagation()}
                sx={{ p: 0.5 }}
              >
                <AutorenewRoundedIcon fontSize="inherit" />
              </IconButton>
            </Tooltip>
          </Box>
        );
      },
    },
    {
      field: "transaction_type",
      headerName: "Type",
      width: 120,
      filterable: false,
      renderCell: (params) => {
        const isTransfer = params.row.is_transfer;
        const label = isTransfer ? "Transfer" : params.value;
        const color = isTransfer
          ? "default"
          : params.value === "Income"
          ? "success"
          : "error";

        return (
          <Chip label={label} size="small" color={color} variant="outlined" />
        );
      },
    },
    {
      field: "amount",
      headerName: "Amount",
      width: 130,
      align: "right",
      headerAlign: "right",
      valueFormatter: (value) => formatCurrency(value),
      sortComparator: (v1, v2) => {
        const num1 = typeof v1 === "string" ? parseFloat(v1) : v1;
        const num2 = typeof v2 === "string" ? parseFloat(v2) : v2;
        return num1 - num2;
      },
      filterable: false,
      cellClassName: (params) =>
        params.row.transaction_type === "Income"
          ? "income-cell"
          : "expense-cell",
    },
    {
      field: "source",
      headerName: "Account",
      width: 180,
      valueGetter: (value) => value || "-",
      filterable: false,
    },
    {
      field: "payment_method",
      headerName: "Institution",
      width: 150,
      valueGetter: (value) => value || "-",
      filterable: false,
    },
    {
      field: "balance",
      headerName: "Balance",
      width: 130,
      align: "right",
      headerAlign: "right",
      valueFormatter: (value) => (value ? formatCurrency(value) : "-"),
      filterable: false,
    },
  ];

  const handleCellClick = (params: any) => {
    // Don't open detail dialog when clicking on editable cells
    const isEditableCell =
      params.field === "description" || params.field === "category_id";
    if (!isEditableCell) {
      setSelectedTransaction(params.row);
      setDetailDialogOpen(true);
    }
  };

  // Filter transactions based on dividend reinvestment visibility
  const filteredTransactions = ((data as any)?.transactions || []).filter(
    (transaction: Transaction) => {
      if (!showDividendReinvestments) {
        const isDividendReinvestment =
          transaction.classification_name === "Dividend Reinvestment" ||
          transaction.classification_name?.includes("Investment Distribution");
        const hasRelationship = transaction.related_transaction_id;

        // Hide transactions that are part of dividend reinvestment pairs
        if (isDividendReinvestment && hasRelationship) {
          return false;
        }
      }
      return true;
    }
  );

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
        }}
      >
        <Typography variant="h4">Transactions</Typography>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={
              detectRelationshipsMutation.isPending ? (
                <CircularProgress size={20} />
              ) : (
                <LinkIcon />
              )
            }
            onClick={handleDetectRelationships}
            disabled={detectRelationshipsMutation.isPending}
          >
            {detectRelationshipsMutation.isPending
              ? "Detecting..."
              : "Detect Relationships"}
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            New Transaction
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              placeholder="Search transactions..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              slotProps={{
                input: {
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                },
                htmlInput: {
                  autoComplete: "off",
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <Box sx={{ display: "flex", gap: 1, justifyContent: "flex-end" }}>
              <Button
                variant="outlined"
                startIcon={<FilterListIcon />}
                onClick={() => setFiltersDialogOpen(true)}
              >
                More Filters
              </Button>
              {(searchInput ||
                Object.values(filters).some((v) => v && v !== true)) && (
                <Button
                  variant="text"
                  onClick={() => {
                    setSearchInput("");
                    setFilters({
                      start_date: "",
                      end_date: "",
                      transaction_type: "",
                      category_id: "",
                      classification_id: "",
                      include_in_analysis: "",
                      is_transfer: "",
                      include_capital_expenses: true,
                      include_transfers: true,
                    });
                  }}
                >
                  Clear All
                </Button>
              )}
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* Summary Statistics */}
      {data && data.summary && (
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: "center" }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Total Income
              </Typography>
              <Typography variant="h6" color="success.main" fontWeight="bold">
                {formatCurrency(data.summary.total_income)}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: "center" }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Total Expenses
              </Typography>
              <Typography variant="h6" color="error.main" fontWeight="bold">
                {formatCurrency(data.summary.total_expenses)}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper
              sx={{
                p: 2,
                textAlign: "center",
                bgcolor:
                  data.summary.net_income >= 0
                    ? "success.lighter"
                    : "error.lighter",
              }}
            >
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Net Income
              </Typography>
              <Typography
                variant="h6"
                color={
                  data.summary.net_income >= 0 ? "success.main" : "error.main"
                }
                fontWeight="bold"
              >
                {formatCurrency(data.summary.net_income)}
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: "center" }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Total Transactions
              </Typography>
              <Typography variant="h6" color="primary.main" fontWeight="bold">
                {data.summary.transaction_count.toLocaleString()}
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* Error Display */}
      {error && (
        <Paper sx={{ p: 3, mb: 2, bgcolor: "error.lighter" }}>
          <Typography color="error" variant="body1" gutterBottom>
            Failed to load transactions
          </Typography>
          <Button variant="outlined" color="error" onClick={() => refetch()}>
            Retry
          </Button>
        </Paper>
      )}

      {/* Data Grid */}
      <Paper
        sx={{
          height: 650,
          width: "100%",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <DataGrid
          key={`${paginationModel.page}-${paginationModel.pageSize}`}
          apiRef={apiRef}
          rows={filteredTransactions}
          columns={columns}
          getRowId={(row) => row.id}
          paginationModel={paginationModel}
          onPaginationModelChange={handlePaginationModelChange}
          pageSizeOptions={[10, 25, 50, 100]}
          rowCount={totalCount}
          paginationMode="server"
          sortingMode="server"
          slotProps={{
            pagination: {
              labelDisplayedRows: ({ from, to, count }) => {
                const start = Math.max(1, from || 0);
                const total =
                  typeof count === "number" ? count.toLocaleString() : count;
                return `${start}${to} of ${total}`; // EN DASH
              },
            },
          }}
          sortModel={sortModel}
          onSortModelChange={(newModel) => setSortModel(newModel)}
          loading={isLoading}
          onCellClick={handleCellClick}
          disableColumnMenu={false}
          columnVisibilityModel={columnVisibilityModel}
          onColumnVisibilityModelChange={setColumnVisibilityModel}
          editMode="cell"
          onCellEditCommit={async (params) => {
            try {
              if (params.field === "category_id") {
                await updateTransaction.mutateAsync({
                  id: Number(params.id),
                  data: { category_id: Number(params.value) },
                });
                enqueueSnackbar("Transaction updated successfully", {
                  variant: "success",
                });
              } else if (params.field === "description") {
                await updateTransaction.mutateAsync({
                  id: Number(params.id),
                  data: { description: String(params.value || "") },
                });
                enqueueSnackbar("Transaction updated successfully", {
                  variant: "success",
                });
              }
            } catch (error) {
              console.error("Cell update error:", error);
              enqueueSnackbar("Failed to update transaction", {
                variant: "error",
              });
            }
          }}
          getRowClassName={(params) => {
            const categoryName = params.row.category_name;
            const isUncategorized =
              !categoryName ||
              categoryName === "nan" ||
              categoryName.trim() === "";

            const hasRelationship = params.row.related_transaction_id;
            const isDividendReinvestment =
              params.row.classification_name === "Dividend Reinvestment" ||
              params.row.classification_name?.includes(
                "Investment Distribution"
              );

            if (hasRelationship && isDividendReinvestment) {
              return "dividend-reinvestment-row";
            }

            return isUncategorized ? "uncategorized-row" : "";
          }}
          sx={{
            flex: 1,
            width: "100%",
            border: 0,
            "& .income-cell": {
              color: "success.main",
              fontWeight: "medium",
            },
            "& .expense-cell": {
              color: "error.main",
              fontWeight: "medium",
            },
            "& .MuiDataGrid-row": {
              cursor: "pointer",
            },
            "& .MuiDataGrid-cell--editable": {
              cursor: "text",
              "&:hover": {
                backgroundColor: "action.hover",
              },
            },
            "& .uncategorized-row": {
              backgroundColor: "warning.lighter",
              "&:hover": {
                backgroundColor: "warning.light",
              },
            },
            "& .dividend-reinvestment-row": {
              backgroundColor: "info.lighter",
              "&:hover": {
                backgroundColor: "info.light",
              },
            },
            "& .MuiDataGrid-footerContainer": {
              minHeight: "52px",
            },
          }}
        />
      </Paper>

      {/* Transaction Detail Dialog */}
      <TransactionDetail
        open={detailDialogOpen}
        onClose={() => {
          setDetailDialogOpen(false);
          setSelectedTransaction(null);
        }}
        transaction={selectedTransaction}
      />

      {/* Create Transaction Dialog */}
      <TransactionForm
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        mode="create"
      />

      {/* Filters Dialog */}
      <Dialog
        open={filtersDialogOpen}
        onClose={() => setFiltersDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Advanced Filters</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                value={filters.start_date}
                onChange={(e) =>
                  setFilters({ ...filters, start_date: e.target.value })
                }
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="End Date"
                type="date"
                value={filters.end_date}
                onChange={(e) =>
                  setFilters({ ...filters, end_date: e.target.value })
                }
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth data-testid="filter-transaction-type">
                <InputLabel>Transaction Type</InputLabel>
                <Select
                  value={filters.transaction_type}
                  label="Transaction Type"
                  onChange={(e) =>
                    setFilters({ ...filters, transaction_type: e.target.value })
                  }
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="Income">Income</MenuItem>
                  <MenuItem value="Expense">Expense</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth data-testid="filter-category">
                <InputLabel>Category</InputLabel>
                <Select
                  value={filters.category_id}
                  label="Category"
                  onChange={(e) =>
                    setFilters({ ...filters, category_id: e.target.value })
                  }
                >
                  <MenuItem value="">All</MenuItem>
                  {categoriesData?.categories?.map((cat) => (
                    <MenuItem key={cat.category_id} value={cat.category_id}>
                      {cat.category_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth data-testid="filter-classification">
                <InputLabel>Classification</InputLabel>
                <Select
                  value={filters.classification_id}
                  label="Classification"
                  onChange={(e) =>
                    setFilters({
                      ...filters,
                      classification_id: e.target.value,
                    })
                  }
                >
                  <MenuItem value="">All</MenuItem>
                  {classificationsData?.classifications?.map((cls) => (
                    <MenuItem
                      key={cls.classification_id}
                      value={cls.classification_id}
                    >
                      {cls.classification_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth data-testid="filter-account">
                <InputLabel>Account</InputLabel>
                <Select
                  value={filters.account_id}
                  label="Account"
                  onChange={(e) =>
                    setFilters({ ...filters, account_id: e.target.value })
                  }
                >
                  <MenuItem value="">All Accounts</MenuItem>
                  {accountsData?.map((account) => (
                    <MenuItem
                      key={account.account_id}
                      value={account.account_id}
                    >
                      {account.account_name}
                      {account.institution_name
                        ? ` (${account.institution_name})`
                        : ""}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Include in Analysis</InputLabel>
                <Select
                  value={filters.include_in_analysis}
                  label="Include in Analysis"
                  onChange={(e) =>
                    setFilters({
                      ...filters,
                      include_in_analysis: e.target.value,
                    })
                  }
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="true">Yes</MenuItem>
                  <MenuItem value="false">No</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Is Transfer</InputLabel>
                <Select
                  value={filters.is_transfer}
                  label="Is Transfer"
                  onChange={(e) =>
                    setFilters({ ...filters, is_transfer: e.target.value })
                  }
                >
                  <MenuItem value="">All</MenuItem>
                  <MenuItem value="true">Yes</MenuItem>
                  <MenuItem value="false">No</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <Box sx={{ mt: 2, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
                <Typography
                  variant="subtitle2"
                  gutterBottom
                  sx={{ fontWeight: 600 }}
                >
                  Quick Filters
                </Typography>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={filters.include_capital_expenses}
                      onChange={(e) =>
                        setFilters({
                          ...filters,
                          include_capital_expenses: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Include Non-Operating Expenses (Capital, Refunds, Reimbursements, etc.)"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={filters.include_transfers}
                      onChange={(e) =>
                        setFilters({
                          ...filters,
                          include_transfers: e.target.checked,
                        })
                      }
                    />
                  }
                  label="Include Transfers"
                />
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={showDividendReinvestments}
                      onChange={(e) =>
                        setShowDividendReinvestments(e.target.checked)
                      }
                    />
                  }
                  label="Show Dividend Reinvestment Pairs (highlighted in blue)"
                />
              </Box>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFiltersDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => {
              setFiltersDialogOpen(false);
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
            }}
            variant="contained"
          >
            Apply Filters
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default TransactionList;
