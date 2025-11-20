import { Box, Typography, useTheme } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface ExpenseStackedBarChartProps {
  data: Array<{
    period: string;
    [key: string]: number | string; // Dynamic keys for categories
  }>;
  categories: string[];
  height?: number;
}

// High contrast color palette for better accessibility
const CATEGORY_COLORS = [
  "#D32F2F", // Dark Red
  "#1565C0", // Dark Blue
  "#2E7D32", // Dark Green
  "#6A1B9A", // Dark Purple
  "#E65100", // Dark Orange (more distinct from red)
  "#00ACC1", // Bright Cyan (lighter, more vibrant teal)
  "#8D6E63", // Light Brown (warmer, lighter tone)
  "#455A64", // Blue Grey
  "#AD1457", // Dark Pink
  "#FDD835", // Bright Yellow (high contrast)
  "#283593", // Dark Indigo
  "#616161", // Medium Grey
];

function ExpenseStackedBarChart({
  data,
  categories,
  height = 400,
}: ExpenseStackedBarChartProps) {
  const theme = useTheme();

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      // Sort payload by value descending
      const sortedPayload = [...payload].sort((a, b) => b.value - a.value);

      // Calculate total
      const total = sortedPayload.reduce((sum, entry) => sum + entry.value, 0);

      return (
        <Box
          sx={{
            backgroundColor: "background.paper",
            border: 1,
            borderColor: "divider",
            borderRadius: 1,
            p: 1.5,
            boxShadow: 2,
            maxHeight: 400,
            overflowY: "auto",
          }}
        >
          <Typography variant="body2" fontWeight="bold" gutterBottom>
            {label}
          </Typography>
          <Typography variant="body2" fontWeight="medium" sx={{ mb: 1 }}>
            Total: ${total.toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </Typography>
          {sortedPayload.map((entry: any, index: number) => (
            <Box key={index} sx={{ display: "flex", justifyContent: "space-between", gap: 2 }}>
              <Typography
                variant="caption"
                sx={{ color: entry.color }}
              >
                {entry.name}:
              </Typography>
              <Typography variant="caption">
                ${entry.value.toLocaleString("en-US", {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </Typography>
            </Box>
          ))}
        </Box>
      );
    }
    return null;
  };

  // Format Y-axis (for dates)
  const formatYAxis = (value: string) => {
    // If it's a date like "2024-01", show as "Jan 24"
    if (value.includes("-")) {
      const [year, month] = value.split("-");
      const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      if (month) {
        return `${monthNames[parseInt(month) - 1]} '${year.slice(2)}`;
      }
    }
    return value;
  };

  // Format X-axis (for currency)
  const formatXAxis = (value: number) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}k`;
    }
    return `$${value.toFixed(0)}`;
  };

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart
        data={data}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
        <XAxis
          dataKey="period"
          stroke={theme.palette.text.secondary}
          style={{ fontSize: "0.875rem" }}
          tick={{ angle: -45, textAnchor: "end" }}
          height={60}
        />
        <YAxis
          stroke={theme.palette.text.secondary}
          style={{ fontSize: "0.875rem" }}
          tickFormatter={formatXAxis}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend
          wrapperStyle={{
            fontSize: "0.875rem",
            paddingTop: "10px",
          }}
        />
        {categories.map((category, index) => (
          <Bar
            key={category}
            dataKey={category}
            stackId="expense"
            fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]}
            name={category}
          />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

export default ExpenseStackedBarChart;