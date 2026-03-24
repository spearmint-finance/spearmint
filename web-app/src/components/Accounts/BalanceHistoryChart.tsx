import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Box, Typography } from '@mui/material';
import { Balance } from '../../types/account';
import { formatCurrency } from '../../utils/formatters';

interface BalanceHistoryChartProps {
  balances: Balance[];
  currency?: string;
}

const BalanceHistoryChart: React.FC<BalanceHistoryChartProps> = ({ balances, currency = "USD" }) => {
  // Prepare data for chart
  const chartData = balances
    .sort((a, b) => new Date(a.balance_date).getTime() - new Date(b.balance_date).getTime())
    .map((balance) => ({
      date: new Date(balance.balance_date).toLocaleDateString(),
      total: balance.total_balance,
      cash: balance.cash_balance || 0,
      investments: balance.investment_value || 0,
    }));

  const formatCompact = (value: number) => formatCurrency(value, currency, 0);

  const hasCashAndInvestments = balances.some(
    (b) => b.cash_balance !== null && b.investment_value !== null
  );

  return (
    <Box>
      <Typography variant="subtitle2" gutterBottom>
        Balance Over Time
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis tickFormatter={formatCompact} />
          <Tooltip formatter={(value: number) => formatCompact(value)} />
          <Legend />

          <Line
            type="monotone"
            dataKey="total"
            stroke="#2196f3"
            name="Total Balance"
            strokeWidth={2}
            dot={{ r: 4 }}
          />

          {hasCashAndInvestments && (
            <>
              <Line
                type="monotone"
                dataKey="cash"
                stroke="#4caf50"
                name="Cash"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={{ r: 3 }}
              />
              <Line
                type="monotone"
                dataKey="investments"
                stroke="#ff9800"
                name="Investments"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={{ r: 3 }}
              />
            </>
          )}
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default BalanceHistoryChart;