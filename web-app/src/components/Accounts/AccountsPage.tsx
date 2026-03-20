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
  Link as LinkIcon,
  AccountBalance as AccountBalanceIcon,
  TrendingUp as TrendingUpIcon,
  AccountBalanceWallet as WalletIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getAccounts, getNetWorth } from '../../api/accounts';
import { formatCurrency } from '../../utils/formatters';
import { getLinkedProviders } from '../../api/aggregator';
import {
  Account,
  getAccountTypeLabel,
  getAccountTypeIcon,
  isAssetAccount,
} from '../../types/account';
import AddAccountDialog from './AddAccountDialog';
import AccountDetailsDialog from './AccountDetailsDialog';
import LinkAccountDialog from './LinkAccountDialog';
import NetWorthCard from './NetWorthCard';
import SyncButton from './SyncButton';
import ReconnectBanner from './ReconnectBanner';
import { useEntityContext } from '../../contexts/EntityContext';

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
  const [linkDialogOpen, setLinkDialogOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
  const [detailsDialogOpen, setDetailsDialogOpen] = useState(false);
  const { selectedEntityId, selectedEntity, entities } = useEntityContext();

  // Fetch accounts (filtered by selected entity)
  const {
    data: accounts = [],
    isLoading: accountsLoading,
    isFetching: accountsFetching,
    error: accountsError,
    refetch: refetchAccounts,
  } = useQuery({
    queryKey: ['accounts', { entity_id: selectedEntityId }],
    queryFn: () =>
      getAccounts(
        selectedEntityId != null ? { entity_id: selectedEntityId } : undefined
      ),
  });

  // Fetch net worth (filtered by selected entity)
  const {
    data: netWorth,
    isLoading: netWorthLoading,
    isFetching: netWorthFetching,
    refetch: refetchNetWorth,
  } = useQuery({
    queryKey: ['netWorth', { entity_id: selectedEntityId }],
    queryFn: () => getNetWorth(
      selectedEntityId != null ? { entity_id: selectedEntityId } : undefined
    ),
  });

  // Fetch linked providers for sync status and reconnect banners
  const { data: linkedProviders = [] } = useQuery({
    queryKey: ['linkedProviders'],
    queryFn: getLinkedProviders,
    retry: false,
  });

  const isRefreshing = (accountsFetching || netWorthFetching) && !accountsLoading && !netWorthLoading;

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
              <Box display="flex" alignItems="center" gap={0.5}>
                {account.link_type && account.link_type !== 'manual' && account.linked_provider_id && (
                  <SyncButton linkedProviderId={account.linked_provider_id} />
                )}
                <Chip
                  label={getAccountTypeLabel(account.account_type)}
                  size="small"
                  color={isLiability ? 'error' : 'success'}
                  variant="outlined"
                />
              </Box>
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

            {selectedEntityId == null && entities.length > 1 && account.entity_id && (() => {
              const entity = entities.find(e => e.entity_id === account.entity_id);
              return entity ? (
                <Box mt={1}>
                  <Chip label={entity.entity_name} size="small" variant="outlined" color="info" />
                </Box>
              ) : null;
            })()}
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
          <IconButton
            onClick={handleRefresh}
            disabled={isRefreshing}
            aria-label="Refresh accounts"
            sx={{
              mr: 1,
              animation: isRefreshing ? 'spin 1s linear infinite' : 'none',
              '@keyframes spin': { '100%': { transform: 'rotate(360deg)' } },
            }}
          >
            <RefreshIcon />
          </IconButton>
          <Button
            variant="outlined"
            startIcon={<LinkIcon />}
            onClick={() => setLinkDialogOpen(true)}
            sx={{ mr: 1 }}
          >
            Link Account
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAddAccount}
          >
            Add Manual
          </Button>
        </Box>
      </Box>

      {/* Reconnect Banner */}
      <ReconnectBanner
        providers={linkedProviders}
        onReconnect={() => setLinkDialogOpen(true)}
      />

      {/* Net Worth Summary */}
      {netWorth && (
        <Box mb={3}>
          <NetWorthCard netWorth={netWorth} entityName={selectedEntity?.entity_name} />
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
              <Box display="flex" gap={1} justifyContent="center">
                <Button variant="contained" startIcon={<LinkIcon />} onClick={() => setLinkDialogOpen(true)}>
                  Link Your Bank
                </Button>
                <Button variant="outlined" startIcon={<AddIcon />} onClick={handleAddAccount}>
                  Add Manually
                </Button>
              </Box>
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

      <LinkAccountDialog
        open={linkDialogOpen}
        onClose={() => setLinkDialogOpen(false)}
        onAccountLinked={() => {
          refetchAccounts();
          refetchNetWorth();
        }}
      />
    </Box>
  );
};

export default AccountsPage;