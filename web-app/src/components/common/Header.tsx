import { AppBar, Toolbar, Typography, IconButton, Box } from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'
import logo from '../../assets/logo.jpg'

interface HeaderProps {
  drawerWidth: number
  onMenuClick: () => void
}

function Header({ drawerWidth, onMenuClick }: HeaderProps) {
  return (
    <AppBar
      position="fixed"
      sx={{
        width: { md: `calc(100% - ${drawerWidth}px)` },
        ml: { md: `${drawerWidth}px` },
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={onMenuClick}
          sx={{ mr: 2, display: { md: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        <Box
          component="img"
          src={logo}
          alt="Spearmint Finance Logo"
          sx={{
            height: 40,
            width: 40,
            borderRadius: '50%',
            mr: 2,
            objectFit: 'cover',
          }}
        />
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          Spearmint Finance
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {/* Future: Add user menu, notifications, etc. */}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header

