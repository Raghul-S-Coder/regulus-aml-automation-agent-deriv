import { apiGet, unwrapData } from "@/app/api/client";

type Customer = {
  customer_id: string;
  full_name: string;
};

type PaginatedResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
};

export async function listCustomers(page = 1, pageSize = 50) {
  const response = await apiGet<{ success: boolean; data: PaginatedResponse<Customer> }>(
    `/api/v1/customers?page=${page}&page_size=${pageSize}`
  );
  return unwrapData(response);
}
