import { createTheme } from '@mui/material/styles'

// Spearmint-themed color palette inspired by the logo
const theme = createTheme({
  palette: {
    primary: {
      main: '#43A047',      // Spearmint green
      light: '#66BB6A',     // Light mint green
      dark: '#2E7D32',      // Deep forest green
      contrastText: '#fff',
    },
    secondary: {
      main: '#26A69A',      // Teal/aqua accent
      light: '#4DB6AC',     // Light teal
      dark: '#00897B',      // Deep teal
      contrastText: '#fff',
    },
    success: {
      main: '#4CAF50',      // Bright green
      light: '#81C784',     // Light success green
      dark: '#388E3C',      // Dark success green
    },
    error: {
      main: '#E53935',
      light: '#EF5350',
      dark: '#C62828',
    },
    warning: {
      main: '#FF9800',
      light: '#FFB74D',
      dark: '#F57C00',
    },
    info: {
      main: '#29B6F6',      // Light blue (complementary)
      light: '#4FC3F7',
      dark: '#0288D1',
    },
    background: {
      default: '#F1F8E9',   // Very light mint background
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(46, 125, 50, 0.1)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 1px 3px rgba(46, 125, 50, 0.15)',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          '&.Mui-selected': {
            backgroundColor: 'rgba(67, 160, 71, 0.12)',
            '&:hover': {
              backgroundColor: 'rgba(67, 160, 71, 0.18)',
            },
          },
          '&:hover': {
            backgroundColor: 'rgba(67, 160, 71, 0.08)',
          },
        },
      },
    },
    MuiListItemIcon: {
      styleOverrides: {
        root: {
          color: '#43A047',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid rgba(67, 160, 71, 0.12)',
        },
      },
    },
  },
})

export default theme

