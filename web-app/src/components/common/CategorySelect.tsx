import { useState } from "react";
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  CircularProgress,
} from "@mui/material";
import type { SxProps, Theme } from "@mui/material";
import { useCategories, useCreateCategory } from "../../hooks/useCategories";

interface CategorySelectProps {
  value: number | null;
  onChange: (categoryId: number | null) => void;
  label?: string;
  noneLabel?: string;
  fullWidth?: boolean;
  sx?: SxProps<Theme>;
}

/**
 * Shared category dropdown with inline "Create New Category" capability.
 * Self-contained: fetches its own category list and manages the creation dialog.
 *
 * Usage:
 *   <CategorySelect value={categoryId} onChange={(id) => setCategoryId(id)} />
 *
 * With react-hook-form Controller:
 *   render={({ field }) => (
 *     <CategorySelect
 *       value={field.value || null}
 *       onChange={(id) => field.onChange(id ?? "")}
 *     />
 *   )}
 */
export default function CategorySelect({
  value,
  onChange,
  label = "Category",
  noneLabel = "None",
  fullWidth = true,
  sx,
}: CategorySelectProps) {
  const { data: categoriesData } = useCategories();
  const createCategory = useCreateCategory();

  const [dialogOpen, setDialogOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newType, setNewType] = useState<"Income" | "Expense" | "Transfer">("Expense");

  const handleCreate = async () => {
    try {
      const created = await createCategory.mutateAsync({
        category_name: newName.trim(),
        category_type: newType,
      });
      onChange(created.category_id);
      setDialogOpen(false);
      setNewName("");
    } catch {
      // mutation error is handled by the hook (snackbar etc.)
    }
  };

  return (
    <>
      <FormControl fullWidth={fullWidth} sx={sx}>
        <InputLabel>{label}</InputLabel>
        <Select
          value={value ?? ""}
          label={label}
          onChange={(e) => {
            const v = e.target.value;
            if (v === "__create__") return; // handled by MenuItem onClick
            onChange(v === "" ? null : Number(v));
          }}
        >
          <MenuItem value="">{noneLabel}</MenuItem>
          {categoriesData?.categories?.map((cat) => (
            <MenuItem key={cat.category_id} value={cat.category_id}>
              {cat.category_name}
            </MenuItem>
          ))}
          <MenuItem
            value="__create__"
            onClick={(e) => {
              e.stopPropagation();
              setDialogOpen(true);
            }}
            sx={{
              borderTop: 1,
              borderColor: "divider",
              fontStyle: "italic",
              color: "primary.main",
            }}
          >
            + Create New Category
          </MenuItem>
        </Select>
      </FormControl>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle>Create New Category</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            fullWidth
            label="Category Name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && newName.trim() && handleCreate()}
            sx={{ mt: 1, mb: 2 }}
          />
          <FormControl fullWidth>
            <InputLabel>Type</InputLabel>
            <Select
              value={newType}
              label="Type"
              onChange={(e) => setNewType(e.target.value as "Income" | "Expense" | "Transfer")}
            >
              <MenuItem value="Expense">Expense</MenuItem>
              <MenuItem value="Income">Income</MenuItem>
              <MenuItem value="Transfer">Transfer</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => { setDialogOpen(false); setNewName(""); }}>Cancel</Button>
          <Button
            variant="contained"
            disabled={!newName.trim() || createCategory.isPending}
            onClick={handleCreate}
          >
            {createCategory.isPending ? <CircularProgress size={20} /> : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
