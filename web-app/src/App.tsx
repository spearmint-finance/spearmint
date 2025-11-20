import { ThemeProvider } from "@mui/material/styles";
import { Routes, Route, Navigate } from "react-router-dom";
import theme from "./theme";
import Layout from "./components/common/Layout";
import Dashboard from "./components/Dashboard/Dashboard";
import AccountsPage from "./components/Accounts/AccountsPage";
import TransactionList from "./components/Transactions/TransactionList";
import AnalysisPage from "./components/Analysis/AnalysisPage";
import IncomeDeepDivePage from "./components/Analysis/Income/IncomeDeepDivePage";
import ExpenseDeepDivePage from "./components/Analysis/Expenses/ExpenseDeepDivePage";
import ProjectionsPage from "./components/Projections/ProjectionsPage";
import ClassificationsPage from "./components/Classifications/ClassificationsPage";
import ImportPage from "./components/Import/ImportPage";
import SettingsPage from "./components/Settings/SettingsPage";
import ScenarioBuilder from "./components/Scenarios/ScenarioBuilder";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="accounts" element={<AccountsPage />} />
          <Route path="transactions" element={<TransactionList />} />
          <Route path="analysis" element={<AnalysisPage />} />
          <Route path="analysis/income" element={<IncomeDeepDivePage />} />
          <Route path="analysis/expenses" element={<ExpenseDeepDivePage />} />
          <Route path="scenarios" element={<ScenarioBuilder />} />
          <Route path="projections" element={<ProjectionsPage />} />
          <Route path="classifications" element={<ClassificationsPage />} />
          <Route path="import" element={<ImportPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;
