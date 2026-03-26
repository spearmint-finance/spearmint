import { useState } from "react";
import { Box, Typography, Stack, Paper, Alert, CircularProgress, Button } from "@mui/material";
import { ArrowBack } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import DateRangePicker, { DateRange } from "../DateRangePicker";
import ExpenseViewToggle, { ExpenseView } from "../ExpenseViewToggle";
import ExportButton from "../ExportButton";
import IncomeOverviewCards from "./IncomeOverviewCards";
import IncomeTrendChart from "./IncomeTrendChart";
import IncomeCategoryList from "./IncomeCategoryList";
import {
  useIncomeAnalysis,
  useCashFlowTrends,
} from "../../../hooks/useAnalysis";
import { format, subMonths } from "date-fns";
import { useEntityContext } from "../../../contexts/EntityContext";

function IncomeDeepDivePage() {
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
  const viewMode: "analysis" | "with_capital" | "complete" =
    expenseView === "operating" ? "analysis" :
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
    data: incomeData,
    isLoading: incomeLoading,
    error: incomeError,
  } = useIncomeAnalysis(params);

  const {
    data: trendsData,
    isLoading: trendsLoading,
    error: trendsError,
  } = useCashFlowTrends({
    ...params,
    period: trendPeriod,
  });

  // Handle errors
  const hasError = incomeError || trendsError;
  const isLoading = incomeLoading || trendsLoading;

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
          Income Analysis
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
            <ExportButton dateRange={dateRange} viewMode={viewMode} incomeData={incomeData} />
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
              <>Excludes transfers AND capital income - shows only regular operating income</>
            ) : expenseView === "with-capital" ? (
              <>Excludes transfers but includes capital income (asset sales, investments) - useful for seeing total income without transfer noise</>
            ) : (
              <>Shows all transactions including transfers and all income types - complete financial picture</>
            )}
          </Alert>
        </Box>
      </Paper>

      {/* Error Display */}
      {hasError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Error loading income data
          </Typography>
          <Typography variant="body2">
            {incomeError?.message || trendsError?.message || "An unknown error occurred"}
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
          {/* Income Overview Cards */}
          <IncomeOverviewCards
            incomeData={incomeData}
            isLoading={incomeLoading}
          />

          {/* Income Trends Chart */}
          <IncomeTrendChart
            trendsData={trendsData}
            isLoading={trendsLoading}
            trendPeriod={trendPeriod}
            onPeriodChange={setTrendPeriod}
          />

          {/* Income Category Breakdown with Expandable Transaction Lists */}
          <IncomeCategoryList
            incomeData={incomeData}
            dateRange={dateRange}
            viewMode={viewMode}
            isLoading={incomeLoading}
          />
        </Stack>
      )}

      {/* Empty State */}
      {!hasError && !isLoading && !incomeData && (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <Typography variant="h6" gutterBottom>
            No Income Data Available
          </Typography>
          <Typography variant="body2" color="text.secondary">
            There is no income data available for the selected period. Try adjusting your
            date range or add some transactions first.
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

export default IncomeDeepDivePage;
