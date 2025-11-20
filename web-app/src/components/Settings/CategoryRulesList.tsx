/**
 * Category Rules List Component
 * Displays all category rules in a table with edit/delete actions
 */

import { useState } from "react";
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Chip,
  Typography,
  Tooltip,
  Alert,
  Button,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CancelIcon from "@mui/icons-material/Cancel";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import LoadingSpinner from "../common/LoadingSpinner";
import ErrorDisplay from "../common/ErrorDisplay";
import CategoryRuleForm from "./CategoryRuleForm";
import ApplyCategoryRulesDialog from "./ApplyCategoryRulesDialog";
import type { CategoryRule } from "../../types/settings";
import {
  useCategoryRules,
  useDeleteCategoryRule,
} from "../../hooks/useCategoryRules";
import { useCategories } from "../../hooks/useCategories";

function CategoryRulesList() {
  const [editingRule, setEditingRule] = useState<CategoryRule | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isApplyDialogOpen, setIsApplyDialogOpen] = useState(false);
  const [applyingRule, setApplyingRule] = useState<{
    id: number;
    name: string;
  } | null>(null);

  // Fetch rules and categories
  const {
    data: rulesData,
    isLoading: rulesLoading,
    error: rulesError,
    refetch: refetchRules,
  } = useCategoryRules();

  const { data: categoriesData } = useCategories();

  const deleteRuleMutation = useDeleteCategoryRule();

  // Get category name by ID
  const getCategoryName = (categoryId: number): string => {
    const category = categoriesData?.categories.find(
      (c) => c.category_id === categoryId
    );
    return category?.category_name || "Unknown";
  };

  // Handle edit rule
  const handleEdit = (rule: CategoryRule) => {
    setEditingRule(rule);
    setIsFormOpen(true);
  };

  // Handle delete rule
  const handleDelete = async (ruleId: number) => {
    if (window.confirm("Are you sure you want to delete this category rule?")) {
      try {
        await deleteRuleMutation.mutateAsync(ruleId);
      } catch (error) {
        console.error("Failed to delete rule:", error);
      }
    }
  };

  // Handle create new rule
  const handleCreateNew = () => {
    setEditingRule(null);
    setIsFormOpen(true);
  };

  // Handle form close
  const handleFormClose = () => {
    setIsFormOpen(false);
    setEditingRule(null);
  };

  // Handle apply single rule
  const handleApplyRule = (rule: CategoryRule) => {
    setApplyingRule({
      id: rule.rule_id,
      name: rule.rule_name,
    });
  };

  // Handle close apply dialog
  const handleCloseApplyDialog = () => {
    setIsApplyDialogOpen(false);
    setApplyingRule(null);
  };

  // Loading state
  if (rulesLoading) {
    return <LoadingSpinner message="Loading category rules..." />;
  }

  // Error state
  if (rulesError) {
    return (
      <ErrorDisplay
        message="Failed to load category rules"
        onRetry={refetchRules}
      />
    );
  }

  const rules = rulesData?.rules || [];

  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography variant="h6">Category Rules</Typography>
        <Box sx={{ display: "flex", gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<PlayArrowIcon />}
            onClick={() => setIsApplyDialogOpen(true)}
            disabled={rules.length === 0}
          >
            Apply Rules
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateNew}
          >
            Create Rule
          </Button>
        </Box>
      </Box>

      {/* Info Alert */}
      <Alert severity="info" sx={{ mb: 3 }}>
        Category rules automatically assign categories to transactions based on
        patterns. Rules are applied in priority order (lower number = higher
        priority).
      </Alert>

      {/* Rules Table */}
      {rules.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <Typography variant="body1" color="text.secondary">
            No category rules found. Create your first rule to get started.
          </Typography>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Priority</TableCell>
                <TableCell>Rule Name</TableCell>
                <TableCell>Category</TableCell>
                <TableCell>Patterns</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rules
                .sort((a, b) => a.rule_priority - b.rule_priority)
                .map((rule) => (
                  <TableRow key={rule.rule_id} hover>
                    <TableCell>
                      <Chip
                        label={rule.rule_priority}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {rule.rule_name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={getCategoryName(rule.category_id)}
                        size="small"
                        color="secondary"
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
                        {rule.description_pattern && (
                          <Tooltip
                            title={`Description: ${rule.description_pattern}`}
                          >
                            <Chip
                              label="Desc"
                              size="small"
                              variant="outlined"
                            />
                          </Tooltip>
                        )}
                        {rule.source_pattern && (
                          <Tooltip title={`Source: ${rule.source_pattern}`}>
                            <Chip label="Src" size="small" variant="outlined" />
                          </Tooltip>
                        )}
                        {(rule.amount_min !== null ||
                          rule.amount_max !== null) && (
                          <Tooltip
                            title={`Amount: ${rule.amount_min || "any"} - ${
                              rule.amount_max || "any"
                            }`}
                          >
                            <Chip label="Amt" size="small" variant="outlined" />
                          </Tooltip>
                        )}
                        {rule.payment_method_pattern && (
                          <Tooltip
                            title={`Payment: ${rule.payment_method_pattern}`}
                          >
                            <Chip label="Pay" size="small" variant="outlined" />
                          </Tooltip>
                        )}
                        {rule.transaction_type_pattern && (
                          <Tooltip
                            title={`Type: ${rule.transaction_type_pattern}`}
                          >
                            <Chip
                              label="Type"
                              size="small"
                              variant="outlined"
                            />
                          </Tooltip>
                        )}
                      </Box>
                    </TableCell>
                    <TableCell>
                      {rule.is_active ? (
                        <Chip
                          icon={<CheckCircleIcon />}
                          label="Active"
                          size="small"
                          color="success"
                        />
                      ) : (
                        <Chip
                          icon={<CancelIcon />}
                          label="Inactive"
                          size="small"
                          color="default"
                        />
                      )}
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title="Apply This Rule">
                        <IconButton
                          size="small"
                          onClick={() => handleApplyRule(rule)}
                          color="success"
                        >
                          <PlayArrowIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Edit Rule">
                        <IconButton
                          size="small"
                          onClick={() => handleEdit(rule)}
                          color="primary"
                        >
                          <EditIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete Rule">
                        <IconButton
                          size="small"
                          onClick={() => handleDelete(rule.rule_id)}
                          color="error"
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Rule Form Dialog */}
      <CategoryRuleForm
        open={isFormOpen}
        onClose={handleFormClose}
        rule={editingRule}
      />

      {/* Apply Rules Dialog */}
      <ApplyCategoryRulesDialog
        open={isApplyDialogOpen || applyingRule !== null}
        onClose={handleCloseApplyDialog}
        ruleId={applyingRule?.id}
        ruleName={applyingRule?.name}
      />
    </Box>
  );
}

export default CategoryRulesList;
