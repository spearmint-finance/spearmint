/**
 * Projection parameter controls component
 * Allows users to configure projection settings
 */

import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Grid,
  Chip,
  Tooltip,
  IconButton,
} from "@mui/material";
import InfoIcon from "@mui/icons-material/Info";
import { ProjectionMethod } from "../../types/projection";

interface ProjectionControlsProps {
  projectionDays: number;
  method: ProjectionMethod;
  confidenceLevel: number;
  onProjectionDaysChange: (days: number) => void;
  onMethodChange: (method: ProjectionMethod) => void;
  onConfidenceLevelChange: (level: number) => void;
}

const PROJECTION_PRESETS = [
  { label: "1 Month", days: 30 },
  { label: "3 Months", days: 90 },
  { label: "6 Months", days: 180 },
  { label: "1 Year", days: 365 },
];

const METHOD_DESCRIPTIONS: Record<ProjectionMethod, string> = {
  [ProjectionMethod.LINEAR_REGRESSION]:
    "Trend-based projection using linear regression. Best for data with clear trends.",
  [ProjectionMethod.MOVING_AVERAGE]:
    "Simple moving average of recent data. Good for stable patterns.",
  [ProjectionMethod.EXPONENTIAL_SMOOTHING]:
    "Exponentially weighted moving average. Emphasizes recent data.",
  [ProjectionMethod.WEIGHTED_AVERAGE]:
    "Weighted average with more weight on recent data. Balanced approach.",
};

function ProjectionControls({
  projectionDays,
  method,
  confidenceLevel,
  onProjectionDaysChange,
  onMethodChange,
  onConfidenceLevelChange,
}: ProjectionControlsProps) {
  return (
    <Paper sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        Projection Settings
      </Typography>

      <Grid container spacing={3}>
        {/* Projection Timeframe */}
        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" gutterBottom>
            Projection Timeframe
          </Typography>
          <Box sx={{ mb: 2 }}>
            {PROJECTION_PRESETS.map((preset) => (
              <Chip
                key={preset.days}
                label={preset.label}
                onClick={() => onProjectionDaysChange(preset.days)}
                color={projectionDays === preset.days ? "primary" : "default"}
                sx={{ mr: 1, mb: 1 }}
              />
            ))}
          </Box>
          <Box sx={{ px: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {projectionDays} days
            </Typography>
            <Slider
              value={projectionDays}
              onChange={(_, value) => onProjectionDaysChange(value as number)}
              min={7}
              max={365}
              step={1}
              marks={[
                { value: 7, label: "1w" },
                { value: 90, label: "3m" },
                { value: 180, label: "6m" },
                { value: 365, label: "1y" },
              ]}
              valueLabelDisplay="auto"
            />
          </Box>
        </Grid>

        {/* Projection Method */}
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Projection Method</InputLabel>
            <Select
              value={method}
              label="Projection Method"
              onChange={(e) => onMethodChange(e.target.value as ProjectionMethod)}
            >
              <MenuItem value={ProjectionMethod.LINEAR_REGRESSION}>
                Linear Regression
              </MenuItem>
              <MenuItem value={ProjectionMethod.MOVING_AVERAGE}>
                Moving Average
              </MenuItem>
              <MenuItem value={ProjectionMethod.EXPONENTIAL_SMOOTHING}>
                Exponential Smoothing
              </MenuItem>
              <MenuItem value={ProjectionMethod.WEIGHTED_AVERAGE}>
                Weighted Average
              </MenuItem>
            </Select>
          </FormControl>
          <Box sx={{ mt: 1, display: "flex", alignItems: "center" }}>
            <Typography variant="caption" color="text.secondary">
              {METHOD_DESCRIPTIONS[method]}
            </Typography>
            <Tooltip title="Learn more about projection methods">
              <IconButton size="small">
                <InfoIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Grid>

        {/* Confidence Level */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Confidence Level: {(confidenceLevel * 100).toFixed(0)}%
          </Typography>
          <Box sx={{ px: 2 }}>
            <Slider
              value={confidenceLevel}
              onChange={(_, value) => onConfidenceLevelChange(value as number)}
              min={0.5}
              max={0.99}
              step={0.01}
              marks={[
                { value: 0.5, label: "50%" },
                { value: 0.68, label: "68%" },
                { value: 0.95, label: "95%" },
                { value: 0.99, label: "99%" },
              ]}
              valueLabelDisplay="auto"
              valueLabelFormat={(value) => `${(value * 100).toFixed(0)}%`}
            />
          </Box>
          <Typography variant="caption" color="text.secondary">
            Higher confidence levels result in wider prediction intervals
          </Typography>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default ProjectionControls;

