/**
 * User Preferences Component
 * Allows users to configure default settings and preferences
 */

import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  MenuItem,
  Button,
  Grid,
  FormControlLabel,
  Switch,
  Alert,
  Divider,
} from '@mui/material';
import { Save as SaveIcon } from '@mui/icons-material';
import type { UserPreferences } from '../../types/settings';

const DEFAULT_PREFERENCES: UserPreferences = {
  defaultDateRange: 'month',
  currencySymbol: '$',
  currencyPosition: 'before',
  decimalPlaces: 2,
  thousandsSeparator: ',',
  decimalSeparator: '.',
  dateFormat: 'MM/DD/YYYY',
  timeFormat: '12h',
  firstDayOfWeek: 0,
  enableNotifications: false,
};

export default function UserPreferencesComponent() {
  const [preferences, setPreferences] = useState<UserPreferences>(DEFAULT_PREFERENCES);
  const [saved, setSaved] = useState(false);

  // Load preferences from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('userPreferences');
    if (stored) {
      try {
        setPreferences(JSON.parse(stored));
      } catch (err) {
        console.error('Failed to parse stored preferences:', err);
      }
    }
  }, []);

  const handleSave = () => {
    localStorage.setItem('userPreferences', JSON.stringify(preferences));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    setPreferences(DEFAULT_PREFERENCES);
    localStorage.removeItem('userPreferences');
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const formatExample = () => {
    const amount = 1234567.89;
    const { currencySymbol, currencyPosition, decimalPlaces, thousandsSeparator, decimalSeparator } =
      preferences;

    const integerPart = Math.floor(amount)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, thousandsSeparator);
    const decimalPart = amount.toFixed(decimalPlaces).split('.')[1];
    const formattedAmount = `${integerPart}${decimalSeparator}${decimalPart}`;

    return currencyPosition === 'before'
      ? `${currencySymbol}${formattedAmount}`
      : `${formattedAmount}${currencySymbol}`;
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">User Preferences</Typography>
        <Box display="flex" gap={1}>
          <Button onClick={handleReset} variant="outlined">
            Reset to Defaults
          </Button>
          <Button onClick={handleSave} variant="contained" startIcon={<SaveIcon />}>
            Save Preferences
          </Button>
        </Box>
      </Box>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Preferences saved successfully!
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          {/* Date & Time Settings */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Date & Time
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Default Date Range"
              value={preferences.defaultDateRange}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  defaultDateRange: e.target.value as UserPreferences['defaultDateRange'],
                })
              }
            >
              <MenuItem value="week">Last Week</MenuItem>
              <MenuItem value="month">Last Month</MenuItem>
              <MenuItem value="quarter">Last Quarter</MenuItem>
              <MenuItem value="year">Last Year</MenuItem>
              <MenuItem value="custom">Custom</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Date Format"
              value={preferences.dateFormat}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  dateFormat: e.target.value as UserPreferences['dateFormat'],
                })
              }
            >
              <MenuItem value="MM/DD/YYYY">MM/DD/YYYY (12/31/2024)</MenuItem>
              <MenuItem value="DD/MM/YYYY">DD/MM/YYYY (31/12/2024)</MenuItem>
              <MenuItem value="YYYY-MM-DD">YYYY-MM-DD (2024-12-31)</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Time Format"
              value={preferences.timeFormat}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  timeFormat: e.target.value as UserPreferences['timeFormat'],
                })
              }
            >
              <MenuItem value="12h">12-hour (3:30 PM)</MenuItem>
              <MenuItem value="24h">24-hour (15:30)</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="First Day of Week"
              value={preferences.firstDayOfWeek}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  firstDayOfWeek: Number(e.target.value) as 0 | 1,
                })
              }
            >
              <MenuItem value={0}>Sunday</MenuItem>
              <MenuItem value={1}>Monday</MenuItem>
            </TextField>
          </Grid>

          {/* Currency Settings */}
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Currency & Number Formatting
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Currency Symbol"
              value={preferences.currencySymbol}
              onChange={(e) =>
                setPreferences({ ...preferences, currencySymbol: e.target.value })
              }
              placeholder="$"
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Currency Position"
              value={preferences.currencyPosition}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  currencyPosition: e.target.value as 'before' | 'after',
                })
              }
            >
              <MenuItem value="before">Before ($1,234.56)</MenuItem>
              <MenuItem value="after">After (1,234.56$)</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              select
              fullWidth
              label="Decimal Places"
              value={preferences.decimalPlaces}
              onChange={(e) =>
                setPreferences({ ...preferences, decimalPlaces: Number(e.target.value) })
              }
            >
              <MenuItem value={0}>0</MenuItem>
              <MenuItem value={1}>1</MenuItem>
              <MenuItem value={2}>2</MenuItem>
              <MenuItem value={3}>3</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              select
              fullWidth
              label="Thousands Separator"
              value={preferences.thousandsSeparator}
              onChange={(e) =>
                setPreferences({ ...preferences, thousandsSeparator: e.target.value })
              }
            >
              <MenuItem value=",">, (comma)</MenuItem>
              <MenuItem value=".">. (period)</MenuItem>
              <MenuItem value=" ">(space)</MenuItem>
              <MenuItem value="">(none)</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              select
              fullWidth
              label="Decimal Separator"
              value={preferences.decimalSeparator}
              onChange={(e) =>
                setPreferences({ ...preferences, decimalSeparator: e.target.value as '.' | ',' })
              }
            >
              <MenuItem value=".">. (period)</MenuItem>
              <MenuItem value=",">, (comma)</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12}>
            <Alert severity="info">
              <Typography variant="body2">
                <strong>Preview:</strong> {formatExample()}
              </Typography>
            </Alert>
          </Grid>

          {/* Notifications */}
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Notifications
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Switch
                  checked={preferences.enableNotifications}
                  onChange={(e) =>
                    setPreferences({ ...preferences, enableNotifications: e.target.checked })
                  }
                />
              }
              label="Enable email notifications"
            />
          </Grid>

          {preferences.enableNotifications && (
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                type="email"
                label="Notification Email"
                value={preferences.notificationEmail || ''}
                onChange={(e) =>
                  setPreferences({ ...preferences, notificationEmail: e.target.value })
                }
                placeholder="your@email.com"
              />
            </Grid>
          )}
        </Grid>
      </Paper>
    </Box>
  );
}

