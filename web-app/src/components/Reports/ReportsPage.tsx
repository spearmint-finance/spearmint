import React, { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Tabs,
  Tab,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  Button,
  Divider,
  Skeleton,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import { useQuery } from "@tanstack/react-query";
import { useEntityContext } from "../../contexts/EntityContext";
import { formatCurrency } from "../../utils/formatters";
import sdk from "../../api/sdk";

/** Fetch P&L from API */
async function fetchPnl(
  entityId: number,
  startDate: string,
  endDate: string
): Promise<any> {
  const baseUrl =
    (sdk as any).config?.baseUrl ||
    (sdk as any).config?.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined"
      ? window.location.origin
      : "http://localhost:8080");
  const url = `${baseUrl}/api/entities/${entityId}/pnl?start_date=${startDate}&end_date=${endDate}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch P&L");
  return res.json();
}

/** Fetch cash flow from API */
async function fetchCashflow(
  entityId: number,
  startDate: string,
  endDate: string
): Promise<any> {
  const baseUrl =
    (sdk as any).config?.baseUrl ||
    (sdk as any).config?.environment ||
    import.meta.env.VITE_API_URL ||
    (typeof window !== "undefined"
      ? window.location.origin
      : "http://localhost:8080");
  const url = `${baseUrl}/api/entities/${entityId}/cashflow?start_date=${startDate}&end_date=${endDate}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch cash flow");
  return res.json();
}

function getDefaultDateRange(): { start: string; end: string } {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  return {
    start: start.toISOString().split("T")[0],
    end: now.toISOString().split("T")[0],
  };
}

const ReportsPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const { selectedEntity, selectedEntityId, entities } = useEntityContext();
  const defaultRange = getDefaultDateRange();
  const [startDate, setStartDate] = useState(defaultRange.start);
  const [endDate, setEndDate] = useState(defaultRange.end);

  const entityId = selectedEntityId ?? entities.find((e) => e.is_default)?.entity_id;
  const entityName = selectedEntity?.entity_name ?? entities.find((e) => e.is_default)?.entity_name ?? "All";

  const {
    data: pnlData,
    isLoading: pnlLoading,
    error: pnlError,
  } = useQuery({
    queryKey: ["pnl", entityId, startDate, endDate],
    queryFn: () =>
      entityId ? fetchPnl(entityId, startDate, endDate) : null,
    enabled: !!entityId,
  });

  const {
    data: cashflowData,
    isLoading: cashflowLoading,
    error: cashflowError,
  } = useQuery({
    queryKey: ["cashflow", entityId, startDate, endDate],
    queryFn: () =>
      entityId ? fetchCashflow(entityId, startDate, endDate) : null,
    enabled: !!entityId && tabValue === 1,
  });

  const handleExportCashflowCsv = () => {
    if (!cashflowData) return;
    const rows: string[] = ["Section,Description,Amount"];
    for (const item of cashflowData.operating?.items ?? []) {
      rows.push(`Operating,"${item.description}",${item.amount}`);
    }
    rows.push(`Operating,TOTAL,${cashflowData.operating?.total ?? 0}`);
    rows.push("");
    for (const item of cashflowData.investing?.items ?? []) {
      rows.push(`Investing,"${item.description}",${item.amount}`);
    }
    rows.push(`Investing,TOTAL,${cashflowData.investing?.total ?? 0}`);
    rows.push("");
    for (const item of cashflowData.financing?.items ?? []) {
      rows.push(`Financing,"${item.description}",${item.amount}`);
    }
    rows.push(`Financing,TOTAL,${cashflowData.financing?.total ?? 0}`);
    rows.push("");
    rows.push(`Net Change in Cash,,${cashflowData.net_change ?? 0}`);

    const blob = new Blob([rows.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cashflow-${entityName}-${startDate}-to-${endDate}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportPnlCsv = () => {
    if (!pnlData) return;
    const rows: string[] = ["Section,Category,Amount"];
    for (const item of pnlData.revenue?.by_category ?? []) {
      rows.push(`Revenue,"${item.category_name}",${item.amount}`);
    }
    rows.push(`Revenue,TOTAL,${pnlData.revenue?.total ?? 0}`);
    rows.push("");
    for (const item of pnlData.expenses?.by_category ?? []) {
      rows.push(`Expenses,"${item.category_name}",${item.amount}`);
    }
    rows.push(`Expenses,TOTAL,${pnlData.expenses?.total ?? 0}`);
    rows.push("");
    rows.push(`Net Income,,${pnlData.net_income ?? 0}`);

    const blob = new Blob([rows.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `pnl-${entityName}-${startDate}-to-${endDate}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!entityId) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="info">
          {entities.length > 0
            ? "Select an entity from the sidebar to view reports."
            : "Create an entity using \"Manage Entities\" in the sidebar to generate P&L and Cash Flow reports."}
        </Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", maxWidth: 1200, mx: "auto" }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography variant="h4">
          Reports — {entityName}
        </Typography>
        <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
          <TextField
            label="Start Date"
            type="date"
            size="small"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End Date"
            type="date"
            size="small"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
        </Box>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={(_, v) => setTabValue(v)}
          aria-label="Report type"
          sx={{ borderBottom: 1, borderColor: "divider" }}
        >
          <Tab label="Profit & Loss" />
          <Tab label="Cash Flow" />
        </Tabs>

        {/* ============ P&L Tab ============ */}
        {tabValue === 0 && (
          <Box sx={{ p: 3 }}>
            {pnlLoading ? (
              <Box>
                <Skeleton height={40} />
                <Skeleton height={30} width="60%" />
                <Skeleton height={30} width="80%" />
                <Skeleton height={30} width="50%" />
              </Box>
            ) : pnlError ? (
              <Alert severity="error">Failed to load P&L data</Alert>
            ) : pnlData ? (
              <>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    mb: 2,
                  }}
                >
                  <Typography variant="subtitle1" color="text.secondary">
                    {pnlData.period?.start} to {pnlData.period?.end}
                  </Typography>
                  <Button
                    size="small"
                    startIcon={<DownloadIcon />}
                    onClick={handleExportPnlCsv}
                  >
                    Export CSV
                  </Button>
                </Box>

                {/* Revenue */}
                <Typography
                  variant="h6"
                  sx={{ mt: 2, mb: 1, color: "success.main" }}
                >
                  Revenue
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Category</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(pnlData.revenue?.by_category ?? []).length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={2} sx={{ color: "text.secondary" }}>
                            No revenue for this period
                          </TableCell>
                        </TableRow>
                      ) : (pnlData.revenue?.by_category ?? []).map(
                        (item: any) => (
                          <TableRow key={item.category_id}>
                            <TableCell>{item.category_name}</TableCell>
                            <TableCell align="right">
                              {item.tax_line_item && (
                                <Chip
                                  label={item.tax_line_item}
                                  size="small"
                                  variant="outlined"
                                  sx={{ mr: 1, fontSize: "0.7rem" }}
                                />
                              )}
                              {formatCurrency(item.amount)}
                            </TableCell>
                          </TableRow>
                        )
                      )}
                      <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>
                          Total Revenue
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: "bold", color: "success.main" }}
                        >
                          {formatCurrency(pnlData.revenue?.total ?? 0)}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Expenses */}
                <Typography
                  variant="h6"
                  sx={{ mt: 3, mb: 1, color: "error.main" }}
                >
                  Expenses
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Category</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(pnlData.expenses?.by_category ?? []).length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={2} sx={{ color: "text.secondary" }}>
                            No expenses for this period
                          </TableCell>
                        </TableRow>
                      ) : (pnlData.expenses?.by_category ?? []).map(
                        (item: any) => (
                          <TableRow key={item.category_id}>
                            <TableCell>{item.category_name}</TableCell>
                            <TableCell align="right">
                              {item.tax_line_item && (
                                <Chip
                                  label={item.tax_line_item}
                                  size="small"
                                  variant="outlined"
                                  sx={{ mr: 1, fontSize: "0.7rem" }}
                                />
                              )}
                              {formatCurrency(item.amount)}
                            </TableCell>
                          </TableRow>
                        )
                      )}
                      <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>
                          Total Expenses
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: "bold", color: "error.main" }}
                        >
                          {formatCurrency(pnlData.expenses?.total ?? 0)}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Net Income */}
                <Divider sx={{ my: 2 }} />
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    px: 2,
                  }}
                >
                  <Typography variant="h6">Net Income</Typography>
                  <Typography
                    variant="h6"
                    sx={{
                      color:
                        (pnlData.net_income ?? 0) >= 0
                          ? "success.main"
                          : "error.main",
                      fontWeight: "bold",
                    }}
                  >
                    {formatCurrency(pnlData.net_income ?? 0)}
                  </Typography>
                </Box>
              </>
            ) : null}
          </Box>
        )}

        {/* ============ Cash Flow Tab ============ */}
        {tabValue === 1 && (
          <Box sx={{ p: 3 }}>
            {cashflowLoading ? (
              <Box>
                <Skeleton height={40} />
                <Skeleton height={30} width="60%" />
                <Skeleton height={30} width="80%" />
              </Box>
            ) : cashflowError ? (
              <Alert severity="error">Failed to load cash flow data</Alert>
            ) : cashflowData ? (
              <>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    mb: 2,
                  }}
                >
                  <Typography variant="subtitle1" color="text.secondary">
                    {cashflowData.period?.start} to {cashflowData.period?.end}
                  </Typography>
                  <Button
                    size="small"
                    startIcon={<DownloadIcon />}
                    onClick={handleExportCashflowCsv}
                  >
                    Export CSV
                  </Button>
                </Box>

                {/* Operating */}
                <Typography variant="h6" sx={{ mb: 1 }}>
                  Operating Activities
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Description</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(cashflowData.operating?.items ?? []).map(
                        (item: any, i: number) => (
                          <TableRow key={i}>
                            <TableCell>{item.description}</TableCell>
                            <TableCell
                              align="right"
                              sx={{
                                color:
                                  item.amount >= 0
                                    ? "success.main"
                                    : "error.main",
                              }}
                            >
                              {formatCurrency(item.amount)}
                            </TableCell>
                          </TableRow>
                        )
                      )}
                      <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>
                          Net Operating
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                          {formatCurrency(cashflowData.operating?.total ?? 0)}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Investing */}
                <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
                  Investing Activities
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Description</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(cashflowData.investing?.items ?? []).length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={2} sx={{ color: "text.secondary" }}>
                            No investing activities
                          </TableCell>
                        </TableRow>
                      ) : (
                        (cashflowData.investing?.items ?? []).map(
                          (item: any, i: number) => (
                            <TableRow key={i}>
                              <TableCell>{item.description}</TableCell>
                              <TableCell align="right">
                                {formatCurrency(item.amount)}
                              </TableCell>
                            </TableRow>
                          )
                        )
                      )}
                      <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>
                          Net Investing
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                          {formatCurrency(cashflowData.investing?.total ?? 0)}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Financing */}
                <Typography variant="h6" sx={{ mt: 3, mb: 1 }}>
                  Financing Activities
                </Typography>
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Description</TableCell>
                        <TableCell align="right">Amount</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {(cashflowData.financing?.items ?? []).length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={2} sx={{ color: "text.secondary" }}>
                            No financing activities
                          </TableCell>
                        </TableRow>
                      ) : (
                        (cashflowData.financing?.items ?? []).map(
                          (item: any, i: number) => (
                            <TableRow key={i}>
                              <TableCell>{item.description}</TableCell>
                              <TableCell align="right">
                                {formatCurrency(item.amount)}
                              </TableCell>
                            </TableRow>
                          )
                        )
                      )}
                      <TableRow>
                        <TableCell sx={{ fontWeight: "bold" }}>
                          Net Financing
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: "bold" }}>
                          {formatCurrency(cashflowData.financing?.total ?? 0)}
                        </TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Net Change */}
                <Divider sx={{ my: 2 }} />
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    px: 2,
                  }}
                >
                  <Typography variant="h6">Net Change in Cash</Typography>
                  <Typography
                    variant="h6"
                    sx={{
                      color:
                        (cashflowData.net_change ?? 0) >= 0
                          ? "success.main"
                          : "error.main",
                      fontWeight: "bold",
                    }}
                  >
                    {formatCurrency(cashflowData.net_change ?? 0)}
                  </Typography>
                </Box>
              </>
            ) : null}
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default ReportsPage;
