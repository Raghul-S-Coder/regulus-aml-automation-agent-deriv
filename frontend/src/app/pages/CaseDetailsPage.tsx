import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { EmptyState, ErrorState, LoadingState } from "@/app/components/States";
import { generateSar, getCase, submitCaseDecision } from "@/app/api/cases";
import { useApi } from "@/app/hooks/useApi";

type DecisionType = "ACCEPT" | "REJECT";

function scoreColor(score: number | null | undefined): string {
  if (score == null) return "bg-gray-100 text-gray-400";
  if (score >= 75) return "bg-red-50 text-red-600 border-red-200";
  if (score >= 50) return "bg-amber-50 text-amber-600 border-amber-200";
  if (score >= 20) return "bg-blue-50 text-blue-600 border-blue-200";
  return "bg-emerald-50 text-emerald-600 border-emerald-200";
}

function riskLabel(score: number): string {
  if (score >= 75) return "HIGH RISK";
  if (score >= 50) return "MEDIUM RISK";
  if (score >= 20) return "LOW RISK";
  return "FALSE POSITIVE";
}

function riskBadgeColor(score: number): string {
  if (score >= 75) return "bg-red-600 text-white";
  if (score >= 50) return "bg-amber-500 text-white";
  if (score >= 20) return "bg-blue-500 text-white";
  return "bg-emerald-500 text-white";
}

export default function CaseDetailsPage() {
  const { caseId } = useParams();
  const [decision, setDecision] = useState<DecisionType>("ACCEPT");
  const [reason, setReason] = useState("");
  const [status, setStatus] = useState("");
  const [nextAction, setNextAction] = useState("");
  const [generating, setGenerating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ reason?: string; nextAction?: string }>({});

  const {
    data: caseData,
    error: caseError,
    loading: caseLoading,
    refetch
  } = useApi(() => getCase(caseId ?? ""), [caseId]);

  const averageScore = useMemo(() => {
    if (!caseData) return 0;
    return Math.round(caseData.case_score_percentage);
  }, [caseData]);

  const handleDecisionToggle = (value: DecisionType) => {
    setDecision(value);
    setErrors({});
    setStatus("");
    if (value === "REJECT") {
      setNextAction("");
    }
  };

  const validate = (): boolean => {
    const newErrors: { reason?: string; nextAction?: string } = {};
    if (!reason.trim()) {
      newErrors.reason = "Decision reason is required.";
    }
    if (decision === "ACCEPT" && !nextAction) {
      newErrors.nextAction = "Next action is required for Accept.";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const submitDecision = async () => {
    if (!validate()) return;
    setSubmitting(true);
    setStatus("");
    try {
      const payload: any = {
        decision,
        decision_by: "compliance_manager",
        decision_reason: reason,
      };

      // Only include next_action for ACCEPT decisions
      if (decision === "ACCEPT") {
        payload.next_action = nextAction;
      }

      await submitCaseDecision(caseId ?? "", payload);
      setStatus(`Decision ${decision} submitted successfully for ${caseId}.`);
      setReason("");
      setNextAction("");
      setErrors({});
      refetch();
    } catch (error) {
      console.error("Error submitting decision:", error);
      setStatus("Unable to submit decision. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const generateDocument = async () => {
    setGenerating(true);
    setStatus("");
    try {
      await generateSar(caseId ?? "");
      setStatus("SAR PDF downloaded successfully.");
    } catch {
      setStatus("Unable to generate document. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  const agents = caseData
    ? [
        { label: "Behavioral", score: caseData.behavoir_agent_score },
        { label: "Network", score: caseData.network_agent_score },
        { label: "Contextual", score: caseData.contextual_agent_score },
        { label: "Evidence", score: caseData.evidence_agent_score },
        { label: "False Positive", score: caseData.false_positive_agent_score }
      ]
    : [];

  const isCaseClosed = caseData?.case_status === "CLOSE" || caseData?.case_status === "ACCEPTED";

  return (
    <div className="space-y-6">
      {/* Header: Case ID + Score + Status */}
      <div className="flex flex-wrap items-center gap-4">
        <div>
          <h2 className="text-2xl font-semibold">Case Details</h2>
          <p className="mt-1 text-sm text-text-muted">Case ID: {caseId}</p>
        </div>
        {caseData && (
          <>
            <div className="flex items-center gap-2 rounded-xl border border-border bg-surface-secondary px-4 py-2">
              <span className="text-sm text-text-muted">Score</span>
              <span className="text-2xl font-bold">{averageScore}%</span>
            </div>
            <span className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wider ${riskBadgeColor(averageScore)}`}>
              {riskLabel(averageScore)}
            </span>
            <span className="rounded-full border border-border bg-surface-secondary px-3 py-1 text-xs font-semibold uppercase tracking-wider text-text-muted">
              {caseData.case_status}
            </span>
          </>
        )}
      </div>

      {caseLoading ? (
        <LoadingState title="Loading case details" />
      ) : caseError ? (
        <ErrorState title="Unable to load case" message={caseError} />
      ) : !caseData ? (
        <EmptyState title="Case not found" />
      ) : (
        <>
          {/* Case Summary + Agent Scores side by side */}
          <div className="grid gap-4 lg:grid-cols-3">
            {/* Case Summary (left 2/3) */}
            <div className="rounded-2xl border border-border bg-surface-secondary p-5 lg:col-span-2">
              <h3 className="text-lg font-semibold">Case Summary</h3>
              <div className="prose prose-sm mt-3 max-w-none text-text-muted">
                <ReactMarkdown>{caseData.case_summary}</ReactMarkdown>
              </div>
            </div>

            {/* Agent Scores (right 1/3) */}
            <div className="rounded-2xl border border-border bg-surface-secondary p-5">
              <h3 className="text-lg font-semibold">Agent Scores</h3>
              <div className="mt-3 space-y-2">
                {agents.map((item) => (
                  <div
                    key={item.label}
                    className={`flex items-center justify-between rounded-xl border px-4 py-3 ${scoreColor(item.score)}`}
                  >
                    <span className="text-xs font-medium uppercase tracking-wide">
                      {item.label}
                    </span>
                    <span className="text-lg font-bold">
                      {item.score != null ? `${Math.round(item.score)}%` : "—"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Decision Section (full width) */}
          <div className="rounded-2xl border border-border bg-surface-secondary p-5">
            <h3 className="text-lg font-semibold">Decision</h3>

            {isCaseClosed ? (
              <p className="mt-3 text-sm text-text-muted">
                This case has been {caseData.case_status === "ACCEPTED" ? "accepted" : "closed"}. No further decisions can be submitted.
              </p>
            ) : (
              <>
                {/* Swipe Decision Toggle */}
                <div className="mt-4">
                  <label className="mb-2 block text-sm font-medium text-text">Decision</label>
                  <div className="relative h-12 w-full max-w-md overflow-hidden rounded-full bg-surface-secondary">
                    {/* Background indicators */}
                    <div className="absolute inset-0 flex">
                      <div className="flex w-1/2 items-center justify-start pl-6">
                        <span className={`text-sm font-semibold transition-opacity ${decision === "REJECT" ? "text-red-600 opacity-100" : "text-text-muted opacity-40"}`}>
                          Reject
                        </span>
                      </div>
                      <div className="flex w-1/2 items-center justify-end pr-6">
                        <span className={`text-sm font-semibold transition-opacity ${decision === "ACCEPT" ? "text-emerald-600 opacity-100" : "text-text-muted opacity-40"}`}>
                          Accept
                        </span>
                      </div>
                    </div>

                    {/* Sliding toggle */}
                    <div
                      className={`absolute inset-y-1 transition-all duration-300 ease-out ${
                        decision === "ACCEPT" ? "left-1/2 right-1" : "left-1 right-1/2"
                      }`}
                    >
                      <div
                        className={`flex h-full cursor-pointer items-center justify-center rounded-full shadow-md transition-colors ${
                          decision === "ACCEPT" ? "bg-emerald-600" : "bg-red-600"
                        }`}
                        onClick={() => handleDecisionToggle(decision === "ACCEPT" ? "REJECT" : "ACCEPT")}
                      >
                        <span className="text-sm font-bold text-white">
                          {decision === "ACCEPT" ? "Accept" : "Reject"}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Next Action — only for ACCEPT */}
                {decision === "ACCEPT" && (
                  <div className="mt-4 space-y-2">
                    <label className="text-sm font-medium text-text" htmlFor="nextAction">
                      Next action <span className="text-red-500">*</span>
                    </label>
                    <select
                      id="nextAction"
                      value={nextAction}
                      onChange={(event) => {
                        setNextAction(event.target.value);
                        if (errors.nextAction) setErrors((e) => ({ ...e, nextAction: undefined }));
                      }}
                      className={[
                        "w-full rounded-xl border bg-surface px-3 py-2 text-sm text-text sm:w-1/2",
                        errors.nextAction ? "border-red-400" : "border-border"
                      ].join(" ")}
                    >
                      <option value="" disabled>Select next action</option>
                      <option value="file-sar">File SAR</option>
                      <option value="escalate">Escalate</option>
                      <option value="request-additional-documents">Request Docs</option>
                    </select>
                    {errors.nextAction && (
                      <p className="text-xs text-red-500">{errors.nextAction}</p>
                    )}
                  </div>
                )}

                {/* Decision Reason */}
                <div className="mt-4 space-y-2">
                  <label className="text-sm font-medium text-text" htmlFor="decisionReason">
                    Decision reason <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    id="decisionReason"
                    value={reason}
                    onChange={(event) => {
                      setReason(event.target.value);
                      if (errors.reason) setErrors((e) => ({ ...e, reason: undefined }));
                    }}
                    className={[
                      "min-h-[100px] w-full rounded-xl border bg-surface px-3 py-2 text-sm text-text",
                      errors.reason ? "border-red-400" : "border-border"
                    ].join(" ")}
                    placeholder={
                      decision === "ACCEPT"
                        ? "Explain why this case warrants filing a SAR or escalation."
                        : "Explain why this case should be rejected (e.g. false positive reasoning)."
                    }
                  />
                  {errors.reason && (
                    <p className="text-xs text-red-500">{errors.reason}</p>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="mt-4 flex gap-3">
                  <button
                    onClick={submitDecision}
                    disabled={submitting}
                    className="rounded-full bg-brand px-5 py-2 text-sm font-semibold text-brand-foreground shadow-soft disabled:opacity-50"
                  >
                    {submitting ? "Submitting..." : "Submit Decision"}
                  </button>
                  <button
                    onClick={generateDocument}
                    disabled={generating}
                    className="rounded-full border border-brand px-5 py-2 text-sm font-semibold text-brand hover:bg-brand hover:text-brand-foreground disabled:opacity-50"
                  >
                    {generating ? "Generating..." : "Generate SAR PDF"}
                  </button>
                </div>
              </>
            )}
          </div>
        </>
      )}

      {status && (
        <div className={[
          "rounded-xl border px-4 py-3 text-sm",
          status.includes("Unable") || status.includes("error")
            ? "border-red-200 bg-red-50 text-red-700"
            : "border-emerald-200 bg-emerald-50 text-emerald-700"
        ].join(" ")}>
          {status}
        </div>
      )}
    </div>
  );
}
