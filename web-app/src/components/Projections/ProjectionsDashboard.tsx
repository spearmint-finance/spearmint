/**
 * Main projections dashboard component
 * Orchestrates all projection components and manages state
 */

import { useState } from "react";
import {
  Box,
  Typography,
  Grid,
  Paper,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Card,
  CardContent,
} from "@mui/material";
import { useAllProjections } from "../../hooks/useProjections";
import { ProjectionMethod } from "../../types/projection";
import ProjectionControls from "./ProjectionControls";
import ForecastChart from "./ForecastChart";
import ScenarioComparison from "./ScenarioComparison";
import { useTheme } from "@mui/material";

function ProjectionsDashboard() {
  const theme = useTheme();
  const [projectionDays, setProjectionDays] = useState(90);
  const [method, setMethod] = useState<ProjectionMethod>(
    ProjectionMethod.LINEAR_REGRESSION
  );
  const [confidenceLevel, setConfidenceLevel] = useState(0.95);
  const [activeTab, setActiveTab] = useState(0);

  // Fetch all projections
  const { data, isLoading, error } = useAllProjections({
    projection_days: projectionDays,
    method,
    confidence_level: confidenceLevel,
    include_scenarios: true,
  });

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        Error loading projections: {error.message}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Financial Projections
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Forecast future income, expenses, and cash flow based on historical data
      </Typography>

      {/* Projection Controls */}
      <ProjectionControls
        projectionDays={projectionDays}
        method={method}
        confidenceLevel={confidenceLevel}
        onProjectionDaysChange={setProjectionDays}
        onMethodChange={setMethod}
        onConfidenceLevelChange={setConfidenceLevel}
      />

      {isLoading ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
          <CircularProgress />
        </Box>
      ) : data ? (
        <>
          {/* Summary Cards */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Projected Income
                  </Typography>
                  <Typography variant="h5" color="success.main">
                    {formatCurrency(data.income.projected_total)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {data.income.projection_period?.days ?? projectionDays} days
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Projected Expenses
                  </Typography>
                  <Typography variant="h5" color="error.main">
                    {formatCurrency(data.expenses.projected_total)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {data.expenses.projection_period?.days ?? projectionDays}{" "}
                    days
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="caption" color="text.secondary">
                    Net Cash Flow
                  </Typography>
                  <Typography
                    variant="h5"
                    color={
                      data.cashflow.projected_cashflow >= 0
                        ? "success.main"
                        : "error.main"
                    }
                  >
                    {formatCurrency(data.cashflow.projected_cashflow)}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {data.cashflow.projection_period?.days ?? projectionDays}{" "}
                    days
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Tabs for different views */}
          <Paper sx={{ mb: 3 }}>
            <Tabs
              value={activeTab}
              onChange={(_, newValue) => setActiveTab(newValue)}
              variant="fullWidth"
            >
              <Tab label="Cash Flow Forecast" />
              <Tab label="Income & Expenses" />
              <Tab label="Scenario Analysis" />
            </Tabs>
          </Paper>

          {/* Tab Content */}
          {activeTab === 0 && (
            <ForecastChart
              data={(data.cashflow.daily_projections ?? []).map((d) => ({
                date: d.date,
                projected: d.projected_cashflow,
                lowerBound: d.cashflow_lower,
                upperBound: d.cashflow_upper,
              }))}
              title="Cash Flow Projection"
              color={theme.palette.primary.main}
            />
          )}

          {activeTab === 1 && (
            <Grid container spacing={3}>
              <Grid item xs={12} lg={6}>
                <ForecastChart
                  data={(data.income.daily_projections ?? []).map((d) => ({
                    date: d.date,
                    projected: d.projected_value,
                    lowerBound: d.lower_bound,
                    upperBound: d.upper_bound,
                  }))}
                  title="Income Projection"
                  color={theme.palette.success.main}
                />
              </Grid>
              <Grid item xs={12} lg={6}>
                <ForecastChart
                  data={(data.expenses.daily_projections ?? []).map((d) => ({
                    date: d.date,
                    projected: d.projected_value,
                    lowerBound: d.lower_bound,
                    upperBound: d.upper_bound,
                  }))}
                  title="Expense Projection"
                  color={theme.palette.error.main}
                />
              </Grid>
            </Grid>
          )}

          {activeTab === 2 && data.cashflow.scenarios && (
            <ScenarioComparison
              scenarios={data.cashflow.scenarios}
              projectionDays={projectionDays}
            />
          )}

          {/* Model Information */}
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Model Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="caption" color="text.secondary">
                  Method
                </Typography>
                <Typography variant="body1">{data.cashflow.method}</Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="caption" color="text.secondary">
                  Confidence Level
                </Typography>
                <Typography variant="body1">
                  {(data.cashflow.confidence_level * 100).toFixed(0)}%
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="caption" color="text.secondary">
                  Historical Period
                </Typography>
                <Typography variant="body1">
                  {data.cashflow.historical_period?.days ?? 365} days
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Typography variant="caption" color="text.secondary">
                  Projection Period
                </Typography>
                <Typography variant="body1">
                  {data.cashflow.projection_period?.days ?? projectionDays} days
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </>
      ) : null}
    </Box>
  );
}

export default ProjectionsDashboard;
