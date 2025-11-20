import { useState } from "react";
import {
  Box,
  Button,
  Menu,
  MenuItem,
  TextField,
  Stack,
  Typography,
  Divider,
} from "@mui/material";
import CalendarTodayIcon from "@mui/icons-material/CalendarToday";
import { format, subDays, subMonths, startOfMonth, startOfYear } from "date-fns";

export interface DateRange {
  start_date: string;
  end_date: string;
}

interface DateRangePickerProps {
  value: DateRange;
  onChange: (range: DateRange) => void;
}

const presetRanges = [
  {
    label: "Last 7 Days",
    getValue: () => ({
      start_date: format(subDays(new Date(), 7), "yyyy-MM-dd"),
      end_date: format(new Date(), "yyyy-MM-dd"),
    }),
  },
  {
    label: "Last 30 Days",
    getValue: () => ({
      start_date: format(subDays(new Date(), 30), "yyyy-MM-dd"),
      end_date: format(new Date(), "yyyy-MM-dd"),
    }),
  },
  {
    label: "Last 3 Months",
    getValue: () => ({
      start_date: format(subMonths(new Date(), 3), "yyyy-MM-dd"),
      end_date: format(new Date(), "yyyy-MM-dd"),
    }),
  },
  {
    label: "This Month",
    getValue: () => ({
      start_date: format(startOfMonth(new Date()), "yyyy-MM-dd"),
      end_date: format(new Date(), "yyyy-MM-dd"),
    }),
  },
  {
    label: "Year to Date",
    getValue: () => ({
      start_date: format(startOfYear(new Date()), "yyyy-MM-dd"),
      end_date: format(new Date(), "yyyy-MM-dd"),
    }),
  },
  {
    label: "All Time",
    getValue: () => ({
      start_date: "",
      end_date: "",
    }),
  },
];

function DateRangePicker({ value, onChange }: DateRangePickerProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [customStart, setCustomStart] = useState(value.start_date);
  const [customEnd, setCustomEnd] = useState(value.end_date);
  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handlePresetSelect = (range: DateRange) => {
    onChange(range);
    setCustomStart(range.start_date);
    setCustomEnd(range.end_date);
    handleClose();
  };

  const handleCustomApply = () => {
    if (customStart && customEnd && customStart <= customEnd) {
      onChange({ start_date: customStart, end_date: customEnd });
      handleClose();
    }
  };

  const getDisplayText = () => {
    if (!value.start_date && !value.end_date) {
      return "All Time";
    }
    if (value.start_date && value.end_date) {
      return `${format(new Date(value.start_date), "MMM d, yyyy")} - ${format(
        new Date(value.end_date),
        "MMM d, yyyy"
      )}`;
    }
    return "Select Date Range";
  };

  return (
    <Box>
      <Button
        variant="outlined"
        startIcon={<CalendarTodayIcon />}
        onClick={handleClick}
        sx={{ minWidth: 250 }}
      >
        {getDisplayText()}
      </Button>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        PaperProps={{
          sx: { minWidth: 320 },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Preset Ranges
          </Typography>
          {presetRanges.map((preset) => (
            <MenuItem
              key={preset.label}
              onClick={() => handlePresetSelect(preset.getValue())}
              sx={{ borderRadius: 1, mb: 0.5 }}
            >
              {preset.label}
            </MenuItem>
          ))}
        </Box>
        <Divider />
        <Box sx={{ p: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Custom Range
          </Typography>
          <Stack spacing={2} sx={{ mt: 1 }}>
            <TextField
              label="Start Date"
              type="date"
              value={customStart}
              onChange={(e) => setCustomStart(e.target.value)}
              InputLabelProps={{ shrink: true }}
              fullWidth
              size="small"
            />
            <TextField
              label="End Date"
              type="date"
              value={customEnd}
              onChange={(e) => setCustomEnd(e.target.value)}
              InputLabelProps={{ shrink: true }}
              fullWidth
              size="small"
              inputProps={{
                min: customStart,
              }}
            />
            <Button
              variant="contained"
              onClick={handleCustomApply}
              disabled={!customStart || !customEnd || customStart > customEnd}
              fullWidth
            >
              Apply
            </Button>
          </Stack>
        </Box>
      </Menu>
    </Box>
  );
}

export default DateRangePicker;
