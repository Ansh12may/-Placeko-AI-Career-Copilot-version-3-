import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  getCurrentUser,
  login as loginApi,
  register as registerApi,
  logout as logoutApi,
  type User,
} from "../api/auth";






interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  login: (
    email: string,
    password: string
  ) => Promise<void>;

  register: (
    fullName: string,
    email: string,
    password: string
  ) => Promise<void>;

  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({
  children,
}: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = user !== null;

  useEffect(() => {
    const restoreSession = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const currentUser = await getCurrentUser();

        setUser(currentUser);
      } catch (error) {
        console.error(
          "Failed to restore authentication:",
          error
        );

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    restoreSession();
  }, []);

  const login = async (
    email: string,
    password: string
  ) => {
    const response = await loginApi(email, password);

    localStorage.setItem(
      "access_token",
      response.data.access_token
    );

    localStorage.setItem(
      "refresh_token",
      response.data.refresh_token
    );

    const currentUser = await getCurrentUser();

    setUser(currentUser);
  };

  const register = async (
    fullName: string,
    email: string,
    password: string
  ) => {
    const response = await registerApi(
      fullName,
      email,
      password
    );

    localStorage.setItem(
      "access_token",
      response.data.access_token
    );

    localStorage.setItem(
      "refresh_token",
      response.data.refresh_token
    );

    const currentUser = await getCurrentUser();

    setUser(currentUser);
  };


  const logout = async () => {
  try {
    await logoutApi();
  } catch (error) {
    console.error("Logout API failed:", error);
  } finally {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);

  }

};

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
};