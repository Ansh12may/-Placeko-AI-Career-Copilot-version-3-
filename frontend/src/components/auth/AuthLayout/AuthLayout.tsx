import type { ReactNode } from "react";
import { ArrowLeft } from "lucide-react";

interface AuthLayoutProps {
  children: ReactNode;
  onBack?: () => void;
}

const AuthLayout = ({ children, onBack }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">

      {/* Back to Landing */}

      <div className="mx-auto max-w-6xl px-6 pt-6">
        <button
          onClick={onBack}
          className="
            flex
            items-center
            gap-2
            text-sm
            font-semibold
            text-slate-600
            transition-colors
            hover:text-indigo-600
            dark:text-slate-300
            dark:hover:text-indigo-400
          "
        >
          <ArrowLeft size={17} />

          Back to Landing Page
        </button>
      </div>

      {/* Auth Content */}

      <main className="flex justify-center px-6 py-10">
        {children}
      </main>

      {/* Footer */}

      <footer className="pb-8 text-center">
        <p className="text-xs text-slate-400 dark:text-slate-500">
          © 2026 Placeko Inc. Secure SSL Authentication.
        </p>
      </footer>

    </div>
  );
};

export default AuthLayout;