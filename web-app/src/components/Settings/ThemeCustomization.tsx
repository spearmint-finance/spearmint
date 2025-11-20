/**
 * Theme Customization Component
 * Allows users to customize the application theme
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
  Card,
  CardContent,
  Radio,
  RadioGroup,
  FormControl,
  FormLabel,
} from '@mui/material';
import {
  Save as SaveIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon,
  SettingsBrightness as AutoModeIcon,
} from '@mui/icons-material';
import type { ThemeSettings } from '../../types/settings';

const DEFAULT_THEME: ThemeSettings = {
  mode: 'light',
  primaryColor: '#1976d2',
  secondaryColor: '#dc004e',
  fontSize: 'medium',
  fontFamily: 'Roboto, sans-serif',
  compactMode: false,
};

const PRESET_COLORS = [
  { name: 'Blue', value: '#1976d2' },
  { name: 'Purple', value: '#9c27b0' },
  { name: 'Green', value: '#2e7d32' },
  { name: 'Orange', value: '#ed6c02' },
  { name: 'Red', value: '#d32f2f' },
  { name: 'Teal', value: '#00897b' },
];

export default function ThemeCustomization() {
  const [theme, setTheme] = useState<ThemeSettings>(DEFAULT_THEME);
  const [saved, setSaved] = useState(false);

  // Load theme from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('themeSettings');
    if (stored) {
      try {
        setTheme(JSON.parse(stored));
      } catch (err) {
        console.error('Failed to parse stored theme:', err);
      }
    }
  }, []);

  const handleSave = () => {
    localStorage.setItem('themeSettings', JSON.stringify(theme));
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
    
    // Trigger a custom event to notify the app of theme change
    window.dispatchEvent(new CustomEvent('themeChange', { detail: theme }));
  };

  const handleReset = () => {
    setTheme(DEFAULT_THEME);
    localStorage.removeItem('themeSettings');
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
    
    // Trigger theme change event
    window.dispatchEvent(new CustomEvent('themeChange', { detail: DEFAULT_THEME }));
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">Theme Customization</Typography>
        <Box display="flex" gap={1}>
          <Button onClick={handleReset} variant="outlined">
            Reset to Defaults
          </Button>
          <Button onClick={handleSave} variant="contained" startIcon={<SaveIcon />}>
            Save Theme
          </Button>
        </Box>
      </Box>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Theme settings saved successfully! Refresh the page to see changes.
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          {/* Theme Mode */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Appearance Mode
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12}>
            <FormControl component="fieldset">
              <RadioGroup
                row
                value={theme.mode}
                onChange={(e) =>
                  setTheme({ ...theme, mode: e.target.value as 'light' | 'dark' | 'system' })
                }
              >
                <Card
                  sx={{
                    mr: 2,
                    cursor: 'pointer',
                    border: theme.mode === 'light' ? 2 : 1,
                    borderColor: theme.mode === 'light' ? 'primary.main' : 'divider',
                  }}
                  onClick={() => setTheme({ ...theme, mode: 'light' })}
                >
                  <CardContent sx={{ textAlign: 'center', py: 2 }}>
                    <LightModeIcon sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="body2">Light</Typography>
                    <Radio value="light" checked={theme.mode === 'light'} />
                  </CardContent>
                </Card>

                <Card
                  sx={{
                    mr: 2,
                    cursor: 'pointer',
                    border: theme.mode === 'dark' ? 2 : 1,
                    borderColor: theme.mode === 'dark' ? 'primary.main' : 'divider',
                  }}
                  onClick={() => setTheme({ ...theme, mode: 'dark' })}
                >
                  <CardContent sx={{ textAlign: 'center', py: 2 }}>
                    <DarkModeIcon sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="body2">Dark</Typography>
                    <Radio value="dark" checked={theme.mode === 'dark'} />
                  </CardContent>
                </Card>

                <Card
                  sx={{
                    cursor: 'pointer',
                    border: theme.mode === 'system' ? 2 : 1,
                    borderColor: theme.mode === 'system' ? 'primary.main' : 'divider',
                  }}
                  onClick={() => setTheme({ ...theme, mode: 'system' })}
                >
                  <CardContent sx={{ textAlign: 'center', py: 2 }}>
                    <AutoModeIcon sx={{ fontSize: 40, mb: 1 }} />
                    <Typography variant="body2">System</Typography>
                    <Radio value="system" checked={theme.mode === 'system'} />
                  </CardContent>
                </Card>
              </RadioGroup>
            </FormControl>
          </Grid>

          {/* Colors */}
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Colors
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Primary Color
            </Typography>
            <Box display="flex" gap={1} flexWrap="wrap" mb={2}>
              {PRESET_COLORS.map((color) => (
                <Box
                  key={color.value}
                  onClick={() => setTheme({ ...theme, primaryColor: color.value })}
                  sx={{
                    width: 60,
                    height: 60,
                    backgroundColor: color.value,
                    borderRadius: 1,
                    cursor: 'pointer',
                    border: theme.primaryColor === color.value ? 3 : 1,
                    borderColor: theme.primaryColor === color.value ? 'text.primary' : 'divider',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    '&:hover': {
                      opacity: 0.8,
                    },
                  }}
                >
                  <Typography variant="caption" sx={{ color: 'white', fontWeight: 'bold' }}>
                    {color.name}
                  </Typography>
                </Box>
              ))}
              <TextField
                type="color"
                value={theme.primaryColor}
                onChange={(e) => setTheme({ ...theme, primaryColor: e.target.value })}
                sx={{ width: 60 }}
                title="Custom color"
              />
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Secondary Color
            </Typography>
            <Box display="flex" gap={1} flexWrap="wrap">
              {PRESET_COLORS.map((color) => (
                <Box
                  key={color.value}
                  onClick={() => setTheme({ ...theme, secondaryColor: color.value })}
                  sx={{
                    width: 60,
                    height: 60,
                    backgroundColor: color.value,
                    borderRadius: 1,
                    cursor: 'pointer',
                    border: theme.secondaryColor === color.value ? 3 : 1,
                    borderColor: theme.secondaryColor === color.value ? 'text.primary' : 'divider',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    '&:hover': {
                      opacity: 0.8,
                    },
                  }}
                >
                  <Typography variant="caption" sx={{ color: 'white', fontWeight: 'bold' }}>
                    {color.name}
                  </Typography>
                </Box>
              ))}
              <TextField
                type="color"
                value={theme.secondaryColor}
                onChange={(e) => setTheme({ ...theme, secondaryColor: e.target.value })}
                sx={{ width: 60 }}
                title="Custom color"
              />
            </Box>
          </Grid>

          {/* Typography */}
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Typography
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Font Size"
              value={theme.fontSize}
              onChange={(e) =>
                setTheme({ ...theme, fontSize: e.target.value as 'small' | 'medium' | 'large' })
              }
            >
              <MenuItem value="small">Small</MenuItem>
              <MenuItem value="medium">Medium</MenuItem>
              <MenuItem value="large">Large</MenuItem>
            </TextField>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              select
              fullWidth
              label="Font Family"
              value={theme.fontFamily}
              onChange={(e) => setTheme({ ...theme, fontFamily: e.target.value })}
            >
              <MenuItem value="Roboto, sans-serif">Roboto (Default)</MenuItem>
              <MenuItem value="Arial, sans-serif">Arial</MenuItem>
              <MenuItem value="'Times New Roman', serif">Times New Roman</MenuItem>
              <MenuItem value="'Courier New', monospace">Courier New</MenuItem>
              <MenuItem value="Georgia, serif">Georgia</MenuItem>
            </TextField>
          </Grid>

          {/* Layout */}
          <Grid item xs={12} sx={{ mt: 2 }}>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Layout
            </Typography>
            <Divider sx={{ mb: 2 }} />
          </Grid>

          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Switch
                  checked={theme.compactMode}
                  onChange={(e) => setTheme({ ...theme, compactMode: e.target.checked })}
                />
              }
              label="Compact Mode (reduces spacing and padding)"
            />
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}

