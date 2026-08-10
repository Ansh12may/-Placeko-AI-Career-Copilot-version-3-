import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getCurrentUser } from "../../api/auth";

const OAuthCallbackPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleOAuthCallback = async () => {
      try {
        // =====================================================
        // Get tokens returned by backend
        // =====================================================

        const accessToken =
          searchParams.get("access_token");

        const refreshToken =
          searchParams.get("refresh_token");

        // =====================================================
        // Validate tokens
        // =====================================================

        if (!accessToken || !refreshToken) {
          throw new Error(
            "Authentication tokens were not returned."
          );
        }

        // =====================================================
        // Store Placeko JWT tokens
        // =====================================================

        localStorage.setItem(
          "access_token",
          accessToken
        );

        localStorage.setItem(
          "refresh_token",
          refreshToken
        );

        // =====================================================
        // Verify authentication
        // =====================================================

        await getCurrentUser();

        // =====================================================
        // Go to dashboard
        //
        // Full page navigation is intentional here.
        // AuthProvider will mount again and restore
        // the authenticated user from localStorage.
        // =====================================================

        window.location.href = "/dashboard";

      } catch (error) {
        console.error(
          "OAuth callback failed:",
          error
        );

        // Remove potentially invalid tokens.

        localStorage.removeItem(
          "access_token"
        );

        localStorage.removeItem(
          "refresh_token"
        );

        setError(
          error instanceof Error
            ? error.message
            : "Google authentication failed."
        );
      }
    };

    handleOAuthCallback();
  }, [searchParams]);

  // =========================================================
  // Error State
  // =========================================================

  if (error) {
    return (
      <div
        className="
          flex
          min-h-screen
          items-center
          justify-center
          bg-slate-50
          px-6
          dark:bg-slate-950
        "
      >
        <div
          className="
            w-full
            max-w-md
            rounded-2xl
            border
            border-red-200
            bg-white
            p-8
            text-center
            shadow-lg
            dark:border-red-900
            dark:bg-slate-900
          "
        >
          <div
            className="
              mx-auto
              flex
              h-12
              w-12
              items-center
              justify-center
              rounded-full
              bg-red-100
              text-red-600
              dark:bg-red-950
              dark:text-red-400
            "
          >
            !
          </div>

          <h1
            className="
              mt-4
              text-lg
              font-bold
              text-slate-900
              dark:text-white
            "
          >
            Authentication Failed
          </h1>

          <p
            className="
              mt-2
              text-sm
              leading-6
              text-slate-500
              dark:text-slate-400
            "
          >
            {error}
          </p>

          <button
            type="button"
            onClick={() => navigate("/login")}
            className="
              mt-6
              rounded-xl
              bg-slate-900
              px-5
              py-2.5
              text-sm
              font-semibold
              text-white
              transition
              hover:bg-slate-800
              dark:bg-white
              dark:text-slate-900
              dark:hover:bg-slate-200
            "
          >
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  // =========================================================
  // Loading State
  // =========================================================

  return (
    <div
      className="
        flex
        min-h-screen
        items-center
        justify-center
        bg-slate-50
        px-6
        dark:bg-slate-950
      "
    >
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
            dark:border-slate-700
            dark:border-t-indigo-400
          "
        />

        <h1
          className="
            mt-5
            text-lg
            font-bold
            text-slate-900
            dark:text-white
          "
        >
          Signing you in...
        </h1>

        <p
          className="
            mt-1
            text-sm
            text-slate-500
            dark:text-slate-400
          "
        >
          Completing Google authentication.
        </p>

      </div>
    </div>
  );
};

export default OAuthCallbackPage;