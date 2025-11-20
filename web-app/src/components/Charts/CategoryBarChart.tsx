import { Box, Typography, useTheme } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

interface CategoryBarChartProps {
  data: Array<{
    name: string;
    value: number;
    count?: number;
  }>;
  title?: string;
  height?: number;
  color?: string;
  horizontal?: boolean;
}

function CategoryBarChart({
  data,
  title,
  height = 300,
  color,
  horizontal = false,
}: CategoryBarChartProps) {
  const theme = useTheme();
  const barColor = color || theme.palette.primary.main;

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
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
            {data.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Amount: ${data.value.toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </Typography>
          {data.count !== undefined && (
            <Typography variant="body2" color="text.secondary">
              Transactions: {data.count}
            </Typography>
          )}
        </Box>
      );
    }
    return null;
  };

  // Truncate long category names
  const truncateName = (name: string, maxLength: number = 15) => {
    if (name.length <= maxLength) return name;
    return name.substring(0, maxLength) + "...";
  };

  return (
    <Box>
      {title && (
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <BarChart
          data={data}
          layout={horizontal ? "vertical" : "horizontal"}
          margin={{ top: 5, right: 30, left: horizontal ? 100 : 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
          {horizontal ? (
            <>
              <XAxis
                type="number"
                stroke={theme.palette.text.secondary}
                style={{ fontSize: "0.875rem" }}
                tickFormatter={(value) =>
                  `$${value.toLocaleString("en-US", {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0,
                  })}`
                }
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke={theme.palette.text.secondary}
                style={{ fontSize: "0.875rem" }}
                tickFormatter={(value) => truncateName(value)}
                width={90}
              />
            </>
          ) : (
            <>
              <XAxis
                dataKey="name"
                stroke={theme.palette.text.secondary}
                style={{ fontSize: "0.875rem" }}
                tickFormatter={(value) => truncateName(value, 10)}
                angle={-45}
                textAnchor="end"
                height={80}
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
            </>
          )}
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="value" fill={barColor} radius={[8, 8, 0, 0]}>
            {data.map((_entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={barColor}
                opacity={1 - (index * 0.1)}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
}

export default CategoryBarChart;

