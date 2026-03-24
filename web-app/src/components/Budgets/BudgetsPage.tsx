import { useState, useMemo } from "react";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Chip,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import SavingsIcon from "@mui/icons-material/Savings";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import { useEntityContext } from "../../contexts/EntityContext";
import { formatCurrency } from "../../utils/formatters";

// API functions
const fetchBudgets = async (entityId?: number | null) => {
  const params = new URLSearchParams();
  if (entityId) params.set("entity_id", String(entityId));
  params.set("is_active", "true");
  const res = await fetch(`/api/budgets?${params}`);
  if (!res.ok) throw new Error("Failed to fetch budgets");
  return res.json();
};

const fetchBudgetSummary = async (year: number, month: number, entityId?: number | null) => {
  const params = new URLSearchParams({ year: String(year), month: String(month) });
  if (entityId) params.set("entity_id", String(entityId));
  const res = await fetch(`/api/budgets/summary?${params}`);
  if (!res.ok) throw new Error("Failed to fetch budget summary");
  return res.json();
};

const fetchCategories = async () => {
  const res = await fetch("/api/categories");
  if (!res.ok) throw new Error("Failed to fetch categories");
  return res.json();
};

const createBudget = async (data: any) => {
  const res = await fetch("/api/budgets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to create budget");
  }
  return res.json();
};

const deleteBudget = async (id: number) => {
  const res = await fetch(`/api/budgets/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete budget");
  return res.json();
};

function BudgetsPage() {
  const { enqueueSnackbar } = useSnackbar();
  const queryClient = useQueryClient();
  const { selectedEntityId } = useEntityContext();

  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [newCategoryId, setNewCategoryId] = useState<number | "">("");
  const [newAmount, setNewAmount] = useState("");

  const { data: summary, isLoading } = useQuery({
    queryKey: ["budget-summary", year, month, selectedEntityId],
    queryFn: () => fetchBudgetSummary(year, month, selectedEntityId),
  });

  const { data: categories = [] } = useQuery({
    queryKey: ["categories"],
    queryFn: fetchCategories,
  });

  const expenseCategories = useMemo(
    () => categories.filter((c: any) => c.category_type === "Expense"),
    [categories]
  );

  const createMutation = useMutation({
    mutationFn: createBudget,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["budget-summary"] });
      queryClient.invalidateQueries({ queryKey: ["budgets"] });
      enqueueSnackbar("Budget created", { variant: "success" });
      setAddDialogOpen(false);
      setNewCategoryId("");
      setNewAmount("");
    },
    onError: (err: any) => {
      enqueueSnackbar(err.message || "Failed to create budget", { variant: "error" });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteBudget,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["budget-summary"] });
      queryClient.invalidateQueries({ queryKey: ["budgets"] });
      enqueueSnackbar("Budget deleted", { variant: "success" });
    },
    onError: () => {
      enqueueSnackbar("Failed to delete budget", { variant: "error" });
    },
  });

  const handlePrevMonth = () => {
    if (month === 1) { setMonth(12); setYear(year - 1); }
    else setMonth(month - 1);
  };

  const handleNextMonth = () => {
    if (month === 12) { setMonth(1); setYear(year + 1); }
    else setMonth(month + 1);
  };

  const handleCreate = () => {
    if (!newCategoryId || !newAmount) return;
    const startDate = `${year}-${String(month).padStart(2, "0")}-01`;
    createMutation.mutate({
      category_id: newCategoryId,
      budget_amount: parseFloat(newAmount),
      period_type: "Monthly",
      start_date: startDate,
      entity_id: selectedEntityId || undefined,
    });
  };

  const monthLabel = new Date(year, month - 1).toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
  });

  const statusColor = (status: string) => {
    if (status === "over_budget") return "error";
    if (status === "warning") return "warning";
    return "success";
  };

  const progressColor = (pct: number): "success" | "warning" | "error" => {
    if (pct > 100) return "error";
    if (pct >= 75) return "warning";
    return "success";
  };

  const budgetItems = summary?.budgets || [];
  const hasBudgets = budgetItems.length > 0;

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h5" fontWeight="bold">Budgets</Typography>
        <Button variant="contained" startIcon={<AddIcon />} onClick={() => setAddDialogOpen(true)}>
          Add Budget
        </Button>
      </Box>

      {/* Month Navigation */}
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", mb: 3, gap: 2 }}>
        <IconButton onClick={handlePrevMonth}><ChevronLeftIcon /></IconButton>
        <Typography variant="h6" sx={{ minWidth: 180, textAlign: "center" }}>{monthLabel}</Typography>
        <IconButton onClick={handleNextMonth}><ChevronRightIcon /></IconButton>
      </Box>

      {/* Summary Totals */}
      {hasBudgets && (
        <Box sx={{ display: "flex", gap: 3, mb: 3, justifyContent: "center" }}>
          <Card sx={{ minWidth: 180 }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography variant="caption" color="text.secondary">Total Budgeted</Typography>
              <Typography variant="h6">{formatCurrency(summary?.total_budgeted || 0)}</Typography>
            </CardContent>
          </Card>
          <Card sx={{ minWidth: 180 }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography variant="caption" color="text.secondary">Total Spent</Typography>
              <Typography variant="h6" color="error.main">{formatCurrency(summary?.total_spent || 0)}</Typography>
            </CardContent>
          </Card>
          <Card sx={{ minWidth: 180 }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography variant="caption" color="text.secondary">Remaining</Typography>
              <Typography
                variant="h6"
                color={(summary?.total_budgeted || 0) - (summary?.total_spent || 0) >= 0 ? "success.main" : "error.main"}
              >
                {formatCurrency((summary?.total_budgeted || 0) - (summary?.total_spent || 0))}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Budget Cards */}
      {isLoading ? (
        <LinearProgress />
      ) : !hasBudgets ? (
        <Box sx={{ textAlign: "center", py: 8 }}>
          <SavingsIcon sx={{ fontSize: 64, color: "text.disabled", mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No budgets yet
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Set monthly spending limits for your categories to track your budget.
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => setAddDialogOpen(true)}>
            Create Your First Budget
          </Button>
        </Box>
      ) : (
        <Grid container spacing={2}>
          {budgetItems.map((item: any) => (
            <Grid item xs={12} sm={6} md={4} key={item.budget_id}>
              <Card
                sx={{
                  height: "100%",
                  borderLeft: 4,
                  borderColor: `${statusColor(item.status)}.main`,
                }}
              >
                <CardContent>
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 1 }}>
                    <Typography variant="subtitle1" fontWeight="medium">
                      {item.category_name}
                    </Typography>
                    <IconButton
                      size="small"
                      onClick={() => deleteMutation.mutate(item.budget_id)}
                      disabled={deleteMutation.isPending}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  </Box>

                  <Box sx={{ mb: 1.5 }}>
                    <LinearProgress
                      variant="determinate"
                      value={Math.min(item.percentage_used, 100)}
                      color={progressColor(item.percentage_used)}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>

                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                    <Typography variant="body2" color="text.secondary">
                      {formatCurrency(item.actual_spent)} of {formatCurrency(item.budget_amount)}
                    </Typography>
                    <Chip
                      label={`${item.percentage_used}%`}
                      size="small"
                      color={statusColor(item.status) as any}
                      variant="outlined"
                    />
                  </Box>

                  {item.remaining < 0 && (
                    <Typography variant="caption" color="error" sx={{ mt: 0.5, display: "block" }}>
                      Over budget by {formatCurrency(Math.abs(item.remaining))}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Add Budget Dialog */}
      <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Add Budget</DialogTitle>
        <DialogContent>
          <TextField
            select
            label="Category"
            value={newCategoryId}
            onChange={(e) => setNewCategoryId(Number(e.target.value))}
            fullWidth
            sx={{ mt: 1, mb: 2 }}
          >
            {expenseCategories.map((cat: any) => (
              <MenuItem key={cat.category_id} value={cat.category_id}>
                {cat.category_name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Monthly Amount"
            type="number"
            value={newAmount}
            onChange={(e) => setNewAmount(e.target.value)}
            fullWidth
            inputProps={{ min: 0, step: 0.01 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleCreate}
            disabled={!newCategoryId || !newAmount || createMutation.isPending}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default BudgetsPage;
