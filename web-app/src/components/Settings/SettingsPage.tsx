/**
 * Settings Page
 * Main settings page with tabs for different configuration sections
 */

import { useState } from "react";
import { Box, Typography, Tabs, Tab, Paper } from "@mui/material";
import {
  Category as CategoryIcon,
  Tune as TuneIcon,
  Palette as PaletteIcon,
  VpnKey as VpnKeyIcon,
} from "@mui/icons-material";
import CategoryManagement from "./CategoryManagement";
import UserPreferences from "./UserPreferences";
import ThemeCustomization from "./ThemeCustomization";
import APIKeysManagement from "./APIKeysManagement";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `settings-tab-${index}`,
    "aria-controls": `settings-tabpanel-${index}`,
  };
}

export default function SettingsPage() {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", overflow: "hidden" }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Paper sx={{ width: "100%" }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="settings tabs"
          sx={{ borderBottom: 1, borderColor: "divider" }}
        >
          <Tab icon={<CategoryIcon />} label="Categories" {...a11yProps(0)} />
          <Tab icon={<TuneIcon />} label="Preferences" {...a11yProps(1)} />
          <Tab icon={<PaletteIcon />} label="Theme" {...a11yProps(2)} />
          <Tab icon={<VpnKeyIcon />} label="API Keys" {...a11yProps(3)} />
        </Tabs>

        <Box sx={{ p: 3 }}>
          <TabPanel value={currentTab} index={0}>
            <CategoryManagement />
          </TabPanel>
          <TabPanel value={currentTab} index={1}>
            <UserPreferences />
          </TabPanel>
          <TabPanel value={currentTab} index={2}>
            <ThemeCustomization />
          </TabPanel>
          <TabPanel value={currentTab} index={3}>
            <APIKeysManagement />
          </TabPanel>
        </Box>
      </Paper>
    </Box>
  );
}
