import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { listTransactions } from "@/app/api/transactions";
import { listAlerts } from "@/app/api/alerts";
import { listCases } from "@/app/api/cases";
import { useApi } from "@/app/hooks/useApi";
import { ErrorState, LoadingState } from "@/app/components/States";

function TrendChart({
  values,
  labels,
  rotateLabels = false
}: {
  values: number[];
  labels: string[];
  rotateLabels?: boolean;
}) {
  const max = Math.max(...values);
  const min = Math.min(...values);
  const chartWidth = 260;
  const chartHeight = 120;
  const paddingLeft = 32;
  const paddingBottom = rotateLabels ? 34 : 24;
  const paddingTop = 12;
  const paddingRight = 8;

  const plotWidth = chartWidth - paddingLeft - paddingRight;
  const plotHeight = chartHeight - paddingTop - paddingBottom;
  const safeRange = max - min || 1;

  const points = values
    .map((value, index) => {
      const x = paddingLeft + (index / (values.length - 1 || 1)) * plotWidth;
      const y = paddingTop + (1 - (value - min) / safeRange) * plotHeight;
      return `${x},${y}`;
    })
    .join(" ");

  const yTicks = [max, Math.round((max + min) / 2), min];
  const xTicks = labels.map((label, index) => ({
    label,
    x: paddingLeft + (index / (labels.length - 1 || 1)) * plotWidth
  }));

  return (
    <svg viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="h-32 w-full">
      <line
        x1={paddingLeft}
        y1={paddingTop}
        x2={paddingLeft}
        y2={chartHeight - paddingBottom}
        stroke="hsl(var(--border))"
        strokeWidth="1"
      />
      <line
        x1={paddingLeft}
        y1={chartHeight - paddingBottom}
        x2={chartWidth - paddingRight}
        y2={chartHeight - paddingBottom}
        stroke="hsl(var(--border))"
        strokeWidth="1"
      />
      {yTicks.map((tick) => {
        const y =
          paddingTop + (1 - (tick - min) / safeRange) * plotHeight;
        return (
          <g key={tick}>
            <line
              x1={paddingLeft}
              y1={y}
              x2={chartWidth - paddingRight}
              y2={y}
              stroke="hsl(var(--border))"
              strokeWidth="1"
              opacity="0.4"
            />
            <text
              x={paddingLeft - 6}
              y={y + 4}
              textAnchor="end"
              fontSize="10"
              fill="hsl(var(--text-muted))"
            >
              {tick}
            </text>
          </g>
        );
      })}
      {xTicks.map((tick, index) =>
        tick.label ? (
          <text
            key={`${tick.label}-${index}`}
            x={tick.x}
            y={chartHeight - 6}
            textAnchor={rotateLabels ? "end" : "middle"}
            fontSize="10"
            fill="hsl(var(--text-muted))"
            transform={
              rotateLabels ? `rotate(-45 ${tick.x} ${chartHeight - 6})` : undefined
            }
          >
            {tick.label}
          </text>
        ) : null
      )}
      <polyline
        points={points}
        fill="none"
        stroke="hsl(var(--brand))"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const refreshMs = 5000;
  const { data: transactions, loading: txLoading, error: txError } = useApi(
    () => listTransactions({ page: 1, page_size: 100 }),
    [],
    refreshMs
  );
  const { data: alerts, loading: alertLoading, error: alertError } = useApi(
    () => listAlerts({ page: 1, page_size: 100 }),
    [],
    refreshMs
  );
  const { data: cases, loading: caseLoading, error: caseError } = useApi(
    () => listCases({ page: 1, page_size: 100 }),
    [],
    refreshMs
  );

  const today = new Date().toDateString();

  const kpis = useMemo(() => {
    const txToday =
      transactions?.items.filter((t) => new Date(t.transaction_date).toDateString() === today)
        .length ?? 0;
    const alertsToday =
      alerts?.items.filter((a) => new Date(a.triggered_date).toDateString() === today).length ?? 0;
    const falsePositives =
      cases?.items.filter((c) => c.case_score_percentage < 20).length ?? 0;
    const highConfidence =
      cases?.items.filter((c) => c.case_score_percentage >= 75).length ?? 0;

    return [
      { label: "Transactions Today", value: txToday.toString(), delta: "Live" },
      { label: "Alerts Today", value: alertsToday.toString(), delta: "Live" },
      { label: "False Positives", value: falsePositives.toString(), delta: "Live" },
      { label: "High Confidence Cases", value: highConfidence.toString(), delta: "Live" }
    ];
  }, [transactions, alerts, cases, today]);

  const trendData = useMemo(() => {
    const days = Array.from({ length: 7 }).map((_, index) => {
      const date = new Date();
      date.setDate(date.getDate() - (6 - index));
      return date.toDateString();
    });
    const labels = days.map((day) => day.split(" ")[0]);

    const trend = (items: { date: string }[]) =>
      days.map((day) => items.filter((item) => new Date(item.date).toDateString() === day).length);

    const txValues = trend(
      transactions?.items.map((item) => ({ date: item.transaction_date })) ?? []
    );
    const alertValues = trend(
      alerts?.items.map((item) => ({ date: item.triggered_date })) ?? []
    );
    const caseValues = trend(
      cases?.items.map((item) => ({ date: item.case_opened_date })) ?? []
    );

    return [
      { label: "Transactions", values: txValues, labels },
      { label: "Alerts", values: alertValues, labels },
      { label: "Cases", values: caseValues, labels }
    ];
  }, [transactions, alerts, cases]);


  if (txError || alertError || caseError) {
    return (
      <ErrorState
        title="Unable to load dashboard data"
        message={txError ?? alertError ?? caseError ?? ""}
      />
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <p className="mt-2 text-sm text-text-muted">
          Daily monitoring overview for compliance leadership.
        </p>
      </div>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {kpis.map((kpi) => (
          <button
            key={kpi.label}
            type="button"
            onClick={() => {
              if (kpi.label === "Transactions Today") navigate("/regulus/monitoring/transactions");
              if (kpi.label === "Alerts Today") navigate("/regulus/monitoring/alerts");
              if (kpi.label === "False Positives") navigate("/regulus/monitoring/cases");
              if (kpi.label === "High Confidence Cases") navigate("/regulus/monitoring/cases");
            }}
            className="rounded-2xl border border-border bg-surface-secondary p-5 text-left transition hover:border-brand"
          >
            <p className="text-xs uppercase tracking-[0.2em] text-text-muted">
              {kpi.label}
            </p>
            <div className="mt-3 flex items-end justify-between">
              <p className="text-2xl font-semibold">{kpi.value}</p>
              <span className="rounded-full bg-brand/10 px-2 py-1 text-xs font-semibold text-brand">
                {kpi.delta}
              </span>
            </div>
          </button>
        ))}
      </section>

      <section className="rounded-2xl border border-border bg-surface-secondary p-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h3 className="text-lg font-semibold">Real-time alerts triage</h3>
            <p className="mt-1 text-sm text-text-muted">
              {cases?.items?.length ? (
                <>
                  {Math.round(
                    (cases.items.filter((c) => c.case_score_percentage < 20).length /
                      cases.items.length) *
                      100
                  )}
                  % of today’s alerts auto-classified as low risk.
                </>
              ) : (
                "No cases available yet."
              )}
            </p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-3">
        {trendData.map((trend) => (
          <div
            key={trend.label}
            className="rounded-2xl border border-border bg-surface-secondary p-5"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm font-semibold text-text">{trend.label} Trend</p>
              <span className="text-xs text-text-muted">Last 7 days</span>
            </div>
            <div className="mt-4">
              <TrendChart values={trend.values} labels={trend.labels} />
            </div>
          </div>
        ))}
      </section>

      {txLoading || alertLoading || caseLoading ? (
        <LoadingState title="Loading dashboard metrics" />
      ) : null}
    </div>
  );
}
