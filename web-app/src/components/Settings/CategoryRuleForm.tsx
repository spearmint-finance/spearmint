/**
 * Category Rule Form Component
 * Dialog for creating/editing category rules
 */

import { useEffect, useState } from "react";
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
import CategorySelect from "../common/CategorySelect";
import { useEntities } from "../../hooks/useEntities";
import { useQuery } from "@tanstack/react-query";
import { getAccounts } from "../../api/accounts";

interface CategoryRuleFormData {
  rule_name: string;
  rule_priority: number;
  category_id: number | "";
  entity_id: number | "";
  account_id: number | "";
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

  const { data: entities = [] } = useEntities();
  const createRuleMutation = useCreateCategoryRule();
  const updateRuleMutation = useUpdateCategoryRule();
  const testRuleMutation = useTestCategoryRule();
  const {
    control,
    handleSubmit,
    reset,
    watch,
    getValues,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<CategoryRuleFormData>({
    defaultValues: {
      rule_name: "",
      rule_priority: 100,
      category_id: "" as any,
      entity_id: "" as any,
      account_id: "" as any,
      is_active: true,
      description_pattern: "",
      source_pattern: "",
      amount_min: "",
      amount_max: "",
      payment_method_pattern: "",
      transaction_type_pattern: "",
    },
  });

  const { data: accountsData } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts(),
  });

  // Reset form when rule changes
  useEffect(() => {
    if (rule) {
      reset({
        rule_name: rule.rule_name,
        rule_priority: rule.rule_priority,
        category_id: rule.category_id || ("" as any),
        entity_id: rule.entity_id || ("" as any),
        account_id: (rule as any).account_id || ("" as any),
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
        entity_id: "" as any,
        account_id: "" as any,
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
  const [formError, setFormError] = useState<string | null>(null);

  const onSubmit = async (data: CategoryRuleFormData) => {
    setFormError(null);

    // Validate at least one assignment target
    if (!data.category_id && !data.entity_id) {
      setFormError("At least one of Category or Entity must be selected.");
      return;
    }

    // Validate at least one pattern is provided
    if (!data.description_pattern && !data.source_pattern && !data.payment_method_pattern
        && !data.amount_min && !data.amount_max && !data.transaction_type_pattern && !data.account_id) {
      setFormError("At least one matching pattern is required.");
      return;
    }

    // Validate amount range
    if (data.amount_min && data.amount_max && parseFloat(data.amount_min) > parseFloat(data.amount_max)) {
      setFormError("Minimum amount cannot be greater than maximum amount.");
      return;
    }

    try {
      const ruleData = {
        rule_name: data.rule_name,
        rule_priority: data.rule_priority,
        category_id: data.category_id ? Number(data.category_id) : null,
        entity_id: data.entity_id ? Number(data.entity_id) : null,
        account_id: data.account_id ? Number(data.account_id) : null,
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
      const detail = error instanceof Error ? error.message : 'Unknown error';
      setFormError(`Failed to save rule: ${detail}`);
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
    <>
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={(e) => e.preventDefault()}>
        <DialogTitle>
          {isEditing ? "Edit Transaction Rule" : "Create Transaction Rule"}
        </DialogTitle>

        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <Alert severity="info" sx={{ mb: 3 }}>
              Rules auto-assign a category and/or entity to matching transactions.
              Use % as wildcard in patterns (e.g., %walmart% matches "WALMART STORE").
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
                  rules={{ required: "Priority is required" }}
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

              {/* Assignment Targets */}
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Assignment (at least one required)
                </Typography>
              </Grid>

              {/* Category */}
              <Grid item xs={12} sm={6}>
                <Controller
                  name="category_id"
                  control={control}
                  render={({ field }) => (
                    <CategorySelect
                      value={field.value ? Number(field.value) : null}
                      onChange={(id) => field.onChange(id ?? "")}
                      label="Category"
                    />
                  )}
                />
              </Grid>

              {/* Entity */}
              <Grid item xs={12} sm={6}>
                <Controller
                  name="entity_id"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Entity</InputLabel>
                      <Select {...field} label="Entity">
                        <MenuItem value="">None</MenuItem>
                        {entities.map((e: any) => (
                          <MenuItem key={e.entity_id} value={e.entity_id}>
                            {e.entity_name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>

              {/* Account Filter */}
              <Grid item xs={12} sm={6}>
                <Controller
                  name="account_id"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth>
                      <InputLabel>Account</InputLabel>
                      <Select {...field} label="Account">
                        <MenuItem value="">Any account</MenuItem>
                        {(accountsData || []).map((a: any) => (
                          <MenuItem key={a.account_id} value={a.account_id}>
                            {a.account_name}{a.institution_name ? ` (${a.institution_name})` : ""}
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

        {formError && (
          <Alert severity="error" sx={{ mx: 3, mb: 1 }} onClose={() => setFormError(null)}>
            {formError}
          </Alert>
        )}

        <DialogActions>
          <Button
            onClick={handleTestRule}
            disabled={testRuleMutation.isPending}
          >
            Test Rule
          </Button>
          <Button onClick={onClose}>Cancel</Button>
          <Button
            variant="contained"
            disabled={isSubmitting}
            onClick={() => {
              const data = getValues();
              if (!data.rule_name?.trim()) {
                setFormError("Rule name is required.");
                return;
              }
              onSubmit(data);
            }}
          >
            {isEditing ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </form>
    </Dialog>

</>
  );
}

export default CategoryRuleForm;
