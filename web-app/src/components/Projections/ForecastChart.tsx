/**
 * Forecast chart with confidence intervals
 * Displays projected values with upper and lower bounds
 */

import { Box, Typography, useTheme, Paper } from "@mui/material";
import {
  LineChart,
  Line,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
  ComposedChart,
} from "recharts";
import { format, parseISO } from "date-fns";

interface ForecastChartProps {
  data: Array<{
    date: string;
    projected: number;
    lowerBound: number;
    upperBound: number;
  }>;
  title: string;
  height?: number;
  color?: string;
  showConfidenceInterval?: boolean;
}

function ForecastChart({
  data,
  title,
  height = 400,
  color,
  showConfidenceInterval = true,
}: ForecastChartProps) {
  const theme = useTheme();
  const lineColor = color || theme.palette.primary.main;

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
            {format(parseISO(label), "MMM dd, yyyy")}
          </Typography>
          {payload.map((entry: any, index: number) => {
            if (entry.dataKey === "projected") {
              return (
                <Typography
                  key={index}
                  variant="body2"
                  sx={{ color: entry.color }}
                >
                  Projected: $
                  {Math.abs(entry.value).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </Typography>
              );
            }
            return null;
          })}
          {showConfidenceInterval && payload[0] && (
            <>
              <Typography variant="body2" color="text.secondary">
                Upper Bound: $
                {Math.abs(payload[0].payload.upperBound).toLocaleString(
                  "en-US",
                  {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  }
                )}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lower Bound: $
                {Math.abs(payload[0].payload.lowerBound).toLocaleString(
                  "en-US",
                  {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  }
                )}
              </Typography>
            </>
          )}
        </Box>
      );
    }
    return null;
  };

  // Format data for confidence interval area
  const chartData = data.map((item) => ({
    ...item,
    confidenceRange: [item.lowerBound, item.upperBound],
  }));

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart
          data={chartData}
          margin={{ top: 10, right: 30, left: 20, bottom: 5 }}
        >
          <defs>
            <linearGradient id="confidenceGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={lineColor} stopOpacity={0.3} />
              <stop offset="95%" stopColor={lineColor} stopOpacity={0.05} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke={theme.palette.divider} />
          <XAxis
            dataKey="date"
            stroke={theme.palette.text.secondary}
            style={{ fontSize: "0.875rem" }}
            tickFormatter={(value) => format(parseISO(value), "MMM dd")}
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
          <ReferenceLine y={0} stroke={theme.palette.divider} strokeWidth={1} />

          {/* Confidence interval area */}
          {showConfidenceInterval && (
            <>
              <Area
                type="monotone"
                dataKey="upperBound"
                stroke="none"
                fill="url(#confidenceGradient)"
                fillOpacity={1}
                name="Upper Bound"
                legendType="none"
              />
              <Area
                type="monotone"
                dataKey="lowerBound"
                stroke="none"
                fill="white"
                fillOpacity={1}
                name="Lower Bound"
                legendType="none"
              />
              <Line
                type="monotone"
                dataKey="upperBound"
                stroke={lineColor}
                strokeWidth={1}
                strokeDasharray="3 3"
                dot={false}
                name="Confidence Interval"
              />
              <Line
                type="monotone"
                dataKey="lowerBound"
                stroke={lineColor}
                strokeWidth={1}
                strokeDasharray="3 3"
                dot={false}
                legendType="none"
              />
            </>
          )}

          {/* Projected line */}
          <Line
            type="monotone"
            dataKey="projected"
            name="Projected"
            stroke={lineColor}
            strokeWidth={3}
            dot={{ fill: lineColor, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </Paper>
  );
}

export default ForecastChart;

