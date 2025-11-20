import { useEffect, useRef, useState } from "react";
import { Box, Typography } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";

interface CategoryPieChartProps {
  data: Array<{
    name: string;
    value: number;
    percentage?: number;
  }>;
  title?: string;
  height?: number;
  colors?: string[];
  colorScheme?: "success" | "error" | "default";
}

// Color palettes
const DEFAULT_COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#8884D8",
  "#82CA9D",
  "#FFC658",
  "#FF6B9D",
  "#C084FC",
  "#34D399",
];

const SUCCESS_COLORS = [
  "#4CAF50",
  "#66BB6A",
  "#81C784",
  "#A5D6A7",
  "#C8E6C9",
  "#43A047",
  "#388E3C",
  "#2E7D32",
  "#1B5E20",
  "#689F38",
];

const ERROR_COLORS = [
  "#F44336",
  "#EF5350",
  "#E57373",
  "#EF9A9A",
  "#FFCDD2",
  "#E53935",
  "#D32F2F",
  "#C62828",
  "#B71C1C",
  "#FF5722",
];

function CategoryPieChart({
  data,
  title,
  height = 300,
  colors,
  colorScheme = "default",
}: CategoryPieChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [chartWidth, setChartWidth] = useState(400);

  useEffect(() => {
    const updateWidth = () => {
      if (containerRef.current) {
        // Get the actual width of the container and subtract padding
        const containerWidth = containerRef.current.offsetWidth;
        // Set chart width to be slightly less than container to prevent overflow
        setChartWidth(Math.max(300, containerWidth - 20));
      }
    };

    updateWidth();
    window.addEventListener("resize", updateWidth);

    // Update on next tick to ensure container is properly rendered
    setTimeout(updateWidth, 0);

    return () => window.removeEventListener("resize", updateWidth);
  }, []);

  // Choose color palette based on colorScheme
  const selectedColors =
    colorScheme === "success"
      ? SUCCESS_COLORS
      : colorScheme === "error"
      ? ERROR_COLORS
      : colors || DEFAULT_COLORS;

  // Custom tooltip component
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload[0]) {
      return (
        <Box
          sx={{
            bgcolor: "background.paper",
            border: 1,
            borderColor: "divider",
            p: 1.5,
            borderRadius: 1,
            boxShadow: 2,
          }}
        >
          <Typography variant="body2" fontWeight="bold">
            {label}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            ${payload[0].value.toLocaleString()}
          </Typography>
          {payload[0].payload.percentage && (
            <Typography variant="caption" color="text.secondary">
              {payload[0].payload.percentage.toFixed(1)}% of total
            </Typography>
          )}
        </Box>
      );
    }
    return null;
  };

  const formatXAxis = (value: number) => {
    if (value >= 1000000) {
      return `$${(value / 1000000).toFixed(1)}M`;
    } else if (value >= 1000) {
      return `$${(value / 1000).toFixed(0)}k`;
    }
    return `$${value.toFixed(0)}`;
  };

  return (
    <div ref={containerRef} style={{ width: "100%", height: height }}>
      {title && (
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
      )}
      <BarChart
        width={chartWidth}
        height={height - (title ? 40 : 0)}
        data={data}
        layout="vertical"
        margin={{ top: 5, right: 90, left: 10, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          type="number"
          tickFormatter={formatXAxis}
          domain={[0, (dataMax: number) => dataMax * 1.06]}
        />
        <YAxis
          type="category"
          dataKey="name"
          width={120}
          tick={{ fill: "#000000", fontSize: 11 }}
          interval={0}
        />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="value" radius={[0, 8, 8, 0]}>
          {data.map((_entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={selectedColors[index % selectedColors.length]}
            />
          ))}
        </Bar>
      </BarChart>
    </div>
  );
}

export default CategoryPieChart;
