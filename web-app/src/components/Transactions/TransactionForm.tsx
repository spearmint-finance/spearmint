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
  CircularProgress,
  Box,
  Divider,
  Autocomplete,
  Chip,
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

interface FormData {
  date: string;
  description: string;
  amount: number;
  transaction_type: "Income" | "Expense" | "Transfer";
  category_id: number; // Required field
  account_id: string; // Empty string = no account selected
  entity_id: string; // Empty string = inherit from account
  notes?: string;
  tags: string[];
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
  const createCategoryMutation = useCreateCategory();
  const { selectedEntityId } = useEntityContext();
  const { data: entitiesData = [] } = useEntities();
  const { data: categoriesData, isLoading: categoriesLoading, refetch: refetchCategories } =
    useCategories({ entity_id: selectedEntityId ?? undefined });
  const { data: accountsData } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts(),
  });

  // State for new category dialog
  const [newCategoryDialogOpen, setNewCategoryDialogOpen] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [newCategoryType, setNewCategoryType] = useState<"Income" | "Expense" | "Transfer">("Expense");

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
    },
  });

  // Watch the transaction type to set default category type
  const transactionType = watch("transaction_type");

  // Reset form when transaction changes
  useEffect(() => {
    if (transaction && mode === "edit") {
      reset({
        date: transaction.date,
        description: transaction.description,
        amount: Math.abs(transaction.amount),
        transaction_type: transaction.is_transfer ? "Transfer" : transaction.transaction_type,
        category_id: transaction.category_id,
        account_id: transaction.account_id ? String(transaction.account_id) : "",
        entity_id: transaction.entity_id ? String(transaction.entity_id) : "",
        notes: transaction.notes || "",
        tags: transaction.tags || [],
      });
    } else if (mode === "create") {
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
        };
        await createMutation.mutateAsync(createData);
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
        };
        await updateMutation.mutateAsync({
          id: transaction.id,
          data: updateData,
        });
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
      });

      // Refresh the categories list
      await refetchCategories();

      // Set the new category as selected in the form
      setValue("category_id", newCategory.category_id);

      // Close the dialog and reset
      setNewCategoryDialogOpen(false);
      setNewCategoryName("");
      setNewCategoryType("Expense");

      enqueueSnackbar(`Category "${newCategoryName}" created successfully`, {
        variant: "success",
      });
    } catch (error) {
      enqueueSnackbar("Failed to create category", { variant: "error" });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
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
                      <FormControlLabel
                        value="Transfer"
                        control={<Radio size="small" />}
                        label="Transfer"
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
                            if (transactionType === "Transfer") return category.category_type === "Transfer";
                            if (transactionType === "Income") return category.category_type === "Income" || category.category_type === "Both";
                            if (transactionType === "Expense") return category.category_type === "Expense" || category.category_type === "Both";
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
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setNewCategoryDialogOpen(false);
            setNewCategoryName("");
            setNewCategoryType("Expense");
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
