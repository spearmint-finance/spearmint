/**
 * Apply Category Rules Dialog Component
 * Dialog for applying category rules to transactions
 */

import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControlLabel,
  Checkbox,
  Typography,
  Alert,
  Box,
  CircularProgress,
} from "@mui/material";
import { useApplyCategoryRules } from "../../hooks/useCategoryRules";

interface ApplyCategoryRulesDialogProps {
  open: boolean;
  onClose: () => void;
  ruleId?: number;
  ruleName?: string;
}

function ApplyCategoryRulesDialog({
  open,
  onClose,
  ruleId,
  ruleName,
}: ApplyCategoryRulesDialogProps) {
  const [forceRecategorize, setForceRecategorize] = useState(false);
  const [result, setResult] = useState<{
    total_processed: number;
    categorized_count: number;
    skipped_count: number;
    rules_applied: number;
  } | null>(null);

  const applyRulesMutation = useApplyCategoryRules();

  const handleApply = async () => {
    try {
      const response = await applyRulesMutation.mutateAsync({
        rule_ids: ruleId ? [ruleId] : undefined,
        force_recategorize: forceRecategorize,
      });
      setResult(response);
    } catch (error) {
      console.error("Failed to apply rules:", error);
    }
  };

  const handleClose = () => {
    setResult(null);
    setForceRecategorize(false);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {ruleId ? `Apply Rule: ${ruleName}` : "Apply All Category Rules"}
      </DialogTitle>

      <DialogContent>
        {!result ? (
          <Box>
            <Typography variant="body2" paragraph>
              {ruleId
                ? `This will apply the "${ruleName}" rule to transactions.`
                : "This will apply all active category rules to transactions."}
            </Typography>

            <FormControlLabel
              control={
                <Checkbox
                  checked={forceRecategorize}
                  onChange={(e) => setForceRecategorize(e.target.checked)}
                />
              }
              label="Force recategorize (apply to already categorized transactions)"
            />

            <Alert severity="info" sx={{ mt: 2 }}>
              By default, only uncategorized transactions will be processed. Enable
              "Force recategorize" to update all matching transactions.
            </Alert>
          </Box>
        ) : (
          <Box>
            <Alert severity="success" sx={{ mb: 2 }}>
              Rules applied successfully!
            </Alert>

            <Typography variant="body2" paragraph>
              <strong>Total Processed:</strong> {result.total_processed}
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Categorized:</strong> {result.categorized_count}
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Skipped:</strong> {result.skipped_count}
            </Typography>
            <Typography variant="body2" paragraph>
              <strong>Rules Applied:</strong> {result.rules_applied}
            </Typography>
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        {!result ? (
          <>
            <Button onClick={handleClose}>Cancel</Button>
            <Button
              onClick={handleApply}
              variant="contained"
              disabled={applyRulesMutation.isPending}
              startIcon={
                applyRulesMutation.isPending ? (
                  <CircularProgress size={20} />
                ) : null
              }
            >
              {applyRulesMutation.isPending ? "Applying..." : "Apply Rules"}
            </Button>
          </>
        ) : (
          <Button onClick={handleClose} variant="contained">
            Close
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}

export default ApplyCategoryRulesDialog;

