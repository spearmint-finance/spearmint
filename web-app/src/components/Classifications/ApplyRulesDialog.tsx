/**
 * Apply Classification Rules Dialog
 * Dialog for applying classification rules to existing transactions
 */

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import { useApplyClassificationRules } from "../../hooks/useClassifications";
import type { ApplyRulesResponse } from "../../types/classification";

interface ApplyRulesDialogProps {
  open: boolean;
  onClose: () => void;
  ruleId?: number | null;
  ruleName?: string;
}

function ApplyRulesDialog({ open, onClose, ruleId, ruleName }: ApplyRulesDialogProps) {
  const [previewResult, setPreviewResult] = useState<ApplyRulesResponse | null>(
    null
  );
  const [appliedResult, setAppliedResult] = useState<ApplyRulesResponse | null>(
    null
  );

  const applyRulesMutation = useApplyClassificationRules();

  // Reset state when dialog opens
  useEffect(() => {
    if (open) {
      setPreviewResult(null);
      setAppliedResult(null);
      applyRulesMutation.reset();
    }
  }, [open]);

  // Handle preview (dry run)
  const handlePreview = async () => {
    setPreviewResult(null);
    setAppliedResult(null);
    try {
      const result = await applyRulesMutation.mutateAsync({
        dry_run: true,
        rule_ids: ruleId ? [ruleId] : undefined
      });
      setPreviewResult(result);
    } catch (error) {
      console.error("Failed to preview rules:", error);
    }
  };

  // Handle apply (actual run)
  const handleApply = async () => {
    setAppliedResult(null);
    try {
      const result = await applyRulesMutation.mutateAsync({
        dry_run: false,
        rule_ids: ruleId ? [ruleId] : undefined
      });
      setAppliedResult(result);
    } catch (error) {
      console.error("Failed to apply rules:", error);
    }
  };

  // Handle close
  const handleClose = () => {
    setPreviewResult(null);
    setAppliedResult(null);
    onClose();
  };

  const result = appliedResult || previewResult;
  const isLoading = applyRulesMutation.isPending;

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {ruleId ? `Apply Rule: ${ruleName}` : "Apply Classification Rules"}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mb: 2 }}>
          <Alert severity="info" sx={{ mb: 2 }}>
            {ruleId
              ? `This will apply the "${ruleName}" rule to existing transactions that match its patterns. Preview first to see what changes will be made.`
              : "This will apply all active classification rules to existing transactions based on their patterns. Preview first to see what changes will be made."}
          </Alert>

          {isLoading && (
            <Box sx={{ display: "flex", justifyContent: "center", my: 3 }}>
              <CircularProgress />
            </Box>
          )}

          {applyRulesMutation.isError && !result && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Failed to apply rules. Please try again.
            </Alert>
          )}

          {appliedResult && (
            <Alert severity="success" icon={<CheckCircleIcon />} sx={{ mb: 2 }}>
              Successfully applied {appliedResult.total_rules_processed} rules and
              updated {appliedResult.total_transactions_updated} transactions!
            </Alert>
          )}

          {result && !isLoading && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {result.dry_run ? "Preview Results" : "Application Results"}
              </Typography>

              <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
                <Chip
                  label={`${result.total_rules_processed} Rules Processed`}
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`${result.total_transactions_updated} Transactions ${result.dry_run ? "Would Be" : ""} Updated`}
                  color="secondary"
                  variant="outlined"
                />
              </Box>

              {result.rules_applied.length > 0 && (
                <TableContainer component={Paper} variant="outlined">
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Rule Name</TableCell>
                        <TableCell>Classification</TableCell>
                        <TableCell align="right">
                          Transactions {result.dry_run ? "Matched" : "Updated"}
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {result.rules_applied.map((rule) => (
                        <TableRow key={rule.rule_id}>
                          <TableCell>{rule.rule_name}</TableCell>
                          <TableCell>
                            <Chip
                              label={rule.classification_name}
                              size="small"
                              color="secondary"
                            />
                          </TableCell>
                          <TableCell align="right">
                            <Chip
                              label={rule.transactions_matched}
                              size="small"
                              color={
                                rule.transactions_matched > 0
                                  ? "success"
                                  : "default"
                              }
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}

              {result.total_transactions_updated === 0 && (
                <Alert severity="warning" sx={{ mt: 2 }}>
                  No transactions matched any rules. Check your rule patterns.
                </Alert>
              )}
            </Box>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={isLoading}>
          Close
        </Button>
        {!appliedResult && (
          <>
            <Button
              onClick={handlePreview}
              disabled={isLoading}
              variant="outlined"
              startIcon={<PlayArrowIcon />}
            >
              Preview Changes
            </Button>
            <Button
              onClick={handleApply}
              disabled={isLoading || !previewResult}
              variant="contained"
              color="primary"
              startIcon={<CheckCircleIcon />}
            >
              Apply Rules
            </Button>
          </>
        )}
      </DialogActions>
    </Dialog>
  );
}

export default ApplyRulesDialog;
