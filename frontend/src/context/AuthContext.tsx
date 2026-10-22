/**
 * Global auth state: current user, login/register/logout actions,
 * and loading state while the initial session is being restored.
 */
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { getToken, setToken, clearToken } from "@/lib/auth";
import { loginUser, registerUser, fetchCurrentUser, extractErrorMessage } from "@/lib/api";
import type { User } from "@/lib/types";

interface AuthContextValue {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    let cancelled = false;

    async function hydrateUser() {
      try {
        const currentUser = await fetchCurrentUser();
        if (!cancelled) {
          setUser(currentUser);
        }
      } catch {
        if (!cancelled) {
          clearToken();
          setUser(null);
        }
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    void hydrateUser();

    return () => {
      cancelled = true;
    };
  }, []);

  async function login(email: string, password: string) {
    try {
      const { access_token } = await loginUser(email, password);
      setToken(access_token);
      const currentUser = await fetchCurrentUser();
      setUser(currentUser);
    } catch (err) {
      clearToken();
      setUser(null);
      throw new Error(extractErrorMessage(err));
    }
  }

  async function register(email: string, password: string, fullName?: string) {
    try {
      await registerUser({ email, password, full_name: fullName });
      await login(email, password);
    } catch (err) {
      clearToken();
      setUser(null);
      throw new Error(extractErrorMessage(err));
    }
  }

  function logout() {
    clearToken();
    setUser(null);
    window.location.href = "/login";
  }

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: user !== null, isLoading, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuthContext must be used within AuthProvider");
  return ctx;
}