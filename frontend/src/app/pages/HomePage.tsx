import { Link } from "react-router-dom";
import WorkflowGraphic from "@/app/components/WorkflowGraphic";

export default function HomePage() {
  return (
    <div className="space-y-16">
      <section className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-border bg-surface-secondary px-4 py-1 text-xs uppercase tracking-[0.2em] text-text-muted">
            RegulusAI for Compliance
          </div>
          <h1 className="text-4xl font-semibold leading-tight lg:text-5xl">
            Compliance teams are drowning in noise. RegulusAI cuts the clutter.
          </h1>
          <p className="text-base text-text-muted lg:text-lg">
            Thousands of alerts. Manual reviews. Missed bad actors. RegulusAI highlights the
            suspicious patterns, explains the why, and delivers investigation-ready cases.
          </p>
          <div className="flex flex-wrap items-center gap-4">
            <Link
              to="/regulus/transaction-simulation"
              className="rounded-full bg-brand px-5 py-2.5 text-sm font-semibold text-brand-foreground shadow-soft"
            >
              Try the Simulation
            </Link>
            <Link
              to="/regulus/login"
              className="rounded-full border border-border px-5 py-2.5 text-sm font-semibold text-text hover:border-brand hover:text-brand"
            >
              Compliance Login
            </Link>
          </div>
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl border border-border bg-surface-secondary p-4">
              <p className="text-sm font-semibold text-text">Fewer false positives</p>
              <p className="text-xs text-text-muted">
                AI scoring reduces noise and surfaces high-confidence cases.
              </p>
            </div>
            <div className="rounded-xl border border-border bg-surface-secondary p-4">
              <p className="text-sm font-semibold text-text">Explainable alerts</p>
              <p className="text-xs text-text-muted">
                Every flag includes context, evidence, and analyst-ready notes.
              </p>
            </div>
            <div className="rounded-xl border border-border bg-surface-secondary p-4">
              <p className="text-sm font-semibold text-text">Real-time defense</p>
              <p className="text-xs text-text-muted">
                Detect laundering patterns before funds leave the system.
              </p>
            </div>
          </div>
        </div>
        <WorkflowGraphic />
      </section>

      <section className="grid gap-6 lg:grid-cols-3">
        <div className="rounded-2xl border border-border bg-surface-secondary p-6">
          <p className="text-sm font-semibold text-text">Behavioral anomalies</p>
          <p className="mt-2 text-sm text-text-muted">
            Detect deviations in deposit, trade, and withdrawal behavior with AI context.
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-surface-secondary p-6">
          <p className="text-sm font-semibold text-text">Network signals</p>
          <p className="mt-2 text-sm text-text-muted">
            Identify coordinated rings via shared IPs, devices, and funding sources.
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-surface-secondary p-6">
          <p className="text-sm font-semibold text-text">Case-ready output</p>
          <p className="mt-2 text-sm text-text-muted">
            Auto-generated evidence summaries and SAR-ready narratives.
          </p>
        </div>
      </section>

      <section className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div className="rounded-2xl border border-border bg-surface-secondary p-6">
          <p className="text-xs uppercase tracking-[0.2em] text-text-muted">How it works</p>
          <h2 className="mt-3 text-2xl font-semibold">From transaction to action</h2>
          <p className="mt-2 text-sm text-text-muted">
            RegulusAI orchestrates rules, AI agents, and compliance review in a single loop.
          </p>
        </div>
        <ol className="grid gap-4 sm:grid-cols-2">
          {[
            "Stream transactions into real-time monitoring.",
            "Detect and score suspicious behavior instantly.",
            "Generate evidence packs for analysts.",
            "Route high-confidence cases to managers.",
            "Capture decisions and feedback loops.",
            "Reduce false positives over time."
          ].map((item) => (
            <li key={item} className="rounded-xl border border-border bg-surface-secondary p-4">
              <p className="text-sm text-text">{item}</p>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
