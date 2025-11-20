/**
 * Scenario comparison component
 * Displays best case, expected, and worst case scenarios side-by-side
 */

import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  useTheme,
  Divider,
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import TrendingFlatIcon from "@mui/icons-material/TrendingFlat";
import { Scenarios } from "../../types/projection";

interface ScenarioComparisonProps {
  scenarios: Scenarios;
  projectionDays: number;
}

function ScenarioComparison({
  scenarios,
  projectionDays,
}: ScenarioComparisonProps) {
  const theme = useTheme();

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const scenarioCards = [
    {
      title: "Best Case",
      data: scenarios.best_case,
      color: theme.palette.success.main,
      icon: <TrendingUpIcon />,
      bgColor: theme.palette.success.light + "20",
    },
    {
      title: "Expected",
      data: scenarios.expected,
      color: theme.palette.primary.main,
      icon: <TrendingFlatIcon />,
      bgColor: theme.palette.primary.light + "20",
    },
    {
      title: "Worst Case",
      data: scenarios.worst_case,
      color: theme.palette.error.main,
      icon: <TrendingDownIcon />,
      bgColor: theme.palette.error.light + "20",
    },
  ];

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Scenario Analysis ({projectionDays} days)
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Compare different financial outcomes based on varying assumptions
      </Typography>

      <Grid container spacing={3}>
        {scenarioCards.map((scenario) => (
          <Grid item xs={12} md={4} key={scenario.title}>
            <Card
              sx={{
                height: "100%",
                borderLeft: 4,
                borderColor: scenario.color,
                backgroundColor: scenario.bgColor,
              }}
            >
              <CardContent>
                <Box
                  sx={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    mb: 2,
                  }}
                >
                  <Typography variant="h6" component="div">
                    {scenario.title}
                  </Typography>
                  <Box sx={{ color: scenario.color }}>{scenario.icon}</Box>
                </Box>

                <Typography
                  variant="caption"
                  color="text.secondary"
                  display="block"
                  sx={{ mb: 2, minHeight: 40 }}
                >
                  {scenario.data.description}
                </Typography>

                <Divider sx={{ my: 2 }} />

                {/* Income */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Projected Income
                  </Typography>
                  <Typography variant="h6" color="success.main">
                    {formatCurrency(scenario.data.income)}
                  </Typography>
                </Box>

                {/* Expenses */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Projected Expenses
                  </Typography>
                  <Typography variant="h6" color="error.main">
                    {formatCurrency(scenario.data.expenses)}
                  </Typography>
                </Box>

                {/* Net Cash Flow */}
                <Box
                  sx={{
                    mt: 2,
                    pt: 2,
                    borderTop: 1,
                    borderColor: "divider",
                  }}
                >
                  <Typography variant="caption" color="text.secondary">
                    Net Cash Flow
                  </Typography>
                  <Typography
                    variant="h5"
                    fontWeight="bold"
                    color={
                      scenario.data.cashflow >= 0
                        ? "success.main"
                        : "error.main"
                    }
                  >
                    {formatCurrency(scenario.data.cashflow)}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Range Summary */}
      <Box sx={{ mt: 3, p: 2, bgcolor: "background.default", borderRadius: 1 }}>
        <Typography variant="subtitle2" gutterBottom>
          Scenario Ranges
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Cash Flow Range
              </Typography>
              <Typography variant="body1" fontWeight="medium">
                {formatCurrency(scenarios.range.cashflow_range)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Income Range
              </Typography>
              <Typography variant="body1" fontWeight="medium">
                {formatCurrency(scenarios.range.income_range)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box>
              <Typography variant="caption" color="text.secondary">
                Expense Range
              </Typography>
              <Typography variant="body1" fontWeight="medium">
                {formatCurrency(scenarios.range.expense_range)}
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
}

export default ScenarioComparison;

