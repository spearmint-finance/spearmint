import {
  Box,
  Card,
  CardContent,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  Grid,
  CircularProgress,
} from "@mui/material";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import TrendLineChart from "../../Charts/TrendLineChart";
import CashFlowAreaChart from "../../Charts/CashFlowAreaChart";
import ExpenseStackedBarChart from "../../Charts/ExpenseStackedBarChart";
import {
  CashFlowTrendsResponse,
  getExpenseCategoryTrends,
  CategoryTrendsResponse
} from "../../../api/analysis";
import { DateRange } from "../DateRangePicker";

interface ExpenseTrendChartProps {
  trendsData?: CashFlowTrendsResponse;
  isLoading?: boolean;
  trendPeriod: "daily" | "weekly" | "monthly" | "quarterly" | "yearly";
  onPeriodChange: (period: "daily" | "weekly" | "monthly" | "quarterly" | "yearly") => void;
  dateRange: DateRange;
  viewMode: "analysis" | "with_capital" | "complete";
}

function ExpenseTrendChart({ trendsData, isLoading, trendPeriod, onPeriodChange, dateRange, viewMode }: ExpenseTrendChartProps) {
  const [chartType, setChartType] = useState<"line" | "area" | "bar">("line");

  // Fetch expense category trends for stacked bar chart
  const { data: categoryTrendsData, isLoading: categoryTrendsLoading } = useQuery<CategoryTrendsResponse>({
    queryKey: ["expense-category-trends", dateRange, viewMode, trendPeriod],
    queryFn: () => getExpenseCategoryTrends({
      start_date: dateRange.start_date || undefined,
      end_date: dateRange.end_date || undefined,
      mode: viewMode,
      period: trendPeriod,
      top_n: 8,
    }),
    enabled: chartType === "bar", // Only fetch when bar chart is selected
  });

  const handleChartTypeChange = (
    _event: React.MouseEvent<HTMLElement>,
    newType: "line" | "area" | "bar" | null
  ) => {
    if (newType !== null) {
      setChartType(newType);
    }
  };

  const handlePeriodChange = (
    _event: React.MouseEvent<HTMLElement>,
    newPeriod: "daily" | "weekly" | "monthly" | "quarterly" | "yearly" | null
  ) => {
    if (newPeriod !== null) {
      onPeriodChange(newPeriod);
    }
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Loading expense trends...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  // Transform data for charts - focus on expenses only
  // Convert negative expense values to positive for display
  const chartData =
    trendsData?.trends.map((trend) => ({
      date: trend.period,
      income: 0, // Not showing income in expense deep-dive
      expense: Math.abs(trend.expenses), // Convert to positive for proper chart display
      netCashFlow: Math.abs(trend.expenses), // Use positive expenses for area chart
    })) || [];

  // Calculate statistics
  const avgExpense = chartData.length > 0
    ? chartData.reduce((sum, d) => sum + d.expense, 0) / chartData.length
    : 0;

  const maxExpense = chartData.length > 0
    ? Math.max(...chartData.map(d => d.expense))
    : 0;

  const minExpense = chartData.length > 0
    ? Math.min(...chartData.map(d => d.expense))
    : 0;

  const totalExpense = chartData.reduce((sum, d) => sum + d.expense, 0);

  // Use the category trends data directly
  const stackedBarData = categoryTrendsData?.data || [];
  const stackedCategories = categoryTrendsData?.categories || [];

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h6">Expense Trends</Typography>
          <Box sx={{ display: "flex", gap: 2 }}>
            <ToggleButtonGroup
              value={trendPeriod}
              exclusive
              onChange={handlePeriodChange}
              aria-label="period"
              size="small"
            >
              <ToggleButton value="daily" aria-label="daily">
                Daily
              </ToggleButton>
              <ToggleButton value="weekly" aria-label="weekly">
                Weekly
              </ToggleButton>
              <ToggleButton value="monthly" aria-label="monthly">
                Monthly
              </ToggleButton>
              <ToggleButton value="quarterly" aria-label="quarterly">
                Quarterly
              </ToggleButton>
              <ToggleButton value="yearly" aria-label="yearly">
                Yearly
              </ToggleButton>
            </ToggleButtonGroup>
            <ToggleButtonGroup
              value={chartType}
              exclusive
              onChange={handleChartTypeChange}
              aria-label="chart type"
              size="small"
            >
              <ToggleButton value="line" aria-label="line chart">
                Line
              </ToggleButton>
              <ToggleButton value="area" aria-label="area chart">
                Area
              </ToggleButton>
              <ToggleButton value="bar" aria-label="bar chart">
                Bar
              </ToggleButton>
            </ToggleButtonGroup>
          </Box>
        </Box>

        {chartData.length > 0 ? (
          <Box>
            {chartType === "line" && (
              <TrendLineChart
                data={chartData}
                height={400}
                showIncome={false}
                showExpense={true}
                showNetCashFlow={false}
              />
            )}
            {chartType === "area" && (
              <CashFlowAreaChart
                data={chartData}
                height={400}
              />
            )}
            {chartType === "bar" && (
              <Box sx={{ height: 400 }}>
                {categoryTrendsLoading ? (
                  <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                    <CircularProgress />
                    <Typography variant="body2" sx={{ ml: 2 }}>Loading category trends...</Typography>
                  </Box>
                ) : stackedBarData.length > 0 ? (
                  <ExpenseStackedBarChart
                    data={stackedBarData}
                    categories={stackedCategories}
                    height={400}
                  />
                ) : (
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center", mt: 4 }}>
                    No category trend data available for this period
                  </Typography>
                )}
              </Box>
            )}
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ py: 8, textAlign: "center" }}>
            No expense trend data available for this period
          </Typography>
        )}

        {/* Summary Statistics */}
        {chartData.length > 0 && (
          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Total Expenses
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${Math.abs(totalExpense).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Average
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${Math.abs(avgExpense).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Highest
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${Math.abs(maxExpense).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={3}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Lowest
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${Math.abs(minExpense).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
          </Grid>
        )}
      </CardContent>
    </Card>
  );
}

export default ExpenseTrendChart;
