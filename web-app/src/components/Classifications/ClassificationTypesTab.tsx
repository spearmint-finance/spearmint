/**
 * Classification Types Tab Component
 * Displays a table of all classification types with CRUD operations
 */

import { useState } from "react";
import {
  Box,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Alert,
  Typography,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import LockIcon from "@mui/icons-material/Lock";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import InfoIcon from "@mui/icons-material/Info";
import {
  useClassifications,
  useCreateClassification,
  useUpdateClassification,
  useDeleteClassification,
} from "../../hooks/useClassifications";
import ClassificationTypeDialog from "./ClassificationTypeDialog";
import type {
  Classification,
  ClassificationCreate,
  ClassificationUpdate,
} from "../../types/classification";

function ClassificationTypesTab() {
  const { data, isLoading, error } = useClassifications();
  const createMutation = useCreateClassification();
  const updateMutation = useUpdateClassification();
  const deleteMutation = useDeleteClassification();

  // Dialog states
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedClassification, setSelectedClassification] =
    useState<Classification | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [classificationToDelete, setClassificationToDelete] =
    useState<Classification | null>(null);

  // Error state for mutations
  const [mutationError, setMutationError] = useState<string | null>(null);

  const handleCreate = () => {
    setSelectedClassification(null);
    setMutationError(null);
    setDialogOpen(true);
  };

  const handleEdit = (classification: Classification) => {
    if (classification.is_system_classification) {
      return; // System classifications cannot be edited
    }
    setSelectedClassification(classification);
    setMutationError(null);
    setDialogOpen(true);
  };

  const handleSave = async (
    data: ClassificationCreate | ClassificationUpdate
  ) => {
    setMutationError(null);

    try {
      if (selectedClassification) {
        // Update existing classification
        await updateMutation.mutateAsync({
          id: selectedClassification.classification_id,
          data: data as ClassificationUpdate,
        });
      } else {
        // Create new classification
        await createMutation.mutateAsync(data as ClassificationCreate);
      }
      setDialogOpen(false);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || err.message || "An error occurred";
      setMutationError(errorMessage);
    }
  };

  const handleDeleteClick = (classification: Classification) => {
    if (classification.is_system_classification) {
      return; // System classifications cannot be deleted
    }
    setClassificationToDelete(classification);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!classificationToDelete) return;

    try {
      await deleteMutation.mutateAsync(
        classificationToDelete.classification_id
      );
      setDeleteDialogOpen(false);
      setClassificationToDelete(null);
    } catch (err: any) {
      const errorMessage =
        err.response?.data?.detail || err.message || "Failed to delete";
      setMutationError(errorMessage);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setClassificationToDelete(null);
  };

  if (isLoading) {
    return (
      <Box sx={{ p: 3, textAlign: "center" }}>
        <Typography>Loading classification types...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Failed to load classification types:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </Alert>
    );
  }

  const classifications = data?.classifications || [];

  return (
    <Box>
      {/* Header with info and action buttons */}
      <Box sx={{ mb: 3, display: "flex", alignItems: "center", gap: 2 }}>
        <Box sx={{ flex: 1 }}>
          <Alert severity="info" icon={<InfoIcon />}>
            Classification types control how transactions are treated in
            financial calculations. System classifications (marked with{" "}
            <LockIcon fontSize="small" sx={{ verticalAlign: "middle" }} />)
            cannot be modified.
          </Alert>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          New Type
        </Button>
      </Box>

      {/* Error message from mutations */}
      {mutationError && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setMutationError(null)}>
          {mutationError}
        </Alert>
      )}

      {/* Classifications table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Code</TableCell>
              <TableCell>Description</TableCell>
              <TableCell align="center">
                <Tooltip title="Include in Income Calculation">
                  <span>Income</span>
                </Tooltip>
              </TableCell>
              <TableCell align="center">
                <Tooltip title="Include in Expense Calculation">
                  <span>Expense</span>
                </Tooltip>
              </TableCell>
              <TableCell align="center">
                <Tooltip title="Include in Cash Flow Calculation">
                  <span>Cash Flow</span>
                </Tooltip>
              </TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {classifications.length === 0 ? (
              <TableRow>
                <TableCell colSpan={8} align="center">
                  <Typography color="text.secondary">
                    No classification types found
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              classifications.map((classification) => (
                <TableRow
                  key={classification.classification_id}
                  sx={{
                    "&:hover": {
                      backgroundColor: classification.is_system_classification
                        ? "action.hover"
                        : "action.selected",
                    },
                  }}
                >
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      {classification.is_system_classification && (
                        <LockIcon fontSize="small" color="action" />
                      )}
                      <Typography variant="body2">
                        {classification.classification_name}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontFamily: "monospace" }}>
                      {classification.classification_code}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Tooltip title={classification.description || ""} placement="top">
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                          maxWidth: 500,
                        }}
                      >
                        {classification.description || "—"}
                      </Typography>
                    </Tooltip>
                  </TableCell>
                  <TableCell align="center">
                    {!classification.exclude_from_income_calc ? (
                      <CheckCircleIcon color="success" fontSize="small" />
                    ) : (
                      <CancelIcon color="error" fontSize="small" />
                    )}
                  </TableCell>
                  <TableCell align="center">
                    {!classification.exclude_from_expense_calc ? (
                      <CheckCircleIcon color="success" fontSize="small" />
                    ) : (
                      <CancelIcon color="error" fontSize="small" />
                    )}
                  </TableCell>
                  <TableCell align="center">
                    {!classification.exclude_from_cashflow_calc ? (
                      <CheckCircleIcon color="success" fontSize="small" />
                    ) : (
                      <CancelIcon color="error" fontSize="small" />
                    )}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={
                        classification.is_system_classification
                          ? "System"
                          : "Custom"
                      }
                      size="small"
                      color={
                        classification.is_system_classification
                          ? "default"
                          : "primary"
                      }
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Tooltip
                      title={
                        classification.is_system_classification
                          ? "System classifications cannot be edited"
                          : "Edit classification"
                      }
                    >
                      <span>
                        <IconButton
                          size="small"
                          onClick={() => handleEdit(classification)}
                          disabled={classification.is_system_classification}
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </span>
                    </Tooltip>
                    <Tooltip
                      title={
                        classification.is_system_classification
                          ? "System classifications cannot be deleted"
                          : "Delete classification"
                      }
                    >
                      <span>
                        <IconButton
                          size="small"
                          onClick={() => handleDeleteClick(classification)}
                          disabled={classification.is_system_classification}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </span>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Create/Edit Dialog */}
      <ClassificationTypeDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSave={handleSave}
        classification={selectedClassification}
        isLoading={createMutation.isPending || updateMutation.isPending}
        error={mutationError}
      />

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={handleDeleteCancel}>
        <DialogTitle>Delete Classification Type</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the classification type "
            {classificationToDelete?.classification_name}"?
          </DialogContentText>
          <DialogContentText sx={{ mt: 2 }}>
            All transactions currently assigned to this classification will be
            automatically reassigned to "Regular Transaction".
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} disabled={deleteMutation.isPending}>
            Cancel
          </Button>
          <Button
            onClick={handleDeleteConfirm}
            color="error"
            variant="contained"
            disabled={deleteMutation.isPending}
          >
            {deleteMutation.isPending ? "Deleting..." : "Delete"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default ClassificationTypesTab;
