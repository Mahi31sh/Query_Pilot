/**
 * Central Axios instance: base URL, auth header injection, and
 * consistent error unwrapping so components never touch Axios directly.
 */
import axios, { AxiosError } from "axios";
import type { AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { getToken, clearToken } from "./auth";
import type {
  AuthResponse,
  QueryResponse,
  QueryHistoryItem,
  TableSchema,
  ApiError,
  User,
} from "./types";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

// Attach the JWT to every outgoing request if one exists.
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getToken();
  if (token) {
    config.headers.set("Authorization", `Bearer ${token}`);
  }
  return config;
});

// Global 401 handling: token expired/invalid -> clear it and force re-login.
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      clearToken();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

/** Extracts a human-readable message from a failed Axios call, falling back
 * gracefully if the backend didn't return the expected ApiError shape. */
export function extractErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    const data = axiosError.response?.data;
    if (data?.message) return data.message;
    if (axiosError.message) return axiosError.message;
    return "Request failed. Please try again.";
  }
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return "Something went wrong. Please try again.";
}

// ---------- Auth ----------

export async function registerUser(payload: {
  email: string;
  password: string;
  full_name?: string;
}): Promise<User> {
  const { data } = await api.post<User>("/auth/register", payload);
  return data;
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}

export async function loginUser(email: string, password: string): Promise<AuthResponse> {
  // Backend expects OAuth2PasswordRequestForm: form-encoded, 'username' field for email.
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const { data } = await api.post<AuthResponse>("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data;
}

// ---------- Query ----------

export async function runQuery(question: string): Promise<QueryResponse> {
  const { data } = await api.post<QueryResponse>("/query", { question });
  return data;
}

// ---------- History ----------

export async function fetchHistory(
  limit = 50,
  offset = 0
): Promise<QueryHistoryItem[]> {
  const { data } = await api.get<QueryHistoryItem[]>("/history", {
    params: { limit, offset },
  });
  return data;
}

// ---------- Schema ----------

export async function fetchIndexedTables(): Promise<TableSchema[]> {
  const { data } = await api.get<TableSchema[]>("/schema/tables");
  return data;
}

export default api;