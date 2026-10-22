/**
 * Token storage helpers. Isolated here so if the storage strategy changes
 * (e.g. httpOnly cookie instead of localStorage) only this file changes.
 */
const TOKEN_KEY = "querypilot_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export function isAuthenticated(): boolean {
  return getToken() !== null;
}