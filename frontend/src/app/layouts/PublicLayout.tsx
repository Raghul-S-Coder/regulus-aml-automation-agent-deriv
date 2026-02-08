import { Link, NavLink, Outlet } from "react-router-dom";
import ThemeToggle from "@/app/components/ThemeToggle";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  [
    "text-sm font-medium transition",
    isActive ? "text-brand" : "text-text-muted hover:text-brand"
  ].join(" ");

export default function PublicLayout() {
  return (
    <div className="min-h-screen bg-surface text-text">
      <header className="border-b border-border">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/regulus" className="text-xl font-semibold text-text">
            RegulusAI
          </Link>
          <nav className="flex items-center gap-6">
            <NavLink to="/regulus" className={navLinkClass} end>
              Home
            </NavLink>
            <NavLink to="/regulus/login" className={navLinkClass}>
              Login
            </NavLink>
            <ThemeToggle />
          </nav>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl px-6 py-10">
        <Outlet />
      </main>
      <footer className="border-t border-border">
        <div className="mx-auto w-full max-w-6xl px-6 py-6 text-sm text-text-muted">
          RegulusAI — AI-powered transaction monitoring
        </div>
      </footer>
    </div>
  );
}
