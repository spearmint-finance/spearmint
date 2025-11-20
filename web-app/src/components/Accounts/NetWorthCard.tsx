import React from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Box,
  LinearProgress,
} from '@mui/material';
import {
  AccountBalance as AccountBalanceIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Wallet as WalletIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';
import { NetWorth } from '../../types/account';

interface NetWorthCardProps {
  netWorth: NetWorth;
}

const NetWorthCard: React.FC<NetWorthCardProps> = ({ netWorth }) => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const assetPercentage = (netWorth.assets / (netWorth.assets + netWorth.liabilities)) * 100;
  const liquidPercentage = (netWorth.liquid_assets / netWorth.assets) * 100;
  const investmentPercentage = (netWorth.investments / netWorth.assets) * 100;

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Net Worth Overview
        </Typography>

        <Grid container spacing={3}>
          {/* Net Worth */}
          <Grid item xs={12} md={3}>
            <Box display="flex" alignItems="center">
              <AccountBalanceIcon
                sx={{ mr: 2, fontSize: 40, color: 'primary.main' }}
              />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Net Worth
                </Typography>
                <Typography variant="h5" color="primary">
                  {formatCurrency(netWorth.net_worth)}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  As of {new Date(netWorth.as_of_date).toLocaleDateString()}
                </Typography>
              </Box>
            </Box>
          </Grid>

          {/* Assets */}
          <Grid item xs={12} sm={6} md={3}>
            <Box display="flex" alignItems="center">
              <TrendingUpIcon
                sx={{ mr: 2, fontSize: 40, color: 'success.main' }}
              />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Total Assets
                </Typography>
                <Typography variant="h6" color="success.main">
                  {formatCurrency(netWorth.assets)}
                </Typography>
              </Box>
            </Box>
          </Grid>

          {/* Liabilities */}
          <Grid item xs={12} sm={6} md={3}>
            <Box display="flex" alignItems="center">
              <TrendingDownIcon
                sx={{ mr: 2, fontSize: 40, color: 'error.main' }}
              />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Total Liabilities
                </Typography>
                <Typography variant="h6" color="error.main">
                  {formatCurrency(netWorth.liabilities)}
                </Typography>
              </Box>
            </Box>
          </Grid>

          {/* Asset Allocation */}
          <Grid item xs={12} md={3}>
            <Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Asset Allocation
              </Typography>
              <Box display="flex" alignItems="center" mb={1}>
                <WalletIcon sx={{ mr: 1, fontSize: 16 }} />
                <Typography variant="caption">
                  Liquid: {formatCurrency(netWorth.liquid_assets)} ({liquidPercentage.toFixed(1)}%)
                </Typography>
              </Box>
              <Box display="flex" alignItems="center">
                <ShowChartIcon sx={{ mr: 1, fontSize: 16 }} />
                <Typography variant="caption">
                  Invested: {formatCurrency(netWorth.investments)} ({investmentPercentage.toFixed(1)}%)
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* Progress Bar */}
        {netWorth.liabilities > 0 && (
          <Box mt={3}>
            <Box display="flex" justifyContent="space-between" mb={1}>
              <Typography variant="caption" color="text.secondary">
                Asset to Liability Ratio
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {assetPercentage.toFixed(1)}% Assets
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={assetPercentage}
              sx={{
                height: 8,
                borderRadius: 1,
                backgroundColor: 'error.light',
                '& .MuiLinearProgress-bar': {
                  backgroundColor: 'success.main',
                },
              }}
            />
          </Box>
        )}

        {/* Account Breakdown */}
        {netWorth.account_breakdown && Object.keys(netWorth.account_breakdown).length > 0 && (
          <Box mt={3}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              By Account Type
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(netWorth.account_breakdown).map(([type, amount]) => (
                <Grid item xs={6} sm={4} md={3} key={type}>
                  <Typography variant="caption" color="text.secondary">
                    {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}
                  </Typography>
                  <Typography variant="body2">
                    {formatCurrency(amount)}
                  </Typography>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default NetWorthCard;