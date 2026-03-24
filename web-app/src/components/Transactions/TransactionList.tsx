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
  Alert,
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
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import RuleIcon from "@mui/icons-material/Rule";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import CloseIcon from "@mui/icons-material/Close";
import {
  useTransactions,
  useUpdateTransaction,
} from "../../hooks/useTransactions";
import { useCategories, useCreateCategory } from "../../hooks/useCategories";
import { formatCurrency, formatDate } from "../../utils/formatters";
import TransactionForm from "./TransactionForm";
import type { Transaction } from "../../types/transaction";
import { useSnackbar } from "notistack";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { detectAllRelationships } from "../../api/relationships";
import CircularProgress from "@mui/material/CircularProgress";
import { categoryRulesApi } from "../../api/categories";
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

  // Inline category creation state
  const [newCatDialogOpen, setNewCatDialogOpen] = useState(false);
  const [newCatName, setNewCatName] = useState("");
  const [newCatType, setNewCatType] = useState<"Income" | "Expense" | "Transfer">("Expense");
  const [pendingCatTxId, setPendingCatTxId] = useState<number | null>(null);
  const [pendingCatSmartIdx, setPendingCatSmartIdx] = useState<number | null>(null);

  // Smart Categorize state
  const [smartCatOpen, setSmartCatOpen] = useState(false);
  const [smartCatLoading, setSmartCatLoading] = useState(false);
  const [smartCatDescriptions, setSmartCatDescriptions] = useState<any[]>([]);
  const [smartCatTotal, setSmartCatTotal] = useState(0);
  const [smartCatTotalTxns, setSmartCatTotalTxns] = useState(0);
  const [smartCatPage, setSmartCatPage] = useState(0);
  const [smartCatClassifying, setSmartCatClassifying] = useState(false);
  const [smartCatApplying, setSmartCatApplying] = useState(false);
  const [smartCatResults, setSmartCatResults] = useState<any[]>([]); // LLM suggestions (not yet applied)
  const [smartCatApplied, setSmartCatApplied] = useState<any[]>([]); // Already applied results
  const [smartCatSelected, setSmartCatSelected] = useState<Set<number>>(new Set());
  const [smartCatApproved, setSmartCatApproved] = useState<Set<number>>(new Set()); // Indices in smartCatResults
  const [smartCatOverrides, setSmartCatOverrides] = useState<Record<number, number>>({}); // index → category_id override

  // Create Rule inline state
  const [ruleDialogOpen, setRuleDialogOpen] = useState(false);
  const [ruleForm, setRuleForm] = useState({
    rule_name: "",
    description_pattern: "",
    category_id: null as number | null,
    entity_id: null as number | null,
  });

  // Hooks for data
  const updateTransaction = useUpdateTransaction();
  const createCategory = useCreateCategory();
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
  const [bulkCategoryDialogOpen, setBulkCategoryDialogOpen] = useState(false);
  const [bulkCategoryId, setBulkCategoryId] = useState<string>("");

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
      const detail = error instanceof Error ? error.message : '';
      enqueueSnackbar(detail ? `Failed to update: ${detail}` : "Failed to update transaction", { variant: "error" });
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
      field: "is_cleared",
      headerName: "",
      width: 40,
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      renderCell: (params) =>
        params.row.is_cleared ? (
          <Tooltip title={`Cleared${params.row.cleared_date ? ` on ${params.row.cleared_date}` : ''}`}>
            <CheckCircleIcon fontSize="small" color="success" />
          </Tooltip>
        ) : null,
    },
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
            <MenuItem
              value="__create__"
              sx={{ borderTop: 1, borderColor: 'divider', fontStyle: 'italic', color: 'primary.main' }}
              onClick={(e) => {
                e.stopPropagation();
                setPendingCatTxId(id);
                setNewCatType(params.row.transaction_type === 'Income' ? 'Income' : 'Expense');
                setNewCatDialogOpen(true);
                apiRef.current.stopCellEditMode({ id, field: "category_id" });
              }}
            >
              + Create New Category
            </MenuItem>
          </Select>
        );
      },
    },
    {
      field: "amount",
      headerName: "Amount",
      width: 150,
      align: "right",
      headerAlign: "right",
      renderCell: (params) => {
        const isSplitPortion = params.row.split_portion;
        return (
          <Box sx={{ display: "flex", alignItems: "center", gap: 0.5, justifyContent: "flex-end", width: "100%" }}>
            {isSplitPortion && (
              <Tooltip title="Showing entity's split portion">
                <Chip label="split" size="small" variant="outlined" color="info" sx={{ height: 18, fontSize: "0.65rem", "& .MuiChip-label": { px: 0.5 } }} />
              </Tooltip>
            )}
            <span>{formatCurrency(params.value)}</span>
          </Box>
        );
      },
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
    {
      field: "actions",
      headerName: "",
      width: 50,
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      renderCell: (params) => (
        <Tooltip title="Create rule from this transaction">
          <IconButton
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              const tx = params.row;
              setRuleForm({
                rule_name: (tx.description || "").slice(0, 50),
                description_pattern: tx.description || "",
                category_id: tx.category_id || null,
                entity_id: tx.entity_id || null,
              });
              setRuleDialogOpen(true);
            }}
          >
            <RuleIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      ),
    },
  ];

  const handleCellClick = useCallback((params: any, event: any) => {
    // Don't open detail dialog when clicking on editable or boolean toggle cells
    const nonClickableFields = [
      "__check__", "description", "category_id", "actions",
      "is_capital_expense", "is_tax_deductible", "is_recurring",
      "is_reimbursable", "exclude_from_income", "exclude_from_expenses",
    ];
    if (nonClickableFields.includes(params.field)) return;
    // Prevent default to stop the click from propagating to sort handlers
    if (event) event.defaultMuiPrevented = true;
    setSelectedTransaction(params.row);
    setDetailDialogOpen(true);
  }, []);

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
            startIcon={<AutoFixHighIcon />}
            onClick={async () => {
              setSmartCatOpen(true);
              setSmartCatLoading(true);
              setSmartCatDescriptions([]);
              setSmartCatResults([]);
              setSmartCatApplied([]);
              setSmartCatSelected(new Set());
              setSmartCatApproved(new Set());
              setSmartCatOverrides({});
              setSmartCatPage(0);
              try {
                const response = await fetch("/api/transactions/uncategorized-descriptions?offset=0&limit=20");
                const data = await response.json();
                if (!response.ok) throw new Error(data.detail || "Failed");
                setSmartCatDescriptions(data.descriptions);
                setSmartCatTotal(data.total);
                setSmartCatTotalTxns(data.total_transactions);
              } catch (err: any) {
                enqueueSnackbar(err.message || "Failed to load descriptions", { variant: "error" });
              } finally {
                setSmartCatLoading(false);
              }
            }}
          >
            Smart Categorize
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
            onClick={() => setBulkCategoryDialogOpen(true)}
          >
            Assign Category
          </Button>
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
          localeText={{
            noRowsLabel: "No transactions match your filters. Try adjusting your search or filters.",
          }}
          onCellClick={handleCellClick}
          disableColumnMenu={false}
          columnVisibilityModel={columnVisibilityModel}
          onColumnVisibilityModelChange={setColumnVisibilityModel}
          checkboxSelection
          disableRowSelectionOnClick
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
            "& .MuiDataGrid-cell": {
              display: "flex",
              alignItems: "center",
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
                if (result.failed && result.failed.length > 0) {
                  enqueueSnackbar(
                    `Updated ${result.updated} of ${result.total} transactions. ${result.failed.length} failed.`,
                    { variant: "warning" }
                  );
                } else {
                  enqueueSnackbar(`Entity updated for ${result.updated} transactions`, { variant: "success" });
                }
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

      {/* Bulk Category Assignment Dialog */}
      <Dialog
        open={bulkCategoryDialogOpen}
        onClose={() => setBulkCategoryDialogOpen(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Assign Category to {selectedRowIds.length} Transactions</DialogTitle>
        <DialogContent>
          <TextField
            select
            fullWidth
            label="Category"
            value={bulkCategoryId}
            onChange={(e) => setBulkCategoryId(e.target.value)}
            sx={{ mt: 1 }}
          >
            <MenuItem value=""><em>Select a category</em></MenuItem>
            {categoriesData?.categories?.map((cat) => (
              <MenuItem key={cat.category_id} value={String(cat.category_id)}>
                {cat.category_name}
              </MenuItem>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBulkCategoryDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            disabled={!bulkCategoryId}
            onClick={async () => {
              const categoryIdValue = parseInt(bulkCategoryId, 10);
              try {
                const response = await fetch("/api/transactions/bulk-update", {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    transaction_ids: selectedRowIds,
                    updates: { category_id: categoryIdValue },
                  }),
                });
                if (!response.ok) throw new Error("Bulk update failed");
                const result = await response.json();
                if (result.failed && result.failed.length > 0) {
                  enqueueSnackbar(
                    `Updated ${result.updated} of ${result.total} transactions. ${result.failed.length} failed.`,
                    { variant: "warning" }
                  );
                } else {
                  enqueueSnackbar(`Category updated for ${result.updated} transactions`, { variant: "success" });
                }
                setBulkCategoryDialogOpen(false);
                setSelectedRowIds([]);
                setBulkCategoryId("");
                queryClient.invalidateQueries({ queryKey: ["transactions"] });
              } catch {
                enqueueSnackbar("Failed to update categories", { variant: "error" });
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

      {/* Smart Categorize Review Dialog */}
      <Dialog open={smartCatOpen} onClose={() => setSmartCatOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box>
              Smart Categorization
              {smartCatTotal > 0 && (
                <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                  {smartCatTotal} unique descriptions, {smartCatTotalTxns} transactions
                </Typography>
              )}
            </Box>
            <IconButton onClick={() => setSmartCatOpen(false)} size="small" aria-label="Close">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {smartCatLoading && (
            <Box display="flex" flexDirection="column" alignItems="center" py={4}>
              <CircularProgress />
              <Typography sx={{ mt: 2 }}>Loading...</Typography>
            </Box>
          )}

          {/* Already applied results */}
          {smartCatApplied.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" color="success.main" gutterBottom>
                Applied ({smartCatApplied.length})
              </Typography>
              <Box sx={{ maxHeight: 150, overflow: 'auto', border: 1, borderColor: 'divider', borderRadius: 1 }}>
                {smartCatApplied.map((r: any, i: number) => (
                  <Box key={i} sx={{ display: 'flex', alignItems: 'center', px: 2, py: 0.5, borderBottom: '1px solid', borderColor: 'divider' }}>
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                      <Typography variant="body2" noWrap>{r.merchant_name}: {r.description}</Typography>
                    </Box>
                    <Chip label={r.applied_category || r.suggested_category} size="small" color="success" sx={{ mx: 1 }} />
                    <Typography variant="caption" color="text.secondary">{r.transaction_count} txns</Typography>
                  </Box>
                ))}
              </Box>
            </Box>
          )}

          {/* Step 2: Review LLM suggestions (not yet applied) */}
          {smartCatResults.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="subtitle2" color="warning.main">
                  Review Suggestions ({smartCatResults.length})
                </Typography>
                <Box>
                  <Button size="small" onClick={() => setSmartCatApproved(new Set(smartCatResults.map((_: any, i: number) => i)))}>
                    Approve All
                  </Button>
                  <Button size="small" onClick={() => setSmartCatApproved(new Set())}>
                    Clear
                  </Button>
                </Box>
              </Box>
              <Box sx={{ maxHeight: 300, overflow: 'auto', border: 1, borderColor: 'divider', borderRadius: 1 }}>
                {smartCatResults.map((r: any, i: number) => (
                  <Box key={i} sx={{
                    display: 'flex', alignItems: 'center', px: 1, py: 1,
                    borderBottom: '1px solid', borderColor: 'divider',
                    bgcolor: smartCatApproved.has(i) ? 'action.selected' : 'transparent',
                  }}>
                    <Checkbox
                      size="small"
                      checked={smartCatApproved.has(i)}
                      onChange={() => {
                        setSmartCatApproved(prev => {
                          const next = new Set(prev);
                          if (next.has(i)) next.delete(i); else next.add(i);
                          return next;
                        });
                      }}
                    />
                    <Box sx={{ flex: 1, minWidth: 0, mr: 1 }}>
                      <Typography variant="body2" noWrap>
                        <strong>{r.merchant_name}</strong> — {r.description}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" noWrap>
                        {r.reasoning} ({Math.round(r.confidence * 100)}% confidence, {r.transaction_count} txns)
                      </Typography>
                    </Box>
                    <FormControl size="small" sx={{ minWidth: 160 }}>
                      <Select
                        value={smartCatOverrides[i] ?? r.category_id ?? (r.suggested_category && !r.category_id ? "__new__" : "")}
                        onChange={(e) => {
                          const val = e.target.value;
                          if (val === "__new__") {
                            // Keep as __new__ — will auto-create on apply
                            setSmartCatOverrides(prev => { const next = { ...prev }; delete next[i]; return next; });
                          } else {
                            setSmartCatOverrides(prev => ({ ...prev, [i]: Number(val) }));
                          }
                          setSmartCatApproved(prev => { const next = new Set(prev); next.add(i); return next; });
                        }}
                        displayEmpty
                        size="small"
                      >
                        {r.suggested_category && !(smartCatOverrides[i] ?? r.category_id) && (
                          <MenuItem value="__new__" sx={{ color: 'success.main', fontWeight: 'bold' }}>
                            {r.suggested_category} (create new)
                          </MenuItem>
                        )}
                        {categoriesData?.categories?.map((cat) => (
                          <MenuItem key={cat.category_id} value={cat.category_id}>{cat.category_name}</MenuItem>
                        ))}
                        <MenuItem
                          value="__create__"
                          sx={{ borderTop: 1, borderColor: 'divider', fontStyle: 'italic', color: 'primary.main' }}
                          onClick={(e) => {
                            e.stopPropagation();
                            setPendingCatSmartIdx(i);
                            setPendingCatTxId(null);
                            setNewCatType("Expense");
                            setNewCatDialogOpen(true);
                          }}
                        >
                          + Create New Category
                        </MenuItem>
                      </Select>
                    </FormControl>
                  </Box>
                ))}
              </Box>
            </Box>
          )}

          {/* Step 1: Select descriptions to classify */}
          {!smartCatLoading && smartCatResults.length === 0 && smartCatDescriptions.length > 0 && (
            <Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="subtitle2">
                  Select descriptions to classify ({smartCatPage * 20 + 1}-{Math.min((smartCatPage + 1) * 20, smartCatTotal)} of {smartCatTotal})
                </Typography>
                <Box>
                  <Button size="small" onClick={() => setSmartCatSelected(new Set(smartCatDescriptions.map((_: any, i: number) => i)))}>
                    Select All
                  </Button>
                  <Button size="small" onClick={() => setSmartCatSelected(new Set())}>
                    Clear
                  </Button>
                </Box>
              </Box>
              <Box sx={{ border: 1, borderColor: 'divider', borderRadius: 1, mb: 2 }}>
                {smartCatDescriptions.map((d: any, i: number) => (
                  <Box
                    key={i}
                    sx={{
                      display: 'flex', alignItems: 'center', px: 1, py: 0.5,
                      borderBottom: '1px solid', borderColor: 'divider',
                      bgcolor: smartCatSelected.has(i) ? 'action.selected' : 'transparent',
                      cursor: 'pointer',
                    }}
                    onClick={() => {
                      setSmartCatSelected(prev => {
                        const next = new Set(prev);
                        if (next.has(i)) next.delete(i); else next.add(i);
                        return next;
                      });
                    }}
                  >
                    <Checkbox size="small" checked={smartCatSelected.has(i)} />
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                      <Typography variant="body2" noWrap>{d.description}</Typography>
                    </Box>
                    <Chip label={`${d.count} txns`} size="small" variant="outlined" sx={{ ml: 1 }} />
                  </Box>
                ))}
              </Box>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Button size="small" disabled={smartCatPage === 0}
                  onClick={async () => {
                    const p = smartCatPage - 1;
                    setSmartCatLoading(true);
                    try {
                      const res = await fetch(`/api/transactions/uncategorized-descriptions?offset=${p * 20}&limit=20`);
                      const data = await res.json();
                      setSmartCatDescriptions(data.descriptions); setSmartCatTotal(data.total); setSmartCatPage(p); setSmartCatSelected(new Set());
                    } finally { setSmartCatLoading(false); }
                  }}>Previous</Button>
                <Typography variant="caption">Page {smartCatPage + 1} of {Math.ceil(smartCatTotal / 20)}</Typography>
                <Button size="small" disabled={(smartCatPage + 1) * 20 >= smartCatTotal}
                  onClick={async () => {
                    const p = smartCatPage + 1;
                    setSmartCatLoading(true);
                    try {
                      const res = await fetch(`/api/transactions/uncategorized-descriptions?offset=${p * 20}&limit=20`);
                      const data = await res.json();
                      setSmartCatDescriptions(data.descriptions); setSmartCatTotal(data.total); setSmartCatPage(p); setSmartCatSelected(new Set());
                    } finally { setSmartCatLoading(false); }
                  }}>Next</Button>
              </Box>
            </Box>
          )}

          {!smartCatLoading && smartCatDescriptions.length === 0 && smartCatResults.length === 0 && smartCatApplied.length === 0 && (
            <Typography color="text.secondary">No uncategorized transactions found.</Typography>
          )}
        </DialogContent>
        <DialogActions sx={{ position: 'sticky', bottom: 0, bgcolor: 'background.paper', borderTop: 1, borderColor: 'divider' }}>
          <Button onClick={() => setSmartCatOpen(false)}>Close</Button>

          {/* Step 1 action: Classify selected descriptions */}
          {smartCatResults.length === 0 && smartCatDescriptions.length > 0 && (
            <Button
              variant="contained"
              disabled={smartCatSelected.size === 0 || smartCatClassifying}
              startIcon={smartCatClassifying ? <CircularProgress size={16} /> : <AutoFixHighIcon />}
              onClick={async () => {
                setSmartCatClassifying(true);
                const descs = Array.from(smartCatSelected).map(i => smartCatDescriptions[i]?.description).filter(Boolean);
                try {
                  const res = await fetch("/api/transactions/classify-batch", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ descriptions: descs, mode: "preview" }),
                  });
                  const data = await res.json();
                  if (!res.ok) throw new Error(data.detail || "Failed");
                  setSmartCatResults(data.results || []);
                  setSmartCatApproved(new Set((data.results || []).map((_: any, i: number) => i)));
                  setSmartCatSelected(new Set());
                } catch (err: any) {
                  enqueueSnackbar(err.message || "Classification failed", { variant: "error" });
                } finally {
                  setSmartCatClassifying(false);
                }
              }}
            >
              {smartCatClassifying ? "Classifying..." : `Classify Selected (${smartCatSelected.size})`}
            </Button>
          )}

          {/* Step 2 actions: Apply approved or go back */}
          {smartCatResults.length > 0 && (
            <>
              <Button
                variant="outlined"
                onClick={() => {
                  setSmartCatResults([]);
                  setSmartCatApproved(new Set());
                  setSmartCatOverrides({});
                }}
              >
                Back
              </Button>
              <Button
                variant="contained"
                disabled={smartCatApproved.size === 0 || smartCatApplying}
                startIcon={smartCatApplying ? <CircularProgress size={16} /> : <AutoFixHighIcon />}
                onClick={async () => {
                  setSmartCatApplying(true);
                  try {
                    // Step 1: Create any new categories that the LLM suggested
                    const updatedOverrides = { ...smartCatOverrides };
                    for (const i of Array.from(smartCatApproved)) {
                      const r = smartCatResults[i];
                      const hasOverride = updatedOverrides[i] !== undefined;
                      const catId = hasOverride ? updatedOverrides[i] : r.category_id;
                      if (!catId && r.suggested_category) {
                        // Need to create this category
                        const created = await createCategory.mutateAsync({
                          category_name: r.suggested_category,
                          category_type: r.transaction_type === "Income" ? "Income" : "Expense",
                        });
                        updatedOverrides[i] = created.category_id;
                      }
                    }
                    setSmartCatOverrides(updatedOverrides);

                    // Step 2: Build assignments with resolved category IDs
                    const assignments = Array.from(smartCatApproved).map(i => {
                      const r = smartCatResults[i];
                      const catId = updatedOverrides[i] ?? r.category_id;
                      return {
                        description: r.description,
                        category_id: catId,
                        suggested_pattern: r.suggested_pattern,
                        rule_name: `Auto: ${r.merchant_name || r.description.slice(0, 30)}`,
                      };
                    }).filter(a => a.category_id);

                    // Step 3: Apply via backend (no LLM call — just DB updates)
                    const res = await fetch("/api/transactions/apply-categories", {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({ assignments, create_rules: true }),
                    });
                    const data = await res.json();
                    if (!res.ok) throw new Error(data.detail || "Failed");

                    // Step 4: Move to applied list
                    const appliedItems = Array.from(smartCatApproved).map(i => {
                      const r = smartCatResults[i];
                      const catId = updatedOverrides[i] ?? r.category_id;
                      const catName = categoriesData?.categories?.find(c => c.category_id === catId)?.category_name || r.suggested_category;
                      return { ...r, applied_category: catName };
                    });
                    setSmartCatApplied(prev => [...prev, ...appliedItems]);
                    setSmartCatResults([]);
                    setSmartCatApproved(new Set());
                    setSmartCatOverrides({});
                    queryClient.invalidateQueries({ queryKey: ["transactions"] });
                    queryClient.invalidateQueries({ queryKey: ["categories"] });
                    enqueueSnackbar(`Applied ${appliedItems.length} classifications (${data.total_updated} transactions updated, ${data.rules_created} rules created)`, { variant: "success" });

                    // Reload descriptions
                    const pageRes = await fetch(`/api/transactions/uncategorized-descriptions?offset=${smartCatPage * 20}&limit=20`);
                    const pageData = await pageRes.json();
                    setSmartCatDescriptions(pageData.descriptions);
                    setSmartCatTotal(pageData.total);
                    setSmartCatTotalTxns(pageData.total_transactions);
                  } catch (err: any) {
                    enqueueSnackbar(err.message || "Apply failed", { variant: "error" });
                  } finally {
                    setSmartCatApplying(false);
                  }
                }}
              >
                {smartCatApplying ? "Applying..." : `Apply Approved (${smartCatApproved.size})`}
              </Button>
            </>
          )}
        </DialogActions>
      </Dialog>

      {/* Create Rule from Transaction Dialog */}
      <Dialog open={ruleDialogOpen} onClose={() => setRuleDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Transaction Rule</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Rule Name"
            value={ruleForm.rule_name}
            onChange={(e) => setRuleForm({ ...ruleForm, rule_name: e.target.value })}
            sx={{ mt: 1, mb: 2 }}
          />
          <TextField
            fullWidth
            label="Description Pattern (matches transactions containing this text)"
            value={ruleForm.description_pattern}
            onChange={(e) => setRuleForm({ ...ruleForm, description_pattern: e.target.value })}
            sx={{ mb: 2 }}
          />
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Assign Category</InputLabel>
            <Select
              value={ruleForm.category_id ?? ""}
              label="Assign Category"
              onChange={(e) => setRuleForm({ ...ruleForm, category_id: e.target.value ? Number(e.target.value) : null })}
            >
              <MenuItem value="">None</MenuItem>
              {categoriesData?.categories?.map((cat) => (
                <MenuItem key={cat.category_id} value={cat.category_id}>
                  {cat.category_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Assign Entity</InputLabel>
            <Select
              value={ruleForm.entity_id ?? ""}
              label="Assign Entity"
              onChange={(e) => setRuleForm({ ...ruleForm, entity_id: e.target.value ? Number(e.target.value) : null })}
            >
              <MenuItem value="">None</MenuItem>
              {entitiesData?.map((entity: any) => (
                <MenuItem key={entity.entity_id} value={entity.entity_id}>
                  {entity.entity_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRuleDialogOpen(false)}>Cancel</Button>
          <Button
            variant="outlined"
            disabled={!ruleForm.rule_name.trim() || !ruleForm.description_pattern.trim()}
            onClick={async () => {
              try {
                await categoryRulesApi.create({
                  rule_name: ruleForm.rule_name.trim(),
                  description_pattern: ruleForm.description_pattern.trim(),
                  category_id: ruleForm.category_id,
                  entity_id: ruleForm.entity_id,
                  is_active: true,
                  rule_priority: 10,
                });
                enqueueSnackbar(`Rule "${ruleForm.rule_name}" created`, { variant: "success" });
                setRuleDialogOpen(false);
              } catch {
                enqueueSnackbar("Failed to create rule", { variant: "error" });
              }
            }}
          >
            Create Only
          </Button>
          <Button
            variant="contained"
            disabled={!ruleForm.rule_name.trim() || !ruleForm.description_pattern.trim()}
            onClick={async () => {
              try {
                const rule = await categoryRulesApi.create({
                  rule_name: ruleForm.rule_name.trim(),
                  description_pattern: ruleForm.description_pattern.trim(),
                  category_id: ruleForm.category_id,
                  entity_id: ruleForm.entity_id,
                  is_active: true,
                  rule_priority: 10,
                });
                const result = await categoryRulesApi.apply({
                  rule_ids: [rule.rule_id],
                  force_recategorize: true,
                });
                queryClient.invalidateQueries({ queryKey: ["transactions"] });
                enqueueSnackbar(
                  `Rule created — ${result.categorized_count} categorized, ${result.entity_assigned_count} entities assigned`,
                  { variant: "success" }
                );
                setRuleDialogOpen(false);
              } catch {
                enqueueSnackbar("Failed to create or apply rule", { variant: "error" });
              }
            }}
          >
            Create & Apply
          </Button>
        </DialogActions>
      </Dialog>

      {/* Inline Create Category Dialog */}
      <Dialog open={newCatDialogOpen} onClose={() => setNewCatDialogOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Create New Category</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Category Name"
            value={newCatName}
            onChange={(e) => setNewCatName(e.target.value)}
            sx={{ mt: 1, mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Type</InputLabel>
            <Select
              value={newCatType}
              label="Type"
              onChange={(e) => setNewCatType(e.target.value as "Income" | "Expense" | "Transfer")}
            >
              <MenuItem value="Income">Income</MenuItem>
              <MenuItem value="Expense">Expense</MenuItem>
              <MenuItem value="Transfer">Transfer</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => { setNewCatDialogOpen(false); setNewCatName(""); }}>Cancel</Button>
          <Button
            variant="contained"
            disabled={!newCatName.trim() || createCategory.isPending}
            onClick={async () => {
              try {
                const created = await createCategory.mutateAsync({
                  category_name: newCatName.trim(),
                  category_type: newCatType,
                });
                // Assign the new category to the pending transaction
                if (pendingCatTxId) {
                  await updateTransaction.mutateAsync({
                    id: pendingCatTxId,
                    data: { category_id: created.category_id },
                  });
                }
                // Or assign to the smart categorize review item
                if (pendingCatSmartIdx !== null) {
                  setSmartCatOverrides(prev => ({ ...prev, [pendingCatSmartIdx]: created.category_id }));
                  setSmartCatApproved(prev => { const next = new Set(prev); next.add(pendingCatSmartIdx); return next; });
                }
                enqueueSnackbar(`Category "${newCatName}" created${pendingCatTxId ? " and assigned" : ""}`, { variant: "success" });
                setNewCatDialogOpen(false);
                setNewCatName("");
                setPendingCatTxId(null);
                setPendingCatSmartIdx(null);
              } catch {
                enqueueSnackbar("Failed to create category", { variant: "error" });
              }
            }}
          >
            {createCategory.isPending ? <CircularProgress size={20} /> : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default TransactionList;
