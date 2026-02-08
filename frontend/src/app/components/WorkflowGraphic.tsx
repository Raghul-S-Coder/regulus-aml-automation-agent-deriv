const steps = [
  { label: "Transactions", detail: "Deposits, trades, withdrawals" },
  { label: "Alerts", detail: "Rules + AI triggers" },
  { label: "AI Analyst", detail: "Behavioral + Network scoring" },
  { label: "Cases", detail: "Evidence packs" },
  { label: "Compliance", detail: "Human decision" }
];

export default function WorkflowGraphic() {
  return (
    <div className="workflow-card">
      <div className="workflow-header">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-text-muted">Live Workflow</p>
          <h3 className="mt-2 text-lg font-semibold">From signal to decision</h3>
        </div>
        <span className="badge-emerald">RegulusAI</span>
      </div>
      <div className="mt-6 space-y-4">
        {steps.map((step, index) => (
          <div key={step.label} className="workflow-row">
            <div className="workflow-dot" />
            <div className="flex-1">
              <p className="text-sm font-semibold text-text">{step.label}</p>
              <p className="text-xs text-text-muted">{step.detail}</p>
            </div>
            <span className="workflow-tag">{index + 1}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
