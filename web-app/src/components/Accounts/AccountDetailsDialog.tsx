import React, { useState } from 'react';
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
} from '@mui/icons-material';
import { useQuery, useMutation } from '@tanstack/react-query';
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
  addBalanceSnapshot,
  updateAccount,
  deleteAccount,
} from '../../api/accounts';
import BalanceHistoryChart from './BalanceHistoryChart';

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
  const [tabValue, setTabValue] = useState(0);
  const [showAddBalance, setShowAddBalance] = useState(false);
  const [newBalance, setNewBalance] = useState('');
  const [newBalanceDate, setNewBalanceDate] = useState(
    new Date().toISOString().split('T')[0]
  );
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    account_name: account.account_name,
    institution_name: account.institution_name || '',
    account_number_last4: account.account_number_last4 || '',
    notes: account.notes || '',
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

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
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
    };
    updateAccountMutation.mutate(update);
  };

  const handleDeleteAccount = () => {
    if (window.confirm(`Are you sure you want to delete ${account.account_name}?`)) {
      deleteAccountMutation.mutate();
    }
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
          </Box>
          <Box>
            {isEditing ? (
              <>
                <IconButton size="small" onClick={handleSaveAccount} disabled={updateAccountMutation.isPending} color="primary">
                  <SaveIcon />
                </IconButton>
                <IconButton size="small" onClick={handleCancelEditing}>
                  <CloseIcon />
                </IconButton>
              </>
            ) : (
              <>
                <IconButton size="small" onClick={handleStartEditing} sx={{ mr: 0.5 }}>
                  <EditIcon />
                </IconButton>
                <IconButton size="small" onClick={handleDeleteAccount}>
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
                  {formatCurrency(account.current_balance || 0)}
                </Typography>
                {account.current_balance_date && (
                  <Typography variant="caption" color="text.secondary">
                    As of {new Date(account.current_balance_date).toLocaleDateString()}
                  </Typography>
                )}
              </Grid>

              {account.institution_name && (
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    Institution
                  </Typography>
                  <Typography variant="body1">{account.institution_name}</Typography>
                  {account.account_number_last4 && (
                    <Typography variant="caption">****{account.account_number_last4}</Typography>
                  )}
                </Grid>
              )}

              {account.has_cash_component && account.cash_balance !== undefined && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Cash Position
                  </Typography>
                  <Typography variant="body1">
                    {formatCurrency(account.cash_balance)}
                  </Typography>
                </Grid>
              )}

              {account.has_investment_component && account.investment_value !== undefined && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Investment Value
                  </Typography>
                  <Typography variant="body1">
                    {formatCurrency(account.investment_value)}
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
                      secondary={formatCurrency(account.opening_balance)}
                    />
                  </ListItem>
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
            <BalanceHistoryChart balances={balanceHistory.balances} />
          ) : (
            <Typography color="text.secondary">No balance history available</Typography>
          )}
        </TabPanel>

        {account.has_investment_component && (
          <TabPanel value={tabValue} index={2}>
            {portfolio ? (
              <Box>
                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Total Value
                    </Typography>
                    <Typography variant="h6">{formatCurrency(portfolio.total_value)}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="text.secondary">
                      Total Gain/Loss
                    </Typography>
                    <Typography
                      variant="h6"
                      color={
                        portfolio.total_gain_loss && portfolio.total_gain_loss > 0
                          ? 'success.main'
                          : 'error.main'
                      }
                    >
                      {formatCurrency(portfolio.total_gain_loss || 0)}
                    </Typography>
                  </Grid>
                </Grid>

                <Typography variant="subtitle2" gutterBottom>
                  Holdings
                </Typography>
                <List>
                  {portfolio.holdings.map((holding) => (
                    <ListItem key={holding.holding_id}>
                      <ListItemText
                        primary={`${holding.symbol} - ${holding.description || 'N/A'}`}
                        secondary={`${holding.quantity} shares @ ${formatCurrency(
                          holding.current_value || 0
                        )}`}
                      />
                      {holding.gain_loss_percent !== undefined && (
                        <Chip
                          label={`${holding.gain_loss_percent > 0 ? '+' : ''}${holding.gain_loss_percent.toFixed(
                            1
                          )}%`}
                          color={holding.gain_loss_percent > 0 ? 'success' : 'error'}
                          size="small"
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
          {reconciliations && reconciliations.length > 0 ? (
            <List>
              {reconciliations.map((recon) => (
                <ListItem key={recon.reconciliation_id}>
                  <ListItemText
                    primary={new Date(recon.statement_date).toLocaleDateString()}
                    secondary={`Statement: ${formatCurrency(
                      recon.statement_balance
                    )} | Calculated: ${formatCurrency(
                      recon.calculated_balance
                    )} | Discrepancy: ${formatCurrency(recon.discrepancy_amount || 0)}`}
                  />
                  {recon.is_reconciled && (
                    <Chip
                      icon={<CheckCircleIcon />}
                      label="Reconciled"
                      color="success"
                      size="small"
                    />
                  )}
                </ListItem>
              ))}
            </List>
          ) : (
            <Typography color="text.secondary">No reconciliations found</Typography>
          )}
        </TabPanel>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default AccountDetailsDialog;