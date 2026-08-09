import { useState } from "react";
import { Lock, Mail, Eye, EyeOff, ArrowRight } from "lucide-react";
import FormInput from "../FormInput";
import OAuthButtons from "../OAuthButtons";
import { useAuth } from "../../../context/AuthContext";


interface LoginFormProps {
  onLogin?: (email: string, password: string) => void;
  onGoogle?: () => void;
  onGithub?: () => void;
  onSignup?: () => void;
  onForgotPassword?: () => void;
}

const LoginForm = ({
  onLogin,
  onGoogle,
  onGithub,
  onSignup,
  onForgotPassword,
}: LoginFormProps) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
const [loginError, setLoginError] = useState("");

const { login } = useAuth();

  const handleSubmit = async (
  event: React.FormEvent<HTMLFormElement>
) => {
  event.preventDefault();
  setLoginError("");
  if (!email || !password) {
    setLoginError("Please enter your email and password.");
    return;
  }
  try {
    setIsLoading(true);
    await login(email, password);
    onLogin?.(email, password);

    
  } catch (error) {
    console.error("Login failed:", error);
    setLoginError(
      "Invalid email or password. Please try again."

    );

  } finally {
    setIsLoading(false);

  }

};
  return (
    <div className="space-y-6">

      {/* Demo Account */}

      <div
        className="
          rounded-xl
          border
          border-indigo-100
          bg-indigo-50
          p-4
          dark:border-indigo-900/50
          dark:bg-indigo-950/30
        "
      >
        <div className="flex items-center justify-between gap-4">

          <div>
            <p className="text-sm font-semibold text-indigo-900 dark:text-indigo-300">
              Demo Account Ready
            </p>

            <p className="mt-1 text-xs text-indigo-600 dark:text-indigo-400">
              Use the demo account to explore Placeko.
            </p>
          </div>

          <button
            type="button"
            onClick={() => {
              setEmail("demo@placeko.com");
              setPassword("demo123");
            }}
            className="
              whitespace-nowrap
              rounded-lg
              bg-indigo-600
              px-3
              py-2
              text-xs
              font-semibold
              text-white
              transition
              hover:bg-indigo-700
            "
          >
            Use Demo
          </button>

        </div>
      </div>

      {/* OAuth */}

      <OAuthButtons
        onGoogle={onGoogle ?? (() => {})}
        onGithub={onGithub ?? (() => {})}
      />

      {/* Divider */}

      <div className="flex items-center gap-4">

        <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />

        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
          Or continue with email
        </span>

        <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />

      </div>

      {/* Form */}

      <form
        onSubmit={handleSubmit}
        className="space-y-5"
      >

        <FormInput
          label="Email Address"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={setEmail}
          icon={Mail}
        />

        {/* Password */}

        <div className="relative">

          <FormInput
            label="Password"
            type={showPassword ? "text" : "password"}
            placeholder="Enter your password"
            value={password}
            onChange={setPassword}
            icon={Lock}
          />

          <button
            type="button"
            onClick={() => setShowPassword((previous) => !previous)}
            className="
              absolute
              right-3
              top-[34px]
              rounded-lg
              p-2
              text-slate-400
              transition
              hover:bg-slate-100
              hover:text-slate-600
              dark:hover:bg-slate-800
            "
            aria-label={
              showPassword
                ? "Hide password"
                : "Show password"
            }
          >
            {showPassword ? (
              <EyeOff size={18} />
            ) : (
              <Eye size={18} />
            )}
          </button>

        </div>

        {/* Remember / Forgot */}

        <div className="flex items-center justify-between">

          <label className="flex cursor-pointer items-center gap-2">

            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(event) =>
                setRememberMe(event.target.checked)
              }
              className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
            />

            <span className="text-sm text-slate-600 dark:text-slate-300">
              Remember me
            </span>

          </label>

          <button
            type="button"
            onClick={onForgotPassword}
            className="
              text-sm
              font-semibold
              text-indigo-600
              hover:text-indigo-700
              dark:text-indigo-400
            "
          >
            Forgot password?
          </button>

        </div>

        {/* Submit */}

        <button

  type="submit"

  disabled={isLoading}

  className="

    flex
    w-full
    items-center
    justify-center
    gap-2
    rounded-xl
    bg-indigo-600
    px-5
    py-3.5
    text-sm
    font-bold
    text-white
    shadow-lg
    shadow-indigo-200
    transition-all
    hover:bg-indigo-700
    disabled:cursor-not-allowed
    disabled:opacity-60
    dark:shadow-none
  "
>
  {isLoading ? "Signing in..." : "Sign In to Dashboard"}
  {!isLoading && <ArrowRight size={17} />}
</button>
      </form>

      {/* Sign Up */}

      <p className="text-center text-sm text-slate-500 dark:text-slate-400">

        Don't have an account?{" "}

        <button
          type="button"
          onClick={onSignup}
          className="font-semibold text-indigo-600 hover:text-indigo-700 dark:text-indigo-400"
        >
          Sign Up
        </button>

      </p>

    </div>
  );
};

export default LoginForm;