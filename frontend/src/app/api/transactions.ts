import { apiGet, unwrapData } from "@/app/api/client";

export type Transaction = {
  transaction_id: string;
  account_number: string;
  transaction_amount: number;
  transaction_currency: string;
  transaction_type: string;
  transaction_status: string;
  transaction_date: string;
};

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

type TransactionFilters = {
  page?: number;
  page_size?: number;
  account_number?: string;
  transaction_type?: string;
  transaction_status?: string;
};

export async function listTransactions(filters: TransactionFilters = {}) {
  const params = new URLSearchParams();
  if (filters.page) params.set("page", String(filters.page));
  if (filters.page_size) params.set("page_size", String(filters.page_size));
  if (filters.account_number) params.set("account_number", filters.account_number);
  if (filters.transaction_type) params.set("transaction_type", filters.transaction_type);
  if (filters.transaction_status) params.set("transaction_status", filters.transaction_status);

  const response = await apiGet<{ success: boolean; data: PaginatedResponse<Transaction> }>(
    `/api/v1/transactions?${params.toString()}`
  );
  return unwrapData(response);
}
