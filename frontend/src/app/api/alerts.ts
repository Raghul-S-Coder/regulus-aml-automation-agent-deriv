import { apiGet, unwrapData } from "@/app/api/client";

export type Alert = {
  alert_id: string;
  account_number: string;
  severity: string;
  rule_id: string;
  description: string;
  triggered_date: string;
};

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

type AlertFilters = {
  page?: number;
  page_size?: number;
  account_number?: string;
  severity?: string;
  rule_id?: string;
};

export async function listAlerts(filters: AlertFilters = {}) {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", String(filters.page));
  if (filters.page_size) params.set("page_size", String(filters.page_size));
  if (filters.account_number) params.set("account_number", filters.account_number);
  if (filters.severity) params.set("severity", filters.severity);
  if (filters.rule_id) params.set("rule_id", filters.rule_id);

  const response = await apiGet<{ success: boolean; data: PaginatedResponse<Alert> }>(
    `/api/v1/alerts?${params.toString()}`
  );
  return unwrapData(response);
}
