import { apiGet, unwrapData } from "@/app/api/client";

type Account = {
  account_number: string;
  customer_id: string;
  account_status: string;
};

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export async function listAccountsByCustomer(customerId: string, page = 1, pageSize = 50) {
  const response = await apiGet<{ success: boolean; data: PaginatedResponse<Account> }>(
    `/api/v1/accounts/customer/${customerId}?page=${page}&page_size=${pageSize}`
  );
  return unwrapData(response);
}
