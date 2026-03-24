import { useState } from "react";
import { Box, Typography, Stack, Paper, Alert, CircularProgress, Button } from "@mui/material";
import { ArrowBack } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import DateRangePicker, { DateRange } from "../DateRangePicker";
import ExpenseViewToggle, { ExpenseView } from "../ExpenseViewToggle";
import ExportButton from "../ExportButton";
import ExpenseOverviewCards from "./ExpenseOverviewCards";
import ExpenseTrendChart from "./ExpenseTrendChart";
import ExpenseCategoryList from "./ExpenseCategoryList";
import {
  useExpenseAnalysis,
  useCashFlowTrends,
} from "../../../hooks/useAnalysis";
import { format, subMonths } from "date-fns";
import { useEntityContext } from "../../../contexts/EntityContext";

function ExpenseDeepDivePage() {
  const navigate = useNavigate();
  const { selectedEntityId } = useEntityContext();

  // State for filters
  const [dateRange, setDateRange] = useState<DateRange>({
    start_date: format(subMonths(new Date(), 3), "yyyy-MM-dd"),
    end_date: format(new Date(), "yyyy-MM-dd"),
  });
  const [expenseView, setExpenseView] = useState<ExpenseView>("operating");
  const [trendPeriod, setTrendPeriod] = useState<
    "daily" | "weekly" | "monthly" | "quarterly" | "yearly"
  >("monthly");

  // Convert expense view to API mode
  const viewMode = expenseView === "operating" ? "analysis" :
                   expenseView === "with-capital" ? "with_capital" :
                   "complete";

  // Prepare params for API calls
  const params = {
    start_date: dateRange.start_date || undefined,
    end_date: dateRange.end_date || undefined,
    mode: viewMode,
    entity_id: selectedEntityId ?? undefined,
  };

  // Fetch data using hooks
  const {
    data: expenseData,
    isLoading: expenseLoading,
    error: expenseError,
  } = useExpenseAnalysis(params);

  const {
    data: trendsData,
    isLoading: trendsLoading,
    error: trendsError,
  } = useCashFlowTrends({
    ...params,
    period: trendPeriod,
  });

  // Handle errors
  const hasError = expenseError || trendsError;
  const isLoading = expenseLoading || trendsLoading;

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      {/* Header with Back Button */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 2 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate("/analysis")}
          variant="outlined"
          size="small"
        >
          Back to Overview
        </Button>
        <Typography variant="h4" sx={{ flex: 1 }}>
          Expense Analysis
        </Typography>
      </Box>

      {/* Filter Controls */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          spacing={2}
          alignItems={{ xs: "stretch", sm: "center" }}
          justifyContent="space-between"
        >
          <DateRangePicker value={dateRange} onChange={setDateRange} />
          <Stack direction="row" spacing={2}>
            <ExpenseViewToggle value={expenseView} onChange={setExpenseView} />
            <ExportButton dateRange={dateRange} viewMode={viewMode} expenseData={expenseData} />
          </Stack>
        </Stack>
        <Box sx={{ mt: 2 }}>
          <Alert severity="info">
            <strong>
              {expenseView === "operating" ? "Operating Only" :
               expenseView === "with-capital" ? "Operating + Capital" :
               "All Transactions"}:
            </strong>{" "}
            {expenseView === "operating" ? (
              <>Excludes transfers AND capital expenses - shows only regular operating expenses</>
            ) : expenseView === "with-capital" ? (
              <>Excludes transfers but includes capital expenses (vehicles, equipment, property) - useful for seeing total spending without transfer noise</>
            ) : (
              <>Shows all transactions including transfers and capital expenses - complete financial picture</>
            )}
          </Alert>
        </Box>
      </Paper>

      {/* Error Display */}
      {hasError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Error loading expense data
          </Typography>
          <Typography variant="body2">
            {expenseError?.message || trendsError?.message || "An unknown error occurred"}
          </Typography>
        </Alert>
      )}

      {/* Loading State */}
      {isLoading && !hasError && (
        <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Content */}
      {!hasError && !isLoading && (
        <Stack spacing={3}>
          {/* Expense Overview Cards */}
          <ExpenseOverviewCards
            expenseData={expenseData}
            isLoading={expenseLoading}
          />

          {/* Expense Trends Chart */}
          <ExpenseTrendChart
            trendsData={trendsData}
            isLoading={trendsLoading}
            trendPeriod={trendPeriod}
            onPeriodChange={setTrendPeriod}
            dateRange={dateRange}
            viewMode={viewMode}
          />

          {/* Expense Category Breakdown with Expandable Transaction Lists */}
          <ExpenseCategoryList
            expenseData={expenseData}
            dateRange={dateRange}
            viewMode={viewMode}
            isLoading={expenseLoading}
          />
        </Stack>
      )}

      {/* Empty State */}
      {!hasError && !isLoading && !expenseData && (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <Typography variant="h6" gutterBottom>
            No Expense Data Available
          </Typography>
          <Typography variant="body2" color="text.secondary">
            There is no expense data available for the selected period. Try adjusting your
            date range or add some transactions first.
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

export default ExpenseDeepDivePage;
