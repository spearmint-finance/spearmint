import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import { useSnackbar } from "notistack";
import {
  useEntities,
  useCreateEntity,
  useUpdateEntity,
  useDeleteEntity,
} from "../../hooks/useEntities";
import { ENTITY_TYPE_LABELS } from "../../types/entity";
import type { EntityCreate } from "../../types/entity";

interface ManageEntitiesDialogProps {
  open: boolean;
  onClose: () => void;
}

const ENTITY_TYPES = [
  { value: "personal", label: "Personal" },
  { value: "business", label: "Business" },
  { value: "rental_property", label: "Rental Property" },
  { value: "side_hustle", label: "Side Hustle" },
] as const;

const ManageEntitiesDialog: React.FC<ManageEntitiesDialogProps> = ({
  open,
  onClose,
}) => {
  const { data: entities = [] } = useEntities();
  const createMutation = useCreateEntity();
  const updateMutation = useUpdateEntity();
  const deleteMutation = useDeleteEntity();
  const { enqueueSnackbar } = useSnackbar();

  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [formData, setFormData] = useState<EntityCreate>({
    entity_name: "",
    entity_type: "business",
    tax_id: "",
    address: "",
    notes: "",
  });

  const resetForm = () => {
    setFormData({
      entity_name: "",
      entity_type: "business",
      tax_id: "",
      address: "",
      notes: "",
    });
    setShowCreateForm(false);
    setEditingId(null);
  };

  const handleCreate = async () => {
    if (!formData.entity_name.trim()) {
      enqueueSnackbar("Entity name is required", { variant: "error" });
      return;
    }
    try {
      await createMutation.mutateAsync(formData);
      enqueueSnackbar(`Created "${formData.entity_name}"`, {
        variant: "success",
      });
      resetForm();
    } catch (err: any) {
      enqueueSnackbar(err.message || "Failed to create entity", {
        variant: "error",
      });
    }
  };

  const handleUpdate = async () => {
    if (!editingId || !formData.entity_name.trim()) return;
    try {
      await updateMutation.mutateAsync({
        id: editingId,
        data: {
          entity_name: formData.entity_name,
          entity_type: formData.entity_type,
          tax_id: formData.tax_id || undefined,
          address: formData.address || undefined,
          notes: formData.notes || undefined,
        },
      });
      enqueueSnackbar("Entity updated", { variant: "success" });
      resetForm();
    } catch (err: any) {
      enqueueSnackbar(err.message || "Failed to update", { variant: "error" });
    }
  };

  const handleDelete = async (id: number, name: string) => {
    try {
      await deleteMutation.mutateAsync(id);
      enqueueSnackbar(`Deleted "${name}"`, { variant: "success" });
    } catch (err: any) {
      enqueueSnackbar(err.message || "Failed to delete", { variant: "error" });
    }
  };

  const startEdit = (entity: any) => {
    setEditingId(entity.entity_id);
    setFormData({
      entity_name: entity.entity_name,
      entity_type: entity.entity_type,
      tax_id: entity.tax_id || "",
      address: entity.address || "",
      notes: entity.notes || "",
    });
    setShowCreateForm(true);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Manage Entities</DialogTitle>
      <DialogContent>
        {entities.length === 0 ? (
          <Alert severity="info" sx={{ mb: 2 }}>
            No entities yet. Create one to separate your finances by business,
            rental property, or personal use.
          </Alert>
        ) : (
          <List dense>
            {entities.map((entity) => (
              <ListItem key={entity.entity_id} divider>
                <ListItemText
                  primary={
                    <Box
                      sx={{ display: "flex", alignItems: "center", gap: 1 }}
                    >
                      {entity.entity_name}
                      {entity.is_default && (
                        <Chip label="Default" size="small" color="primary" />
                      )}
                    </Box>
                  }
                  secondary={
                    <>
                      {ENTITY_TYPE_LABELS[entity.entity_type] ||
                        entity.entity_type}
                      {entity.account_count > 0 &&
                        ` \u00B7 ${entity.account_count} account${entity.account_count !== 1 ? "s" : ""}`}
                      {entity.tax_id && ` \u00B7 EIN: ${entity.tax_id}`}
                    </>
                  }
                />
                <ListItemSecondaryAction>
                  <IconButton
                    size="small"
                    onClick={() => startEdit(entity)}
                  >
                    <EditIcon fontSize="small" />
                  </IconButton>
                  {!entity.is_default && (
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() =>
                        handleDelete(entity.entity_id, entity.entity_name)
                      }
                      disabled={entity.account_count > 0}
                    >
                      <DeleteIcon fontSize="small" />
                    </IconButton>
                  )}
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        )}

        {showCreateForm ? (
          <Box sx={{ mt: 2, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
            <Typography variant="subtitle2" gutterBottom>
              {editingId ? "Edit Entity" : "New Entity"}
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={8}>
                <TextField
                  fullWidth
                  label="Name"
                  size="small"
                  value={formData.entity_name}
                  onChange={(e) =>
                    setFormData({ ...formData, entity_name: e.target.value })
                  }
                  placeholder="e.g. Acme LLC, 123 Main St"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth size="small">
                  <InputLabel>Type</InputLabel>
                  <Select
                    value={formData.entity_type}
                    label="Type"
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        entity_type: e.target.value as any,
                      })
                    }
                  >
                    {ENTITY_TYPES.map((t) => (
                      <MenuItem key={t.value} value={t.value}>
                        {t.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              {formData.entity_type === "business" && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Tax ID (EIN)"
                    size="small"
                    value={formData.tax_id || ""}
                    onChange={(e) =>
                      setFormData({ ...formData, tax_id: e.target.value })
                    }
                    placeholder="12-3456789"
                  />
                </Grid>
              )}
              {formData.entity_type === "rental_property" && (
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Property Address"
                    size="small"
                    value={formData.address || ""}
                    onChange={(e) =>
                      setFormData({ ...formData, address: e.target.value })
                    }
                    placeholder="123 Main St, Austin TX 78701"
                  />
                </Grid>
              )}
              <Grid item xs={12}>
                <Box sx={{ display: "flex", gap: 1, justifyContent: "flex-end" }}>
                  <Button size="small" onClick={resetForm}>
                    Cancel
                  </Button>
                  <Button
                    size="small"
                    variant="contained"
                    onClick={editingId ? handleUpdate : handleCreate}
                    disabled={
                      createMutation.isPending || updateMutation.isPending
                    }
                  >
                    {editingId ? "Save" : "Create"}
                  </Button>
                </Box>
              </Grid>
            </Grid>
          </Box>
        ) : (
          <Box sx={{ mt: 2 }}>
            <Button
              startIcon={<AddIcon />}
              onClick={() => setShowCreateForm(true)}
              variant="outlined"
              fullWidth
            >
              Add Entity
            </Button>
          </Box>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default ManageEntitiesDialog;
