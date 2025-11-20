/**
 * Reconciliation Dashboard Component
 * Shows unclassified transactions and allows quick classification
 */

import { useState } from "react";
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Checkbox,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
  Grid,
  Card,
  CardContent,
} from "@mui/material";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { useTransactions } from "../../hooks/useTransactions";
import {
  useClassifications,
  useBulkClassifyTransactions,
  useAutoClassifyTransactions,
} from "../../hooks/useClassifications";
import { formatCurrency, formatDate } from "../../utils/formatters";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorDisplay from "../common/ErrorDisplay";

function ReconciliationDashboard() {
  const [selectedTransactions, setSelectedTransactions] = useState<number[]>(
    []
  );
  const [selectedClassification, setSelectedClassification] = useState<
    number | ""
  >("");

  // Fetch all transactions (we'll filter unclassified in the UI)
  // Note: Backend doesn't have a direct "unclassified_only" filter yet
  const {
    data: transactionsData,
    isLoading: transactionsLoading,
    error: transactionsError,
    refetch: refetchTransactions,
  } = useTransactions({
    limit: 1000,
    offset: 0,
  });

  // Fetch classifications
  const { data: classificationsData } = useClassifications();

  const bulkClassifyMutation = useBulkClassifyTransactions();
  const autoClassifyMutation = useAutoClassifyTransactions();

  // Filter unclassified transactions (classification_id is null or 1 for "Standard")
  // We'll consider transactions without a classification or with classification_id = 1 as unclassified
  const allTransactions = transactionsData?.transactions || [];
  const transactions = allTransactions.filter(
    (t) => !t.classification_id || t.classification_id === 1
  );
  const unclassifiedCount = transactions.length;

  // Handle select all
  const handleSelectAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      const allIds = transactions.map((t) => t.id);
      setSelectedTransactions(allIds);
    } else {
      setSelectedTransactions([]);
    }
  };

  // Handle select individual
  const handleSelectTransaction = (transactionId: number) => {
    setSelectedTransactions((prev) =>
      prev.includes(transactionId)
        ? prev.filter((id) => id !== transactionId)
        : [...prev, transactionId]
    );
  };

  // Handle bulk classify
  const handleBulkClassify = async () => {
    if (!selectedClassification || selectedTransactions.length === 0) {
      alert("Please select transactions and a classification");
      return;
    }

    try {
      const result = await bulkClassifyMutation.mutateAsync({
        transaction_ids: selectedTransactions,
        classification_id: Number(selectedClassification),
      });

      alert(
        `Successfully classified ${result.success_count} transaction(s). Failed: ${result.failed_count}`
      );

      // Clear selection
      setSelectedTransactions([]);
      setSelectedClassification("");
    } catch (error) {
      console.error("Failed to bulk classify:", error);
    }
  };

  // Handle auto classify
  const handleAutoClassify = async () => {
    if (
      !window.confirm(
        "This will automatically classify all unclassified transactions using active rules. Continue?"
      )
    ) {
      return;
    }

    try {
      const result = await autoClassifyMutation.mutateAsync({});

      alert(
        `Auto-classification complete!\n` +
          `Processed: ${result.total_processed}\n` +
          `Classified: ${result.classified_count}\n` +
          `Skipped: ${result.skipped_count}`
      );
    } catch (error) {
      console.error("Failed to auto classify:", error);
    }
  };

  // Loading state
  if (transactionsLoading) {
    return <LoadingSpinner message="Loading unclassified transactions..." />;
  }

  // Error state
  if (transactionsError) {
    return (
      <ErrorDisplay
        message="Failed to load transactions"
        onRetry={refetchTransactions}
      />
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography variant="h6">Reconciliation Dashboard</Typography>
        <Button
          variant="contained"
          startIcon={<AutoFixHighIcon />}
          onClick={handleAutoClassify}
          disabled={autoClassifyMutation.isPending || unclassifiedCount === 0}
        >
          Auto-Classify All
        </Button>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Unclassified Transactions
              </Typography>
              <Typography variant="h4">{unclassifiedCount}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Selected
              </Typography>
              <Typography variant="h4">
                {selectedTransactions.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Transactions
              </Typography>
              <Typography variant="h4">{allTransactions.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Bulk Actions */}
      {transactions.length > 0 && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth size="small">
                <InputLabel>Select Classification</InputLabel>
                <Select
                  value={selectedClassification}
                  onChange={(e) =>
                    setSelectedClassification(e.target.value as number)
                  }
                  label="Select Classification"
                >
                  {classificationsData?.classifications.map((c) => (
                    <MenuItem
                      key={c.classification_id}
                      value={c.classification_id}
                    >
                      {c.classification_name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Button
                variant="contained"
                fullWidth
                startIcon={<CheckCircleIcon />}
                onClick={handleBulkClassify}
                disabled={
                  bulkClassifyMutation.isPending ||
                  selectedTransactions.length === 0 ||
                  !selectedClassification
                }
              >
                Apply to {selectedTransactions.length} Selected
              </Button>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Transactions Table */}
      {transactions.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <CheckCircleIcon
            sx={{ fontSize: 60, color: "success.main", mb: 2 }}
          />
          <Typography variant="h6" gutterBottom>
            All Transactions Classified!
          </Typography>
          <Typography variant="body1" color="text.secondary">
            There are no unclassified transactions at this time.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell padding="checkbox">
                  <Checkbox
                    checked={
                      selectedTransactions.length === transactions.length &&
                      transactions.length > 0
                    }
                    indeterminate={
                      selectedTransactions.length > 0 &&
                      selectedTransactions.length < transactions.length
                    }
                    onChange={handleSelectAll}
                  />
                </TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Category</TableCell>
                <TableCell align="right">Amount</TableCell>
                <TableCell>Type</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {transactions.map((transaction) => (
                <TableRow
                  key={transaction.id}
                  hover
                  selected={selectedTransactions.includes(transaction.id)}
                >
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={selectedTransactions.includes(transaction.id)}
                      onChange={() => handleSelectTransaction(transaction.id)}
                    />
                  </TableCell>
                  <TableCell>{formatDate(transaction.date)}</TableCell>
                  <TableCell>{transaction.description}</TableCell>
                  <TableCell>
                    {transaction.category_name || (
                      <Chip label="Uncategorized" size="small" />
                    )}
                  </TableCell>
                  <TableCell align="right">
                    {formatCurrency(transaction.amount)}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={transaction.transaction_type}
                      size="small"
                      color={
                        transaction.transaction_type === "Income"
                          ? "success"
                          : "error"
                      }
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {transactions.length > 0 && (
        <Alert severity="info" sx={{ mt: 2 }}>
          <strong>Tip:</strong> Select transactions and apply a classification,
          or use "Auto-Classify All" to apply rules automatically.
        </Alert>
      )}
    </Box>
  );
}

export default ReconciliationDashboard;
