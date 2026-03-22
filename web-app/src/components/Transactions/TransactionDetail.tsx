import { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Chip,
  Divider,
  Grid,
  IconButton,
  Autocomplete,
  TextField,
  FormControlLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import CloseIcon from "@mui/icons-material/Close";
import LinkIcon from "@mui/icons-material/Link";
import LocalOfferIcon from "@mui/icons-material/LocalOffer";
import SaveIcon from "@mui/icons-material/Save";
import { useSnackbar } from "notistack";
import { useQuery } from "@tanstack/react-query";
import type { Transaction } from "../../types/transaction";
import { useDeleteTransaction, useUpdateTransaction } from "../../hooks/useTransactions";
import { useEntities } from "../../hooks/useEntities";
import { getAccounts } from "../../api/accounts";
import { formatCurrency, formatDate } from "../../utils/formatters";
import TransactionForm from "./TransactionForm";

// Default tag suggestions matching seed_tags.py
const DEFAULT_TAG_SUGGESTIONS = [
  "capital-expense",
  "tax-deductible",
  "recurring",
  "reimbursable",
  "exclude-from-income",
  "exclude-from-expenses",
];

interface TransactionDetailProps {
  open: boolean;
  onClose: () => void;
  transaction: Transaction | null;
}

function TransactionDetail({
  open,
  onClose,
  transaction,
}: TransactionDetailProps) {
  const { enqueueSnackbar } = useSnackbar();
  const deleteMutation = useDeleteTransaction();
  const updateMutation = useUpdateTransaction();
  const { data: entities = [] } = useEntities();
  const { data: accountsData } = useQuery({
    queryKey: ["accounts"],
    queryFn: () => getAccounts(),
  });
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [duplicateDialogOpen, setDuplicateDialogOpen] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [editingTags, setEditingTags] = useState(false);
  const [editedTags, setEditedTags] = useState<string[]>([]);

  const linkedAccount = transaction?.account_id && accountsData
    ? accountsData.find((a) => a.account_id === transaction.account_id)
    : null;

  if (!transaction) {
    return null;
  }

  const handleDelete = async () => {
    try {
      await deleteMutation.mutateAsync(transaction.id);
      enqueueSnackbar("Transaction deleted successfully", {
        variant: "success",
      });
      setDeleteConfirmOpen(false);
      onClose();
    } catch (error) {
      const detail = error instanceof Error ? error.message : '';
      enqueueSnackbar(detail ? `Failed to delete: ${detail}` : "Failed to delete transaction", { variant: "error" });
    }
  };

  const handleStartEditTags = () => {
    setEditedTags(transaction.tags || []);
    setEditingTags(true);
  };

  const handleSaveTags = async () => {
    try {
      await updateMutation.mutateAsync({
        id: transaction.id,
        data: { tag_names: editedTags },
      });
      enqueueSnackbar("Tags updated successfully", { variant: "success" });
      setEditingTags(false);
    } catch (error) {
      enqueueSnackbar("Failed to update tags", { variant: "error" });
    }
  };

  return (
    <>
      <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Typography variant="h6">Transaction Details</Typography>
            <IconButton onClick={onClose} size="small" aria-label="Close transaction details">
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            {/* Transaction Type */}
            <Grid item xs={12}>
              <Chip
                label={transaction.transaction_type}
                color={
                  transaction.transaction_type === "Income"
                    ? "success"
                    : "error"
                }
                size="medium"
              />
            </Grid>

            {/* Description */}
            <Grid item xs={12}>
              <Typography variant="caption" color="text.secondary">
                Description
              </Typography>
              <Typography variant="h6">{transaction.description}</Typography>
            </Grid>

            {/* Amount */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                Amount
              </Typography>
              <Typography
                variant="h5"
                color={
                  transaction.transaction_type === "Income"
                    ? "success.main"
                    : "error.main"
                }
              >
                {transaction.transaction_type === "Income" ? "+" : "-"}
                {formatCurrency(Math.abs(transaction.amount))}
              </Typography>
            </Grid>

            {/* Date */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                Date
              </Typography>
              <Typography variant="body1">
                {formatDate(transaction.date, "long")}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* Category */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                Category
              </Typography>
              <Typography variant="body1">
                {transaction.category_name || "Uncategorized"}
              </Typography>
            </Grid>

            {/* Account */}
            {linkedAccount && (
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" color="text.secondary">
                  Account
                </Typography>
                <Typography variant="body1">
                  {linkedAccount.account_name}
                  {linkedAccount.institution_name
                    ? ` (${linkedAccount.institution_name})`
                    : ""}
                </Typography>
              </Grid>
            )}

            {/* Source */}
            {transaction.source && (
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" color="text.secondary">
                  Source
                </Typography>
                <Typography variant="body1">{transaction.source}</Typography>
              </Grid>
            )}

            {/* Payment Method */}
            {transaction.payment_method && (
              <Grid item xs={12} sm={6}>
                <Typography variant="caption" color="text.secondary">
                  Payment Method
                </Typography>
                <Typography variant="body1">{transaction.payment_method}</Typography>
              </Grid>
            )}

            {/* Transfer Flag */}
            {transaction.is_transfer && (
              <Grid item xs={12} sm={6}>
                <Chip label="Transfer" size="small" color="info" variant="outlined" />
              </Grid>
            )}

            {/* Balance */}
            {transaction.balance !== undefined &&
              transaction.balance !== null && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="caption" color="text.secondary">
                    Balance After
                  </Typography>
                  <Typography variant="body1">
                    {formatCurrency(transaction.balance)}
                  </Typography>
                </Grid>
              )}

            {/* Related Transaction */}
            {transaction.related_transaction_id && (
              <Grid item xs={12}>
                <Divider sx={{ my: 1 }} />
                <Box
                  sx={{
                    p: 2,
                    bgcolor: "info.lighter",
                    borderRadius: 1,
                    border: "1px solid",
                    borderColor: "info.light",
                  }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      alignItems: "center",
                      gap: 1,
                      mb: 1,
                    }}
                  >
                    <LinkIcon fontSize="small" color="primary" />
                    <Typography variant="subtitle2" color="primary">
                      Linked Transaction
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    This transaction is linked to another transaction (e.g., transfer pair).
                  </Typography>
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ mt: 1, display: "block" }}
                  >
                    Related Transaction ID:{" "}
                    {transaction.related_transaction_id}
                  </Typography>
                </Box>
              </Grid>
            )}

            {/* Notes */}
            {transaction.notes && (
              <Grid item xs={12}>
                <Typography variant="caption" color="text.secondary">
                  Notes
                </Typography>
                <Typography variant="body2">{transaction.notes}</Typography>
              </Grid>
            )}

            {/* Splits */}
            {transaction.splits && transaction.splits.length > 0 && (
              <Grid item xs={12}>
                <Divider sx={{ my: 1 }} />
                <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: "block" }}>
                  Split into {transaction.splits.length} items
                </Typography>
                <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
                  {transaction.splits.map((split) => (
                    <Box
                      key={split.split_id}
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        p: 1,
                        border: "1px solid",
                        borderColor: "divider",
                        borderRadius: 1,
                      }}
                    >
                      <Box>
                        <Typography variant="body2">
                          {split.category_name || `Category #${split.category_id}`}
                        </Typography>
                        {split.description && (
                          <Typography variant="caption" color="text.secondary">
                            {split.description}
                          </Typography>
                        )}
                      </Box>
                      <Typography variant="body2" fontWeight="medium">
                        {formatCurrency(split.amount)}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              </Grid>
            )}

            {/* Entity Assignment */}
            {entities.length > 0 && (
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth size="small">
                  <InputLabel>Entity</InputLabel>
                  <Select
                    value={transaction.entity_id ?? ""}
                    label="Entity"
                    onChange={async (e) => {
                      const newEntityId = e.target.value === "" ? null : Number(e.target.value);
                      try {
                        await updateMutation.mutateAsync({
                          id: transaction.id,
                          data: { entity_id: newEntityId },
                        });
                        enqueueSnackbar("Entity updated", { variant: "success" });
                      } catch {
                        enqueueSnackbar("Failed to update entity", { variant: "error" });
                      }
                    }}
                    disabled={updateMutation.isPending}
                  >
                    <MenuItem value="">Inherit from account</MenuItem>
                    {entities.map((entity) => (
                      <MenuItem key={entity.entity_id} value={entity.entity_id}>
                        {entity.entity_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            )}

            {/* Properties */}
            <Grid item xs={12}>
              <Divider sx={{ my: 1 }} />
              <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: "block" }}>
                Properties
              </Typography>
              <Grid container spacing={0}>
                {([
                  { field: "is_capital_expense" as const, label: "Capital Expense" },
                  { field: "is_tax_deductible" as const, label: "Tax Deductible" },
                  { field: "is_recurring" as const, label: "Recurring" },
                  { field: "is_reimbursable" as const, label: "Reimbursable" },
                  { field: "exclude_from_income" as const, label: "Exclude from Income" },
                  { field: "exclude_from_expenses" as const, label: "Exclude from Expenses" },
                ] as const).map(({ field, label }) => (
                  <Grid item xs={6} sm={4} key={field}>
                    <FormControlLabel
                      control={
                        <Checkbox
                          size="small"
                          checked={!!transaction[field]}
                          onChange={async (e) => {
                            try {
                              await updateMutation.mutateAsync({
                                id: transaction.id,
                                data: { [field]: e.target.checked },
                              });
                              enqueueSnackbar(`${label} updated`, { variant: "success" });
                            } catch {
                              enqueueSnackbar(`Failed to update ${label}`, { variant: "error" });
                            }
                          }}
                          disabled={updateMutation.isPending}
                        />
                      }
                      label={<Typography variant="body2">{label}</Typography>}
                    />
                  </Grid>
                ))}
              </Grid>
            </Grid>

            {/* Tags */}
            <Grid item xs={12}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 0.5 }}>
                <Typography variant="caption" color="text.secondary">
                  Tags
                </Typography>
                {!editingTags && (
                  <IconButton
                    size="small"
                    onClick={handleStartEditTags}
                    aria-label="Edit tags"
                    sx={{ p: 0.25 }}
                  >
                    <LocalOfferIcon fontSize="small" sx={{ fontSize: 16 }} />
                  </IconButton>
                )}
              </Box>
              {editingTags ? (
                <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
                  <Autocomplete
                    multiple
                    freeSolo
                    options={DEFAULT_TAG_SUGGESTIONS.filter(
                      (tag) => !editedTags.includes(tag)
                    )}
                    value={editedTags}
                    onChange={(_event, newValue) => {
                      setEditedTags(newValue);
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
                        size="small"
                        placeholder="Add tags..."
                      />
                    )}
                  />
                  <Box sx={{ display: "flex", gap: 1 }}>
                    <Button
                      size="small"
                      variant="contained"
                      startIcon={<SaveIcon />}
                      onClick={handleSaveTags}
                      disabled={updateMutation.isPending}
                    >
                      Save
                    </Button>
                    <Button
                      size="small"
                      onClick={() => setEditingTags(false)}
                      disabled={updateMutation.isPending}
                    >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              ) : transaction.tags && transaction.tags.length > 0 ? (
                <Box
                  sx={{ display: "flex", gap: 1, flexWrap: "wrap", mt: 0.5 }}
                >
                  {transaction.tags.map((tag, index) => (
                    <Chip
                      key={index}
                      label={tag}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No tags
                </Typography>
              )}
            </Grid>

            {/* Metadata */}
            {transaction.created_at && (
              <Grid item xs={12}>
                <Divider sx={{ my: 1 }} />
                <Typography variant="caption" color="text.secondary">
                  Created: {formatDate(transaction.created_at, "long")}
                  {transaction.updated_at &&
                    transaction.updated_at !== transaction.created_at &&
                    ` • Updated: ${formatDate(transaction.updated_at, "long")}`}
                </Typography>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button
            startIcon={<DeleteIcon />}
            color="error"
            onClick={() => setDeleteConfirmOpen(true)}
          >
            Delete
          </Button>
          <Box sx={{ flex: 1 }} />
          <Button
            startIcon={<ContentCopyIcon />}
            onClick={() => setDuplicateDialogOpen(true)}
          >
            Duplicate
          </Button>
          <Button onClick={onClose}>Close</Button>
          <Button
            variant="contained"
            startIcon={<EditIcon />}
            onClick={() => setEditDialogOpen(true)}
          >
            Edit
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Dialog */}
      <TransactionForm
        open={editDialogOpen}
        onClose={() => setEditDialogOpen(false)}
        transaction={transaction}
        mode="edit"
      />

      {/* Duplicate Dialog */}
      <TransactionForm
        open={duplicateDialogOpen}
        onClose={() => setDuplicateDialogOpen(false)}
        mode="create"
        defaultTransaction={transaction}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteConfirmOpen}
        onClose={() => setDeleteConfirmOpen(false)}
        aria-labelledby="delete-transaction-dialog-title"
      >
        <DialogTitle id="delete-transaction-dialog-title">Confirm Delete</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete this transaction? This action cannot
            be undone.
          </Typography>
          <Box sx={{ mt: 2, p: 2, bgcolor: "grey.100", borderRadius: 1 }}>
            <Typography variant="body2" fontWeight="medium">
              {transaction.description}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {formatCurrency(transaction.amount)} •{" "}
              {formatDate(transaction.date)}
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            color="error"
            onClick={handleDelete}
            disabled={deleteMutation.isPending}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default TransactionDetail;
