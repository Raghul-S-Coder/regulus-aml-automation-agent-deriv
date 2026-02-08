import { useMemo, useState } from "react";
import { EmptyState, ErrorState, LoadingState } from "@/app/components/States";
import { listAlerts } from "@/app/api/alerts";
import { useApi } from "@/app/hooks/useApi";

type AlertRow = {
  id: string;
  account: string;
  severity: "low" | "medium" | "high";
  rule: string;
  description: string;
  date: string;
};

const severityStyle = (severity: AlertRow["severity"]) =>
  ({
    low: "bg-emerald-500/10 text-emerald-600",
    medium: "bg-amber-500/10 text-amber-600",
    high: "bg-rose-500/10 text-rose-600"
  })[severity];

export default function AlertsPage() {
  const [severity, setSeverity] = useState("all");
  const [rule, setRule] = useState("all");
  const [query, setQuery] = useState("");

  const { data, error, loading } = useApi(
    () =>
      listAlerts({
        page: 1,
        page_size: 50,
        severity: severity === "all" ? undefined : severity,
        rule_id: rule === "all" ? undefined : rule
      }),
    [severity, rule]
  );

  const rows: AlertRow[] = (data?.items ?? []).map((item) => ({
    id: item.alert_id,
    account: item.account_number,
    severity: item.severity as AlertRow["severity"],
    rule: item.rule_id,
    description: item.description,
    date: new Date(item.triggered_date).toLocaleString()
  }));

  const filtered = useMemo(() => {
    return rows.filter((row) => {
      const severityMatch = severity === "all" || row.severity === severity;
      const ruleMatch = rule === "all" || row.rule.toLowerCase().includes(rule);
      const queryMatch =
        !query ||
        row.account.toLowerCase().includes(query.toLowerCase()) ||
        row.id.toLowerCase().includes(query.toLowerCase());
      return severityMatch && ruleMatch && queryMatch;
    });
  }, [rows, severity, rule, query]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Alerts</h2>
        <p className="mt-2 text-sm text-text-muted">
          Review AML alerts flagged by rules and AI signals.
        </p>
      </div>

      <div className="grid gap-3 rounded-2xl border border-border bg-surface-secondary p-4 sm:grid-cols-3">
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">
            Severity
          </label>
          <select
            value={severity}
            onChange={(event) => setSeverity(event.target.value)}
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          >
            <option value="all">All</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">Rule</label>
          <select
            value={rule}
            onChange={(event) => setRule(event.target.value)}
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          >
            <option value="all">All</option>
            <option value="RULE-01">High Deposit</option>
            <option value="RULE-03">Rapid Cycle</option>
            <option value="RULE-05">Cross-Border</option>
          </select>
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">
            Search
          </label>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Account or Alert ID"
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-surface-secondary">
        {loading ? (
          <div className="p-6">
            <LoadingState title="Loading alerts" />
          </div>
        ) : error ? (
          <div className="p-6">
            <ErrorState title="Unable to load alerts" message={error} />
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-6">
            <EmptyState title="No alerts found" message="Try changing the filters." />
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-secondary/80 text-xs uppercase tracking-[0.2em] text-text-muted">
              <tr>
                <th className="px-4 py-3">Alert ID</th>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Rule</th>
                <th className="px-4 py-3">Description</th>
                <th className="px-4 py-3">Date</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row.id} className="border-t border-border">
                  <td className="px-4 py-3 font-medium text-text">{row.id}</td>
                  <td className="px-4 py-3 text-text-muted">{row.account}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-1 text-xs font-semibold ${severityStyle(
                        row.severity
                      )}`}
                    >
                      {row.severity}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-text-muted">{row.rule}</td>
                  <td className="px-4 py-3 text-text-muted">{row.description}</td>
                  <td className="px-4 py-3 text-text-muted">{row.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
