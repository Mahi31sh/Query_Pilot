/**
 * Shared TypeScript types mirroring the backend's Pydantic schemas
 * (app/schemas.py) exactly, so the frontend/backend contract stays in sync.
 */

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export type ChartType = "bar" | "pie" | "line" | "scatter" | "table" | "kpi";

export interface ChartSpec {
  chart_type: ChartType;
  data: Record<string, unknown>[];
  x_key: string | null;
  y_key: string | null;
  label: string | null;
}

export interface QueryResponse {
  question: string;
  generated_sql: string;
  explanation: string;
  columns: string[];
  rows: Record<string, unknown>[];
  row_count: number;
  chart: ChartSpec;
  retry_count: number;
  execution_time_ms: number;
}

export interface QueryHistoryItem {
  id: string;
  question: string;
  generated_sql: string;
  success: boolean;
  error_message: string | null;
  retry_count: number;
  row_count: number | null;
  chart_type: ChartType | null;
  created_at: string;
}

export interface TableSchema {
  table_name: string;
  columns: { name: string; type: string }[];
  description: string | null;
}

/** Discriminated union for chat message rendering — either the user's
 * question or the assistant's structured query result/error. */
export type ChatMessage =
  | { id: string; role: "user"; content: string }
  | { id: string; role: "assistant"; result: QueryResponse }
  | { id: string; role: "assistant-error"; message: string };

export interface ApiError {
  error: string;
  message: string;
}