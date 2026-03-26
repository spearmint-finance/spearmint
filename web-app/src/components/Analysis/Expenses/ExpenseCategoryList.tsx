import { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  LinearProgress,
  Alert,
  AlertTitle,
  IconButton,
  CircularProgress,
} from "@mui/material";
import {
  ExpandMore,
  Warning,
  Edit,
} from "@mui/icons-material";
import TransactionDetail from "../../Transactions/TransactionDetail";
import type { Transaction } from "../../../types/transaction";
import { ExpenseAnalysisResponse } from "../../../api/analysis";
import { getTransactions, TransactionListParams } from "../../../api/transactions";
import { categoriesApi } from "../../../api/categories";
import { useQuery } from "@tanstack/react-query";
import { DateRange } from "../DateRangePicker";
import { format } from "date-fns";

interface ExpenseCategoryListProps {
  expenseData?: ExpenseAnalysisResponse;
  dateRange: DateRange;
  viewMode: "analysis" | "with_capital" | "complete";
  isLoading?: boolean;
}

interface CategoryData {
  category: string;
  total: number;
  count: number;
  percentage: number;
  hasWarning: boolean;
  warningType?: "transfer" | "income" | "unusual";
}

function ExpenseCategoryList({ expenseData, dateRange, viewMode, isLoading }: ExpenseCategoryListProps) {
  const [expandedCategory, setExpandedCategory] = useState<string | false>(false);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [detailDialogOpen, setDetailDialogOpen] = useState(false);

  // Fetch categories to check for transfer/income categories
  const { data: categoriesData } = useQuery({
    queryKey: ["categories"],
    queryFn: () => categoriesApi.getAll(),
  });

  // Fetch transactions for expanded category
  const { data: transactionsData, isLoading: transactionsLoading } = useQuery({
    queryKey: ["expense-transactions", expandedCategory, dateRange, viewMode],
    queryFn: async () => {
      if (!expandedCategory || !categoriesData) return null;

      // Find category ID by name
      const category = categoriesData.categories.find(
        (c) => c.category_name === expandedCategory
      );

      if (!category) return null;

      const params: TransactionListParams = {
        start_date: dateRange.start_date || undefined,
        end_date: dateRange.end_date || undefined,
        transaction_type: "Expense",
        category_id: category.category_id,
        include_in_analysis: viewMode === "analysis" ? true : undefined,
        limit: 100,
        sort_by: "amount",
        sort_order: "asc", // asc because expenses are negative, so smallest (most negative) first
      };

      const response = await getTransactions(params);
      return response;
    },
    enabled: !!expandedCategory && !!categoriesData,
  });

  const handleAccordionChange = (category: string) => (_event: React.SyntheticEvent, isExpanded: boolean) => {
    setExpandedCategory(isExpanded ? category : false);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(Math.abs(value));
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Loading expense categories...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (!expenseData) {
    return null;
  }

  // Identify suspicious categories
  const suspiciousKeywords = {
    transfer: ["transfer", "payment to", "credit card payment", "loan payment", "mortgage", "bill pay"],
    income: [
      "salary", "paycheck", "wage", "bonus", "commission", "dividend",
      "interest income", "refund", "reimbursement", "cashback", "reward",
    ],
  };

  const checkCategoryWarning = (categoryName: string): { hasWarning: boolean; warningType?: "transfer" | "income" | "unusual" } => {
    const lowerName = categoryName.toLowerCase();

    // Check if it's a transfer category
    const category = categoriesData?.categories.find((c) => c.category_name === categoryName);
    if (category?.category_type === "Transfer") {
      return { hasWarning: true, warningType: "transfer" };
    }

    // Check for transfer keywords
    if (suspiciousKeywords.transfer.some((keyword) => lowerName.includes(keyword))) {
      return { hasWarning: true, warningType: "transfer" };
    }

    // Check for income keywords
    if (suspiciousKeywords.income.some((keyword) => lowerName.includes(keyword))) {
      return { hasWarning: true, warningType: "income" };
    }

    return { hasWarning: false };
  };

  // Convert expense breakdown to array and sort by amount (highest to lowest)
  const categories: CategoryData[] = Object.entries(expenseData.breakdown_by_category)
    .map(([category, data]) => {
      const warning = checkCategoryWarning(category);
      return {
        category,
        total: data.total,
        count: data.count,
        percentage: data.percentage,
        ...warning,
      };
    })
    .sort((a, b) => Math.abs(b.total) - Math.abs(a.total)); // Sort by absolute value for expenses

  const hasDataQualityIssues = categories.some((cat) => cat.hasWarning);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Expenses by Category
        </Typography>

        {/* Data Quality Warning */}
        {hasDataQualityIssues && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            <AlertTitle>Data Quality Issues Detected</AlertTitle>
            Some expense categories may be miscategorized. Review categories marked with{" "}
            <Warning fontSize="small" sx={{ verticalAlign: "middle" }} /> for potential issues.
          </Alert>
        )}

        {categories.length > 0 ? (
          <Box>
            {categories.map((cat) => (
              <Accordion
                key={cat.category}
                expanded={expandedCategory === cat.category}
                onChange={handleAccordionChange(cat.category)}
                sx={{
                  mb: 1,
                  "&:before": { display: "none" },
                  border: cat.hasWarning ? "1px solid" : "none",
                  borderColor: cat.hasWarning ? "warning.main" : "transparent",
                }}
              >
                <AccordionSummary
                  expandIcon={<ExpandMore />}
                  sx={{
                    "& .MuiAccordionSummary-content": {
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    },
                  }}
                >
                  <Box sx={{ display: "flex", alignItems: "center", gap: 1, flex: 1 }}>
                    {cat.hasWarning && (
                      <Warning color="warning" fontSize="small" />
                    )}
                    <Typography variant="body1" fontWeight="medium">
                      {cat.category} - {cat.percentage.toFixed(1)}%
                    </Typography>
                    {cat.hasWarning && (
                      <Chip
                        label={
                          cat.warningType === "transfer"
                            ? "Possible Transfer"
                            : cat.warningType === "income"
                            ? "Possible Income"
                            : "Unusual"
                        }
                        size="small"
                        color="warning"
                        variant="outlined"
                      />
                    )}
                  </Box>
                  <Box sx={{ display: "flex", flexDirection: "column", alignItems: "flex-end", mr: 2 }}>
                    <Typography variant="body1" fontWeight="medium">
                      {formatCurrency(cat.total)}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {cat.count} transactions
                    </Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Box>
                    <LinearProgress
                      variant="determinate"
                      value={cat.percentage}
                      color="error"
                      sx={{ height: 6, borderRadius: 3, mb: 2 }}
                    />

                    {transactionsLoading ? (
                      <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
                        <CircularProgress size={24} />
                      </Box>
                    ) : transactionsData && transactionsData.transactions.length > 0 ? (
                      <TableContainer component={Paper} variant="outlined">
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell>Date</TableCell>
                              <TableCell>Description</TableCell>
                              <TableCell align="right">Amount</TableCell>
                              <TableCell align="center">Actions</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {transactionsData.transactions.map((transaction) => (
                              <TableRow
                                key={transaction.id}
                                sx={{
                                  "&:last-child td, &:last-child th": { border: 0 },
                                  backgroundColor: transaction.amount > 0 ? "success.lighter" : "inherit",
                                }}
                              >
                                <TableCell>
                                  {format(new Date(transaction.date), "MMM dd, yyyy")}
                                </TableCell>
                                <TableCell>
                                  {transaction.description}
                                  {transaction.amount > 0 && (
                                    <Chip
                                      label="Positive Amount"
                                      size="small"
                                      color="success"
                                      sx={{ ml: 1 }}
                                    />
                                  )}
                                </TableCell>
                                <TableCell align="right">
                                  {formatCurrency(transaction.amount)}
                                </TableCell>
                                <TableCell align="center">
                                  <IconButton
                                    size="small"
                                    onClick={() => {
                                      setSelectedTransaction(transaction);
                                      setDetailDialogOpen(true);
                                    }}
                                    title="Edit transaction"
                                  >
                                    <Edit fontSize="small" />
                                  </IconButton>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    ) : (
                      <Typography variant="body2" color="text.secondary" sx={{ py: 2, textAlign: "center" }}>
                        No transactions found
                      </Typography>
                    )}
                  </Box>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ py: 4, textAlign: "center" }}>
            No expense categories available for this period
          </Typography>
        )}
      </CardContent>

      {/* Transaction Detail Dialog */}
      <TransactionDetail
        open={detailDialogOpen}
        onClose={() => {
          setDetailDialogOpen(false);
          setSelectedTransaction(null);
        }}
        transaction={selectedTransaction}
      />
    </Card>
  );
}

export default ExpenseCategoryList;
