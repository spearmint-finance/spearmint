import { useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import { useEntityContext } from "../../contexts/EntityContext";
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Chip,
  Alert,
  Skeleton,
  Button,
  LinearProgress,
  ToggleButton,
  ToggleButtonGroup,
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import { useQuery } from "@tanstack/react-query";
import {
  useFinancialSummary,
  useCashFlowTrends,
  useExpenseCategoryTrends,
} from "../../hooks/useAnalysis";
import { getNetWorth, getAccountSummary } from "../../api/accounts";
import {
  formatCurrency,
  formatPercentage,
  formatDate,
} from "../../utils/formatters";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorDisplay from "../common/ErrorDisplay";
import TrendLineChart from "../Charts/TrendLineChart";
import CategoryPieChart from "../Charts/CategoryPieChart";
import CategoryBarChart from "../Charts/CategoryBarChart";
import ExpenseStackedBarChart from "../Charts/ExpenseStackedBarChart";
import DateRangePicker, {
  DateRange,
} from "../Analysis/DateRangePicker";
import ExpenseViewToggle, {
  ExpenseView,
} from "../Analysis/ExpenseViewToggle";
import ExportButton from "../Analysis/ExportButton";

function Dashboard() {
  const { selectedEntityId, selectedEntity } = useEntityContext();
  const [dateRange, setDateRange] = useState<DateRange>({
    start_date: "",
    end_date: "",
  });
  const [expenseView, setExpenseView] = useState<ExpenseView>("operating");
  const [trendPeriod, setTrendPeriod] = useState<"daily" | "weekly" | "monthly" | "quarterly" | "yearly">("monthly");

  // Convert expense view to API mode
  const viewMode = expenseView === "operating" ? "analysis" :
                   expenseView === "with-capital" ? "with_capital" :
                   "complete";

  // Fetch comprehensive dashboard data using the summary endpoint
  const {
    data: summary,
    isLoading,
    isFetching,
    error,
    refetch,
  } = useFinancialSummary({
    mode: viewMode,
    top_n: 5,
    recent_count: 5,
    start_date: dateRange.start_date || undefined,
    end_date: dateRange.end_date || undefined,
    entity_id: selectedEntityId ?? undefined,
  });

  // Fetch cash flow trends for charts
  const { data: trendsData } = useCashFlowTrends({
    mode: viewMode,
    period: trendPeriod,
    start_date: dateRange.start_date || undefined,
    end_date: dateRange.end_date || undefined,
    entity_id: selectedEntityId ?? undefined,
  });

  // Fetch expense category trends for stacked bar chart
  const { data: categoryTrends } = useExpenseCategoryTrends({
    period: trendPeriod,
    mode: viewMode,
    top_n: 5,
    start_date: dateRange.start_date || undefined,
    end_date: dateRange.end_date || undefined,
    entity_id: selectedEntityId ?? undefined,
  });

  // Fetch net worth data (entity-scoped)
  const { data: netWorth, isLoading: netWorthLoading } = useQuery({
    queryKey: ["netWorth", selectedEntityId],
    queryFn: () => getNetWorth(
      selectedEntityId ? { entity_id: selectedEntityId } : undefined
    ),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Fetch account summary for quick balances view
  const { data: accountSummary, isLoading: accountsLoading } = useQuery({
    queryKey: ["accountSummary"],
    queryFn: () => getAccountSummary(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Loading state
  if (isLoading) {
    return <LoadingSpinner message="Loading dashboard data..." />;
  }

  // Error state
  if (error) {
    return (
      <ErrorDisplay message="Failed to load dashboard data" onRetry={refetch} />
    );
  }

  // No data state
  if (!summary) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="info">
          No financial data available. Import transactions to get started.
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Box sx={{ display: "flex", alignItems: "baseline", gap: 1 }}>
          <Typography variant="h4">Dashboard</Typography>
          {selectedEntity && (
            <Chip
              label={selectedEntity.entity_name}
              size="small"
              color="primary"
              variant="outlined"
            />
          )}
        </Box>
        <Box sx={{ display: "flex", alignItems: "center", gap: 2, flexWrap: "wrap" }}>
          <ExpenseViewToggle value={expenseView} onChange={setExpenseView} />
          <DateRangePicker value={dateRange} onChange={setDateRange} />
          <ExportButton
            dateRange={dateRange}
            viewMode={viewMode}
            summaryData={summary}
          />
        </Box>
      </Box>
      {isFetching && !isLoading && (
        <LinearProgress sx={{ mb: 1, borderRadius: 1 }} />
      )}

      {/* Overview Cards */}
      <Grid container spacing={3}>
        {/* Total Income Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Total Income
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="success.main">
                {formatCurrency(summary.total_income)}
              </Typography>
              {summary.period_start && (
                <Typography variant="caption" color="text.secondary">
                  {formatDate(summary.period_start)} -{" "}
                  {formatDate(summary.period_end || new Date().toISOString())}
                </Typography>
              )}
              <Typography
                variant="caption"
                color="text.secondary"
                display="block"
              >
                {summary.income_count} transactions
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Total Expenses Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <TrendingDownIcon color="error" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Total Expenses
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="error.main">
                {formatCurrency(summary.total_expenses)}
              </Typography>
              {summary.period_start && (
                <Typography variant="caption" color="text.secondary">
                  {formatDate(summary.period_start)} -{" "}
                  {formatDate(summary.period_end || new Date().toISOString())}
                </Typography>
              )}
              <Typography
                variant="caption"
                color="text.secondary"
                display="block"
              >
                {summary.expense_count} transactions
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Net Cash Flow Card */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                <AccountBalanceWalletIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Net Cash Flow
                </Typography>
              </Box>
              <Typography
                variant="h4"
                component="div"
                color={
                  summary.net_cash_flow >= 0 ? "success.main" : "error.main"
                }
              >
                {formatCurrency(summary.net_cash_flow)}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {summary.income_count + summary.expense_count} total
                transactions
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Financial Health Indicators */}
        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Income/Expense Ratio
              </Typography>
              <Typography
                variant="h4"
                component="div"
                color={
                  summary.financial_health.income_to_expense_ratio === null
                    ? "text.primary"
                    : summary.financial_health.income_to_expense_ratio > 1
                    ? "success.main"
                    : summary.financial_health.income_to_expense_ratio < 1
                    ? "error.main"
                    : "text.primary"
                }
              >
                {summary.financial_health.income_to_expense_ratio !== null
                  ? summary.financial_health.income_to_expense_ratio.toFixed(2)
                  : "N/A"}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {summary.financial_health.income_to_expense_ratio === null
                  ? "No data available"
                  : summary.financial_health.income_to_expense_ratio > 1
                  ? "Positive cash flow"
                  : summary.financial_health.income_to_expense_ratio === 1
                  ? "Income equals expenses"
                  : "Spending exceeds income"}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Savings Rate
              </Typography>
              <Typography
                variant="h4"
                component="div"
                color={
                  summary.financial_health.savings_rate === null
                    ? "text.primary"
                    : summary.financial_health.savings_rate > 0
                    ? "success.main"
                    : summary.financial_health.savings_rate < 0
                    ? "error.main"
                    : "text.primary"
                }
              >
                {summary.financial_health.savings_rate !== null
                  ? formatPercentage(summary.financial_health.savings_rate * 100)
                  : "N/A"}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Of income saved
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Daily Cash Flow
              </Typography>
              <Typography
                variant="h4"
                component="div"
                color={
                  summary.financial_health.net_daily_cash_flow >= 0
                    ? "success.main"
                    : "error.main"
                }
              >
                {formatCurrency(summary.financial_health.net_daily_cash_flow)}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Average per day
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Net Worth Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
                <AccountBalanceIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6" color="text.secondary">
                  Net Worth
                </Typography>
              </Box>
              {netWorthLoading ? (
                <Box>
                  <Skeleton variant="text" width="60%" height={40} />
                  <Skeleton variant="text" width="80%" />
                </Box>
              ) : netWorth ? (
                <Box>
                  <Typography
                    variant="h4"
                    component="div"
                    color={
                      parseFloat(String(netWorth.net_worth ?? netWorth.netWorth ?? 0)) >= 0 ? "primary.main" : "error.main"
                    }
                    gutterBottom
                  >
                    {formatCurrency(netWorth.net_worth ?? netWorth.netWorth ?? 0)}
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Assets
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {formatCurrency(netWorth.assets)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Liabilities
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        {formatCurrency(netWorth.liabilities)}
                      </Typography>
                    </Grid>
                  </Grid>
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ mt: 1, display: "block" }}
                  >
                    As of {formatDate(netWorth.as_of_date ?? netWorth.asOfDate ?? '')}
                  </Typography>
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No account data available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Account Balances Quick View */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  mb: 1,
                }}
              >
                <Typography variant="h6" color="text.secondary">
                  Account Balances
                </Typography>
                <Button
                  component={RouterLink}
                  to="/accounts"
                  size="small"
                >
                  View All
                </Button>
              </Box>
              {accountsLoading ? (
                <Box>
                  <Skeleton variant="text" width="100%" />
                  <Skeleton variant="text" width="100%" />
                  <Skeleton variant="text" width="100%" />
                </Box>
              ) : accountSummary && accountSummary.length > 0 ? (
                <Box>
                  {accountSummary.slice(0, 5).map((account) => (
                    <Box
                      key={account.account_id}
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        py: 1,
                        borderBottom: "1px solid",
                        borderColor: "divider",
                        "&:last-child": { borderBottom: "none" },
                      }}
                    >
                      <Box>
                        <Typography variant="body2" fontWeight="medium">
                          {account.account_name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {account.account_type}
                          {account.institution
                            ? ` • ${account.institution}`
                            : ""}
                        </Typography>
                      </Box>
                      <Typography
                        variant="body1"
                        fontWeight="medium"
                        color={
                          account.current_balance >= 0
                            ? "text.primary"
                            : "error.main"
                        }
                      >
                        {formatCurrency(account.current_balance)}
                      </Typography>
                    </Box>
                  ))}
                  {accountSummary.length > 5 && (
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ mt: 1, display: "block" }}
                    >
                      +{accountSummary.length - 5} more accounts
                    </Typography>
                  )}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No accounts set up yet
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Charts Section */}
        {trendsData && trendsData.trends.length > 0 && (
          <>
            {/* Cash Flow Trend Chart */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 2,
                    flexWrap: "wrap",
                    gap: 1,
                  }}
                >
                  <Typography variant="h6">Income & Expense Trends</Typography>
                  <ToggleButtonGroup
                    value={trendPeriod}
                    exclusive
                    onChange={(_e, val) => val && setTrendPeriod(val)}
                    size="small"
                    aria-label="trend period"
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
                </Box>
                <TrendLineChart
                  data={trendsData.trends.map((t) => ({
                    date: t.period,
                    income: Number(t.income),
                    expense: Number(t.expenses),
                    netCashFlow: Number(t.net_cash_flow),
                  }))}
                  height={350}
                  showIncome={true}
                  showExpense={true}
                  showNetCashFlow={true}
                />
              </Paper>
            </Grid>
          </>
        )}

        {/* Expense Category Trends - Stacked Bar Chart */}
        {categoryTrends &&
          categoryTrends.categories.length > 0 &&
          categoryTrends.data.length > 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Expense Categories ({trendPeriod.charAt(0).toUpperCase() + trendPeriod.slice(1)})
                </Typography>
                <ExpenseStackedBarChart
                  data={categoryTrends.data}
                  categories={categoryTrends.categories}
                  height={400}
                />
              </Paper>
            </Grid>
          )}

        {/* Category Charts */}
        {(summary.top_income_categories.length > 0 ||
          summary.top_expense_categories.length > 0) && (
          <>
            {/* Top Income Categories */}
            {summary.top_income_categories.length > 0 && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      mb: 1,
                    }}
                  >
                    <Typography variant="h6">
                      Top Income Categories
                    </Typography>
                    <Button
                      component={RouterLink}
                      to="/analysis/income"
                      size="small"
                    >
                      Deep Dive
                    </Button>
                  </Box>
                  <CategoryPieChart
                    data={summary.top_income_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      percentage: cat.percentage,
                    }))}
                    height={350}
                    colorScheme="success"
                  />
                </Paper>
              </Grid>
            )}

            {/* Top Expense Categories */}
            {summary.top_expense_categories.length > 0 && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      mb: 1,
                    }}
                  >
                    <Typography variant="h6">
                      Top Expense Categories
                    </Typography>
                    <Button
                      component={RouterLink}
                      to="/analysis/expenses"
                      size="small"
                    >
                      Deep Dive
                    </Button>
                  </Box>
                  <CategoryPieChart
                    data={summary.top_expense_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      percentage: cat.percentage,
                    }))}
                    height={350}
                    colorScheme="error"
                  />
                </Paper>
              </Grid>
            )}

            {/* Income Breakdown - Bar Chart */}
            {summary.top_income_categories.length > 0 && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <CategoryBarChart
                    data={summary.top_income_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      count: cat.count,
                    }))}
                    title="Income Breakdown"
                    height={350}
                    horizontal={true}
                    color="#4caf50"
                  />
                </Paper>
              </Grid>
            )}

            {/* Expense Breakdown - Bar Chart */}
            {summary.top_expense_categories.length > 0 && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <CategoryBarChart
                    data={summary.top_expense_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      count: cat.count,
                    }))}
                    title="Expense Breakdown"
                    height={350}
                    horizontal={true}
                  />
                </Paper>
              </Grid>
            )}
          </>
        )}

        {/* Recent Transactions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                mb: 1,
              }}
            >
              <Typography variant="h6">Recent Transactions</Typography>
              <Button
                component={RouterLink}
                to="/transactions"
                size="small"
              >
                View All
              </Button>
            </Box>
            {summary.recent_transactions.length > 0 ? (
              <Box>
                {summary.recent_transactions.map((transaction) => (
                  <Box
                    key={transaction.transaction_id}
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      py: 2,
                      borderBottom: "1px solid",
                      borderColor: "divider",
                      "&:last-child": { borderBottom: "none" },
                    }}
                  >
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="body1" fontWeight="medium">
                        {transaction.description}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {formatDate(transaction.transaction_date)} •{" "}
                        {transaction.category || "Uncategorized"}
                      </Typography>
                    </Box>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                      <Chip
                        label={transaction.transaction_type}
                        size="small"
                        color={
                          transaction.transaction_type === "Income"
                            ? "success"
                            : "error"
                        }
                        variant="outlined"
                      />
                      <Typography
                        variant="h6"
                        color={
                          transaction.transaction_type === "Income"
                            ? "success.main"
                            : "error.main"
                        }
                        sx={{ minWidth: 100, textAlign: "right" }}
                      >
                        {transaction.transaction_type === "Income" ? "+" : "-"}
                        {formatCurrency(Math.abs(transaction.amount))}
                      </Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No transactions yet. Import data to get started.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
