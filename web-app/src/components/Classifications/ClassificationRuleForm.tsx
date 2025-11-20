/**
 * Classification Rule Form Component
 * Dialog for creating/editing classification rules
 */

import { useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Switch,
  Grid,
  Alert,
  Box,
  Typography,
} from "@mui/material";
import {
  useCreateClassificationRule,
  useUpdateClassificationRule,
  useClassifications,
  useTestClassificationRule,
} from "../../hooks/useClassifications";
import type {
  ClassificationRule,
  ClassificationRuleFormData,
} from "../../types/classification";

interface ClassificationRuleFormProps {
  open: boolean;
  onClose: () => void;
  rule?: ClassificationRule | null;
}

function ClassificationRuleForm({
  open,
  onClose,
  rule,
}: ClassificationRuleFormProps) {
  const isEditing = !!rule;

  const { data: classificationsData } = useClassifications();
  const createRuleMutation = useCreateClassificationRule();
  const updateRuleMutation = useUpdateClassificationRule();
  const testRuleMutation = useTestClassificationRule();

  const {
    control,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<ClassificationRuleFormData>({
    defaultValues: {
      rule_name: "",
      rule_priority: 100,
      classification_id: "" as any,
      is_active: true,
      description_pattern: "",
      category_pattern: "",
      source_pattern: "",
      amount_min: "",
      amount_max: "",
      payment_method_pattern: "",
      transaction_type_filter: "both", // Added: Income, Expense, or Both
    },
  });

  // Reset form when rule changes
  useEffect(() => {
    if (rule) {
      // Determine transaction type from amount ranges
      let transactionTypeFilter = "both";
      let amountMinDisplay = "";
      let amountMaxDisplay = "";

      // Check if this is an expense rule (negative amounts)
      if (
        rule.amount_min !== null &&
        rule.amount_min !== undefined &&
        rule.amount_min < 0
      ) {
        transactionTypeFilter = "expense";
        // For expenses: backend stores min as more negative, max as less negative
        // Convert back to positive user-friendly values

        // If min and max are equal, it means "exactly this amount" - convert to just minimum
        if (rule.amount_min === rule.amount_max) {
          amountMinDisplay = Math.abs(rule.amount_min).toString();
          amountMaxDisplay = ""; // Clear max to mean "at least"
        } else {
          if (rule.amount_max !== null && rule.amount_max !== undefined) {
            amountMinDisplay = Math.abs(rule.amount_max).toString(); // Max becomes Min
          }
          if (
            rule.amount_min !== null &&
            rule.amount_min !== undefined &&
            rule.amount_min !== -Infinity
          ) {
            amountMaxDisplay = Math.abs(rule.amount_min).toString(); // Min becomes Max
          }
        }
      }
      // Check if this is an income rule (positive amounts)
      else if (
        rule.amount_min !== null &&
        rule.amount_min !== undefined &&
        rule.amount_min >= 0
      ) {
        transactionTypeFilter = "income";
        amountMinDisplay = rule.amount_min.toString();
        if (rule.amount_max !== null && rule.amount_max !== undefined) {
          amountMaxDisplay = rule.amount_max.toString();
        }
      }
      // If only max is set, check its sign
      else if (rule.amount_max !== null && rule.amount_max !== undefined) {
        if (rule.amount_max < 0) {
          transactionTypeFilter = "expense";
          amountMinDisplay = Math.abs(rule.amount_max).toString();
        } else {
          transactionTypeFilter = "income";
          amountMaxDisplay = rule.amount_max.toString();
        }
      }

      reset({
        rule_name: rule.rule_name,
        rule_priority: rule.rule_priority,
        classification_id: rule.classification_id,
        is_active: rule.is_active,
        description_pattern: rule.description_pattern || "",
        category_pattern: rule.category_pattern || "",
        source_pattern: rule.source_pattern || "",
        amount_min: amountMinDisplay,
        amount_max: amountMaxDisplay,
        payment_method_pattern: rule.payment_method_pattern || "",
        transaction_type_filter: transactionTypeFilter,
      });
    } else {
      reset({
        rule_name: "",
        rule_priority: 100,
        classification_id: "" as any,
        is_active: true,
        description_pattern: "",
        category_pattern: "",
        source_pattern: "",
        amount_min: "",
        amount_max: "",
        payment_method_pattern: "",
        transaction_type_filter: "both",
      });
    }
  }, [rule, reset]);

  // Handle form submission
  const onSubmit = async (data: ClassificationRuleFormData) => {
    try {
      // Convert amounts based on transaction type
      let amountMin: number | undefined = undefined;
      let amountMax: number | undefined = undefined;

      if (data.transaction_type_filter === "expense") {
        // For expenses, amounts are stored as negative
        if (data.amount_min) {
          amountMax = -parseFloat(data.amount_min); // Min expense becomes Max (less negative)
        }
        if (data.amount_max) {
          amountMin = -parseFloat(data.amount_max); // Max expense becomes Min (more negative)
        }
      } else if (data.transaction_type_filter === "income") {
        // For income, amounts are stored as positive
        if (data.amount_min) {
          amountMin = parseFloat(data.amount_min);
        }
        if (data.amount_max) {
          amountMax = parseFloat(data.amount_max);
        }
      }
      // For "both", don't set amount filters

      const ruleData = {
        rule_name: data.rule_name,
        rule_priority: data.rule_priority,
        classification_id: Number(data.classification_id),
        is_active: data.is_active,
        description_pattern: data.description_pattern || null,
        category_pattern: data.category_pattern || null,
        source_pattern: data.source_pattern || null,
        amount_min: amountMin,
        amount_max: amountMax,
        payment_method_pattern: data.payment_method_pattern || null,
      };

      if (isEditing && rule) {
        await updateRuleMutation.mutateAsync({
          id: rule.rule_id,
          data: ruleData,
        });
      } else {
        await createRuleMutation.mutateAsync(ruleData);
      }

      onClose();
    } catch (error) {
      console.error("Failed to save rule:", error);
    }
  };

  // Handle test rule
  const handleTestRule = async () => {
    const formData = watch();
    try {
      // Convert amounts based on transaction type (same logic as submit)
      let amountMin: number | undefined = undefined;
      let amountMax: number | undefined = undefined;

      if (formData.transaction_type_filter === "expense") {
        if (formData.amount_min) {
          amountMax = -parseFloat(formData.amount_min);
        }
        if (formData.amount_max) {
          amountMin = -parseFloat(formData.amount_max);
        }
      } else if (formData.transaction_type_filter === "income") {
        if (formData.amount_min) {
          amountMin = parseFloat(formData.amount_min);
        }
        if (formData.amount_max) {
          amountMax = parseFloat(formData.amount_max);
        }
      }

      const result = await testRuleMutation.mutateAsync({
        description_pattern: formData.description_pattern || undefined,
        category_pattern: formData.category_pattern || undefined,
        source_pattern: formData.source_pattern || undefined,
        amount_min: amountMin,
        amount_max: amountMax,
        payment_method_pattern: formData.payment_method_pattern || undefined,
      });

      alert(
        `This rule would match ${result.matching_transactions} transaction(s).`
      );
    } catch (error) {
      console.error("Failed to test rule:", error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>
          {isEditing
            ? "Edit Classification Rule"
            : "Create Classification Rule"}
        </DialogTitle>

        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Alert severity="info" sx={{ mb: 3 }}>
              Rules use SQL LIKE patterns. Use % as wildcard (e.g., %transfer%
              matches "Bank Transfer"). Leave fields empty to ignore them.
            </Alert>

            <Grid container spacing={2}>
              {/* Rule Name */}
              <Grid item xs={12} sm={8}>
                <Controller
                  name="rule_name"
                  control={control}
                  rules={{ required: "Rule name is required" }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Rule Name"
                      fullWidth
                      error={!!errors.rule_name}
                      helperText={errors.rule_name?.message}
                    />
                  )}
                />
              </Grid>

              {/* Priority */}
              <Grid item xs={12} sm={4}>
                <Controller
                  name="rule_priority"
                  control={control}
                  rules={{
                    required: "Priority is required",
                    min: { value: 1, message: "Priority must be at least 1" },
                  }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Priority"
                      type="number"
                      fullWidth
                      error={!!errors.rule_priority}
                      helperText={
                        errors.rule_priority?.message ||
                        "Lower = higher priority"
                      }
                    />
                  )}
                />
              </Grid>

              {/* Classification */}
              <Grid item xs={12}>
                <Controller
                  name="classification_id"
                  control={control}
                  rules={{ required: "Classification is required" }}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.classification_id}>
                      <InputLabel>Classification</InputLabel>
                      <Select {...field} label="Classification">
                        {classificationsData?.classifications.map((c) => (
                          <MenuItem
                            key={c.classification_id}
                            value={c.classification_id}
                          >
                            {c.classification_name} ({c.classification_code})
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>

              {/* Active Status */}
              <Grid item xs={12}>
                <Controller
                  name="is_active"
                  control={control}
                  render={({ field }) => (
                    <FormControlLabel
                      control={<Switch {...field} checked={field.value} />}
                      label="Active (rule will be applied automatically)"
                    />
                  )}
                />
              </Grid>

              {/* Pattern Fields */}
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
                  Pattern Matching (at least one pattern required)
                </Typography>
              </Grid>

              {/* Transaction Type Filter */}
              <Grid item xs={12}>
                <Controller
                  name="transaction_type_filter"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Transaction Type</InputLabel>
                      <Select {...field} label="Transaction Type">
                        <MenuItem value="both">
                          Both Income and Expense
                        </MenuItem>
                        <MenuItem value="income">Income Only</MenuItem>
                        <MenuItem value="expense">Expense Only</MenuItem>
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="description_pattern"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Description Pattern"
                      fullWidth
                      placeholder="%grocery%"
                      helperText="Match transaction description"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Controller
                  name="category_pattern"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Category Pattern"
                      fullWidth
                      placeholder="%food%"
                      helperText="Match category name"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Controller
                  name="source_pattern"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Source Pattern"
                      fullWidth
                      placeholder="%checking%"
                      helperText="Match source/account"
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Controller
                  name="amount_min"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Minimum Amount"
                      type="number"
                      fullWidth
                      placeholder="2000.00"
                      helperText="Enter positive amounts (e.g., 2000 means at least $2,000)"
                      disabled={watch("transaction_type_filter") === "both"}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <Controller
                  name="amount_max"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Maximum Amount"
                      type="number"
                      fullWidth
                      placeholder="10000.00"
                      helperText="Enter positive amounts (e.g., 10000 means up to $10,000)"
                      disabled={watch("transaction_type_filter") === "both"}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="payment_method_pattern"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Payment Method Pattern"
                      fullWidth
                      placeholder="%credit card%"
                      helperText="Match payment method"
                    />
                  )}
                />
              </Grid>
            </Grid>
          </Box>
        </DialogContent>

        <DialogActions>
          <Button
            onClick={handleTestRule}
            disabled={testRuleMutation.isPending}
          >
            Test Rule
          </Button>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" disabled={isSubmitting}>
            {isEditing ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}

export default ClassificationRuleForm;
