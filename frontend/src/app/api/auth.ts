const tokenKey = "regulus_token";
const tokenExpiryKey = "regulus_token_expiry";

type LoginPayload = {
  username: string;
  password: string;
};

type SignupPayload = {
  organization_id: string;
  username: string;
  full_name: string;
  email: string;
  user_type: string;
  password: string;
  is_active?: boolean;
};

export function login(payload: LoginPayload) {
  if (!payload.username || !payload.password) {
    throw new Error("Invalid credentials");
  }
  return import("@/app/api/client").then(async ({ apiPost, unwrapData }) => {
    const response = await apiPost<{ success: boolean; data: { token: string; expires_at: string } }>(
      "/api/v1/auth/login",
      payload
    );
    const data = unwrapData(response);
    localStorage.setItem(tokenKey, data.token);
    if (data.expires_at) {
      localStorage.setItem(tokenExpiryKey, data.expires_at);
    }
    return data;
  });
}

export async function signup(payload: SignupPayload) {
  if (!payload.username || !payload.password) {
    throw new Error("Invalid signup payload");
  }
  const { apiPost, unwrapData } = await import("@/app/api/client");
  const response = await apiPost("/api/v1/users", payload);
  return unwrapData(response);
}

export function logout() {
  localStorage.removeItem(tokenKey);
  localStorage.removeItem(tokenExpiryKey);
}

export function getToken() {
  const expiresAt = localStorage.getItem(tokenExpiryKey);
  if (expiresAt && new Date(expiresAt) <= new Date()) {
    localStorage.removeItem(tokenKey);
    localStorage.removeItem(tokenExpiryKey);
    window.dispatchEvent(new CustomEvent("session-expired"));
    return null;
  }
  return localStorage.getItem(tokenKey);
}
