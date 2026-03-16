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
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import { useQuery } from "@tanstack/react-query";
import {
  useFinancialSummary,
  useCashFlowTrends,
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

function Dashboard() {
  // Fetch comprehensive dashboard data using the summary endpoint
  const {
    data: summary,
    isLoading,
    error,
    refetch,
  } = useFinancialSummary({
    mode: "analysis",
    top_n: 5,
    recent_count: 5,
  });

  // Fetch cash flow trends for charts
  const { data: trendsData } = useCashFlowTrends({
    mode: "analysis",
    period: "monthly",
  });

  // Fetch net worth data
  const { data: netWorth, isLoading: netWorthLoading } = useQuery({
    queryKey: ["netWorth"],
    queryFn: () => getNetWorth(),
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
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

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
              <Typography variant="h4" component="div">
                {summary.financial_health.income_to_expense_ratio !== null
                  ? summary.financial_health.income_to_expense_ratio.toFixed(2)
                  : "N/A"}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {summary.financial_health.income_to_expense_ratio &&
                summary.financial_health.income_to_expense_ratio > 1
                  ? "Positive cash flow"
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
              <Typography variant="h4" component="div">
                {summary.financial_health.savings_rate !== null
                  ? formatPercentage(summary.financial_health.savings_rate)
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
                      parseFloat(String(netWorth.netWorth || netWorth.net_worth || 0)) >= 0 ? "primary.main" : "error.main"
                    }
                    gutterBottom
                  >
                    {formatCurrency(netWorth.netWorth || netWorth.net_worth || 0)}
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
                    As of {formatDate(netWorth.asOfDate || netWorth.as_of_date || '')}
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
              <Typography variant="h6" color="text.secondary" gutterBottom>
                Account Balances
              </Typography>
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
                <TrendLineChart
                  data={trendsData.trends.map((t) => ({
                    date: t.period,
                    income: Number(t.income),
                    expense: Number(t.expenses),
                    netCashFlow: Number(t.net_cash_flow),
                  }))}
                  title="Income & Expense Trends"
                  height={350}
                  showIncome={true}
                  showExpense={true}
                  showNetCashFlow={false}
                />
              </Paper>
            </Grid>
          </>
        )}

        {/* Category Charts */}
        {(summary.top_income_categories.length > 0 ||
          summary.top_expense_categories.length > 0) && (
          <>
            {/* Top Income Categories */}
            {summary.top_income_categories.length > 0 && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <CategoryPieChart
                    data={summary.top_income_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      percentage: cat.percentage,
                    }))}
                    title="Top Income Categories"
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
                  <CategoryPieChart
                    data={summary.top_expense_categories.map((cat) => ({
                      name: cat.category,
                      value: Number(cat.amount),
                      percentage: cat.percentage,
                    }))}
                    title="Top Expense Categories"
                    height={350}
                    colorScheme="error"
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
            <Typography variant="h6" gutterBottom>
              Recent Transactions
            </Typography>
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
