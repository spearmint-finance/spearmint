import { useEffect, useState } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Grid,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  Checkbox,
  CircularProgress,
  Box,
  Divider,
  Autocomplete,
  Chip,
  Typography,
  IconButton,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useSnackbar } from "notistack";
import type {
  Transaction,
  TransactionCreate,
  TransactionUpdate,
} from "../../types/transaction";
import {
  useCreateTransaction,
  useUpdateTransaction,
  useSetTransactionSplits,
} from "../../hooks/useTransactions";

import { useCategories, useCreateCategory } from "../../hooks/useCategories";
import { useQuery } from "@tanstack/react-query";
import { getAccounts } from "../../api/accounts";
import { useEntityContext } from "../../contexts/EntityContext";
import { useEntities } from "../../hooks/useEntities";

interface TransactionFormProps {
  open: boolean;
  onClose: () => void;
  transaction?: Transaction | null;
  mode: "create" | "edit";
}

// Default tag suggestions matching seed_tags.py
const DEFAULT_TAG_SUGGESTIONS = [
  "capital-expense",
  "tax-deductible",
  "recurring",
  "reimbursable",
  "exclude-from-income",
  "exclude-from-expenses",
];

interface SplitRow {
  amount: number;
  category_id: number;
  entity_id: string; // empty string = none
  description: string;
}

interface FormData {
  date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense";
  category_id: number; // Required field
  account_id: string; // Empty string = no account selected
  entity_id: string; // Empty string = inherit from account
  notes?: string;
  tags: string[];
  is_capital_expense: boolean;
  is_tax_deductible: boolean;
  is_recurring: boolean;
  is_reimbursable: boolean;
  exclude_from_income: boolean;
  exclude_from_expenses: boolean;
  splits: SplitRow[];
}

function TransactionForm({
  open,
  onClose,
  transaction,
  mode,
}: TransactionFormProps) {
  const { enqueueSnackbar } = useSnackbar();
  const createMutation = useCreateTransaction();
  const updateMutation = useUpdateTransaction();
  const setTransactionSplitsMutation = useSetTransactionSplits();
  const createCategoryMutation = useCreateCategory();
  const { selectedEntityId } = useEntityContext();
  const { data: entitiesData = [] } = useEntities();

  // Track the form's entity_id to filter categories by the transaction's entity, not the global selector
  const [formEntityId, setFormEntityId] = useState<number | undefined>(undefined);
  const categoryEntityId = formEntityId ?? selectedEntityId ?? undefined;
  const { data: categoriesData, isLoading: categoriesLoading, refetch: refetchCategories } =
    useCategories({ entity_id: categoryEntityId });
  const { data: accountsData } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts(),
  });

  // State for new category dialog
  const [newCategoryDialogOpen, setNewCategoryDialogOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryType, setNewCategoryType] = useState<"Income" | "Expense" | "Transfer">("Expense");
  const [newCategoryParentId, setNewCategoryParentId] = useState<number | null>(null);

  // Get today's date in local timezone (YYYY-MM-DD format)
  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const {
    control,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    defaultValues: {
      date: getTodayDate(),
      description: "",
      amount: 0,
      transaction_type: "Expense",
      category_id: "" as any, // Empty string for unselected state
      account_id: "",
      entity_id: "",
      notes: "",
      tags: [],
      is_capital_expense: false,
      is_tax_deductible: false,
      is_recurring: false,
      is_reimbursable: false,
      exclude_from_income: false,
      exclude_from_expenses: false,
      splits: [],
    },
  });

  // Watch the transaction type to set default category type
  const transactionType = watch("transaction_type");

  // Reset form when transaction changes
  useEffect(() => {
    if (transaction && mode === "edit") {
      // Use the transaction's entity_id to filter categories
      setFormEntityId(transaction.entity_id ?? undefined);
      reset({
        date: transaction.date,
        description: transaction.description,
        amount: Math.abs(transaction.amount),
        transaction_type: transaction.transaction_type === "Transfer" ? "Expense" : transaction.transaction_type,
        category_id: transaction.category_id,
        account_id: transaction.account_id ? String(transaction.account_id) : "",
        entity_id: transaction.entity_id ? String(transaction.entity_id) : "",
        notes: transaction.notes || "",
        tags: transaction.tags || [],
        is_capital_expense: !!transaction.is_capital_expense,
        is_tax_deductible: !!transaction.is_tax_deductible,
        is_recurring: !!transaction.is_recurring,
        is_reimbursable: !!transaction.is_reimbursable,
        exclude_from_income: !!transaction.exclude_from_income,
        exclude_from_expenses: !!transaction.exclude_from_expenses,
        splits: transaction.splits?.map(s => ({
          amount: s.amount,
          category_id: s.category_id ?? 0,
          entity_id: s.entity_id ? String(s.entity_id) : "",
          description: s.description ?? "",
        })) ?? [],
      });
    } else if (mode === "create") {
      setFormEntityId(selectedEntityId ?? undefined);
      reset({
        date: getTodayDate(),
        description: "",
        amount: 0,
        transaction_type: "Expense",
        category_id: "" as any, // Empty string for unselected state
        account_id: "",
        entity_id: selectedEntityId ? String(selectedEntityId) : "",
        notes: "",
        tags: [],
        is_capital_expense: false,
        is_tax_deductible: false,
        is_recurring: false,
        is_reimbursable: false,
        exclude_from_income: false,
        exclude_from_expenses: false,
        splits: [],
      });
    }
  }, [transaction, mode, reset]);

  const onSubmit = async (data: FormData) => {
    try {
      // Ensure category_id is a number (Material-UI select returns string)
      const categoryId =
        typeof data.category_id === "string"
          ? parseInt(data.category_id, 10)
          : data.category_id;

      // Validate category_id
      if (!categoryId || isNaN(categoryId) || categoryId <= 0) {
        enqueueSnackbar("Please select a valid category", {
          variant: "error",
        });
        return;
      }

      // Validate splits sum if splits exist
      if (data.splits.length > 0) {
        const splitSum = data.splits.reduce((sum, s) => sum + (Number(s.amount) || 0), 0);
        const parentAmount = Math.abs(Number(data.amount) || 0);
        if (Math.abs(splitSum - parentAmount) > 0.01) {
          enqueueSnackbar(
            `Splits sum (${splitSum.toFixed(2)}) doesn't match transaction amount (${parentAmount.toFixed(2)})`,
            { variant: "error" }
          );
          return;
        }
        // Validate each split has a category
        const missingCategory = data.splits.some(s => !s.category_id || s.category_id === 0);
        if (missingCategory) {
          enqueueSnackbar("Each split must have a category selected", { variant: "error" });
          return;
        }
      }

      const accountId = data.account_id ? parseInt(data.account_id, 10) : undefined;
      const entityId = data.entity_id ? parseInt(data.entity_id, 10) : null;

      if (mode === "create") {
        const createData: TransactionCreate = {
          date: data.date,
          description: data.description,
          amount: data.amount,
          transaction_type: data.transaction_type,
          category_id: categoryId,
          account_id: accountId,
          entity_id: entityId,
          notes: data.notes,
          tag_names: data.tags.length > 0 ? data.tags : undefined,
          is_capital_expense: data.is_capital_expense,
          is_tax_deductible: data.is_tax_deductible,
          is_recurring: data.is_recurring,
          is_reimbursable: data.is_reimbursable,
          exclude_from_income: data.exclude_from_income,
          exclude_from_expenses: data.exclude_from_expenses,
        };
        const created = await createMutation.mutateAsync(createData);
        if (data.splits.length > 0) {
          const splitData = data.splits.map(s => ({
            amount: s.amount,
            category_id: typeof s.category_id === 'string' ? parseInt(s.category_id, 10) : s.category_id,
            entity_id: s.entity_id ? parseInt(s.entity_id, 10) : null,
            description: s.description || undefined,
          }));
          await setTransactionSplitsMutation.mutateAsync({ id: created.id, splits: splitData });
        }
        enqueueSnackbar("Transaction created successfully", {
          variant: "success",
        });
      } else if (transaction) {
        const updateData: TransactionUpdate = {
          date: data.date,
          description: data.description,
          amount: data.amount,
          transaction_type: data.transaction_type,
          category_id: categoryId,
          account_id: accountId,
          entity_id: entityId,
          notes: data.notes,
          tag_names: data.tags,
          is_capital_expense: data.is_capital_expense,
          is_tax_deductible: data.is_tax_deductible,
          is_recurring: data.is_recurring,
          is_reimbursable: data.is_reimbursable,
          exclude_from_income: data.exclude_from_income,
          exclude_from_expenses: data.exclude_from_expenses,
        };
        await updateMutation.mutateAsync({
          id: transaction.id,
          data: updateData,
        });
        // Save splits separately via the splits endpoint
        const splitData = data.splits.map(s => ({
          amount: s.amount,
          category_id: typeof s.category_id === 'string' ? parseInt(s.category_id, 10) : s.category_id,
          entity_id: s.entity_id ? parseInt(s.entity_id, 10) : null,
          description: s.description || undefined,
        }));
        if (splitData.length > 0 || (transaction.splits && transaction.splits.length > 0)) {
          await setTransactionSplitsMutation.mutateAsync({ id: transaction.id, splits: splitData });
        }
        enqueueSnackbar("Transaction updated successfully", {
          variant: "success",
        });
      }
      onClose();
    } catch (error) {
      enqueueSnackbar(
        mode === "create"
          ? "Failed to create transaction"
          : "Failed to update transaction",
        { variant: "error" }
      );
    }
  };

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) {
      enqueueSnackbar("Please enter a category name", { variant: "warning" });
      return;
    }

    try {
      const newCategory = await createCategoryMutation.mutateAsync({
        category_name: newCategoryName,
        category_type: newCategoryType,
        entity_id: formEntityId ?? null,
        parent_category_id: newCategoryParentId,
      });

      // Refresh the categories list
      await refetchCategories();

      // Set the new category as selected in the form
      setValue("category_id", newCategory.category_id);

      // Close the dialog and reset
      setNewCategoryDialogOpen(false);
      setNewCategoryName("");
      setNewCategoryType("Expense");
      setNewCategoryParentId(null);

      enqueueSnackbar(`Category "${newCategoryName}" created successfully`, {
        variant: "success",
      });
    } catch (error) {
      enqueueSnackbar("Failed to create category", { variant: "error" });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {mode === "create" ? "Add New Transaction" : "Edit Transaction"}
      </DialogTitle>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          <Grid container spacing={2}>
            {/* Date */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="date"
                control={control}
                rules={{ required: "Date is required" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Date"
                    type="date"
                    fullWidth
                    error={!!errors.date}
                    helperText={errors.date?.message}
                    InputLabelProps={{ shrink: true }}
                  />
                )}
              />
            </Grid>

            {/* Transaction Type */}
            <Grid item xs={12} sm={6}>
              <FormControl component="fieldset">
                <FormLabel component="legend">Type</FormLabel>
                <Controller
                  name="transaction_type"
                  control={control}
                  render={({ field }) => (
                    <RadioGroup {...field} row>
                      <FormControlLabel
                        value="Income"
                        control={<Radio size="small" />}
                        label="Income"
                      />
                      <FormControlLabel
                        value="Expense"
                        control={<Radio size="small" />}
                        label="Expense"
                      />
                    </RadioGroup>
                  )}
                />
              </FormControl>
            </Grid>

            {/* Description */}
            <Grid item xs={12}>
              <Controller
                name="description"
                control={control}
                rules={{
                  required: "Description is required",
                  minLength: {
                    value: 3,
                    message: "Description must be at least 3 characters",
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Description"
                    fullWidth
                    error={!!errors.description}
                    helperText={errors.description?.message}
                  />
                )}
              />
            </Grid>

            {/* Amount */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="amount"
                control={control}
                rules={{
                  required: "Amount is required",
                  min: {
                    value: 0.01,
                    message: "Amount must be greater than 0",
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Amount"
                    type="number"
                    fullWidth
                    error={!!errors.amount}
                    helperText={errors.amount?.message}
                    inputProps={{ step: "0.01", min: "0" }}
                  />
                )}
              />
            </Grid>

            {/* Category */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="category_id"
                control={control}
                rules={{ required: "Category is required" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Category"
                    select
                    fullWidth
                    required
                    value={field.value || ""}
                    error={!!errors.category_id}
                    helperText={errors.category_id?.message}
                    disabled={categoriesLoading}
                    onChange={(e) => {
                      const value = e.target.value;
                      if (value === "CREATE_NEW") {
                        // Set default category type based on current transaction type
                        setNewCategoryType(transactionType || "Expense");
                        setNewCategoryDialogOpen(true);
                      } else {
                        field.onChange(value);
                      }
                    }}
                  >
                    <MenuItem value="">
                      <em>Select a category</em>
                    </MenuItem>
                    {categoriesLoading ? (
                      <MenuItem disabled>
                        <CircularProgress size={20} />
                      </MenuItem>
                    ) : (
                      [
                        ...(categoriesData?.categories
                          .filter((category) => {
                            // Filter categories by selected transaction type
                            if (transactionType === "Income") return category.category_type === "Income" || category.category_type === "Both" || category.category_type === "Transfer";
                            if (transactionType === "Expense") return category.category_type === "Expense" || category.category_type === "Both" || category.category_type === "Transfer";
                            return true;
                          })
                          .map((category) => (
                          <MenuItem
                            key={category.category_id}
                            value={category.category_id}
                          >
                            {category.category_name}
                          </MenuItem>
                        )) || []),
                        <Divider key="divider" />,
                        <MenuItem key="create-new" value="CREATE_NEW">
                          <Box sx={{ display: "flex", alignItems: "center", gap: 1, color: "primary.main", fontWeight: "medium" }}>
                            <AddIcon fontSize="small" />
                            Create New Category
                          </Box>
                        </MenuItem>
                      ]
                    )}
                  </TextField>
                )}
              />
            </Grid>

            {/* Account (optional) */}
            <Grid item xs={12}>
              <Controller
                name="account_id"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Account (optional)"
                    select
                    fullWidth
                    value={field.value || ""}
                  >
                    <MenuItem value="">
                      <em>No account</em>
                    </MenuItem>
                    {accountsData?.map((account) => (
                      <MenuItem
                        key={account.account_id}
                        value={String(account.account_id)}
                      >
                        {account.account_name}
                        {account.institution_name
                          ? ` (${account.institution_name})`
                          : ""}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>

            {/* Entity (optional) */}
            {entitiesData.length > 0 && (
              <Grid item xs={12} sm={6}>
                <Controller
                  name="entity_id"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Entity"
                      select
                      fullWidth
                      value={field.value || ""}
                      onChange={(e) => {
                        field.onChange(e);
                        const newEntityId = e.target.value ? parseInt(e.target.value, 10) : undefined;
                        setFormEntityId(newEntityId);
                      }}
                    >
                      <MenuItem value="">
                        <em>Inherit from account</em>
                      </MenuItem>
                      {entitiesData.map((entity) => (
                        <MenuItem
                          key={entity.entity_id}
                          value={String(entity.entity_id)}
                        >
                          {entity.entity_name}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
            )}

            {/* Notes */}
            <Grid item xs={12}>
              <Controller
                name="notes"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Notes"
                    fullWidth
                    multiline
                    rows={3}
                  />
                )}
              />
            </Grid>

            {/* Properties */}
            <Grid item xs={12}>
              <Divider sx={{ mb: 1 }} />
              <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: "block" }}>
                Properties
              </Typography>
              <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0 }}>
                {([
                  { name: "is_capital_expense" as const, label: "Capital Expense" },
                  { name: "is_tax_deductible" as const, label: "Tax Deductible" },
                  { name: "is_recurring" as const, label: "Recurring" },
                  { name: "is_reimbursable" as const, label: "Reimbursable" },
                  { name: "exclude_from_income" as const, label: "Exclude from Income" },
                  { name: "exclude_from_expenses" as const, label: "Exclude from Expenses" },
                ]).map(({ name, label }) => (
                  <Controller
                    key={name}
                    name={name}
                    control={control}
                    render={({ field }) => (
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={!!field.value}
                            onChange={(e) => field.onChange(e.target.checked)}
                            size="small"
                          />
                        }
                        label={label}
                        sx={{ minWidth: "50%" }}
                      />
                    )}
                  />
                ))}
              </Box>
            </Grid>

            {/* Splits */}
            <Grid item xs={12}>
              <Divider sx={{ mb: 1 }} />
              <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 1 }}>
                <Typography variant="caption" color="text.secondary">
                  Split Transaction
                </Typography>
                <Box sx={{ display: "flex", gap: 1 }}>
                  {(watch("splits") || []).length >= 2 && (
                    <Button
                      size="small"
                      onClick={() => {
                        const currentSplits = watch("splits") || [];
                        const parentAmount = Math.abs(Number(watch("amount")) || 0);
                        const count = currentSplits.length;
                        if (count === 0 || parentAmount === 0) return;
                        const evenAmount = Math.round((parentAmount / count) * 100) / 100;
                        const lastAmount = Math.round((parentAmount - evenAmount * (count - 1)) * 100) / 100;
                        const updated = currentSplits.map((s: SplitRow, i: number) => ({
                          ...s,
                          amount: i === count - 1 ? lastAmount : evenAmount,
                        }));
                        setValue("splits", updated);
                      }}
                    >
                      Split Evenly
                    </Button>
                  )}
                  <Button
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => {
                      const currentSplits = watch("splits") || [];
                      const parentAmount = Math.abs(Number(watch("amount")) || 0);
                      const usedAmount = currentSplits.reduce((sum: number, s: SplitRow) => sum + (Number(s.amount) || 0), 0);
                      const remaining = Math.round((parentAmount - usedAmount) * 100) / 100;
                      setValue("splits", [
                        ...currentSplits,
                        { amount: Math.max(0, remaining), category_id: 0, entity_id: "", description: "" }
                      ]);
                    }}
                  >
                    Add Split
                  </Button>
                </Box>
              </Box>
              <Controller
                name="splits"
                control={control}
                render={({ field }) => (
                  <Box>
                    {(field.value || []).length === 0 ? (
                      <Typography variant="caption" color="text.disabled" sx={{ fontStyle: "italic" }}>
                        No splits — transaction is a single line item
                      </Typography>
                    ) : (
                      <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                        {/* Split sum validation */}
                        {(() => {
                          const total = (field.value || []).reduce((sum: number, s: SplitRow) => sum + (Number(s.amount) || 0), 0);
                          const parentAmount = watch("amount") || 0;
                          const diff = Math.abs(total - Number(parentAmount));
                          return diff > 0.01 ? (
                            <Typography variant="caption" color="error">
                              Splits sum {total.toFixed(2)} ≠ transaction amount {Number(parentAmount).toFixed(2)}
                            </Typography>
                          ) : (
                            <Typography variant="caption" color="success.main">
                              Splits sum to {total.toFixed(2)} ✓
                            </Typography>
                          );
                        })()}
                        {(field.value || []).map((split: SplitRow, idx: number) => (
                          <Box key={idx} sx={{ display: "flex", gap: 1, alignItems: "flex-start", p: 1, border: "1px solid", borderColor: "divider", borderRadius: 1 }}>
                            <TextField
                              label="Amount"
                              type="number"
                              size="small"
                              value={split.amount || ""}
                              onChange={(e) => {
                                const updated = [...field.value];
                                updated[idx] = { ...updated[idx], amount: e.target.value === "" ? 0 : parseFloat(e.target.value) || 0 };
                                field.onChange(updated);
                              }}
                              inputProps={{ step: "0.01", min: "0" }}
                              sx={{ width: 110 }}
                            />
                            <TextField
                              label="Category"
                              select
                              size="small"
                              value={split.category_id || ""}
                              onChange={(e) => {
                                const updated = [...field.value];
                                updated[idx] = { ...updated[idx], category_id: parseInt(e.target.value, 10) || 0 };
                                field.onChange(updated);
                              }}
                              sx={{ flex: 1, minWidth: 120 }}
                              disabled={categoriesLoading}
                            >
                              <MenuItem value=""><em>Select</em></MenuItem>
                              {categoriesData?.categories.map((cat) => (
                                <MenuItem key={cat.category_id} value={cat.category_id}>
                                  {cat.category_name}
                                </MenuItem>
                              ))}
                            </TextField>
                            {entitiesData.length > 0 && (
                              <TextField
                                label="Entity"
                                select
                                size="small"
                                value={split.entity_id || ""}
                                onChange={(e) => {
                                  const updated = [...field.value];
                                  updated[idx] = { ...updated[idx], entity_id: e.target.value };
                                  field.onChange(updated);
                                }}
                                sx={{ width: 120 }}
                              >
                                <MenuItem value=""><em>None</em></MenuItem>
                                {entitiesData.map((entity) => (
                                  <MenuItem key={entity.entity_id} value={String(entity.entity_id)}>
                                    {entity.entity_name}
                                  </MenuItem>
                                ))}
                              </TextField>
                            )}
                            <TextField
                              label="Description"
                              size="small"
                              value={split.description || ""}
                              onChange={(e) => {
                                const updated = [...field.value];
                                updated[idx] = { ...updated[idx], description: e.target.value };
                                field.onChange(updated);
                              }}
                              sx={{ flex: 1 }}
                            />
                            <IconButton
                              size="small"
                              onClick={() => {
                                const updated = field.value.filter((_: SplitRow, i: number) => i !== idx);
                                field.onChange(updated);
                              }}
                              color="error"
                            >
                              ✕
                            </IconButton>
                          </Box>
                        ))}
                      </Box>
                    )}
                  </Box>
                )}
              />
            </Grid>

            {/* Tags */}
            <Grid item xs={12}>
              <Controller
                name="tags"
                control={control}
                render={({ field }) => (
                  <Autocomplete
                    multiple
                    freeSolo
                    options={DEFAULT_TAG_SUGGESTIONS.filter(
                      (tag) => !field.value.includes(tag)
                    )}
                    value={field.value}
                    onChange={(_event, newValue) => {
                      field.onChange(newValue);
                    }}
                    renderTags={(value, getTagProps) =>
                      value.map((option, index) => (
                        <Chip
                          variant="outlined"
                          label={option}
                          size="small"
                          {...getTagProps({ index })}
                          key={option}
                        />
                      ))
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Tags"
                        placeholder="Add tags..."
                        helperText="Select from suggestions or type to create new tags"
                      />
                    )}
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button type="submit" variant="contained" disabled={isSubmitting}>
            {mode === "create" ? "Create" : "Update"}
          </Button>
        </DialogActions>
      </form>

      {/* Create New Category Dialog */}
      <Dialog
        open={newCategoryDialogOpen}
        onClose={() => setNewCategoryDialogOpen(false)}
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle>Create New Category</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, pt: 1 }}>
            <TextField
              label="Category Name"
              fullWidth
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
              autoFocus
              required
            />
            <FormControl>
              <FormLabel>Category Type</FormLabel>
              <RadioGroup
                value={newCategoryType}
                onChange={(e) => setNewCategoryType(e.target.value as "Income" | "Expense" | "Transfer")}
              >
                <FormControlLabel
                  value="Income"
                  control={<Radio />}
                  label="Income"
                />
                <FormControlLabel
                  value="Expense"
                  control={<Radio />}
                  label="Expense"
                />
                <FormControlLabel
                  value="Transfer"
                  control={<Radio />}
                  label="Transfer (excluded from analysis)"
                />
              </RadioGroup>
            </FormControl>
            <TextField
              select
              label="Parent Category (optional)"
              fullWidth
              value={newCategoryParentId ?? ""}
              onChange={(e) => setNewCategoryParentId(e.target.value ? Number(e.target.value) : null)}
            >
              <MenuItem value="">
                <em>None (Root Category)</em>
              </MenuItem>
              {categoriesData?.categories
                .filter((c) => !c.parent_category_id)
                .map((cat) => (
                  <MenuItem key={cat.category_id} value={cat.category_id}>
                    {cat.category_name}
                  </MenuItem>
                ))}
            </TextField>
            {formEntityId && (
              <Typography variant="caption" color="text.secondary">
                This category will be scoped to{" "}
                <strong>{entitiesData.find((e) => e.entity_id === formEntityId)?.entity_name || "selected entity"}</strong>
              </Typography>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setNewCategoryDialogOpen(false);
            setNewCategoryName("");
            setNewCategoryType("Expense");
            setNewCategoryParentId(null);
          }}>
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleCreateCategory}
            disabled={!newCategoryName.trim() || createCategoryMutation.isPending}
          >
            {createCategoryMutation.isPending ? <CircularProgress size={20} /> : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </Dialog>
  );
}

export default TransactionForm;
