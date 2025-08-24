import { createContext, useContext } from "react";
import { seedUsers } from "@/shared/data";

type User = (typeof seedUsers)[number] | null;

type Ctx = {
  user: User;
  logout: () => Promise<void>;
  redirectToLogin: () => Promise<void>;
  exchangeCodeForSessionToken: () => Promise<void>;
};

const defaultUser = seedUsers?.[0] ?? null;

const AuthCtx = createContext<Ctx>({
  user: defaultUser,
  logout: async () => {},
  redirectToLogin: async () => {},
  exchangeCodeForSessionToken: async () => {},
});

export const useAuth = () => useContext(AuthCtx);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const value: Ctx = {
    user: defaultUser,
    logout: async () => {},
    redirectToLogin: async () => {},
    exchangeCodeForSessionToken: async () => {},
  };
  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
}

