import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  LinearProgress,
} from "@mui/material";
import {
  ExpenseAnalysisResponse,
  IncomeAnalysisResponse,
} from "../../api/analysis";
import CategoryPieChart from "../Charts/CategoryPieChart";

interface CategoryBreakdownProps {
  incomeData?: IncomeAnalysisResponse;
  expenseData?: ExpenseAnalysisResponse;
  isLoading?: boolean;
}

interface CategoryItemProps {
  category: string;
  amount: number;
  percentage: number;
  count: number;
  color: "success" | "error";
}

function CategoryItem({
  category,
  amount,
  percentage,
  count,
  color,
}: CategoryItemProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(Math.abs(value));
  };

  return (
    <Box sx={{ mb: 2 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 0.5,
        }}
      >
        <Typography variant="body2" fontWeight="medium">
          {category}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {formatCurrency(amount)} ({count} txn)
        </Typography>
      </Box>
      <LinearProgress
        variant="determinate"
        value={percentage}
        color={color}
        sx={{ height: 6, borderRadius: 3 }}
      />
      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
        {percentage.toFixed(1)}% of total
      </Typography>
    </Box>
  );
}

function CategoryBreakdown({
  incomeData,
  expenseData,
  isLoading,
}: CategoryBreakdownProps) {
  if (isLoading) {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Loading...
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Loading...
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  }

  // Convert income breakdown to array and sort by amount
  const incomeCategories = incomeData
    ? Object.entries(incomeData.breakdown_by_category)
        .map(([category, data]) => ({
          category,
          ...data,
        }))
        .sort((a, b) => b.total - a.total)
        .slice(0, 5) // Top 5
    : [];

  // Convert expense breakdown to array and sort by amount (absolute value for expenses)
  const expenseCategories = expenseData
    ? Object.entries(expenseData.breakdown_by_category)
        .map(([category, data]) => ({
          category,
          ...data,
        }))
        .sort((a, b) => Math.abs(b.total) - Math.abs(a.total)) // Sort by absolute value to get largest expenses
        .slice(0, 5) // Top 5
    : [];

  // Prepare data for pie charts
  const incomePieData = incomeCategories.map((cat) => ({
    name: cat.category,
    value: cat.total,
  }));

  const expensePieData = expenseCategories.map((cat) => ({
    name: cat.category,
    value: Math.abs(cat.total), // Convert negative expense values to positive for display
  }));

  return (
    <Grid container spacing={3}>
      {/* Income Breakdown */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Income by Category
            </Typography>
            {incomeCategories.length > 0 ? (
              <>
                <Box sx={{ mb: 3 }}>
                  <CategoryPieChart
                    data={incomePieData}
                    height={250}
                    colorScheme="success"
                  />
                </Box>
                <Box>
                  {incomeCategories.map((cat) => (
                    <CategoryItem
                      key={cat.category}
                      category={cat.category}
                      amount={cat.total}
                      percentage={cat.percentage}
                      count={cat.count}
                      color="success"
                    />
                  ))}
                </Box>
              </>
            ) : (
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ py: 4, textAlign: "center" }}
              >
                No income data available for this period
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>

      {/* Expense Breakdown */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Expenses by Category
            </Typography>
            {expenseCategories.length > 0 ? (
              <>
                <Box sx={{ mb: 3, height: 250 }}>
                  <CategoryPieChart
                    data={expensePieData}
                    height={250}
                    colorScheme="error"
                  />
                </Box>
                <Box>
                  {expenseCategories.map((cat) => (
                    <CategoryItem
                      key={cat.category}
                      category={cat.category}
                      amount={cat.total}
                      percentage={cat.percentage}
                      count={cat.count}
                      color="error"
                    />
                  ))}
                </Box>
              </>
            ) : (
              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ py: 4, textAlign: "center" }}
              >
                No expense data available for this period
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}

export default CategoryBreakdown;
