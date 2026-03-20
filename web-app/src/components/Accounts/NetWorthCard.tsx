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
  entityName?: string;
}

const NetWorthCard: React.FC<NetWorthCardProps> = ({ netWorth, entityName }) => {
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const assets = Number(netWorth.assets) || 0;
  const liabilities = Number(netWorth.liabilities) || 0;
  const liquidAssets = Number(netWorth.liquid_assets ?? netWorth.liquidAssets) || 0;
  const investments = Number(netWorth.investments) || 0;
  const netWorthValue = Number(netWorth.net_worth ?? netWorth.netWorth) || 0;
  const asOfDate = netWorth.as_of_date ?? netWorth.asOfDate;

  const totalAssetsAndLiabilities = assets + liabilities;
  const assetPercentage = totalAssetsAndLiabilities > 0
    ? (assets / totalAssetsAndLiabilities) * 100
    : 0;
  const liquidPercentage = assets > 0
    ? (liquidAssets / assets) * 100
    : 0;
  const investmentPercentage = assets > 0
    ? (investments / assets) * 100
    : 0;

  return (
    <Card elevation={2}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Net Worth{entityName ? ` — ${entityName}` : ' Overview'}
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
                  {formatCurrency(netWorthValue)}
                </Typography>
                {asOfDate && (
                  <Typography variant="caption" color="text.secondary">
                    As of {new Date(asOfDate).toLocaleDateString()}
                  </Typography>
                )}
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
                  {formatCurrency(assets)}
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
                  {formatCurrency(liabilities)}
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
                  Liquid: {formatCurrency(liquidAssets)} ({liquidPercentage.toFixed(1)}%)
                </Typography>
              </Box>
              <Box display="flex" alignItems="center">
                <ShowChartIcon sx={{ mr: 1, fontSize: 16 }} />
                <Typography variant="caption">
                  Invested: {formatCurrency(investments)} ({investmentPercentage.toFixed(1)}%)
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        {/* Progress Bar */}
        {liabilities > 0 && (
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
        {(() => {
          const breakdown = netWorth.account_breakdown ?? netWorth.accountBreakdown;
          return breakdown && Object.keys(breakdown).length > 0 && (
          <Box mt={3}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              By Account Type
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(breakdown).map(([type, amount]) => (
                <Grid item xs={6} sm={4} md={3} key={type}>
                  <Typography variant="caption" color="text.secondary">
                    {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}
                  </Typography>
                  <Typography variant="body2">
                    {formatCurrency(Number(amount) || 0)}
                  </Typography>
                </Grid>
              ))}
            </Grid>
          </Box>
          );
        })()}
      </CardContent>
    </Card>
  );
};

export default NetWorthCard;