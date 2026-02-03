/**
 * API Keys Management Component
 * UI for managing API keys used by MCP server clients (Claude, Gemini, ChatGPT)
 */

import { useState } from "react";
import {
  Box,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Chip,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Snackbar,
  Tabs,
  Tab,
  Card,
  CardContent,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  ContentCopy as CopyIcon,
  Key as KeyIcon,
  Check as CheckIcon,
  Warning as WarningIcon,
} from "@mui/icons-material";
import {
  useApiKeys,
  useCreateApiKey,
  useRevokeApiKey,
} from "../../hooks/useApiKeys";
import type { APIKey, APIKeyCreated } from "../../types/auth";
import { MCP_CLIENTS, generateMCPConfig } from "../../types/auth";

export default function APIKeysManagement() {
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [keyName, setKeyName] = useState("");
  const [newlyCreatedKey, setNewlyCreatedKey] = useState<APIKeyCreated | null>(
    null
  );
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [keyToDelete, setKeyToDelete] = useState<APIKey | null>(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [configTab, setConfigTab] = useState(0);

  // Queries and mutations
  const { data, isLoading, error } = useApiKeys();
  const createMutation = useCreateApiKey();
  const revokeMutation = useRevokeApiKey();

  const handleOpenCreateDialog = () => {
    setKeyName("");
    setNewlyCreatedKey(null);
    setCreateDialogOpen(true);
  };

  const handleCloseCreateDialog = () => {
    setCreateDialogOpen(false);
    setKeyName("");
    setNewlyCreatedKey(null);
  };

  const handleCreateKey = async () => {
    if (!keyName.trim()) return;

    try {
      const result = await createMutation.mutateAsync({ name: keyName.trim() });
      setNewlyCreatedKey(result);
    } catch (err) {
      console.error("Failed to create API key:", err);
      showSnackbar("Failed to create API key");
    }
  };

  const handleOpenDeleteDialog = (key: APIKey) => {
    setKeyToDelete(key);
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
    setKeyToDelete(null);
  };

  const handleRevokeKey = async () => {
    if (!keyToDelete) return;

    try {
      await revokeMutation.mutateAsync({ keyId: keyToDelete.key_id });
      handleCloseDeleteDialog();
      showSnackbar("API key revoked successfully");
    } catch (err) {
      console.error("Failed to revoke API key:", err);
      showSnackbar("Failed to revoke API key");
    }
  };

  const copyToClipboard = async (text: string, label: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showSnackbar(`${label} copied to clipboard`);
    } catch (err) {
      console.error("Failed to copy:", err);
      showSnackbar("Failed to copy to clipboard");
    }
  };

  const showSnackbar = (message: string) => {
    setSnackbarMessage(message);
    setSnackbarOpen(true);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "-";
    return new Date(dateString).toLocaleString();
  };

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
        Failed to load API keys:{" "}
        {error instanceof Error ? error.message : "Unknown error"}
      </Alert>
    );
  }

  const keys = data?.keys || [];

  return (
    <Box>
      {/* Header */}
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={3}
      >
        <Box>
          <Typography variant="h6">API Keys</Typography>
          <Typography variant="body2" color="text.secondary">
            Manage API keys for MCP server integration with AI assistants
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleOpenCreateDialog}
        >
          Generate New Key
        </Button>
      </Box>

      {/* Info Alert */}
      <Alert severity="info" sx={{ mb: 3 }}>
        API keys allow AI assistants (Claude, Gemini, ChatGPT) to securely
        access your financial data through the MCP server. Keep your keys
        secure and never share them publicly.
      </Alert>

      {/* Keys Table */}
      {keys.length === 0 ? (
        <Paper sx={{ p: 4, textAlign: "center" }}>
          <KeyIcon sx={{ fontSize: 48, color: "text.disabled", mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No API Keys
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Generate your first API key to enable AI assistant integration
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleOpenCreateDialog}
          >
            Generate New Key
          </Button>
        </Paper>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Key Prefix</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Last Used</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {keys.map((key) => (
                <TableRow key={key.key_id}>
                  <TableCell>
                    <Box display="flex" alignItems="center" gap={1}>
                      <KeyIcon fontSize="small" color="action" />
                      <Typography variant="body2">{key.name}</Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <code style={{ fontSize: "0.85rem" }}>
                      {key.key_prefix}...
                    </code>
                  </TableCell>
                  <TableCell>
                    {key.is_active ? (
                      <Chip
                        icon={<CheckIcon />}
                        label="Active"
                        size="small"
                        color="success"
                      />
                    ) : (
                      <Chip
                        icon={<WarningIcon />}
                        label="Revoked"
                        size="small"
                        color="error"
                      />
                    )}
                  </TableCell>
                  <TableCell>{formatDate(key.created_at)}</TableCell>
                  <TableCell>{formatDate(key.last_used_at)}</TableCell>
                  <TableCell align="right">
                    {key.is_active && (
                      <Tooltip title="Revoke key">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleOpenDeleteDialog(key)}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      </Tooltip>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Create Key Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={handleCloseCreateDialog}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {newlyCreatedKey ? "API Key Created" : "Generate New API Key"}
        </DialogTitle>
        <DialogContent>
          {!newlyCreatedKey ? (
            <Box mt={1}>
              <TextField
                label="Key Name"
                placeholder="e.g., Claude Desktop"
                value={keyName}
                onChange={(e) => setKeyName(e.target.value)}
                fullWidth
                autoFocus
                helperText="A descriptive name to identify this key"
              />
            </Box>
          ) : (
            <Box>
              {/* Key Display */}
              <Alert severity="warning" sx={{ mb: 3 }}>
                <Typography variant="body2" fontWeight="bold">
                  Save this key now - it won't be shown again!
                </Typography>
              </Alert>

              <Card variant="outlined" sx={{ mb: 3 }}>
                <CardContent>
                  <Box
                    display="flex"
                    alignItems="center"
                    justifyContent="space-between"
                    gap={2}
                  >
                    <Box flex={1} overflow="hidden">
                      <Typography variant="caption" color="text.secondary">
                        API Key
                      </Typography>
                      <Typography
                        variant="body1"
                        fontFamily="monospace"
                        sx={{
                          wordBreak: "break-all",
                          backgroundColor: "action.hover",
                          p: 1,
                          borderRadius: 1,
                          mt: 0.5,
                        }}
                      >
                        {newlyCreatedKey.key}
                      </Typography>
                    </Box>
                    <IconButton
                      onClick={() =>
                        copyToClipboard(newlyCreatedKey.key, "API key")
                      }
                      color="primary"
                    >
                      <CopyIcon />
                    </IconButton>
                  </Box>
                </CardContent>
              </Card>

              {/* Configuration Examples */}
              <Typography variant="subtitle2" gutterBottom>
                Configuration Examples
              </Typography>
              <Typography variant="body2" color="text.secondary" mb={2}>
                Copy the configuration for your preferred AI assistant:
              </Typography>

              <Tabs
                value={configTab}
                onChange={(_, newValue) => setConfigTab(newValue)}
                sx={{ borderBottom: 1, borderColor: "divider" }}
              >
                {MCP_CLIENTS.map((client) => (
                  <Tab key={client.type} label={client.displayName} />
                ))}
              </Tabs>

              {MCP_CLIENTS.map((client, idx) => (
                <Box
                  key={client.type}
                  hidden={configTab !== idx}
                  sx={{ mt: 2 }}
                >
                  {configTab === idx && (
                    <Box>
                      <Box
                        display="flex"
                        justifyContent="space-between"
                        alignItems="center"
                        mb={1}
                      >
                        <Typography variant="caption" color="text.secondary">
                          {client.displayName} Configuration
                        </Typography>
                        <Button
                          size="small"
                          startIcon={<CopyIcon />}
                          onClick={() =>
                            copyToClipboard(
                              generateMCPConfig(client.type, newlyCreatedKey.key),
                              `${client.displayName} config`
                            )
                          }
                        >
                          Copy Config
                        </Button>
                      </Box>
                      <Paper
                        variant="outlined"
                        sx={{
                          p: 2,
                          backgroundColor: "grey.900",
                          overflow: "auto",
                          maxHeight: 200,
                        }}
                      >
                        <Typography
                          component="pre"
                          variant="body2"
                          fontFamily="monospace"
                          sx={{
                            color: "grey.100",
                            margin: 0,
                            whiteSpace: "pre-wrap",
                            wordBreak: "break-all",
                          }}
                        >
                          {generateMCPConfig(client.type, newlyCreatedKey.key)}
                        </Typography>
                      </Paper>
                    </Box>
                  )}
                </Box>
              ))}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          {!newlyCreatedKey ? (
            <>
              <Button onClick={handleCloseCreateDialog}>Cancel</Button>
              <Button
                onClick={handleCreateKey}
                variant="contained"
                disabled={!keyName.trim() || createMutation.isPending}
              >
                {createMutation.isPending ? (
                  <CircularProgress size={20} />
                ) : (
                  "Generate Key"
                )}
              </Button>
            </>
          ) : (
            <Button onClick={handleCloseCreateDialog} variant="contained">
              Done
            </Button>
          )}
        </DialogActions>
      </Dialog>

      {/* Revoke Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onClose={handleCloseDeleteDialog}>
        <DialogTitle>Revoke API Key</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to revoke "{keyToDelete?.name}"?
          </Typography>
          <Alert severity="warning" sx={{ mt: 2 }}>
            Any AI assistants using this key will lose access to your financial
            data. This action cannot be undone.
          </Alert>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>Cancel</Button>
          <Button
            onClick={handleRevokeKey}
            color="error"
            variant="contained"
            disabled={revokeMutation.isPending}
          >
            {revokeMutation.isPending ? (
              <CircularProgress size={20} />
            ) : (
              "Revoke Key"
            )}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={() => setSnackbarOpen(false)}
        message={snackbarMessage}
      />
    </Box>
  );
}
