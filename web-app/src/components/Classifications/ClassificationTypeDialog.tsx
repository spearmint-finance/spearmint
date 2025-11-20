/**
 * Dialog for creating and editing Classification Types
 */

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControlLabel,
  Checkbox,
  Box,
  Alert,
  Tooltip,
  IconButton,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";
import type {
  Classification,
  ClassificationCreate,
  ClassificationUpdate,
} from "../../types/classification";

interface ClassificationTypeDialogProps {
  open: boolean;
  onClose: () => void;
  onSave: (data: ClassificationCreate | ClassificationUpdate) => void;
  classification?: Classification | null;
  isLoading?: boolean;
  error?: string | null;
}

function ClassificationTypeDialog({
  open,
  onClose,
  onSave,
  classification,
  isLoading = false,
  error = null,
}: ClassificationTypeDialogProps) {
  const isEditMode = !!classification;

  // Form state
  const [formData, setFormData] = useState({
    classification_name: "",
    classification_code: "",
    description: "",
    exclude_from_income_calc: false,
    exclude_from_expense_calc: false,
    exclude_from_cashflow_calc: false,
  });

  // Validation errors
  const [errors, setErrors] = useState({
    classification_name: "",
    classification_code: "",
  });

  // Initialize form with classification data when editing
  useEffect(() => {
    if (classification) {
      setFormData({
        classification_name: classification.classification_name,
        classification_code: classification.classification_code,
        description: classification.description || "",
        exclude_from_income_calc: classification.exclude_from_income_calc,
        exclude_from_expense_calc: classification.exclude_from_expense_calc,
        exclude_from_cashflow_calc: classification.exclude_from_cashflow_calc,
      });
    } else {
      // Reset form for create mode
      setFormData({
        classification_name: "",
        classification_code: "",
        description: "",
        exclude_from_income_calc: false,
        exclude_from_expense_calc: false,
        exclude_from_cashflow_calc: false,
      });
    }
    setErrors({ classification_name: "", classification_code: "" });
  }, [classification, open]);

  const handleChange = (field: string, value: string | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (field in errors) {
      setErrors((prev) => ({ ...prev, [field]: "" }));
    }
  };

  const handleCodeChange = (value: string) => {
    // Auto-format code to uppercase and replace spaces with underscores
    const formattedCode = value.toUpperCase().replace(/\s+/g, "_");
    handleChange("classification_code", formattedCode);
  };

  const validate = (): boolean => {
    const newErrors = {
      classification_name: "",
      classification_code: "",
    };

    if (!formData.classification_name.trim()) {
      newErrors.classification_name = "Name is required";
    }

    if (!formData.classification_code.trim()) {
      newErrors.classification_code = "Code is required";
    } else if (!/^[A-Z0-9_]+$/.test(formData.classification_code)) {
      newErrors.classification_code =
        "Code must contain only uppercase letters, numbers, and underscores";
    }

    setErrors(newErrors);
    return !newErrors.classification_name && !newErrors.classification_code;
  };

  const handleSubmit = () => {
    if (!validate()) {
      return;
    }

    const dataToSave = isEditMode
      ? ({
          classification_name: formData.classification_name,
          description: formData.description || undefined,
          exclude_from_income_calc: formData.exclude_from_income_calc,
          exclude_from_expense_calc: formData.exclude_from_expense_calc,
          exclude_from_cashflow_calc: formData.exclude_from_cashflow_calc,
        } as ClassificationUpdate)
      : ({
          classification_name: formData.classification_name,
          classification_code: formData.classification_code,
          description: formData.description || undefined,
          exclude_from_income_calc: formData.exclude_from_income_calc,
          exclude_from_expense_calc: formData.exclude_from_expense_calc,
          exclude_from_cashflow_calc: formData.exclude_from_cashflow_calc,
        } as ClassificationCreate);

    onSave(dataToSave);
  };

  const handleCancel = () => {
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleCancel} maxWidth="sm" fullWidth>
      <DialogTitle>
        {isEditMode ? "Edit Classification Type" : "Create Classification Type"}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2, display: "flex", flexDirection: "column", gap: 2 }}>
          {error && <Alert severity="error">{error}</Alert>}

          <TextField
            label="Classification Name"
            value={formData.classification_name}
            onChange={(e) =>
              handleChange("classification_name", e.target.value)
            }
            error={!!errors.classification_name}
            helperText={
              errors.classification_name || "Display name (e.g., Refund/Return)"
            }
            required
            fullWidth
          />

          <TextField
            label="Classification Code"
            value={formData.classification_code}
            onChange={(e) => handleCodeChange(e.target.value)}
            error={!!errors.classification_code}
            helperText={
              errors.classification_code ||
              "Internal code (e.g., REFUND). Uppercase letters, numbers, and underscores only."
            }
            required
            fullWidth
            disabled={isEditMode} // Code cannot be changed when editing
          />

          <TextField
            label="Description"
            value={formData.description}
            onChange={(e) => handleChange("description", e.target.value)}
            helperText="Optional description of what this classification is for"
            multiline
            rows={2}
            fullWidth
          />

          <Box sx={{ mt: 1 }}>
            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.exclude_from_income_calc}
                    onChange={(e) =>
                      handleChange("exclude_from_income_calc", e.target.checked)
                    }
                  />
                }
                label="Exclude from Income Calculation"
              />
              <Tooltip title="When checked, transactions with this classification will not be counted as income in financial reports">
                <IconButton size="small">
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>

            <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.exclude_from_expense_calc}
                    onChange={(e) =>
                      handleChange(
                        "exclude_from_expense_calc",
                        e.target.checked
                      )
                    }
                  />
                }
                label="Exclude from Expense Calculation"
              />
              <Tooltip title="When checked, transactions with this classification will not be counted as expenses in financial reports">
                <IconButton size="small">
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>

            <Box sx={{ display: "flex", alignItems: "center" }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={formData.exclude_from_cashflow_calc}
                    onChange={(e) =>
                      handleChange(
                        "exclude_from_cashflow_calc",
                        e.target.checked
                      )
                    }
                  />
                }
                label="Exclude from Cash Flow Calculation"
              />
              <Tooltip title="When checked, transactions with this classification will not be counted in cash flow calculations">
                <IconButton size="small">
                  <InfoIcon fontSize="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel} disabled={isLoading}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={isLoading}
        >
          {isLoading ? "Saving..." : isEditMode ? "Save Changes" : "Create"}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ClassificationTypeDialog;
