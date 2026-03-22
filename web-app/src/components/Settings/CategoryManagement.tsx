/**
 * Category Management Component
 * Editable grid for managing categories with tabs for categories and rules
 */

import { useState, useMemo } from "react";
import {
  Box,
  Button,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  IconButton,
  Tabs,
  Tab,
  Paper,
  InputAdornment,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Folder as FolderIcon,
  FolderOpen as FolderOpenIcon,
  Rule as RuleIcon,
  Category as CategoryIcon,
  Search as SearchIcon,
} from "@mui/icons-material";
import {
  DataGrid,
  GridColDef,
  GridRenderCellParams,
} from "@mui/x-data-grid";
import {
  useCategories,
  useCreateCategory,
  useUpdateCategory,
  useDeleteCategory,
} from "../../hooks/useCategories";
import { useEntities } from "../../hooks/useEntities";
import type { Category, CategoryCreate } from "../../types/settings";
import CategoryRulesList from "./CategoryRulesList";

interface CategoryFormData {
  category_name: string;
  category_type: "Income" | "Expense" | "Both" | "Transfer";
  parent_category_id: number | null;
  description: string;
  entity_id: number | null;
}

const emptyFormData: CategoryFormData = {
  category_name: "",
  category_type: "Expense",
  parent_category_id: null,
  description: "",
  entity_id: null,
};

export default function CategoryManagement() {
  const [currentTab, setCurrentTab] = useState(0);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);
  const [formData, setFormData] = useState<CategoryFormData>(emptyFormData);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [categoryToDelete, setCategoryToDelete] = useState<Category | null>(
    null
  );
  const [searchText, setSearchText] = useState("");
  const [typeFilter, setTypeFilter] = useState<string>("All");
  const [entityFilter, setEntityFilter] = useState<string>("All");

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  // Queries and mutations
  const { data, isLoading, error } = useCategories();
  const { data: entities = [] } = useEntities();
  const createMutation = useCreateCategory();
  const updateMutation = useUpdateCategory();
  const deleteMutation = useDeleteCategory();

  const handleOpenDialog = (category?: Category) => {
    if (category) {
      setEditingCategory(category);
      setFormData({
        category_name: category.category_name,
        category_type: category.category_type,
        parent_category_id: category.parent_category_id,
        description: category.description || "",
        entity_id: category.entity_id ?? null,
      });
    } else {
      setEditingCategory(null);
      setFormData(emptyFormData);
    }
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setEditingCategory(null);
    setFormData(emptyFormData);
  };

  const handleSubmit = async () => {
    try {
      if (editingCategory) {
        await updateMutation.mutateAsync({
          categoryId: editingCategory.category_id,
          category: formData,
        });
      } else {
        await createMutation.mutateAsync(formData as CategoryCreate);
      }
      handleCloseDialog();
    } catch (err) {
      console.error("Failed to save category:", err);
    }
  };

  const handleOpenDeleteDialog = (category: Category) => {
    setCategoryToDelete(category);
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
    setCategoryToDelete(null);
  };

  const handleDelete = async (force: boolean = false) => {
    if (!categoryToDelete) return;

    try {
      await deleteMutation.mutateAsync({
        categoryId: categoryToDelete.category_id,
        force,
      });
      handleCloseDeleteDialog();
    } catch (err) {
      console.error("Failed to delete category:", err);
    }
  };

  const categories = data?.categories || [];
  const parentCategories = categories.filter((c) => !c.parent_category_id);

  // Filter categories by search text, type, and entity
  const filteredCategories = useMemo(() => {
    let result = categories;
    if (searchText.trim()) {
      const lower = searchText.toLowerCase();
      result = result.filter((c) =>
        c.category_name.toLowerCase().includes(lower) ||
        (c.description && c.description.toLowerCase().includes(lower))
      );
    }
    if (typeFilter !== "All") {
      result = result.filter((c) => c.category_type === typeFilter);
    }
    if (entityFilter === "Global") {
      result = result.filter((c) => !c.entity_id);
    } else if (entityFilter !== "All") {
      const entityId = parseInt(entityFilter, 10);
      result = result.filter((c) => c.entity_id === entityId);
    }
    // Sort hierarchically: parents first (sorted), then children under each parent
    const roots = result.filter((c) => !c.parent_category_id);
    const children = result.filter((c) => c.parent_category_id);
    roots.sort((a, b) => a.category_name.localeCompare(b.category_name));
    const sorted: typeof result = [];
    for (const root of roots) {
      sorted.push(root);
      const kids = children
        .filter((c) => c.parent_category_id === root.category_id)
        .sort((a, b) => a.category_name.localeCompare(b.category_name));
      sorted.push(...kids);
    }
    // Add orphan children (parent filtered out)
    const placed = new Set(sorted.map((c) => c.category_id));
    for (const child of children) {
      if (!placed.has(child.category_id)) sorted.push(child);
    }
    return sorted;
  }, [categories, searchText, typeFilter, entityFilter]);

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Failed to load categories:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </Alert>
    );
  }

  // Define DataGrid columns
  const columns: GridColDef[] = [
    {
      field: "category_name",
      headerName: "Name",
      flex: 1,
      minWidth: 200,
      editable: true,
      renderCell: (params: GridRenderCellParams) => (
        <Box display="flex" alignItems="center" gap={1} sx={params.row.parent_category_id ? { pl: 3 } : {}}>
          {params.row.parent_category_id ? (
            <FolderIcon fontSize="small" color="action" />
          ) : (
            <FolderOpenIcon fontSize="small" color="primary" />
          )}
          {params.value}
        </Box>
      ),
    },
    {
      field: "category_type",
      headerName: "Type",
      width: 120,
      editable: true,
      type: "singleSelect",
      valueOptions: ["Income", "Expense", "Both", "Transfer"],
      renderCell: (params: GridRenderCellParams) => (
        <Chip
          label={params.value}
          size="small"
          color={
            params.value === "Income"
              ? "success"
              : params.value === "Expense"
              ? "error"
              : params.value === "Transfer"
              ? "info"
              : "default"
          }
        />
      ),
    },
    {
      field: "parent_category_id",
      headerName: "Parent",
      width: 150,
      editable: true,
      type: "singleSelect",
      valueOptions: [
        { value: null, label: "None" },
        ...parentCategories.map((cat) => ({
          value: cat.category_id,
          label: cat.category_name,
        })),
      ],
      valueGetter: (params) => params || null,
      renderCell: (params: GridRenderCellParams) => {
        const parent = categories.find((c) => c.category_id === params.value);
        return parent?.category_name || "-";
      },
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1,
      minWidth: 150,
      editable: true,
      renderCell: (params: GridRenderCellParams) => (
        <Typography variant="body2" color="text.secondary" noWrap>
          {params.value || "-"}
        </Typography>
      ),
    },
    {
      field: "entity_id",
      headerName: "Entity",
      width: 150,
      renderCell: (params: GridRenderCellParams) => {
        if (!params.value) return <Chip label="Global" size="small" variant="outlined" />;
        const entity = entities.find((e) => e.entity_id === params.value);
        return entity ? (
          <Chip label={entity.entity_name} size="small" color="primary" variant="outlined" />
        ) : "-";
      },
    },
    {
      field: "transaction_count",
      headerName: "Txns",
      width: 80,
      type: "number",
      renderCell: (params: GridRenderCellParams) => {
        const count = params.value ?? 0;
        return (
          <Chip
            label={count}
            size="small"
            variant={count > 0 ? "filled" : "outlined"}
            color={count > 0 ? "default" : "default"}
          />
        );
      },
    },
    {
      field: "actions",
      headerName: "Actions",
      width: 110,
      sortable: false,
      filterable: false,
      renderCell: (params: GridRenderCellParams) => (
        <Box display="flex" gap={0.5}>
          <IconButton
            size="small"
            onClick={() => handleOpenDialog(params.row as Category)}
            title="Edit category"
            color="primary"
          >
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleOpenDeleteDialog(params.row as Category)}
            title="Delete category"
            color="error"
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Box>
      ),
    },
  ];

  // Handle cell edit
  const handleProcessRowUpdate = async (newRow: Category, oldRow: Category) => {
    try {
      await updateMutation.mutateAsync({
        categoryId: newRow.category_id,
        category: {
          category_name: newRow.category_name,
          category_type: newRow.category_type,
          parent_category_id: newRow.parent_category_id,
          description: newRow.description,
          entity_id: newRow.entity_id ?? null,
        },
      });
      return newRow;
    } catch (error) {
      console.error("Failed to update category:", error);
      return oldRow; // Revert on error
    }
  };

  return (
    <Box>
      <Paper sx={{ width: "100%" }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="category management tabs"
          sx={{ borderBottom: 1, borderColor: "divider" }}
        >
          <Tab icon={<CategoryIcon />} label="Categories" />
          <Tab icon={<RuleIcon />} label="Category Rules" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Categories Tab */}
          {currentTab === 0 && (
            <Box>
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                mb={3}
              >
                <Typography variant="h6">Category Management</Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => handleOpenDialog()}
                >
                  Add Category
                </Button>
              </Box>

              <Box display="flex" gap={2} mb={2}>
                <TextField
                  size="small"
                  placeholder="Search categories..."
                  value={searchText}
                  onChange={(e) => setSearchText(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon fontSize="small" />
                      </InputAdornment>
                    ),
                  }}
                  sx={{ flex: 1, maxWidth: 400 }}
                />
                <TextField
                  select
                  size="small"
                  label="Type"
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                  sx={{ minWidth: 130 }}
                >
                  <MenuItem value="All">All Types</MenuItem>
                  <MenuItem value="Income">Income</MenuItem>
                  <MenuItem value="Expense">Expense</MenuItem>
                  <MenuItem value="Both">Both</MenuItem>
                  <MenuItem value="Transfer">Transfer</MenuItem>
                </TextField>
                {entities.length > 0 && (
                  <TextField
                    select
                    size="small"
                    label="Entity"
                    value={entityFilter}
                    onChange={(e) => setEntityFilter(e.target.value)}
                    sx={{ minWidth: 150 }}
                  >
                    <MenuItem value="All">All Entities</MenuItem>
                    <MenuItem value="Global">Global Only</MenuItem>
                    {entities.map((entity) => (
                      <MenuItem key={entity.entity_id} value={String(entity.entity_id)}>
                        {entity.entity_name}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
                <Typography variant="body2" color="text.secondary" alignSelf="center">
                  {filteredCategories.length} of {categories.length}
                </Typography>
              </Box>

              <Box sx={{ height: 600, width: "100%" }}>
                <DataGrid
                  rows={filteredCategories}
                  columns={columns}
                  getRowId={(row) => row.category_id}
                  processRowUpdate={handleProcessRowUpdate}
                  onProcessRowUpdateError={(error) =>
                    console.error("Row update error:", error)
                  }
                  pageSizeOptions={[10, 25, 50, 100]}
                  initialState={{
                    pagination: { paginationModel: { pageSize: 25 } },
                  }}
                  disableRowSelectionOnClick
                  sx={{
                    "& .MuiDataGrid-cell:focus": {
                      outline: "none",
                    },
                    "& .MuiDataGrid-cell:focus-within": {
                      outline: "2px solid #1976d2",
                      outlineOffset: "-1px",
                    },
                  }}
                />
              </Box>
            </Box>
          )}

          {/* Category Rules Tab */}
          {currentTab === 1 && <CategoryRulesList />}
        </Box>
      </Paper>

      {/* Create/Edit Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editingCategory ? "Edit Category" : "Create Category"}
        </DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} mt={1}>
            <TextField
              label="Category Name"
              value={formData.category_name}
              onChange={(e) =>
                setFormData({ ...formData, category_name: e.target.value })
              }
              required
              fullWidth
            />

            <TextField
              select
              label="Category Type"
              value={formData.category_type}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  category_type: e.target.value as
                    | "Income"
                    | "Expense"
                    | "Both"
                    | "Transfer",
                })
              }
              required
              fullWidth
            >
              <MenuItem value="Income">Income</MenuItem>
              <MenuItem value="Expense">Expense</MenuItem>
              <MenuItem value="Transfer">Transfer</MenuItem>
            </TextField>

            <TextField
              select
              label="Parent Category"
              value={formData.parent_category_id || ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  parent_category_id: e.target.value
                    ? Number(e.target.value)
                    : null,
                })
              }
              fullWidth
            >
              <MenuItem value="">None (Root Category)</MenuItem>
              {parentCategories.map((cat) => (
                <MenuItem key={cat.category_id} value={cat.category_id}>
                  {cat.category_name}
                </MenuItem>
              ))}
            </TextField>

            <TextField
              label="Description"
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              multiline
              rows={3}
              fullWidth
            />

            <TextField
              select
              label="Entity"
              value={formData.entity_id ?? ""}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  entity_id: e.target.value ? Number(e.target.value) : null,
                })
              }
              fullWidth
              helperText="Global categories are shared across all entities"
            >
              <MenuItem value="">Global (all entities)</MenuItem>
              {entities.map((entity) => (
                <MenuItem key={entity.entity_id} value={entity.entity_id}>
                  {entity.entity_name}
                </MenuItem>
              ))}
            </TextField>

          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSubmit}
            variant="contained"
            disabled={
              !formData.category_name ||
              createMutation.isPending ||
              updateMutation.isPending
            }
          >
            {editingCategory ? "Update" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={handleCloseDeleteDialog}>
        <DialogTitle>Delete Category</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{categoryToDelete?.category_name}"?
          </Typography>
          <Alert severity="warning" sx={{ mt: 2 }}>
            This action cannot be undone. If this category has transactions or
            child categories, you'll need to force delete.
          </Alert>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>Cancel</Button>
          <Button onClick={() => handleDelete(false)} color="error">
            Delete
          </Button>
          <Button
            onClick={() => handleDelete(true)}
            color="error"
            variant="contained"
          >
            Force Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
