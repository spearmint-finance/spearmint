import { useState } from "react";
import { Box, Typography, Stack, Paper, Alert, CircularProgress, Button } from "@mui/material";
import { ArrowForward } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import DateRangePicker, { DateRange } from "./DateRangePicker";
import ExpenseViewToggle, { ExpenseView } from "./ExpenseViewToggle";
import ExportButton from "./ExportButton";
import AnalysisSummaryCards from "./AnalysisSummaryCards";
import CategoryBreakdown from "./CategoryBreakdown";
import TrendsSection from "./TrendsSection";
import {
  useCashFlowAnalysis,
  useFinancialHealth,
  useIncomeAnalysis,
  useExpenseAnalysis,
  useCashFlowTrends,
} from "../../hooks/useAnalysis";
import { format, subMonths } from "date-fns";

function AnalysisPage() {
  const navigate = useNavigate();

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
  };

  // Fetch data using hooks
  const {
    data: cashFlowData,
    isLoading: cashFlowLoading,
    error: cashFlowError,
  } = useCashFlowAnalysis(params);

  // Also fetch operating-only data when in with_capital mode to show breakdown
  const {
    data: operatingOnlyCashFlow,
    isLoading: operatingOnlyLoading,
    error: operatingOnlyError,
  } = useCashFlowAnalysis(
    expenseView === "with-capital"
      ? { ...params, mode: "analysis" }
      : params
  );

  const {
    data: healthData,
    isLoading: healthLoading,
    error: healthError,
  } = useFinancialHealth(params);

  const {
    data: incomeData,
    isLoading: incomeLoading,
    error: incomeError,
  } = useIncomeAnalysis(params);

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
  const hasError =
    cashFlowError || healthError || incomeError || expenseError || trendsError || operatingOnlyError;
  const isLoading =
    cashFlowLoading || healthLoading || incomeLoading || expenseLoading || trendsLoading || operatingOnlyLoading;

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        Financial Analysis
      </Typography>

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
            <ExportButton
              dateRange={dateRange}
              viewMode={viewMode}
              incomeData={incomeData}
              expenseData={expenseData}
              cashFlowData={cashFlowData}
            />
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
              <>Excludes transfers AND capital expenses - shows only regular operating income and expenses</>
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
            Error loading analysis data
          </Typography>
          <Typography variant="body2">
            {cashFlowError?.message ||
              healthError?.message ||
              incomeError?.message ||
              expenseError?.message ||
              trendsError?.message ||
              "An unknown error occurred"}
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
          {/* Summary Cards */}
          <AnalysisSummaryCards
            cashFlow={cashFlowData}
            health={healthData}
            operatingOnlyCashFlow={operatingOnlyCashFlow}
            expenseView={expenseView}
            isLoading={cashFlowLoading || healthLoading}
          />

          {/* Trends Section */}
          <TrendsSection
            trendsData={trendsData}
            isLoading={trendsLoading}
            onPeriodChange={setTrendPeriod}
          />

          {/* Category Breakdown */}
          <CategoryBreakdown
            incomeData={incomeData}
            expenseData={expenseData}
            isLoading={incomeLoading || expenseLoading}
          />

          {/* Deep-Dive Analysis Links */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Deep-Dive Analysis
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Explore detailed breakdowns and insights for specific financial areas
            </Typography>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={2}>
              <Button
                variant="outlined"
                endIcon={<ArrowForward />}
                onClick={() => navigate("/analysis/income")}
                sx={{ flex: 1 }}
              >
                Income Analysis
              </Button>
              <Button
                variant="outlined"
                endIcon={<ArrowForward />}
                onClick={() => navigate("/analysis/expenses")}
                sx={{ flex: 1 }}
              >
                Expense Analysis
              </Button>
            </Stack>
          </Paper>
        </Stack>
      )}

      {/* Empty State */}
      {!hasError && !isLoading && !cashFlowData && !trendsData && (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <Typography variant="h6" gutterBottom>
            No Data Available
          </Typography>
          <Typography variant="body2" color="text.secondary">
            There is no transaction data available for the selected period. Try adjusting your
            date range or add some transactions first.
          </Typography>
        </Paper>
      )}
    </Box>
  );
}

export default AnalysisPage;
