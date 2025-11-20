/**
 * Category Rule Form Component
 * Dialog for creating/editing category rules
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
import type { CategoryRule } from "../../types/settings";
import {
  useCreateCategoryRule,
  useUpdateCategoryRule,
  useTestCategoryRule,
} from "../../hooks/useCategoryRules";
import { useCategories } from "../../hooks/useCategories";

interface CategoryRuleFormData {
  rule_name: string;
  rule_priority: number;
  category_id: number | "";
  is_active: boolean;
  description_pattern: string;
  source_pattern: string;
  amount_min: string;
  amount_max: string;
  payment_method_pattern: string;
  transaction_type_pattern: "Income" | "Expense" | "";
}

interface CategoryRuleFormProps {
  open: boolean;
  onClose: () => void;
  rule?: CategoryRule | null;
}

function CategoryRuleForm({ open, onClose, rule }: CategoryRuleFormProps) {
  const isEditing = !!rule;

  const { data: categoriesData } = useCategories();
  const createRuleMutation = useCreateCategoryRule();
  const updateRuleMutation = useUpdateCategoryRule();
  const testRuleMutation = useTestCategoryRule();

  const {
    control,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<CategoryRuleFormData>({
    defaultValues: {
      rule_name: "",
      rule_priority: 100,
      category_id: "" as any,
      is_active: true,
      description_pattern: "",
      source_pattern: "",
      amount_min: "",
      amount_max: "",
      payment_method_pattern: "",
      transaction_type_pattern: "",
    },
  });

  // Reset form when rule changes
  useEffect(() => {
    if (rule) {
      reset({
        rule_name: rule.rule_name,
        rule_priority: rule.rule_priority,
        category_id: rule.category_id,
        is_active: rule.is_active,
        description_pattern: rule.description_pattern || "",
        source_pattern: rule.source_pattern || "",
        amount_min: rule.amount_min?.toString() || "",
        amount_max: rule.amount_max?.toString() || "",
        payment_method_pattern: rule.payment_method_pattern || "",
        transaction_type_pattern: rule.transaction_type_pattern || "",
      });
    } else {
      reset({
        rule_name: "",
        rule_priority: 100,
        category_id: "" as any,
        is_active: true,
        description_pattern: "",
        source_pattern: "",
        amount_min: "",
        amount_max: "",
        payment_method_pattern: "",
        transaction_type_pattern: "",
      });
    }
  }, [rule, reset]);

  // Handle form submission
  const onSubmit = async (data: CategoryRuleFormData) => {
    try {
      const ruleData = {
        rule_name: data.rule_name,
        rule_priority: data.rule_priority,
        category_id: Number(data.category_id),
        is_active: data.is_active,
        description_pattern: data.description_pattern || null,
        source_pattern: data.source_pattern || null,
        amount_min: data.amount_min ? parseFloat(data.amount_min) : null,
        amount_max: data.amount_max ? parseFloat(data.amount_max) : null,
        payment_method_pattern: data.payment_method_pattern || null,
        transaction_type_pattern: data.transaction_type_pattern || null,
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
      const result = await testRuleMutation.mutateAsync({
        description_pattern: formData.description_pattern || undefined,
        source_pattern: formData.source_pattern || undefined,
        amount_min: formData.amount_min
          ? parseFloat(formData.amount_min)
          : undefined,
        amount_max: formData.amount_max
          ? parseFloat(formData.amount_max)
          : undefined,
        payment_method_pattern: formData.payment_method_pattern || undefined,
        transaction_type_pattern:
          formData.transaction_type_pattern || undefined,
        limit: 10,
      });

      alert(
        `This rule would match ${result.total_matches} transaction(s).\n\n` +
          `Sample transactions:\n${result.sample_transactions
            .map(
              (t) => `- ${t.transaction_date}: ${t.description} ($${t.amount})`
            )
            .join("\n")}`
      );
    } catch (error) {
      console.error("Failed to test rule:", error);
      alert("Failed to test rule. Please check your patterns.");
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>
          {isEditing ? "Edit Category Rule" : "Create Category Rule"}
        </DialogTitle>

        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Alert severity="info" sx={{ mb: 3 }}>
              Rules use SQL LIKE patterns. Use % as wildcard (e.g., %walmart%
              matches "WALMART STORE"). Leave fields empty to ignore them.
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

              {/* Category */}
              <Grid item xs={12}>
                <Controller
                  name="category_id"
                  control={control}
                  rules={{ required: "Category is required" }}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.category_id}>
                      <InputLabel>Category</InputLabel>
                      <Select {...field} label="Category">
                        {categoriesData?.categories.map((c) => (
                          <MenuItem key={c.category_id} value={c.category_id}>
                            {c.category_name} ({c.category_type})
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

              {/* Transaction Type Pattern */}
              <Grid item xs={12}>
                <Controller
                  name="transaction_type_pattern"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Transaction Type</InputLabel>
                      <Select {...field} label="Transaction Type">
                        <MenuItem value="">Any</MenuItem>
                        <MenuItem value="Income">Income Only</MenuItem>
                        <MenuItem value="Expense">Expense Only</MenuItem>
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
                      placeholder="%walmart%"
                      helperText="Match transaction description"
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
                      placeholder="50.00"
                      helperText="Minimum transaction amount"
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
                      placeholder="500.00"
                      helperText="Maximum transaction amount"
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

export default CategoryRuleForm;
