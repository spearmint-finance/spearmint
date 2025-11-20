import { Box, Typography, useTheme } from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface TrendLineChartProps {
  data: Array<{
    date: string;
    income?: number;
    expense?: number;
    netCashFlow?: number;
    [key: string]: any;
  }>;
  title?: string;
  height?: number;
  showIncome?: boolean;
  showExpense?: boolean;
  showNetCashFlow?: boolean;
}

function TrendLineChart({
  data,
  title,
  height = 300,
  showIncome = true,
  showExpense = true,
  showNetCashFlow = false,
}: TrendLineChartProps) {
  const theme = useTheme();

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <Box
          sx={{
            backgroundColor: "background.paper",
            border: 1,
            borderColor: "divider",
            borderRadius: 1,
            p: 1.5,
            boxShadow: 2,
          }}
        >
          <Typography variant="body2" fontWeight="medium" gutterBottom>
            {label}
          </Typography>
          {payload.map((entry: any, index: number) => (
            <Typography
              key={index}
              variant="body2"
              sx={{ color: entry.color }}
            >
              {entry.name}: ${Math.abs(entry.value).toLocaleString("en-US", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </Typography>
          ))}
        </Box>
      );
    }
    return null;
  };

  return (
    <Box>
      {title && (
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <LineChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
          <XAxis
            dataKey="date"
            stroke={theme.palette.text.secondary}
            style={{ fontSize: "0.875rem" }}
          />
          <YAxis
            stroke={theme.palette.text.secondary}
            style={{ fontSize: "0.875rem" }}
            tickFormatter={(value) =>
              `$${value.toLocaleString("en-US", {
                minimumFractionDigits: 0,
                maximumFractionDigits: 0,
              })}`
            }
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{
              fontSize: "0.875rem",
              paddingTop: "10px",
            }}
          />
          {showIncome && (
            <Line
              type="monotone"
              dataKey="income"
              name="Income"
              stroke={theme.palette.success.main}
              strokeWidth={2}
              dot={{ fill: theme.palette.success.main, r: 4 }}
              activeDot={{ r: 6 }}
            />
          )}
          {showExpense && (
            <Line
              type="monotone"
              dataKey="expense"
              name="Expense"
              stroke={theme.palette.error.main}
              strokeWidth={2}
              dot={{ fill: theme.palette.error.main, r: 4 }}
              activeDot={{ r: 6 }}
            />
          )}
          {showNetCashFlow && (
            <Line
              type="monotone"
              dataKey="netCashFlow"
              name="Net Cash Flow"
              stroke={theme.palette.primary.main}
              strokeWidth={2}
              dot={{ fill: theme.palette.primary.main, r: 4 }}
              activeDot={{ r: 6 }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
}

export default TrendLineChart;

