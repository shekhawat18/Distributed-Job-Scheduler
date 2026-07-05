import {
  createContext,
  useContext,
  useState,
  type ReactNode,
} from "react";

import type { User, AuthResponse } from "../../../types";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  setCredentials: (authData: AuthResponse) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);

  const setCredentials = (authData: AuthResponse) => {
    localStorage.setItem("token", authData.access_token);
    setUser(authData.user);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: user !== null,
        setCredentials,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }

  return context;
}