import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";

import { useAuth } from "../../../context/AuthContext";

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute = ({
  children,
}: ProtectedRouteProps) => {
  const {
    isAuthenticated,
    isLoading,
  } = useAuth();

  // Still checking existing token
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="text-center">

          <div
            className="
              mx-auto
              h-10
              w-10
              animate-spin
              rounded-full
              border-4
              border-slate-200
              border-t-indigo-600
            "
          />

          <p className="mt-4 text-sm text-slate-500 dark:text-slate-400">
            Loading your account...
          </p>

        </div>
      </div>
    );
  }

  // No valid authentication
  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  // Authenticated
  return <>{children}</>;
};

export default ProtectedRoute;