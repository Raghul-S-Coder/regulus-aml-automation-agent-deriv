import { getToken } from "@/app/api/auth";

export function useAuth() {
  const token = getToken();
  const isAuthenticated = Boolean(token);

  return { isAuthenticated };
}
