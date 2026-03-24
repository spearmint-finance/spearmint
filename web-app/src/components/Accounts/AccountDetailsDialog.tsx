import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Tabs,
  Tab,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Chip,
  IconButton,
  TextField,
  InputAdornment,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Checkbox,
  LinearProgress,
} from '@mui/material';
import {
  Delete as DeleteIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Close as CloseIcon,
  TrendingUp as TrendingUpIcon,
  AccountBalance as AccountBalanceIcon,
  History as HistoryIcon,
  CheckCircle as CheckCircleIcon,
  Receipt as ReceiptIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Account,
  AccountUpdate,
  getAccountTypeLabel,
  getAccountTypeIcon,
} from '../../types/account';
import {
  getBalanceHistory,
  getPortfolioSummary,
  getReconciliations,
  createReconciliation,
  completeReconciliation,
  addHolding,
  updateHolding,
  deleteHolding,
  addBalanceSnapshot,
  updateAccount,
  deleteAccount,
} from '../../api/accounts';
import { getTransactions } from '../../api/transactions';
import type { Transaction } from '../../types/transaction';
import type { Reconciliation } from '../../types/account';
import BalanceHistoryChart from './BalanceHistoryChart';
import { formatCurrency } from '../../utils/formatters';
import { useEntityContext } from '../../contexts/EntityContext';
import { ENTITY_TYPE_LABELS } from '../../types/entity';

interface AccountDetailsDialogProps {
  open: boolean;
  account: Account;
  onClose: () => void;
  onAccountUpdated: () => void;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`account-detail-tabpanel-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
}

const AccountDetailsDialog: React.FC<AccountDetailsDialogProps> = ({
  open,
  account,
  onClose,
  onAccountUpdated,
}) => {
  const navigate = useNavigate();
  const { entities } = useEntityContext();
  const acctCurrency = account?.currency || "USD";
  const [tabValue, setTabValue] = useState(0);
  const [showAddBalance, setShowAddBalance] = useState(false);
  const [newBalance, setNewBalance] = useState('');
  const [newBalanceDate, setNewBalanceDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
  const [showReconForm, setShowReconForm] = useState(false);
  const [reconDate, setReconDate] = useState(new Date().toISOString().split('T')[0]);
  const [reconBalance, setReconBalance] = useState('');
  const [showHoldingForm, setShowHoldingForm] = useState(false);
  const [editingHoldingId, setEditingHoldingId] = useState<number | null>(null);
  const [holdingForm, setHoldingForm] = useState({
    symbol: '',
    quantity: '',
    as_of_date: new Date().toISOString().split('T')[0],
    cost_basis: '',
    current_value: '',
  });
  const [activeRecon, setActiveRecon] = useState<Reconciliation | null>(null);
  const [clearedIds, setClearedIds] = useState<Set<number>>(new Set());
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    account_name: account.account_name,
    institution_name: account.institution_name || '',
    account_number_last4: account.account_number_last4 || '',
    notes: account.notes || '',
    entity_ids: account.entity_ids || [],
    is_active: account.is_active,
  });

  // Fetch balance history
  const { data: balanceHistory } = useQuery({
    queryKey: ['balanceHistory', account.account_id],
    queryFn: () => getBalanceHistory(account.account_id),
    enabled: open && tabValue === 1,
  });

  // Fetch portfolio if it's an investment account
  const { data: portfolio } = useQuery({
    queryKey: ['portfolio', account.account_id],
    queryFn: () => getPortfolioSummary(account.account_id),
    enabled: open && account.has_investment_component && tabValue === 2,
  });

  // Fetch reconciliations
  const { data: reconciliations } = useQuery({
    queryKey: ['reconciliations', account.account_id],
    queryFn: () => getReconciliations(account.account_id),
    enabled: open && tabValue === 3,
  });

  // Fetch account transactions for reconciliation clearing
  const { data: reconTransactions, isLoading: reconTxLoading } = useQuery({
    queryKey: ['reconTransactions', account.account_id, activeRecon?.statement_date],
    queryFn: () =>
      getTransactions({
        account_id: account.account_id,
        end_date: activeRecon!.statement_date,
        limit: 1000,
        sort_by: 'transaction_date',
        sort_order: 'desc',
      }),
    enabled: !!activeRecon,
  });

  // Compute running cleared balance
  const clearedBalance = useMemo(() => {
    if (!reconTransactions?.transactions) return 0;
    return reconTransactions.transactions
      .filter((t: Transaction) => clearedIds.has(t.id))
      .reduce((sum: number, t: Transaction) => {
        return sum + (t.transaction_type === 'Income' ? t.amount : -t.amount);
      }, account.opening_balance || 0);
  }, [reconTransactions, clearedIds, account.opening_balance]);

  const discrepancy = activeRecon
    ? activeRecon.statement_balance - clearedBalance
    : 0;

  // Complete reconciliation mutation
  const completeReconMutation = useMutation({
    mutationFn: () =>
      completeReconciliation(activeRecon!.reconciliation_id, {
        reconciled_by: 'user',
        cleared_transaction_ids: Array.from(clearedIds),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reconciliations', account.account_id] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      setActiveRecon(null);
      setClearedIds(new Set());
    },
  });

  const handleToggleCleared = (txId: number) => {
    setClearedIds((prev) => {
      const next = new Set(prev);
      if (next.has(txId)) {
        next.delete(txId);
      } else {
        next.add(txId);
      }
      return next;
    });
  };

  const handleSelectAllCleared = () => {
    if (!reconTransactions?.transactions) return;
    const allIds = reconTransactions.transactions.map((t: Transaction) => t.id);
    setClearedIds(new Set(allIds));
  };

  const handleDeselectAllCleared = () => {
    setClearedIds(new Set());
  };

  const handleStartClearing = (recon: Reconciliation) => {
    setActiveRecon(recon);
    // Pre-select already-cleared transactions
    if (reconTransactions?.transactions) {
      const alreadyCleared = reconTransactions.transactions
        .filter((t: Transaction) => t.is_cleared)
        .map((t: Transaction) => t.id);
      setClearedIds(new Set(alreadyCleared));
    } else {
      setClearedIds(new Set());
    }
  };

  // Add balance mutation
  const addBalanceMutation = useMutation({
    mutationFn: (data: { balance: number; date: string }) =>
      addBalanceSnapshot(account.account_id, {
        balance_date: data.date,
        total_balance: data.balance,
        balance_type: 'statement',
      }),
    onSuccess: () => {
      onAccountUpdated();
      setShowAddBalance(false);
      setNewBalance('');
    },
  });

  // Update account mutation
  const updateAccountMutation = useMutation({
    mutationFn: (data: AccountUpdate) => updateAccount(account.account_id, data),
    onSuccess: () => {
      onAccountUpdated();
      setIsEditing(false);
    },
  });

  // Create reconciliation mutation
  const createReconMutation = useMutation({
    mutationFn: () =>
      createReconciliation(account.account_id, {
        statement_date: reconDate,
        statement_balance: parseFloat(reconBalance),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reconciliations', account.account_id] });
      setShowReconForm(false);
      setReconBalance('');
    },
  });

  // Add holding mutation
  const addHoldingMutation = useMutation({
    mutationFn: () =>
      addHolding(account.account_id, {
        symbol: holdingForm.symbol,
        quantity: parseFloat(holdingForm.quantity),
        as_of_date: holdingForm.as_of_date,
        cost_basis: holdingForm.cost_basis ? parseFloat(holdingForm.cost_basis) : undefined,
        current_value: holdingForm.current_value ? parseFloat(holdingForm.current_value) : undefined,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', account.account_id] });
      queryClient.invalidateQueries({ queryKey: ['holdings', account.account_id] });
      setShowHoldingForm(false);
      setHoldingForm({ symbol: '', quantity: '', as_of_date: new Date().toISOString().split('T')[0], cost_basis: '', current_value: '' });
    },
  });

  // Update holding mutation
  const updateHoldingMutation = useMutation({
    mutationFn: () =>
      updateHolding(editingHoldingId!, {
        symbol: holdingForm.symbol,
        quantity: parseFloat(holdingForm.quantity),
        as_of_date: holdingForm.as_of_date,
        cost_basis: holdingForm.cost_basis ? parseFloat(holdingForm.cost_basis) : null,
        current_value: holdingForm.current_value ? parseFloat(holdingForm.current_value) : null,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', account.account_id] });
      queryClient.invalidateQueries({ queryKey: ['holdings', account.account_id] });
      setShowHoldingForm(false);
      setEditingHoldingId(null);
      setHoldingForm({ symbol: '', quantity: '', as_of_date: new Date().toISOString().split('T')[0], cost_basis: '', current_value: '' });
    },
  });

  // Delete holding mutation
  const deleteHoldingMutation = useMutation({
    mutationFn: (holdingId: number) => deleteHolding(holdingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio', account.account_id] });
      queryClient.invalidateQueries({ queryKey: ['holdings', account.account_id] });
    },
  });

  // Delete account mutation
  const deleteAccountMutation = useMutation({
    mutationFn: () => deleteAccount(account.account_id),
    onSuccess: () => {
      onAccountUpdated();
      onClose();
    },
  });

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAddBalance = () => {
    const balance = parseFloat(newBalance);
    if (!isNaN(balance)) {
      addBalanceMutation.mutate({ balance, date: newBalanceDate });
    }
  };

  const handleStartEditing = () => {
    setEditForm({
      account_name: account.account_name,
      institution_name: account.institution_name || '',
      account_number_last4: account.account_number_last4 || '',
      notes: account.notes || '',
      entity_ids: account.entity_ids || [],
      is_active: account.is_active,
    });
    setIsEditing(true);
  };

  const handleCancelEditing = () => {
    setIsEditing(false);
  };

  const handleSaveAccount = () => {
    if (!editForm.account_name.trim()) return;
    const update: AccountUpdate = {
      account_name: editForm.account_name.trim(),
      institution_name: editForm.institution_name.trim() || undefined,
      account_number_last4: editForm.account_number_last4 || undefined,
      notes: editForm.notes.trim() || undefined,
      entity_ids: editForm.entity_ids,
      is_active: editForm.is_active,
    };
    updateAccountMutation.mutate(update);
  };

  const handleDeleteAccount = () => {
    setConfirmDeleteOpen(true);
  };

  const handleConfirmDelete = () => {
    deleteAccountMutation.mutate();
    setConfirmDeleteOpen(false);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center">
            <Typography variant="h6" component="span" sx={{ mr: 2 }}>
              {getAccountTypeIcon(account.account_type)} {account.account_name}
            </Typography>
            <Chip
              label={getAccountTypeLabel(account.account_type)}
              size="small"
              color="primary"
              variant="outlined"
            />
            {!account.is_active && (
              <Chip
                label="Inactive"
                size="small"
                color="warning"
                sx={{ ml: 1 }}
              />
            )}
          </Box>
          <Box>
            {isEditing ? (
              <>
                <IconButton size="small" onClick={handleSaveAccount} disabled={updateAccountMutation.isPending} color="primary" aria-label="Save account changes">
                  <SaveIcon />
                </IconButton>
                <IconButton size="small" onClick={handleCancelEditing} aria-label="Cancel editing">
                  <CloseIcon />
                </IconButton>
              </>
            ) : (
              <>
                <IconButton size="small" onClick={handleStartEditing} sx={{ mr: 0.5 }} aria-label="Edit account details">
                  <EditIcon />
                </IconButton>
                <IconButton size="small" onClick={handleDeleteAccount} aria-label="Delete account">
                  <DeleteIcon />
                </IconButton>
              </>
            )}
          </Box>
        </Box>
      </DialogTitle>

      <DialogContent>
        {/* Account Summary */}
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  Current Balance
                </Typography>
                <Typography variant="h5">
                  {formatCurrency(account.current_balance || 0, acctCurrency)}
                </Typography>
                {account.current_balance_date && (
                  <Typography variant="caption" color="text.secondary">
                    As of {new Date(account.current_balance_date).toLocaleDateString()}
                  </Typography>
                )}
              </Grid>

              <Grid item xs={12} sm={6}>
                {account.institution_name && (
                  <>
                    <Typography variant="body2" color="text.secondary">
                      Institution
                    </Typography>
                    <Typography variant="body1">{account.institution_name}</Typography>
                    {account.account_number_last4 && (
                      <Typography variant="caption">****{account.account_number_last4}</Typography>
                    )}
                  </>
                )}
                {acctCurrency !== "USD" && (
                  <Box sx={{ mt: account.institution_name ? 1 : 0 }}>
                    <Typography variant="body2" color="text.secondary">
                      Currency
                    </Typography>
                    <Typography variant="body1">{acctCurrency}</Typography>
                  </Box>
                )}
              </Grid>

              {account.has_cash_component && account.cash_balance !== undefined && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Cash Position
                  </Typography>
                  <Typography variant="body1">
                    {formatCurrency(account.cash_balance, acctCurrency)}
                  </Typography>
                </Grid>
              )}

              {account.has_investment_component && account.investment_value !== undefined && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Investment Value
                  </Typography>
                  <Typography variant="body1">
                    {formatCurrency(account.investment_value, acctCurrency)}
                  </Typography>
                </Grid>
              )}
            </Grid>
          </CardContent>
        </Card>

        {/* Tabs */}
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Details" icon={<AccountBalanceIcon />} iconPosition="start" />
          <Tab label="Balance History" icon={<HistoryIcon />} iconPosition="start" />
          {account.has_investment_component && (
            <Tab label="Portfolio" icon={<TrendingUpIcon />} iconPosition="start" />
          )}
          <Tab label="Reconciliations" icon={<CheckCircleIcon />} iconPosition="start" />
        </Tabs>

        {/* Tab Panels */}
        <TabPanel value={tabValue} index={0}>
          {isEditing ? (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Account Name"
                  fullWidth
                  value={editForm.account_name}
                  onChange={(e) => setEditForm({ ...editForm, account_name: e.target.value })}
                  required
                  error={!editForm.account_name.trim()}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Institution Name"
                  fullWidth
                  value={editForm.institution_name}
                  onChange={(e) => setEditForm({ ...editForm, institution_name: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Account Number (Last 4)"
                  fullWidth
                  value={editForm.account_number_last4}
                  onChange={(e) => {
                    const val = e.target.value.replace(/\D/g, '').slice(0, 4);
                    setEditForm({ ...editForm, account_number_last4: val });
                  }}
                  inputProps={{ maxLength: 4, pattern: '[0-9]*' }}
                />
              </Grid>
              {entities.length > 0 && (
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Entities</InputLabel>
                    <Select
                      multiple
                      value={editForm.entity_ids}
                      label="Entities"
                      onChange={(e) => setEditForm({ ...editForm, entity_ids: e.target.value as number[] })}
                      renderValue={(selected) =>
                        (selected as number[])
                          .map((id) => entities.find((e) => e.entity_id === id)?.entity_name)
                          .filter(Boolean)
                          .join(', ')
                      }
                    >
                      {entities.map((entity) => (
                        <MenuItem key={entity.entity_id} value={entity.entity_id}>
                          {entity.entity_name} ({ENTITY_TYPE_LABELS[entity.entity_type] || entity.entity_type})
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              )}
              <Grid item xs={12}>
                <TextField
                  label="Notes"
                  fullWidth
                  multiline
                  rows={3}
                  value={editForm.notes}
                  onChange={(e) => setEditForm({ ...editForm, notes: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={editForm.is_active}
                      onChange={(e) => setEditForm({ ...editForm, is_active: e.target.checked })}
                    />
                  }
                  label={editForm.is_active ? "Active" : "Inactive"}
                />
              </Grid>
              {updateAccountMutation.isError && (
                <Grid item xs={12}>
                  <Alert severity="error">Failed to update account. Please try again.</Alert>
                </Grid>
              )}
            </Grid>
          ) : (
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Typography variant="subtitle2" gutterBottom>
                  Account Information
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText
                      primary="Account Type"
                      secondary={getAccountTypeLabel(account.account_type)}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Created"
                      secondary={new Date(account.created_at).toLocaleDateString()}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Opening Balance"
                      secondary={formatCurrency(account.opening_balance, acctCurrency)}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Status"
                      secondary={account.is_active ? "Active" : "Inactive"}
                    />
                  </ListItem>
                  {account.entity_ids.length > 0 && (
                    <ListItem>
                      <ListItemText
                        primary={account.entity_ids.length === 1 ? "Entity" : "Entities"}
                        secondary={account.entity_ids
                          .map((id) => {
                            const entity = entities.find((e) => e.entity_id === id);
                            return entity
                              ? `${entity.entity_name} (${ENTITY_TYPE_LABELS[entity.entity_type] || entity.entity_type})`
                              : null;
                          })
                          .filter(Boolean)
                          .join(', ')}
                      />
                    </ListItem>
                  )}
                  {account.notes && (
                    <ListItem>
                      <ListItemText primary="Notes" secondary={account.notes} />
                    </ListItem>
                  )}
                </List>
              </Grid>
            </Grid>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {showAddBalance ? (
            <Box mb={2}>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} sm={4}>
                  <TextField
                    label="Balance"
                    type="number"
                    fullWidth
                    value={newBalance}
                    onChange={(e) => setNewBalance(e.target.value)}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    label="Date"
                    type="date"
                    fullWidth
                    value={newBalanceDate}
                    onChange={(e) => setNewBalanceDate(e.target.value)}
                    InputLabelProps={{ shrink: true }}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Button
                    variant="contained"
                    onClick={handleAddBalance}
                    disabled={!newBalance || addBalanceMutation.isPending}
                    sx={{ mr: 1 }}
                  >
                    Add
                  </Button>
                  <Button onClick={() => setShowAddBalance(false)}>Cancel</Button>
                </Grid>
                {addBalanceMutation.isError && (
                  <Grid item xs={12}>
                    <Alert severity="error">Failed to add balance snapshot. Please try again.</Alert>
                  </Grid>
                )}
              </Grid>
            </Box>
          ) : (
            <Box mb={2}>
              <Button variant="outlined" onClick={() => setShowAddBalance(true)}>
                Add Balance Snapshot
              </Button>
            </Box>
          )}

          {balanceHistory && balanceHistory.balances.length > 0 ? (
            <BalanceHistoryChart balances={balanceHistory.balances} currency={acctCurrency} />
          ) : (
            <Typography color="text.secondary">No balance history available</Typography>
          )}
        </TabPanel>

        {account.has_investment_component && (
          <TabPanel value={tabValue} index={2}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="subtitle2">Portfolio</Typography>
              <Button
                size="small"
                startIcon={<AddIcon />}
                onClick={() => setShowHoldingForm(true)}
                disabled={showHoldingForm}
              >
                Add Holding
              </Button>
            </Box>

            {showHoldingForm && (
              <Card variant="outlined" sx={{ mb: 2, p: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  {editingHoldingId ? 'Edit Holding' : 'New Holding'}
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <TextField
                      label="Symbol"
                      value={holdingForm.symbol}
                      onChange={(e) => setHoldingForm({ ...holdingForm, symbol: e.target.value.toUpperCase() })}
                      fullWidth
                      size="small"
                      placeholder="AAPL"
                    />
                  </Grid>
                  <Grid item xs={4}>
                    <TextField
                      label="Quantity"
                      type="number"
                      value={holdingForm.quantity}
                      onChange={(e) => setHoldingForm({ ...holdingForm, quantity: e.target.value })}
                      fullWidth
                      size="small"
                    />
                  </Grid>
                  <Grid item xs={4}>
                    <TextField
                      label="As of Date"
                      type="date"
                      value={holdingForm.as_of_date}
                      onChange={(e) => setHoldingForm({ ...holdingForm, as_of_date: e.target.value })}
                      fullWidth
                      size="small"
                      InputLabelProps={{ shrink: true }}
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      label="Cost Basis"
                      type="number"
                      value={holdingForm.cost_basis}
                      onChange={(e) => setHoldingForm({ ...holdingForm, cost_basis: e.target.value })}
                      fullWidth
                      size="small"
                      InputProps={{ startAdornment: <InputAdornment position="start">$</InputAdornment> }}
                    />
                  </Grid>
                  <Grid item xs={6}>
                    <TextField
                      label="Current Value"
                      type="number"
                      value={holdingForm.current_value}
                      onChange={(e) => setHoldingForm({ ...holdingForm, current_value: e.target.value })}
                      fullWidth
                      size="small"
                      InputProps={{ startAdornment: <InputAdornment position="start">$</InputAdornment> }}
                    />
                  </Grid>
                </Grid>
                <Box display="flex" justifyContent="flex-end" gap={1} mt={2}>
                  <Button size="small" onClick={() => {
                    setShowHoldingForm(false);
                    setEditingHoldingId(null);
                    setHoldingForm({ symbol: '', quantity: '', as_of_date: new Date().toISOString().split('T')[0], cost_basis: '', current_value: '' });
                  }}>Cancel</Button>
                  <Button
                    size="small"
                    variant="contained"
                    onClick={() => editingHoldingId ? updateHoldingMutation.mutate() : addHoldingMutation.mutate()}
                    disabled={!holdingForm.symbol || !holdingForm.quantity || addHoldingMutation.isPending || updateHoldingMutation.isPending}
                  >
                    {editingHoldingId
                      ? (updateHoldingMutation.isPending ? 'Saving...' : 'Save')
                      : (addHoldingMutation.isPending ? 'Adding...' : 'Add')}
                  </Button>
                </Box>
              </Card>
            )}

            {portfolio ? (
              <Box>
                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Total Value
                    </Typography>
                    <Typography variant="h6">{formatCurrency(portfolio.total_value, acctCurrency)}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Total Gain/Loss
                    </Typography>
                    <Typography
                      variant="h6"
                      color={
                        portfolio.total_gain_loss == null
                          ? 'text.secondary'
                          : portfolio.total_gain_loss > 0
                            ? 'success.main'
                            : portfolio.total_gain_loss < 0
                              ? 'error.main'
                              : 'text.primary'
                      }
                    >
                      {portfolio.total_gain_loss != null
                        ? formatCurrency(portfolio.total_gain_loss, acctCurrency)
                        : 'N/A'}
                    </Typography>
                  </Grid>
                </Grid>

                <Typography variant="subtitle2" gutterBottom>
                  Holdings
                </Typography>
                <List>
                  {portfolio.holdings.map((holding) => (
                    <ListItem
                      key={holding.holding_id}
                      secondaryAction={
                        <Box>
                          <IconButton
                            size="small"
                            onClick={() => {
                              setEditingHoldingId(holding.holding_id);
                              setHoldingForm({
                                symbol: holding.symbol,
                                quantity: String(holding.quantity),
                                as_of_date: holding.as_of_date || new Date().toISOString().split('T')[0],
                                cost_basis: holding.cost_basis != null ? String(holding.cost_basis) : '',
                                current_value: holding.current_value != null ? String(holding.current_value) : '',
                              });
                              setShowHoldingForm(true);
                            }}
                            title="Edit holding"
                          >
                            <EditIcon fontSize="small" />
                          </IconButton>
                          <IconButton
                            edge="end"
                            size="small"
                            onClick={() => {
                              if (window.confirm(`Delete holding ${holding.symbol}?`)) {
                                deleteHoldingMutation.mutate(holding.holding_id);
                              }
                            }}
                            title="Delete holding"
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </Box>
                      }
                    >
                      <ListItemText
                        primary={`${holding.symbol} - ${holding.description || 'N/A'}`}
                        secondary={`${holding.quantity} shares @ ${formatCurrency(
                          holding.current_value || 0, acctCurrency
                        )}${holding.gain_loss != null ? ` (${holding.gain_loss >= 0 ? '+' : ''}${formatCurrency(holding.gain_loss, acctCurrency)})` : ''}`}
                      />
                      {holding.gain_loss_percent != null && (
                        <Chip
                          label={`${holding.gain_loss_percent > 0 ? '+' : ''}${holding.gain_loss_percent.toFixed(
                            1
                          )}%`}
                          color={holding.gain_loss_percent > 0 ? 'success' : 'error'}
                          size="small"
                          sx={{ mr: 4 }}
                        />
                      )}
                    </ListItem>
                  ))}
                </List>
              </Box>
            ) : (
              <Typography color="text.secondary">No portfolio data available</Typography>
            )}
          </TabPanel>
        )}

        <TabPanel value={tabValue} index={3}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="subtitle2">Reconciliations</Typography>
            <Button
              size="small"
              startIcon={<AddIcon />}
              onClick={() => setShowReconForm(true)}
              disabled={showReconForm}
            >
              Start Reconciliation
            </Button>
          </Box>

          {showReconForm && (
            <Card variant="outlined" sx={{ mb: 2, p: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                New Reconciliation
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    label="Statement Date"
                    type="date"
                    value={reconDate}
                    onChange={(e) => setReconDate(e.target.value)}
                    fullWidth
                    size="small"
                    InputLabelProps={{ shrink: true }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    label="Statement Balance"
                    type="number"
                    value={reconBalance}
                    onChange={(e) => setReconBalance(e.target.value)}
                    fullWidth
                    size="small"
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
              </Grid>
              <Box display="flex" justifyContent="flex-end" gap={1} mt={2}>
                <Button
                  size="small"
                  onClick={() => {
                    setShowReconForm(false);
                    setReconBalance('');
                  }}
                >
                  Cancel
                </Button>
                <Button
                  size="small"
                  variant="contained"
                  onClick={() => createReconMutation.mutate()}
                  disabled={!reconBalance || createReconMutation.isPending}
                >
                  {createReconMutation.isPending ? 'Creating...' : 'Create'}
                </Button>
              </Box>
            </Card>
          )}

          {/* Active reconciliation clearing UI */}
          {activeRecon && (
            <Card variant="outlined" sx={{ mb: 2, p: 2 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="subtitle2">
                  Clearing Transactions — Statement {new Date(activeRecon.statement_date).toLocaleDateString()}
                </Typography>
                <Button size="small" onClick={() => { setActiveRecon(null); setClearedIds(new Set()); }}>
                  Cancel
                </Button>
              </Box>

              {/* Running totals */}
              <Grid container spacing={2} sx={{ mb: 2 }}>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">Statement Balance</Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {formatCurrency(activeRecon.statement_balance, acctCurrency)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">Cleared Balance</Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {formatCurrency(clearedBalance, acctCurrency)}
                  </Typography>
                </Grid>
                <Grid item xs={4}>
                  <Typography variant="caption" color="text.secondary">Difference</Typography>
                  <Typography
                    variant="body1"
                    fontWeight="bold"
                    color={Math.abs(discrepancy) < 0.01 ? 'success.main' : 'warning.main'}
                  >
                    {formatCurrency(discrepancy, acctCurrency)}
                  </Typography>
                </Grid>
              </Grid>

              {reconTxLoading && <LinearProgress sx={{ mb: 1 }} />}

              {reconTransactions?.transactions && reconTransactions.transactions.length > 0 && (
                <>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="caption" color="text.secondary">
                      {clearedIds.size} of {reconTransactions.transactions.length} transactions cleared
                    </Typography>
                    <Box>
                      <Button size="small" onClick={handleSelectAllCleared}>Select All</Button>
                      <Button size="small" onClick={handleDeselectAllCleared}>Clear All</Button>
                    </Box>
                  </Box>

                  <Box sx={{ maxHeight: 300, overflow: 'auto', border: 1, borderColor: 'divider', borderRadius: 1 }}>
                    <List dense disablePadding>
                      {reconTransactions.transactions.map((tx: Transaction) => (
                        <ListItem
                          key={tx.id}
                          dense
                          sx={{
                            borderBottom: '1px solid',
                            borderBottomColor: 'divider',
                            bgcolor: clearedIds.has(tx.id) ? 'action.selected' : 'transparent',
                          }}
                        >
                          <Checkbox
                            checked={clearedIds.has(tx.id)}
                            onChange={() => handleToggleCleared(tx.id)}
                            size="small"
                          />
                          <ListItemText
                            primary={
                              <Box display="flex" justifyContent="space-between">
                                <Typography variant="body2" noWrap sx={{ maxWidth: '60%' }}>
                                  {tx.description || 'No description'}
                                </Typography>
                                <Typography
                                  variant="body2"
                                  color={tx.transaction_type === 'Income' ? 'success.main' : 'error.main'}
                                >
                                  {tx.transaction_type === 'Income' ? '+' : '-'}{formatCurrency(Math.abs(tx.amount), acctCurrency)}
                                </Typography>
                              </Box>
                            }
                            secondary={tx.date}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </>
              )}

              {reconTransactions?.transactions && reconTransactions.transactions.length === 0 && (
                <Typography color="text.secondary" variant="body2">
                  No transactions found for this account up to {new Date(activeRecon.statement_date).toLocaleDateString()}.
                </Typography>
              )}

              <Box display="flex" justifyContent="flex-end" gap={1} mt={2}>
                <Button
                  variant="contained"
                  color="success"
                  onClick={() => completeReconMutation.mutate()}
                  disabled={completeReconMutation.isPending}
                >
                  {completeReconMutation.isPending ? 'Completing...' : 'Finish Reconciliation'}
                </Button>
              </Box>
              {completeReconMutation.isError && (
                <Alert severity="error" sx={{ mt: 1 }}>Failed to complete reconciliation.</Alert>
              )}
            </Card>
          )}

          {reconciliations && reconciliations.length > 0 ? (
            <List>
              {reconciliations.map((recon) => (
                <ListItem
                  key={recon.reconciliation_id}
                  sx={{ cursor: recon.is_reconciled ? 'default' : 'pointer' }}
                  onClick={() => {
                    if (!recon.is_reconciled && !activeRecon) {
                      handleStartClearing(recon);
                    }
                  }}
                >
                  <ListItemText
                    primary={new Date(recon.statement_date).toLocaleDateString()}
                    secondary={`Statement: ${formatCurrency(
                      recon.statement_balance, acctCurrency
                    )} | Calculated: ${formatCurrency(
                      recon.calculated_balance, acctCurrency
                    )} | Discrepancy: ${formatCurrency(recon.discrepancy_amount || 0, acctCurrency)}`}
                  />
                  {recon.is_reconciled ? (
                    <Chip
                      icon={<CheckCircleIcon />}
                      label="Reconciled"
                      color="success"
                      size="small"
                    />
                  ) : (
                    <Chip
                      label={activeRecon?.reconciliation_id === recon.reconciliation_id ? 'Clearing...' : 'Click to clear'}
                      color={activeRecon?.reconciliation_id === recon.reconciliation_id ? 'info' : 'warning'}
                      size="small"
                    />
                  )}
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography color="text.secondary">
              No reconciliations yet. Click "Start Reconciliation" to compare your
              statement balance against calculated transactions.
            </Typography>
          )}
        </TabPanel>
      </DialogContent>

      <DialogActions>
        <Button
          startIcon={<ReceiptIcon />}
          onClick={() => {
            onClose();
            navigate(`/transactions?account_id=${account.account_id}`);
          }}
        >
          View Transactions
        </Button>
        <Box sx={{ flex: 1 }} />
        <Button onClick={onClose}>Close</Button>
      </DialogActions>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={confirmDeleteOpen}
        onClose={() => setConfirmDeleteOpen(false)}
        aria-labelledby="delete-account-dialog-title"
      >
        <DialogTitle id="delete-account-dialog-title">Delete Account</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete <strong>{account.account_name}</strong>? This action cannot be undone.
          </Typography>
          {deleteAccountMutation.isError && (
            <Alert severity="error" sx={{ mt: 2 }}>Failed to delete account. Please try again.</Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmDeleteOpen(false)}>Cancel</Button>
          <Button
            onClick={handleConfirmDelete}
            color="error"
            variant="contained"
            disabled={deleteAccountMutation.isPending}
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Dialog>
  );
};

export default AccountDetailsDialog;