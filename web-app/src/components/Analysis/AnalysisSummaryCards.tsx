import { Box, Card, CardContent, Grid, Typography } from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import AccountBalanceWalletIcon from "@mui/icons-material/AccountBalanceWallet";
import FavoriteIcon from "@mui/icons-material/Favorite";
import { CashFlowResponse, FinancialHealthResponse } from "../../api/analysis";

interface AnalysisSummaryCardsProps {
  cashFlow?: CashFlowResponse;
  health?: FinancialHealthResponse;
  operatingOnlyCashFlow?: CashFlowResponse;
  expenseView?: "operating" | "with-capital" | "all";
  isLoading?: boolean;
}

interface SummaryCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: React.ReactNode;
  color: string;
}

function SummaryCard({ title, value, subtitle, icon, color }: SummaryCardProps) {
  return (
    <Card sx={{ height: "100%" }}>
      <CardContent>
        <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
              color: `${color}.main`,
              borderRadius: 2,
              p: 1,
              mr: 2,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icon}
          </Box>
          <Typography variant="body2" color="text.secondary">
            {title}
          </Typography>
        </Box>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

function AnalysisSummaryCards({
  cashFlow,
  health,
  operatingOnlyCashFlow,
  expenseView,
  isLoading,
}: AnalysisSummaryCardsProps) {
  if (isLoading) {
    return (
      <Grid container spacing={3}>
        {[1, 2, 3, 4].map((i) => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <Card sx={{ height: 150 }}>
              <CardContent>
                <Typography variant="body2" color="text.secondary">
                  Loading...
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }

  const formatCurrency = (amount: number, useAbsoluteValue: boolean = true) => {
    const value = useAbsoluteValue ? Math.abs(amount) : amount;
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatPercentage = (value: number | null) => {
    if (value === null) return "N/A";
    return `${(value * 100).toFixed(1)}%`;
  };

  const netCashFlow = cashFlow?.net_cash_flow ?? 0;
  const savingsRate = health?.savings_rate ?? null;
  const incomeExpenseRatio = health?.income_to_expense_ratio ?? null;

  // Calculate expense breakdown when in with-capital mode
  const getExpenseBreakdown = () => {
    if (expenseView === "with-capital" && cashFlow && operatingOnlyCashFlow) {
      const totalExpenses = Math.abs(cashFlow.total_expenses);
      const operatingExpenses = Math.abs(operatingOnlyCashFlow.total_expenses);
      const capitalExpenses = totalExpenses - operatingExpenses;

      return {
        operating: operatingExpenses,
        capital: capitalExpenses,
      };
    }
    return null;
  };

  const expenseBreakdown = getExpenseBreakdown();

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <SummaryCard
          title="Total Income"
          value={formatCurrency(cashFlow?.total_income || 0)}
          subtitle={`${cashFlow?.income_count || 0} transactions`}
          icon={<TrendingUpIcon />}
          color="success"
        />
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <SummaryCard
          title="Total Expenses"
          value={formatCurrency(cashFlow?.total_expenses || 0)}
          subtitle={
            expenseBreakdown
              ? `Operating: ${formatCurrency(expenseBreakdown.operating)} | Capital: ${formatCurrency(expenseBreakdown.capital)}`
              : `${cashFlow?.expense_count || 0} transactions`
          }
          icon={<TrendingDownIcon />}
          color="error"
        />
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <SummaryCard
          title="Net Cash Flow"
          value={formatCurrency(netCashFlow, false)}
          subtitle={`${cashFlow?.income_count || 0} income, ${cashFlow?.expense_count || 0} expenses`}
          icon={<AccountBalanceWalletIcon />}
          color={netCashFlow >= 0 ? "success" : "error"}
        />
      </Grid>
      <Grid item xs={12} sm={6} md={3}>
        <SummaryCard
          title="Financial Health"
          value={formatPercentage(savingsRate)}
          subtitle={
            incomeExpenseRatio !== null
              ? `Ratio: ${incomeExpenseRatio.toFixed(2)}`
              : "Insufficient data"
          }
          icon={<FavoriteIcon />}
          color="primary"
        />
      </Grid>
    </Grid>
  );
}

export default AnalysisSummaryCards;
