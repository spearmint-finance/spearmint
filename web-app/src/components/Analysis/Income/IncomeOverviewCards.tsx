import { Grid, Card, CardContent, Typography, Box, Skeleton } from "@mui/material";
import {
  TrendingUp,
  AccountBalance,
  Receipt,
  Analytics,
} from "@mui/icons-material";
import { IncomeAnalysisResponse } from "../../../api/analysis";

interface IncomeOverviewCardsProps {
  incomeData?: IncomeAnalysisResponse;
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

function IncomeOverviewCards({ incomeData, isLoading }: IncomeOverviewCardsProps) {
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

  if (!incomeData) {
    return null;
  }

  const totalIncome = incomeData.total_income;
  const transactionCount = incomeData.transaction_count;
  const averageTransaction = incomeData.average_transaction;
  const categoryCount = Object.keys(incomeData.breakdown_by_category).length;

  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
        Income Overview
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Income"
            value={formatCurrency(totalIncome)}
            subtitle={incomeData.mode === "analysis" ? "Analysis mode" : "Complete mode"}
            icon={<AccountBalance />}
            color="success"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Transactions"
            value={transactionCount.toString()}
            subtitle={`${categoryCount} income sources`}
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
            title="Income Sources"
            value={categoryCount.toString()}
            subtitle="Active categories"
            icon={<TrendingUp />}
            color="secondary"
          />
        </Grid>
      </Grid>
    </Box>
  );
}

export default IncomeOverviewCards;
