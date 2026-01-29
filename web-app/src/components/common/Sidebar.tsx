import { useNavigate, useLocation } from "react-router-dom";
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
} from "@mui/material";
import DashboardIcon from "@mui/icons-material/Dashboard";
import logo from "../../assets/logo.jpg";
import ReceiptIcon from "@mui/icons-material/Receipt";
import BarChartIcon from "@mui/icons-material/BarChart";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import CategoryIcon from "@mui/icons-material/Category";
import SettingsIcon from "@mui/icons-material/Settings";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import PsychologyIcon from "@mui/icons-material/Psychology";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";

interface SidebarProps {
  drawerWidth: number;
  mobileOpen: boolean;
  onDrawerToggle: () => void;
  isMobile: boolean;
}

const menuItems = [
  { text: "Dashboard", icon: <DashboardIcon />, path: "/dashboard" },
  { text: "Accounts", icon: <AccountBalanceIcon />, path: "/accounts" },
  { text: "Transactions", icon: <ReceiptIcon />, path: "/transactions" },
  { text: "Analysis", icon: <BarChartIcon />, path: "/analysis" },
  { text: "Scenarios", icon: <PsychologyIcon />, path: "/scenarios" },
  { text: "Projections", icon: <TrendingUpIcon />, path: "/projections" },
  { text: "Classifications", icon: <CategoryIcon />, path: "/classifications" },
  { text: "Import", icon: <UploadFileIcon />, path: "/import" },
];

const bottomMenuItems = [
  { text: "Settings", icon: <SettingsIcon />, path: "/settings" },
];

function Sidebar({
  drawerWidth,
  mobileOpen,
  onDrawerToggle,
  isMobile,
}: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      onDrawerToggle();
    }
  };

  const drawer = (
    <>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          py: 2,
          px: 2,
          minHeight: 64,
          background: "linear-gradient(135deg, #E8F5E9 0%, #B2DFDB 100%)",
        }}
      >
        <Box
          component="img"
          src={logo}
          alt="Spearmint Finance"
          sx={{
            height: 48,
            width: 48,
            borderRadius: "50%",
            objectFit: "cover",
            boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
            mb: 1,
          }}
        />
        <Typography
          variant="subtitle2"
          sx={{
            fontWeight: 600,
            color: "primary.dark",
            letterSpacing: "0.5px",
          }}
        >
          Spearmint Finance
        </Typography>
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List sx={{ mt: "auto" }}>
        {bottomMenuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </>
  );

  return (
    <>
      {/* Mobile drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={onDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better mobile performance
        }}
        sx={{
          display: { xs: "block", md: "none" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
      >
        {drawer}
      </Drawer>
      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", md: "block" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
        open
      >
        {drawer}
      </Drawer>
    </>
  );
}

export default Sidebar;
