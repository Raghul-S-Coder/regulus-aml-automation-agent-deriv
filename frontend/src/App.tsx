import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import AppRoutes from "@/app/routes";

function SessionExpiryPopup() {
  const navigate = useNavigate();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handler = () => setVisible(true);
    window.addEventListener("session-expired", handler);
    return () => window.removeEventListener("session-expired", handler);
  }, []);

  if (!visible) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4">
      <div className="w-full max-w-sm rounded-2xl border border-border bg-surface-secondary p-6 text-center">
        <h3 className="text-lg font-semibold">Session Expired</h3>
        <p className="mt-2 text-sm text-text-muted">
          Your session has expired. Please sign in again.
        </p>
        <button
          onClick={() => {
            setVisible(false);
            navigate("/regulus", { replace: true });
          }}
          className="mt-4 w-full rounded-full bg-brand px-4 py-2 text-sm font-semibold text-brand-foreground shadow-soft"
        >
          Go to Home
        </button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <>
      <SessionExpiryPopup />
      <AppRoutes />
    </>
  );
}
