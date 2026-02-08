import { getToken } from "@/app/api/auth";

export const baseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

type RequestOptions = {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
  headers?: Record<string, string>;
};

export function buildHeaders(extra?: Record<string, string>) {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-Request-ID": crypto.randomUUID(),
    "X-Forwarded-For": "127.0.0.1",
    "X-Device-Id": "regulus-ui",
    ...extra
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  return headers;
}

export class ApiError extends Error {
  code?: string;
  status?: number;

  constructor(message: string, code?: string, status?: number) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestOptions = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: options.method ?? "GET",
    headers: buildHeaders(options.headers),
    body: options.body ? JSON.stringify(options.body) : undefined
  });

  if (!response.ok) {
    const contentType = response.headers.get("content-type") ?? "";
    if (contentType.includes("application/json")) {
      const payload = (await response.json()) as {
        message?: string;
        error_code?: string;
      };
      if (response.status === 401) {
        localStorage.removeItem("regulus_token");
        localStorage.removeItem("regulus_token_expiry");
        window.dispatchEvent(new CustomEvent("session-expired"));
      }
      throw new ApiError(payload.message || "Request failed", payload.error_code, response.status);
    }
    const message = await response.text();
    if (response.status === 401) {
      localStorage.removeItem("regulus_token");
      localStorage.removeItem("regulus_token_expiry");
      window.dispatchEvent(new CustomEvent("session-expired"));
    }
    throw new ApiError(message || "Request failed", undefined, response.status);
  }

  return (await response.json()) as T;
}

export function apiGet<T>(path: string) {
  return request<T>(path, { method: "GET" });
}

export function apiPost<T>(path: string, body?: unknown) {
  return request<T>(path, { method: "POST", body });
}

export function unwrapData<T>(response: unknown): T {
  if (response && typeof response === "object" && "data" in response) {
    return (response as { data: T }).data;
  }
  return response as T;
}
