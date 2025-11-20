import { Box, Typography, useTheme } from "@mui/material";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

interface CashFlowAreaChartProps {
  data: Array<{
    date: string;
    income?: number;
    expense?: number;
    netCashFlow?: number;
    cumulativeCashFlow?: number;
    [key: string]: any;
  }>;
  title?: string;
  height?: number;
  showCumulative?: boolean;
}

function CashFlowAreaChart({
  data,
  title,
  height = 300,
  showCumulative = false,
}: CashFlowAreaChartProps) {
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
        <AreaChart
          data={data}
          margin={{ top: 10, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={theme.palette.success.main}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={theme.palette.success.main}
                stopOpacity={0.1}
              />
            </linearGradient>
            <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={theme.palette.error.main}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={theme.palette.error.main}
                stopOpacity={0.1}
              />
            </linearGradient>
            <linearGradient id="colorNetCashFlow" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={theme.palette.primary.main}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={theme.palette.primary.main}
                stopOpacity={0.1}
              />
            </linearGradient>
          </defs>
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
          <ReferenceLine y={0} stroke={theme.palette.divider} strokeWidth={2} />
          
          {showCumulative ? (
            <Area
              type="monotone"
              dataKey="cumulativeCashFlow"
              name="Cumulative Cash Flow"
              stroke={theme.palette.primary.main}
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorNetCashFlow)"
            />
          ) : (
            <>
              <Area
                type="monotone"
                dataKey="income"
                name="Income"
                stroke={theme.palette.success.main}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorIncome)"
              />
              <Area
                type="monotone"
                dataKey="expense"
                name="Expense"
                stroke={theme.palette.error.main}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorExpense)"
              />
            </>
          )}
        </AreaChart>
      </ResponsiveContainer>
    </Box>
  );
}

export default CashFlowAreaChart;

