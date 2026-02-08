import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { EmptyState, ErrorState, LoadingState } from "@/app/components/States";
import { listCases } from "@/app/api/cases";
import { useApi } from "@/app/hooks/useApi";

type CaseRow = {
  id: string;
  account: string;
  score: number;
  status: "OPEN" | "CLOSE";
  classification: "High" | "Medium" | "Low" | "False Positive";
  date: string;
};

const statusStyle = (status: CaseRow["status"]) =>
  status === "OPEN" ? "bg-brand/10 text-brand" : "bg-slate-500/10 text-slate-500";

export default function CasesPage() {
  const [status, setStatus] = useState("all");
  const [query, setQuery] = useState("");

  const { data, error, loading } = useApi(
    () =>
      listCases({
        page: 1,
        page_size: 50,
        status: status === "all" ? undefined : status
      }),
    [status]
  );

  const rows: CaseRow[] = (data?.items ?? []).map((item) => {
    const score = Math.round(item.case_score_percentage);
    let classification: CaseRow["classification"] = "Low";
    if (score >= 75) classification = "High";
    else if (score >= 50) classification = "Medium";
    else if (score >= 20) classification = "Low";
    else classification = "False Positive";
    return {
      id: item.case_id,
      account: item.account_number,
      score,
      status: item.case_status as CaseRow["status"],
      classification,
      date: new Date(item.case_opened_date).toLocaleString()
    };
  });

  const filtered = useMemo(() => {
    return rows.filter((row) => {
      const statusMatch = status === "all" || row.status === status;
      const queryMatch =
        !query ||
        row.id.toLowerCase().includes(query.toLowerCase()) ||
        row.account.toLowerCase().includes(query.toLowerCase());
      return statusMatch && queryMatch;
    });
  }, [rows, status, query]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">Cases</h2>
        <p className="mt-2 text-sm text-text-muted">
          Review case outcomes and open investigation work.
        </p>
      </div>

      <div className="grid gap-3 rounded-2xl border border-border bg-surface-secondary p-4 sm:grid-cols-2">
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">Status</label>
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          >
            <option value="all">All</option>
            <option value="OPEN">Open</option>
            <option value="CLOSE">Closed</option>
          </select>
        </div>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-text-muted">Search</label>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Case ID or Account"
            className="mt-2 w-full rounded-xl border border-border bg-surface px-3 py-2 text-sm"
          />
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-border bg-surface-secondary">
        {loading ? (
          <div className="p-6">
            <LoadingState title="Loading cases" />
          </div>
        ) : error ? (
          <div className="p-6">
            <ErrorState title="Unable to load cases" message={error} />
          </div>
        ) : filtered.length === 0 ? (
          <div className="p-6">
            <EmptyState title="No cases found" message="Try adjusting the filters." />
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-surface-secondary/80 text-xs uppercase tracking-[0.2em] text-text-muted">
              <tr>
                <th className="px-4 py-3">Case ID</th>
                <th className="px-4 py-3">Account</th>
                <th className="px-4 py-3">Score</th>
                <th className="px-4 py-3">Classification</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Date</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((row) => (
                <tr key={row.id} className="border-t border-border">
                  <td className="px-4 py-3 font-medium text-text">
                    <Link
                      to={`/regulus/monitoring/cases/${row.id}`}
                      className="text-brand hover:underline"
                    >
                      {row.id}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-text-muted">{row.account}</td>
                  <td className="px-4 py-3 text-text">{row.score}%</td>
                  <td className="px-4 py-3 text-text-muted">{row.classification}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`rounded-full px-2 py-1 text-xs font-semibold ${statusStyle(
                        row.status
                      )}`}
                    >
                      {row.status}
                    </span>
                  </td>
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
