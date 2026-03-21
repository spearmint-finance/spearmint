import { useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Switch,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Alert,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import FileUpload from "./FileUpload";
import ImportHistory from "./ImportHistory";
import type { ImportResponse } from "../../types/import";
import { useImportDetail } from "../../hooks/useImport";

export default function ImportPage() {
  const [mode, setMode] = useState<"full" | "incremental" | "update">(
    "incremental"
  );
  const [skipDuplicates, setSkipDuplicates] = useState(true);
  const [lastImportResult, setLastImportResult] =
    useState<ImportResponse | null>(null);
  const [selectedImportId, setSelectedImportId] = useState<number | null>(null);

  const { data: importDetail } = useImportDetail(selectedImportId);

  const handleImportSuccess = (result: ImportResponse) => {
    setLastImportResult(result);
  };

  const handleViewDetail = (importId: number) => {
    setSelectedImportId(importId);
  };

  const handleCloseDetail = () => {
    setSelectedImportId(null);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Import Transactions
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload Excel files to import your financial transactions
      </Typography>

      <Grid container spacing={3}>
        {/* Upload Section */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload File
            </Typography>

            {/* Import Options */}
            <Box sx={{ mb: 3 }}>
              <FormControl component="fieldset" sx={{ mb: 2 }}>
                <FormLabel component="legend">Import Mode</FormLabel>
                <RadioGroup
                  row
                  value={mode}
                  onChange={(e) =>
                    setMode(e.target.value as "full" | "incremental" | "update")
                  }
                >
                  <FormControlLabel
                    value="incremental"
                    control={<Radio />}
                    label="Incremental (Add new)"
                  />
                  <FormControlLabel
                    value="update"
                    control={<Radio />}
                    label="Update (Modify existing)"
                  />
                  <FormControlLabel
                    value="full"
                    control={<Radio />}
                    label="Full (Replace all)"
                  />
                </RadioGroup>
              </FormControl>

              <FormControlLabel
                control={
                  <Switch
                    checked={skipDuplicates}
                    onChange={(e) => setSkipDuplicates(e.target.checked)}
                  />
                }
                label="Skip duplicate transactions"
              />
            </Box>

            <Divider sx={{ mb: 3 }} />

            {/* File Upload Component */}
            <FileUpload
              mode={mode}
              skipDuplicates={skipDuplicates}
              onSuccess={handleImportSuccess}
            />

            {/* Last Import Result */}
            {lastImportResult && (
              <Alert
                severity={
                  lastImportResult.successful_rows > 0
                    ? "success"
                    : lastImportResult.skipped_duplicates > 0
                    ? "info"
                    : "error"
                }
                sx={{ mt: 3 }}
              >
                <Typography variant="subtitle2" gutterBottom>
                  Import Summary
                </Typography>
                <Typography variant="body2">
                  Total Rows: {lastImportResult.total_rows} | Successful:{" "}
                  {lastImportResult.successful_rows} | Failed:{" "}
                  {lastImportResult.failed_rows} | Duplicates Skipped:{" "}
                  {lastImportResult.skipped_duplicates}
                </Typography>
                {(lastImportResult.accounts_created > 0 || lastImportResult.accounts_skipped > 0) && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    Accounts: {lastImportResult.accounts_created} created
                    {lastImportResult.accounts_skipped > 0 && `, ${lastImportResult.accounts_skipped} already existed`}
                  </Typography>
                )}
                {lastImportResult.skipped_duplicates > 0 && (
                  <Typography variant="body2" color="info" sx={{ mt: 1 }}>
                    {lastImportResult.skipped_duplicates} duplicate transaction{lastImportResult.skipped_duplicates !== 1 ? 's' : ''} {lastImportResult.skipped_duplicates !== 1 ? 'were' : 'was'} skipped to prevent double-counting
                  </Typography>
                )}
                {lastImportResult.errors.length > 0 && (
                  <Typography variant="body2" color="error" sx={{ mt: 1 }}>
                    {lastImportResult.errors.length} error(s) occurred
                  </Typography>
                )}
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Info Section */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              File Format Requirements
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              <strong>Required columns:</strong>
            </Typography>
            <List dense>
              <ListItem>
                <ListItemText primary="Date" secondary="Transaction date" />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Amount"
                  secondary="Transaction amount (negative = expense, positive = income)"
                />
              </ListItem>
              <ListItem>
                <ListItemText primary="Category" secondary="Category name" />
              </ListItem>
            </List>

            <Typography
              variant="body2"
              color="text.secondary"
              paragraph
              sx={{ mt: 2 }}
            >
              <strong>Optional columns:</strong>
            </Typography>
            <List dense>
              <ListItem>
                <ListItemText
                  primary="Description / Full Description"
                  secondary="Transaction description"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Account"
                  secondary="Account name or source"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Institution"
                  secondary="Financial institution"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Transaction ID"
                  secondary="External transaction ID"
                />
              </ListItem>
            </List>

            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="caption">
                <strong>Note:</strong> Transaction type (Income/Expense) is
                automatically determined from the amount. Negative amounts are
                expenses, positive are income.
              </Typography>
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                <strong>Tiller support:</strong> If your file has an
                &quot;Accounts&quot; sheet, accounts will be auto-created with
                balances, types, and institution info.
              </Typography>
            </Alert>
          </Paper>
        </Grid>

        {/* Import History */}
        <Grid item xs={12}>
          <ImportHistory onViewDetail={handleViewDetail} />
        </Grid>
      </Grid>

      {/* Import Detail Dialog */}
      <Dialog
        open={selectedImportId !== null}
        onClose={handleCloseDetail}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Import Details</DialogTitle>
        <DialogContent>
          {importDetail && (
            <Box>
              <Typography variant="body2" gutterBottom>
                <strong>File:</strong> {importDetail.file_name}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Date:</strong>{" "}
                {new Date(importDetail.import_date).toLocaleString()}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Mode:</strong> {importDetail.import_mode}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Total Rows:</strong> {importDetail.total_rows}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Successful:</strong> {importDetail.successful_rows}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Failed:</strong> {importDetail.failed_rows}
              </Typography>
              <Typography variant="body2" gutterBottom>
                <strong>Classified:</strong> {importDetail.classified_rows}
              </Typography>

              {importDetail.error_log && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Error Log:
                  </Typography>
                  <Paper
                    sx={{
                      p: 2,
                      bgcolor: "grey.100",
                      maxHeight: 200,
                      overflow: "auto",
                    }}
                  >
                    <Typography
                      variant="body2"
                      component="pre"
                      sx={{ whiteSpace: "pre-wrap", fontFamily: "monospace" }}
                    >
                      {importDetail.error_log}
                    </Typography>
                  </Paper>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetail}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
