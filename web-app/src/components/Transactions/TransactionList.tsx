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
  Badge,
  Autocomplete,
} from "@mui/material";
import IconButton from "@mui/material/IconButton";

import {
  DataGrid,
  GridColDef,
  GridPaginationModel,
  GridColumnVisibilityModel,
  GridRowModel,
  GridRowModesModel,
  GridEventListener,
  useGridApiRef,
} from "@mui/x-data-grid";
import SearchIcon from "@mui/icons-material/Search";
import FilterListIcon from "@mui/icons-material/FilterList";
import AddIcon from "@mui/icons-material/Add";
import LinkIcon from "@mui/icons-material/Link";
import DownloadIcon from "@mui/icons-material/Download";
import {
  useTransactions,
  useUpdateTransaction,
} from "../../hooks/useTransactions";
import { useCategories } from "../../hooks/useCategories";
import { formatCurrency, formatDate } from "../../utils/formatters";
import TransactionForm from "./TransactionForm";
import type { Transaction } from "../../types/transaction";
import { useSnackbar } from "notistack";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { detectAllRelationships } from "../../api/relationships";
import CircularProgress from "@mui/material/CircularProgress";
import { useSearchParams } from "react-router-dom";
import { getAccounts } from "../../api/accounts";
import { getTransactions } from "../../api/transactions";
import { useEntityContext } from "../../contexts/EntityContext";
import { useEntities } from "../../hooks/useEntities";

function TransactionList() {
  const [searchParams] = useSearchParams();
  const initialAccountId = searchParams.get("account_id") || "";
  const { selectedEntityId } = useEntityContext();
  const { data: entitiesData = [] } = useEntities();

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
    useState<GridColumnVisibilityModel>({
      is_capital_expense: false,
      is_tax_deductible: false,
      is_recurring: false,
      is_reimbursable: false,
      exclude_from_income: false,
      exclude_from_expenses: false,
    });
  // Grid API ref to control edit mode programmatically
  const apiRef = useGridApiRef();

  // Row editing state
  const [rowModesModel, setRowModesModel] = useState<GridRowModesModel>({});

  // Hooks for data
  const updateTransaction = useUpdateTransaction();
  // Fetch all categories (unfiltered) so inline editors can filter per-row by entity
  const { data: categoriesData } = useCategories();
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
  const [isExporting, setIsExporting] = useState(false);
  const [filtersDialogOpen, setFiltersDialogOpen] = useState(false);

  // Bulk selection state
  const [selectedRowIds, setSelectedRowIds] = useState<number[]>([]);
  const [bulkEntityDialogOpen, setBulkEntityDialogOpen] = useState(false);
  const [bulkEntityId, setBulkEntityId] = useState<string>("");

  // State for advanced filters
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    transaction_type: "",
    category_id: "",
    account_id: initialAccountId,
    include_in_analysis: "",
    is_transfer: "",
    include_capital_expenses: true,
    include_transfers: true,
  });

  // Fetch transactions with filters
  const { data, isLoading, error, refetch } = useTransactions({
    search_text: searchText || undefined,
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
    transaction_type: filters.transaction_type || undefined,
    category_id: filters.category_id ? Number(filters.category_id) : undefined,
    account_id: filters.account_id ? Number(filters.account_id) : undefined,
    include_in_analysis: filters.include_in_analysis
      ? filters.include_in_analysis === "true"
      : undefined,
    is_transfer: filters.is_transfer
      ? filters.is_transfer === "true"
      : undefined,
    entity_id: selectedEntityId ?? undefined,
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

        return (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              width: "100%",
            }}
          >
            {hasRelationship && (
              <Tooltip title="Part of a linked transaction pair - Click row to view related transaction">
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
        const isUncategorized = !categoryName;
        const splits = params.row.splits || [];
        const hasSplits = splits.length > 0;

        if (isUncategorized && !hasSplits) {
          return (
            <Typography variant="body2" sx={{ color: "warning.main", fontStyle: "italic" }}>
              Uncategorized
            </Typography>
          );
        }

        if (hasSplits) {
          return (
            <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
              <Typography variant="body2" noWrap>
                {categoryName || "Split"}
              </Typography>
              <Typography variant="caption" sx={{
                bgcolor: "action.selected",
                px: 0.5,
                borderRadius: 0.5,
                fontSize: "0.65rem",
                whiteSpace: "nowrap",
              }}>
                {splits.length} splits
              </Typography>
            </Box>
          );
        }

        return categoryName;
      },
      renderEditCell: (params) => {
        const id = params.id as number;
        const currentValue =
          (params.value as number) ?? params.row.category_id ?? "";
        // Filter categories by the row's entity_id: show entity-scoped + global categories
        const rowEntityId = params.row.entity_id;
        const rowCategoryOptions = categoriesData?.categories
          ?.filter((cat) => !rowEntityId || !cat.entity_id || cat.entity_id === rowEntityId)
          .map((cat) => ({ value: cat.category_id, label: cat.category_name })) || [];
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
                enqueueSnackbar("Failed to update transaction", {
                  variant: "error",
                });
              } finally {
                apiRef.current.stopCellEditMode({ id, field: "category_id" });
              }
            }}
          >
            {rowCategoryOptions.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </Select>
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
      field: "account_id",
      headerName: "Account",
      width: 220,
      valueGetter: (_value, row) => {
        if (row.account_id && accountsData) {
          const account = accountsData.find(
            (a) => a.account_id === row.account_id
          );
          if (account) {
            return account.institution_name
              ? `${account.account_name} (${account.institution_name})`
              : account.account_name;
          }
        }
        return row.source || "-";
      },
      filterable: false,
    },
    {
      field: "entity_id",
      headerName: "Entity",
      width: 140,
      filterable: false,
      sortable: false,
      valueGetter: (_value, row) => {
        if (row.entity_id) {
          const entity = entitiesData.find((e) => e.entity_id === row.entity_id);
          return entity?.entity_name || "-";
        }
        if (row.account_id && accountsData) {
          const account = accountsData.find((a) => a.account_id === row.account_id);
          if (account && account.entity_ids?.length > 0) {
            return account.entity_ids
              .map((eid: number) => entitiesData.find((e) => e.entity_id === eid)?.entity_name)
              .filter(Boolean)
              .join(", ");
          }
        }
        return "-";
      },
      renderCell: (params) => (
        <Typography
          variant="body2"
          color={params.row.entity_id ? "text.primary" : "text.secondary"}
          sx={{ fontStyle: params.row.entity_id ? "normal" : "italic" }}
          noWrap
        >
          {params.value}
        </Typography>
      ),
    } as GridColDef,
    ...([
      { field: "is_capital_expense", headerName: "CapEx" },
      { field: "is_tax_deductible", headerName: "Tax Ded." },
      { field: "is_recurring", headerName: "Recurring" },
      { field: "is_reimbursable", headerName: "Reimb." },
      { field: "exclude_from_income", headerName: "Excl. Income" },
      { field: "exclude_from_expenses", headerName: "Excl. Expense" },
    ].map((col) => ({
      field: col.field,
      headerName: col.headerName,
      width: 90,
      filterable: false,
      sortable: false,
      renderCell: (params: any) => (
        <Checkbox
          size="small"
          checked={!!params.value}
          onClick={(e) => e.stopPropagation()}
          onChange={async (e) => {
            e.stopPropagation();
            try {
              await updateTransaction.mutateAsync({
                id: params.row.id,
                data: { [col.field]: e.target.checked },
              });
              enqueueSnackbar("Transaction updated", { variant: "success" });
            } catch {
              enqueueSnackbar("Failed to update transaction", { variant: "error" });
            }
          }}
        />
      ),
    })) as GridColDef[]),
  ];

  const handleCellClick = (params: any) => {
    // Don't open detail dialog when clicking on editable or boolean toggle cells
    const nonClickableFields = [
      "__check__", "description", "category_id",
      "is_capital_expense", "is_tax_deductible", "is_recurring",
      "is_reimbursable", "exclude_from_income", "exclude_from_expenses",
    ];
    if (!nonClickableFields.includes(params.field)) {
      setSelectedTransaction(params.row);
      setDetailDialogOpen(true);
    }
  };

  const filteredTransactions = (data as any)?.transactions || [];

  // Count active advanced filters (excludes search and default-on checkboxes)
  const activeFilterCount = [
    filters.start_date,
    filters.end_date,
    filters.transaction_type,
    filters.category_id,
    filters.account_id,
    filters.include_in_analysis,
    filters.is_transfer,
    !filters.include_capital_expenses ? "on" : "",
    !filters.include_transfers ? "on" : "",
  ].filter(Boolean).length;

  const handleExportCsv = useCallback(async () => {
    setIsExporting(true);
    try {
      // Fetch all matching transactions (no pagination)
      const allData = await getTransactions({
        search_text: searchText || undefined,
        start_date: filters.start_date || undefined,
        end_date: filters.end_date || undefined,
        transaction_type: filters.transaction_type || undefined,
        category_id: filters.category_id
          ? Number(filters.category_id)
          : undefined,
        account_id: filters.account_id
          ? Number(filters.account_id)
          : undefined,
        entity_id: selectedEntityId ?? undefined,
        include_in_analysis: filters.include_in_analysis
          ? filters.include_in_analysis === "true"
          : undefined,
        is_transfer: filters.is_transfer
          ? filters.is_transfer === "true"
          : undefined,
        include_capital_expenses: filters.include_capital_expenses,
        include_transfers: filters.include_transfers,
        limit: 10000,
        offset: 0,
        sort_by: sortModel[0]?.field
          ? fieldToApiFieldMap[sortModel[0].field] || sortModel[0].field
          : "transaction_date",
        sort_order: sortModel[0]?.sort || "desc",
      });

      const rows = allData.transactions;
      if (rows.length === 0) {
        enqueueSnackbar("No transactions to export", { variant: "info" });
        return;
      }

      // Resolve account names
      const getAccountName = (accountId?: number) => {
        if (!accountId || !accountsData) return "";
        const account = accountsData.find((a) => a.account_id === accountId);
        return account?.account_name || "";
      };

      const headers = [
        "Date",
        "Description",
        "Amount",
        "Type",
        "Category",
        "Account",
        "Transfer",
        "Notes",
        "Tags",
      ];
      const csvRows = rows.map((tx) => [
        tx.date,
        `"${(tx.description || "").replace(/"/g, '""')}"`,
        tx.amount,
        tx.transaction_type,
        tx.category_name || "",
        getAccountName(tx.account_id),
        tx.is_transfer ? "Yes" : "No",
        `"${(tx.notes || "").replace(/"/g, '""')}"`,
        `"${(tx.tags || []).join(", ")}"`,
      ]);

      const csv = [headers.join(","), ...csvRows.map((r) => r.join(","))].join(
        "\n"
      );
      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `transactions-${new Date().toISOString().split("T")[0]}.csv`;
      link.click();
      URL.revokeObjectURL(url);

      enqueueSnackbar(`Exported ${rows.length} transactions`, {
        variant: "success",
      });
    } catch {
      enqueueSnackbar("Failed to export transactions", { variant: "error" });
    } finally {
      setIsExporting(false);
    }
  }, [
    searchText,
    filters,
    sortModel,
    fieldToApiFieldMap,
    accountsData,
    selectedEntityId,
    enqueueSnackbar,
  ]);

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
            variant="outlined"
            startIcon={
              isExporting ? (
                <CircularProgress size={20} />
              ) : (
                <DownloadIcon />
              )
            }
            onClick={handleExportCsv}
            disabled={isExporting}
          >
            {isExporting ? "Exporting..." : "Export CSV"}
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
              <Badge
                badgeContent={activeFilterCount}
                color="primary"
                invisible={activeFilterCount === 0}
              >
                <Button
                  variant="outlined"
                  startIcon={<FilterListIcon />}
                  onClick={() => setFiltersDialogOpen(true)}
                >
                  More Filters
                </Button>
              </Badge>
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
                      account_id: "",
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

      {/* Bulk Action Bar */}
      {selectedRowIds.length > 0 && (
        <Paper sx={{ p: 1.5, mb: 1, display: "flex", alignItems: "center", gap: 2, bgcolor: "primary.50" }}>
          <Typography variant="body2" sx={{ fontWeight: "medium" }}>
            {selectedRowIds.length} selected
          </Typography>
          <Button
            size="small"
            variant="outlined"
            onClick={() => setBulkEntityDialogOpen(true)}
          >
            Assign Entity
          </Button>
          <Button
            size="small"
            variant="text"
            onClick={() => setSelectedRowIds([])}
          >
            Clear Selection
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
                return `${start}–${to} of ${total}`; // EN DASH
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
          checkboxSelection
          onRowSelectionModelChange={(model) => {
            // MUI DataGrid v7: model is { type, ids: Set<GridRowId> }
            const ids = model && typeof model === 'object' && 'ids' in model
              ? Array.from((model as any).ids)
              : Array.isArray(model) ? model : [];
            setSelectedRowIds(ids as number[]);
          }}
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
              enqueueSnackbar("Failed to update transaction", {
                variant: "error",
              });
            }
          }}
          getRowClassName={(params) => {
            const categoryName = params.row.category_name;
            const isUncategorized = !categoryName;

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
            "& .MuiDataGrid-footerContainer": {
              minHeight: "52px",
            },
          }}
        />
      </Paper>

      {/* Edit Transaction Dialog (opens when clicking a row) */}
      <TransactionForm
        open={detailDialogOpen}
        onClose={() => {
          setDetailDialogOpen(false);
          setSelectedTransaction(null);
        }}
        transaction={selectedTransaction}
        mode="edit"
      />

      {/* Create Transaction Dialog */}
      <TransactionForm
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        mode="create"
      />

      {/* Bulk Entity Assignment Dialog */}
      <Dialog
        open={bulkEntityDialogOpen}
        onClose={() => setBulkEntityDialogOpen(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Assign Entity to {selectedRowIds.length} Transactions</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Entity"
            value={bulkEntityId}
            onChange={(e) => setBulkEntityId(e.target.value)}
            sx={{ mt: 1 }}
          >
            <MenuItem value=""><em>None (clear entity)</em></MenuItem>
            {entitiesData.map((entity) => (
              <MenuItem key={entity.entity_id} value={String(entity.entity_id)}>
                {entity.entity_name}
              </MenuItem>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBulkEntityDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={async () => {
              const entityIdValue = bulkEntityId === "" ? null : parseInt(bulkEntityId, 10);
              try {
                const response = await fetch("/api/transactions/bulk-update", {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    transaction_ids: selectedRowIds,
                    updates: { entity_id: entityIdValue },
                  }),
                });
                if (!response.ok) throw new Error("Bulk update failed");
                const result = await response.json();
                enqueueSnackbar(`Entity updated for ${result.updated} transactions`, { variant: "success" });
                setBulkEntityDialogOpen(false);
                setSelectedRowIds([]);
                setBulkEntityId("");
                queryClient.invalidateQueries({ queryKey: ["transactions"] });
              } catch {
                enqueueSnackbar("Failed to update entities", { variant: "error" });
              }
            }}
          >
            Assign
          </Button>
        </DialogActions>
      </Dialog>

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
              <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                {[
                  {
                    label: "Last 30 days",
                    getRange: () => {
                      const end = new Date();
                      const start = new Date();
                      start.setDate(start.getDate() - 30);
                      return {
                        start_date: start.toISOString().split("T")[0],
                        end_date: end.toISOString().split("T")[0],
                      };
                    },
                  },
                  {
                    label: "This month",
                    getRange: () => {
                      const now = new Date();
                      const start = new Date(
                        now.getFullYear(),
                        now.getMonth(),
                        1
                      );
                      return {
                        start_date: start.toISOString().split("T")[0],
                        end_date: now.toISOString().split("T")[0],
                      };
                    },
                  },
                  {
                    label: "Last month",
                    getRange: () => {
                      const now = new Date();
                      const start = new Date(
                        now.getFullYear(),
                        now.getMonth() - 1,
                        1
                      );
                      const end = new Date(
                        now.getFullYear(),
                        now.getMonth(),
                        0
                      );
                      return {
                        start_date: start.toISOString().split("T")[0],
                        end_date: end.toISOString().split("T")[0],
                      };
                    },
                  },
                  {
                    label: "Year to date",
                    getRange: () => {
                      const now = new Date();
                      const start = new Date(now.getFullYear(), 0, 1);
                      return {
                        start_date: start.toISOString().split("T")[0],
                        end_date: now.toISOString().split("T")[0],
                      };
                    },
                  },
                ].map((preset) => (
                  <Chip
                    key={preset.label}
                    label={preset.label}
                    size="small"
                    variant={
                      filters.start_date ===
                        preset.getRange().start_date &&
                      filters.end_date === preset.getRange().end_date
                        ? "filled"
                        : "outlined"
                    }
                    color={
                      filters.start_date ===
                        preset.getRange().start_date &&
                      filters.end_date === preset.getRange().end_date
                        ? "primary"
                        : "default"
                    }
                    onClick={() =>
                      setFilters({
                        ...filters,
                        ...preset.getRange(),
                      })
                    }
                  />
                ))}
              </Box>
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
            <Grid item xs={12} data-testid="filter-category">
              <Autocomplete
                options={categoriesData?.categories || []}
                getOptionLabel={(option) => option.category_name}
                value={
                  categoriesData?.categories?.find(
                    (c) => c.category_id === Number(filters.category_id)
                  ) || null
                }
                onChange={(_e, newValue) =>
                  setFilters({
                    ...filters,
                    category_id: newValue ? String(newValue.category_id) : "",
                  })
                }
                renderInput={(params) => (
                  <TextField {...params} label="Category" placeholder="Search categories..." />
                )}
                isOptionEqualToValue={(option, value) =>
                  option.category_id === value.category_id
                }
                groupBy={(option) =>
                  option.parent_category_id
                    ? categoriesData?.categories?.find(
                        (c) => c.category_id === option.parent_category_id
                      )?.category_name || "Other"
                    : option.category_name
                }
              />
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
