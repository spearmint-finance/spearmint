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
  Select,
  MenuItem,
  FormControl,
} from "@mui/material";
import { useState } from "react";
import { useEntityContext } from "../../contexts/EntityContext";
import { ENTITY_TYPE_LABELS } from "../../types/entity";
import ManageEntitiesDialog from "../Entities/ManageEntitiesDialog";
import DashboardIcon from "@mui/icons-material/Dashboard";
import logo from "../../assets/logo.jpg";
import ReceiptIcon from "@mui/icons-material/Receipt";
import BarChartIcon from "@mui/icons-material/BarChart";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import SettingsIcon from "@mui/icons-material/Settings";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import PsychologyIcon from "@mui/icons-material/Psychology";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import AssessmentIcon from "@mui/icons-material/Assessment";
import SavingsIcon from "@mui/icons-material/Savings";

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
  { text: "Budgets", icon: <SavingsIcon />, path: "/budgets" },
  { text: "Analysis", icon: <BarChartIcon />, path: "/analysis" },
  { text: "Reports", icon: <AssessmentIcon />, path: "/reports" },
  { text: "Scenarios", icon: <PsychologyIcon />, path: "/scenarios" },
  { text: "Projections", icon: <TrendingUpIcon />, path: "/projections" },
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
  const { entities, selectedEntityId, setSelectedEntityId } =
    useEntityContext();
  const [manageEntitiesOpen, setManageEntitiesOpen] = useState(false);

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
      <Box sx={{ px: 2, py: 1.5 }}>
        <FormControl fullWidth size="small">
          <Select
            value={selectedEntityId ?? "all"}
            onChange={(e) => {
              const val = e.target.value;
              if (val === "manage") {
                setManageEntitiesOpen(true);
                return;
              }
              setSelectedEntityId(val === "all" ? null : Number(val));
            }}
            sx={{ fontSize: "0.85rem" }}
          >
            <MenuItem value="all">
              {entities.length > 0 ? "All Entities" : "Personal"}
            </MenuItem>
            {entities.map((entity) => (
              <MenuItem key={entity.entity_id} value={entity.entity_id}>
                {entity.entity_name}
                <Typography
                  component="span"
                  variant="caption"
                  sx={{ ml: 1, color: "text.secondary" }}
                >
                  {ENTITY_TYPE_LABELS[entity.entity_type] || entity.entity_type}
                  {entity.account_count > 0 && ` · ${entity.account_count}`}
                </Typography>
              </MenuItem>
            ))}
            <Divider />
            <MenuItem value="manage" sx={{ color: "primary.main", fontWeight: 500 }}>
              Manage Entities...
            </MenuItem>
          </Select>
        </FormControl>
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
      <ManageEntitiesDialog
        open={manageEntitiesOpen}
        onClose={() => setManageEntitiesOpen(false)}
      />
    </>
  );
}

export default Sidebar;
