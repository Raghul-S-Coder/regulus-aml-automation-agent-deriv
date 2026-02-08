import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import ThemeToggle from "@/app/components/ThemeToggle";
import { logout } from "@/app/api/auth";

const sidebarLinkClass = ({ isActive }: { isActive: boolean }) =>
  [
    "flex items-center rounded-lg px-3 py-2 text-sm font-medium transition",
    isActive
      ? "bg-surface-secondary text-brand shadow-soft"
      : "text-text-muted hover:text-brand hover:bg-surface-secondary"
  ].join(" ");

export default function MonitoringLayout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/regulus/login", { replace: true });
  };

  return (
    <div className="min-h-screen bg-surface text-text">
      <div className="flex min-h-screen">
        <aside className="w-64 border-r border-border bg-surface-secondary/60 px-4 py-6">
          <Link to="/regulus" className="mb-8 block text-lg font-semibold">
            RegulusAI
          </Link>
          <nav className="space-y-1">
            <NavLink to="/regulus/monitoring/dashboard" className={sidebarLinkClass}>
              Dashboard
            </NavLink>
            <NavLink to="/regulus/monitoring/transactions" className={sidebarLinkClass}>
              Transactions
            </NavLink>
            <NavLink to="/regulus/monitoring/alerts" className={sidebarLinkClass}>
              Alerts
            </NavLink>
            <NavLink to="/regulus/monitoring/cases" className={sidebarLinkClass}>
              Cases
            </NavLink>
          </nav>
        </aside>
        <div className="flex flex-1 flex-col">
          <header className="flex items-center justify-between border-b border-border px-6 py-4">
            <div>
              <h1 className="text-lg font-semibold">Monitoring</h1>
              <p className="text-sm text-text-muted">Compliance Manager Console</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="hidden rounded-full border border-border px-3 py-1 text-xs font-semibold text-text-muted sm:block">
                CM-0001 • Regulus Financial
              </div>
              <ThemeToggle />
              <button
                onClick={handleLogout}
                className="rounded-full border border-border px-3 py-1 text-sm text-text-muted hover:border-brand hover:text-brand"
              >
                Logout
              </button>
            </div>
          </header>
          <main className="flex-1 px-6 py-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
