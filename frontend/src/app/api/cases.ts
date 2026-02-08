import { apiGet, apiPost, baseUrl, buildHeaders, unwrapData } from "@/app/api/client";

export type CaseListItem = {
  case_id: string;
  account_number: string;
  case_status: string;
  case_score_percentage: number;
  case_opened_date: string;
};

export type CaseDetail = {
  case_id: string;
  account_number: string;
  case_status: string;
  case_score_percentage: number;
  case_summary: string;
  behavoir_agent_score?: number;
  behavoir_agent_summary?: string;
  network_agent_score?: number;
  network_agent_summary?: string;
  contextual_agent_score?: number;
  contextual_agent_summary?: string;
  evidence_agent_score?: number;
  evidence_agent_summary?: string;
  false_positive_agent_score?: number;
  false_positive_agent_summary?: string;
};

export type CaseDocument = {
  document_id: string;
  content_type: string;
  content: string;
  version: number;
};

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

type CaseFilters = {
  page?: number;
  page_size?: number;
  status?: string;
};

export async function listCases(filters: CaseFilters = {}) {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", String(filters.page));
  if (filters.page_size) params.set("page_size", String(filters.page_size));
  if (filters.status) params.set("status", filters.status);

  const response = await apiGet<{ success: boolean; data: PaginatedResponse<CaseListItem> }>(
    `/api/v1/cases?${params.toString()}`
  );
  return unwrapData(response);
}

export async function getCase(caseId: string) {
  const response = await apiGet<{ success: boolean; data: CaseDetail }>(`/api/v1/cases/${caseId}`);
  return unwrapData(response);
}

export async function getCaseDocuments(caseId: string) {
  const response = await apiGet<{ success: boolean; data: CaseDocument[] }>(
    `/api/v1/cases/${caseId}/documents`
  );
  return unwrapData(response);
}

export async function submitCaseDecision(caseId: string, payload: object) {
  const response = await apiPost(`/api/v1/cases/${caseId}/decisions`, payload);
  return unwrapData(response);
}

export async function generateSar(caseId: string) {
  const headers = buildHeaders();
  delete headers["Content-Type"];

  const response = await fetch(`${baseUrl}/api/v1/cases/${caseId}/generate-sar`, {
    method: "POST",
    headers,
  });

  if (!response.ok) {
    throw new Error("Failed to generate SAR PDF");
  }

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `SAR_${caseId}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
