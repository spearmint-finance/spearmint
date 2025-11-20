import { Grid, Card, CardContent, Typography, Box, Skeleton } from "@mui/material";
import {
  TrendingDown,
  ShoppingCart,
  Receipt,
  Analytics,
} from "@mui/icons-material";
import { ExpenseAnalysisResponse } from "../../../api/analysis";

interface ExpenseOverviewCardsProps {
  expenseData?: ExpenseAnalysisResponse;
  isLoading?: boolean;
}

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: React.ReactNode;
  color: string;
}

function StatCard({ title, value, subtitle, icon, color }: StatCardProps) {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <Box sx={{ flex: 1 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ mb: 0.5 }}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
              color: `${color}.main`,
              p: 1,
              borderRadius: 2,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}

function ExpenseOverviewCards({ expenseData, isLoading }: ExpenseOverviewCardsProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  if (isLoading) {
    return (
      <Grid container spacing={3}>
        {[1, 2, 3, 4].map((i) => (
          <Grid item xs={12} sm={6} md={3} key={i}>
            <Card>
              <CardContent>
                <Skeleton variant="text" width="60%" />
                <Skeleton variant="text" width="80%" height={40} />
                <Skeleton variant="text" width="40%" />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }

  if (!expenseData) {
    return null;
  }

  const totalExpenses = expenseData.total_expenses;
  const transactionCount = expenseData.transaction_count;
  const averageTransaction = expenseData.average_transaction;
  const categoryCount = Object.keys(expenseData.breakdown_by_category).length;

  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
        Expense Overview
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Expenses"
            value={formatCurrency(totalExpenses)}
            subtitle={expenseData.mode === "analysis" ? "Analysis mode" : "Complete mode"}
            icon={<ShoppingCart />}
            color="error"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Transactions"
            value={transactionCount.toString()}
            subtitle={`${categoryCount} expense categories`}
            icon={<Receipt />}
            color="info"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Average Amount"
            value={formatCurrency(averageTransaction)}
            subtitle="Per transaction"
            icon={<Analytics />}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Expense Categories"
            value={categoryCount.toString()}
            subtitle="Active categories"
            icon={<TrendingDown />}
            color="warning"
          />
        </Grid>
      </Grid>
    </Box>
  );
}

export default ExpenseOverviewCards;
