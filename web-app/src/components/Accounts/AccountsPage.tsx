import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  IconButton,
  Chip,
  Alert,
  Tabs,
  Tab,
  Paper,
  Skeleton,
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  AccountBalance as AccountBalanceIcon,
  TrendingUp as TrendingUpIcon,
  AccountBalanceWallet as WalletIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getAccounts, getNetWorth } from '../../api/accounts';
import {
  Account,
  getAccountTypeLabel,
  getAccountTypeIcon,
  isAssetAccount,
} from '../../types/account';
import AddAccountDialog from './AddAccountDialog';
import AccountDetailsDialog from './AccountDetailsDialog';
import NetWorthCard from './NetWorthCard';

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
      id={`account-tabpanel-${index}`}
      aria-labelledby={`account-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const AccountsPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);

  // Fetch accounts
  const {
    data: accounts = [],
    isLoading: accountsLoading,
    error: accountsError,
    refetch: refetchAccounts,
  } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => getAccounts(),
  });

  // Fetch net worth
  const {
    data: netWorth,
    isLoading: netWorthLoading,
    refetch: refetchNetWorth,
  } = useQuery({
    queryKey: ['netWorth'],
    queryFn: () => getNetWorth(),
  });

  // Filter accounts by type
  const assetAccounts = accounts.filter((acc) => isAssetAccount(acc.account_type));
  const liabilityAccounts = accounts.filter((acc) => !isAssetAccount(acc.account_type));

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleAddAccount = () => {
    setAddDialogOpen(true);
  };

  const handleAccountClick = (account: Account) => {
    setSelectedAccount(account);
    setDetailsDialogOpen(true);
  };

  const handleRefresh = () => {
    refetchAccounts();
    refetchNetWorth();
  };

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const renderAccountCard = (account: Account) => {
    const isLiability = !isAssetAccount(account.account_type);
    // Use current_balance if available, otherwise fall back to opening_balance
    const balance = account.current_balance ?? account.opening_balance ?? 0;
    const displayBalance = isLiability ? Math.abs(balance) : balance;

    return (
      <Grid item xs={12} sm={6} md={4} key={account.account_id}>
        <Card
          sx={{
            cursor: 'pointer',
            '&:hover': { boxShadow: 3 },
            height: '100%',
          }}
          onClick={() => handleAccountClick(account)}
        >
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="start">
              <Box>
                <Typography variant="h6" gutterBottom>
                  <span style={{ marginRight: 8 }}>
                    {getAccountTypeIcon(account.account_type)}
                  </span>
                  {account.account_name}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {account.institution_name || 'No institution'}
                </Typography>
              </Box>
              <Chip
                label={getAccountTypeLabel(account.account_type)}
                size="small"
                color={isLiability ? 'error' : 'success'}
                variant="outlined"
              />
            </Box>

            <Box mt={2}>
              <Typography variant="h5" color={isLiability ? 'error' : 'primary'}>
                {isLiability && balance < 0 && '-'}
                {formatCurrency(displayBalance)}
              </Typography>
              {account.current_balance_date && (
                <Typography variant="caption" color="text.secondary">
                  As of {new Date(account.current_balance_date).toLocaleDateString()}
                </Typography>
              )}
            </Box>

            {account.has_cash_component && account.has_investment_component && (
              <Box mt={2}>
                <Grid container spacing={1}>
                  {account.cash_balance !== undefined && (
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Cash
                      </Typography>
                      <Typography variant="body2">
                        {formatCurrency(account.cash_balance)}
                      </Typography>
                    </Grid>
                  )}
                  {account.investment_value !== undefined && (
                    <Grid item xs={6}>
                      <Typography variant="caption" color="text.secondary">
                        Investments
                      </Typography>
                      <Typography variant="body2">
                        {formatCurrency(account.investment_value)}
                      </Typography>
                    </Grid>
                  )}
                </Grid>
              </Box>
            )}

            {account.account_number_last4 && (
              <Box mt={1}>
                <Typography variant="caption" color="text.secondary">
                  ****{account.account_number_last4}
                </Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      </Grid>
    );
  };

  if (accountsLoading || netWorthLoading) {
    return (
      <Box>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1">Accounts</Typography>
        </Box>
        <Skeleton variant="rounded" height={120} sx={{ mb: 3 }} />
        <Grid container spacing={3}>
          {[0, 1, 2].map((i) => (
            <Grid item xs={12} sm={6} md={4} key={i}>
              <Card>
                <CardContent>
                  <Skeleton variant="text" width="60%" height={32} />
                  <Skeleton variant="text" width="40%" height={20} sx={{ mb: 2 }} />
                  <Skeleton variant="text" width="50%" height={40} />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  if (accountsError) {
    return (
      <Alert severity="error">
        Error loading accounts: {accountsError.message}
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Accounts
        </Typography>
        <Box>
          <IconButton onClick={handleRefresh} sx={{ mr: 1 }}>
            <RefreshIcon />
          </IconButton>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddAccount}
          >
            Add Account
          </Button>
        </Box>
      </Box>

      {/* Net Worth Summary */}
      {netWorth && (
        <Box mb={3}>
          <NetWorthCard netWorth={netWorth} />
        </Box>
      )}

      {/* Account Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          aria-label="account tabs"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab
            label={`All Accounts (${accounts.length})`}
            icon={<WalletIcon />}
            iconPosition="start"
          />
          <Tab
            label={`Assets (${assetAccounts.length})`}
            icon={<TrendingUpIcon />}
            iconPosition="start"
          />
          <Tab
            label={`Liabilities (${liabilityAccounts.length})`}
            icon={<AccountBalanceIcon />}
            iconPosition="start"
          />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          {accounts.length > 0 ? (
            <Grid container spacing={3}>
              {accounts.map(renderAccountCard)}
            </Grid>
          ) : (
            <Box textAlign="center" py={4}>
              <AccountBalanceIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 1 }} />
              <Typography color="text.secondary" gutterBottom>
                No accounts yet
              </Typography>
              <Button variant="outlined" startIcon={<AddIcon />} onClick={handleAddAccount}>
                Add Your First Account
              </Button>
            </Box>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          {assetAccounts.length > 0 ? (
            <Grid container spacing={3}>
              {assetAccounts.map(renderAccountCard)}
            </Grid>
          ) : (
            <Box textAlign="center" py={4}>
              <TrendingUpIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 1 }} />
              <Typography color="text.secondary" gutterBottom>
                No asset accounts
              </Typography>
              <Button variant="outlined" startIcon={<AddIcon />} onClick={handleAddAccount}>
                Add an Asset Account
              </Button>
            </Box>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          {liabilityAccounts.length > 0 ? (
            <Grid container spacing={3}>
              {liabilityAccounts.map(renderAccountCard)}
            </Grid>
          ) : (
            <Box textAlign="center" py={4}>
              <AccountBalanceIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 1 }} />
              <Typography color="text.secondary">
                No liability accounts
              </Typography>
            </Box>
          )}
        </TabPanel>
      </Paper>

      {/* Dialogs */}
      <AddAccountDialog
        open={addDialogOpen}
        onClose={() => setAddDialogOpen(false)}
        onAccountCreated={() => {
          refetchAccounts();
          refetchNetWorth();
        }}
      />

      {selectedAccount && (
        <AccountDetailsDialog
          open={detailsDialogOpen}
          account={selectedAccount}
          onClose={() => {
            setDetailsDialogOpen(false);
            setSelectedAccount(null);
          }}
          onAccountUpdated={() => {
            refetchAccounts();
            refetchNetWorth();
          }}
        />
      )}
    </Box>
  );
};

export default AccountsPage;