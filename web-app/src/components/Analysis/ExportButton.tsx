import { useState } from "react";
import {
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  Snackbar,
  Alert,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import TableChartIcon from "@mui/icons-material/TableChart";
import { format } from "date-fns";
import type {
  IncomeAnalysisResponse,
  ExpenseAnalysisResponse,
  CashFlowResponse,
  FinancialSummaryResponse,
} from "../../api/analysis";

interface ExportButtonProps {
  dateRange: {
    start_date: string;
    end_date: string;
  };
  viewMode: "analysis" | "with_capital" | "complete";
  /** Analysis page: pass individual data sources */
  incomeData?: IncomeAnalysisResponse;
  expenseData?: ExpenseAnalysisResponse;
  cashFlowData?: CashFlowResponse;
  /** Dashboard: pass the combined summary instead */
  summaryData?: FinancialSummaryResponse;
  onExport?: (format: "csv") => Promise<void>;
}

/** Escape a CSV field — wrap in quotes if it contains commas, quotes, or newlines */
function escapeCsvField(value: string | number): string {
  const str = String(value);
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function formatCurrency(value: number): string {
  return value.toFixed(2);
}

function ExportButton({
  dateRange,
  viewMode,
  incomeData,
  expenseData,
  cashFlowData,
  summaryData,
  onExport,
}: ExportButtonProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleExportCSV = async () => {
    setIsExporting(true);
    try {
      if (onExport) {
        await onExport("csv");
      } else if (summaryData) {
        await exportSummaryToCSV();
      } else {
        await exportToCSV();
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Export failed. Please try again.";
      setError(message);
    } finally {
      setIsExporting(false);
      handleClose();
    }
  };

  const exportToCSV = async () => {
    const rows: string[][] = [];

    // Header metadata
    rows.push(["Financial Analysis Export"]);
    rows.push([
      `Date Range: ${dateRange.start_date} to ${dateRange.end_date}`,
    ]);
    rows.push([`Mode: ${viewMode}`]);
    rows.push([
      `Export Date: ${format(new Date(), "yyyy-MM-dd HH:mm:ss")}`,
    ]);
    rows.push([]);

    // Cash flow summary
    if (cashFlowData) {
      rows.push(["Cash Flow Summary"]);
      rows.push(["Metric", "Amount"]);
      rows.push(["Total Income", formatCurrency(cashFlowData.total_income)]);
      rows.push([
        "Total Expenses",
        formatCurrency(cashFlowData.total_expenses),
      ]);
      rows.push([
        "Net Cash Flow",
        formatCurrency(cashFlowData.net_cash_flow),
      ]);
      rows.push(["Income Transactions", String(cashFlowData.income_count)]);
      rows.push(["Expense Transactions", String(cashFlowData.expense_count)]);
      rows.push([]);
    }

    // Income categories
    if (incomeData) {
      rows.push(["Income by Category"]);
      rows.push(["Category", "Type", "Amount", "Count", "Percentage"]);

      const categories = Object.entries(incomeData.breakdown_by_category)
        .map(([category, data]) => ({ category, ...data }))
        .sort((a, b) => b.total - a.total);

      for (const cat of categories) {
        rows.push([
          cat.category,
          "Income",
          formatCurrency(cat.total),
          String(cat.count),
          cat.percentage.toFixed(1) + "%",
        ]);
      }

      rows.push([
        "Total Income",
        "",
        formatCurrency(incomeData.total_income),
        String(incomeData.transaction_count),
        "100.0%",
      ]);
      rows.push([]);
    }

    // Expense categories
    if (expenseData) {
      rows.push(["Expenses by Category"]);
      rows.push(["Category", "Type", "Amount", "Count", "Percentage"]);

      const categories = Object.entries(expenseData.breakdown_by_category)
        .map(([category, data]) => ({ category, ...data }))
        .sort((a, b) => Math.abs(b.total) - Math.abs(a.total));

      for (const cat of categories) {
        rows.push([
          cat.category,
          "Expense",
          formatCurrency(Math.abs(cat.total)),
          String(cat.count),
          cat.percentage.toFixed(1) + "%",
        ]);
      }

      rows.push([
        "Total Expenses",
        "",
        formatCurrency(Math.abs(expenseData.total_expenses)),
        String(expenseData.transaction_count),
        "100.0%",
      ]);
    }

    downloadCSV(rows, `financial-analysis-${dateRange.start_date}-to-${dateRange.end_date}.csv`);
  };

  const exportSummaryToCSV = async () => {
    if (!summaryData) return;
    const rows: string[][] = [];

    // Header metadata
    rows.push(["Dashboard Summary Export"]);
    const start = dateRange.start_date || summaryData.period_start || "all time";
    const end = dateRange.end_date || summaryData.period_end || "present";
    rows.push([`Date Range: ${start} to ${end}`]);
    rows.push([`Mode: ${viewMode}`]);
    rows.push([`Export Date: ${format(new Date(), "yyyy-MM-dd HH:mm:ss")}`]);
    rows.push([]);

    // Cash flow summary
    rows.push(["Cash Flow Summary"]);
    rows.push(["Metric", "Amount"]);
    rows.push(["Total Income", formatCurrency(summaryData.total_income)]);
    rows.push(["Total Expenses", formatCurrency(summaryData.total_expenses)]);
    rows.push(["Net Cash Flow", formatCurrency(summaryData.net_cash_flow)]);
    rows.push(["Income Transactions", String(summaryData.income_count)]);
    rows.push(["Expense Transactions", String(summaryData.expense_count)]);
    rows.push([]);

    // Financial health indicators
    rows.push(["Financial Health"]);
    rows.push(["Indicator", "Value"]);
    rows.push([
      "Income/Expense Ratio",
      summaryData.financial_health.income_to_expense_ratio !== null
        ? summaryData.financial_health.income_to_expense_ratio.toFixed(2)
        : "N/A",
    ]);
    rows.push([
      "Savings Rate",
      summaryData.financial_health.savings_rate !== null
        ? (summaryData.financial_health.savings_rate * 100).toFixed(1) + "%"
        : "N/A",
    ]);
    rows.push([
      "Avg Daily Income",
      formatCurrency(summaryData.financial_health.average_daily_income),
    ]);
    rows.push([
      "Avg Daily Expense",
      formatCurrency(summaryData.financial_health.average_daily_expense),
    ]);
    rows.push([
      "Net Daily Cash Flow",
      formatCurrency(summaryData.financial_health.net_daily_cash_flow),
    ]);
    rows.push([]);

    // Top income categories
    if (summaryData.top_income_categories.length > 0) {
      rows.push(["Top Income Categories"]);
      rows.push(["Category", "Amount", "Count", "Percentage"]);
      for (const cat of summaryData.top_income_categories) {
        rows.push([
          cat.category,
          formatCurrency(cat.amount),
          String(cat.count),
          cat.percentage.toFixed(1) + "%",
        ]);
      }
      rows.push([]);
    }

    // Top expense categories
    if (summaryData.top_expense_categories.length > 0) {
      rows.push(["Top Expense Categories"]);
      rows.push(["Category", "Amount", "Count", "Percentage"]);
      for (const cat of summaryData.top_expense_categories) {
        rows.push([
          cat.category,
          formatCurrency(Math.abs(cat.amount)),
          String(cat.count),
          cat.percentage.toFixed(1) + "%",
        ]);
      }
      rows.push([]);
    }

    // Recent transactions
    if (summaryData.recent_transactions.length > 0) {
      rows.push(["Recent Transactions"]);
      rows.push(["Date", "Description", "Type", "Category", "Amount"]);
      for (const txn of summaryData.recent_transactions) {
        rows.push([
          txn.transaction_date,
          txn.description,
          txn.transaction_type,
          txn.category || "Uncategorized",
          formatCurrency(txn.amount),
        ]);
      }
    }

    const filename = dateRange.start_date
      ? `dashboard-summary-${dateRange.start_date}-to-${dateRange.end_date}.csv`
      : `dashboard-summary-${format(new Date(), "yyyy-MM-dd")}.csv`;
    downloadCSV(rows, filename);
  };

  const downloadCSV = (rows: string[][], filename: string) => {
    const csvContent = rows
      .map((row) => row.map(escapeCsvField).join(","))
      .join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <>
      <Button
        variant="outlined"
        startIcon={
          isExporting ? <CircularProgress size={20} /> : <DownloadIcon />
        }
        onClick={handleClick}
        disabled={isExporting}
      >
        Export
      </Button>
      <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
        <MenuItem onClick={handleExportCSV} disabled={isExporting}>
          <ListItemIcon>
            <TableChartIcon fontSize="small" />
          </ListItemIcon>
          <ListItemText>Export as CSV</ListItemText>
        </MenuItem>
      </Menu>
      <Snackbar
        open={!!error}
        autoHideDuration={6000}
        onClose={() => setError(null)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setError(null)}
          severity="error"
          variant="filled"
        >
          {error}
        </Alert>
      </Snackbar>
    </>
  );
}

export default ExportButton;
