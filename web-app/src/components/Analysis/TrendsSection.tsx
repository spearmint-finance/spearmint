import {
  Box,
  Card,
  CardContent,
  Typography,
  ToggleButton,
  ToggleButtonGroup,
  Grid,
} from "@mui/material";
import { useState } from "react";
import TrendLineChart from "../Charts/TrendLineChart";
import CashFlowAreaChart from "../Charts/CashFlowAreaChart";
import { CashFlowTrendsResponse } from "../../api/analysis";

interface TrendsSectionProps {
  trendsData?: CashFlowTrendsResponse;
  isLoading?: boolean;
  onPeriodChange?: (period: "daily" | "weekly" | "monthly" | "quarterly" | "yearly") => void;
}

function TrendsSection({ trendsData, isLoading, onPeriodChange }: TrendsSectionProps) {
  const [chartType, setChartType] = useState<"line" | "area" | "bar">("line");
  const [period, setPeriod] = useState<"daily" | "weekly" | "monthly" | "quarterly" | "yearly">(
    "monthly"
  );

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
      setPeriod(newPeriod);
      onPeriodChange?.(newPeriod);
    }
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Loading trends...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  // Transform data for charts
  const chartData =
    trendsData?.trends.map((trend) => ({
      date: trend.period,
      income: trend.income,
      expense: Math.abs(trend.expenses),
      netCashFlow: trend.net_cash_flow,
    })) || [];

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h6">Cash Flow Trends</Typography>
          <Box sx={{ display: "flex", gap: 2 }}>
            <ToggleButtonGroup
              value={period}
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
                showIncome={true}
                showExpense={true}
                showNetCashFlow={true}
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
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center", mt: 4 }}>
                  Bar chart view - Coming soon
                </Typography>
              </Box>
            )}
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ py: 8, textAlign: "center" }}>
            No trend data available for this period
          </Typography>
        )}

        {/* Summary Statistics */}
        {chartData.length > 0 && (
          <Grid container spacing={2} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={4}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Average Income
                </Typography>
                <Typography variant="h6" color="success.main">
                  ${(
                    chartData.reduce((sum, d) => sum + d.income, 0) / chartData.length
                  ).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Average Expenses
                </Typography>
                <Typography variant="h6" color="error.main">
                  ${(
                    chartData.reduce((sum, d) => sum + d.expense, 0) / chartData.length
                  ).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box sx={{ textAlign: "center" }}>
                <Typography variant="body2" color="text.secondary">
                  Average Net Flow
                </Typography>
                <Typography
                  variant="h6"
                  color={
                    chartData.reduce((sum, d) => sum + d.netCashFlow, 0) / chartData.length >= 0
                      ? "success.main"
                      : "error.main"
                  }
                >
                  ${(
                    chartData.reduce((sum, d) => sum + d.netCashFlow, 0) / chartData.length
                  ).toLocaleString("en-US", {
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

export default TrendsSection;
