import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import PublicLayout from "@/app/layouts/PublicLayout";
import MonitoringLayout from "@/app/layouts/MonitoringLayout";
import HomePage from "@/app/pages/HomePage";
import LoginPage from "@/app/pages/LoginPage";
import SignupPage from "@/app/pages/SignupPage";
import TransactionDemoPage from "@/app/pages/TransactionDemoPage";
import DashboardPage from "@/app/pages/DashboardPage";
import TransactionsPage from "@/app/pages/TransactionsPage";
import AlertsPage from "@/app/pages/AlertsPage";
import CasesPage from "@/app/pages/CasesPage";
import CaseDetailsPage from "@/app/pages/CaseDetailsPage";
import { useAuth } from "@/app/hooks/useAuth";

function RequireAuth() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/regulus/login" replace />;
  }

  return <Outlet />;
}

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/regulus" element={<PublicLayout />}>
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="signup" element={<SignupPage />} />
        <Route path="transaction-simulation" element={<TransactionDemoPage />} />
      </Route>

      <Route element={<RequireAuth />}>
        <Route path="/regulus/monitoring" element={<MonitoringLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="transactions" element={<TransactionsPage />} />
          <Route path="alerts" element={<AlertsPage />} />
          <Route path="cases" element={<CasesPage />} />
          <Route path="cases/:caseId" element={<CaseDetailsPage />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/regulus" replace />} />
    </Routes>
  );
}
