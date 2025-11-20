/**
 * Classification Manager Component
 * Main container with tabs for Types, Rules, and Reconciliation
 */

import { useState } from "react";
import { Box, Tabs, Tab, Paper } from "@mui/material";
import CategoryIcon from "@mui/icons-material/Category";
import RuleIcon from "@mui/icons-material/Rule";
import AssignmentIcon from "@mui/icons-material/Assignment";
import ClassificationTypesTab from "./ClassificationTypesTab";
import ClassificationRulesList from "./ClassificationRulesList";
import ReconciliationDashboard from "./ReconciliationDashboard";

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
      id={`classification-tabpanel-${index}`}
      aria-labelledby={`classification-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

function ClassificationManager() {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <Box>
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="classification management tabs"
        >
          <Tab
            icon={<CategoryIcon />}
            label="Classification Types"
            iconPosition="start"
          />
          <Tab
            icon={<RuleIcon />}
            label="Classification Rules"
            iconPosition="start"
          />
          <Tab
            icon={<AssignmentIcon />}
            label="Reconciliation"
            iconPosition="start"
          />
        </Tabs>
      </Paper>

      <TabPanel value={currentTab} index={0}>
        <ClassificationTypesTab />
      </TabPanel>

      <TabPanel value={currentTab} index={1}>
        <ClassificationRulesList />
      </TabPanel>

      <TabPanel value={currentTab} index={2}>
        <ReconciliationDashboard />
      </TabPanel>
    </Box>
  );
}

export default ClassificationManager;

