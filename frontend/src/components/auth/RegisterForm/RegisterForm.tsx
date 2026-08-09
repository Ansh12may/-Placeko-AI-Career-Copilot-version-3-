import { useState } from "react";
import {
  User,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
} from "lucide-react";

import FormInput from "../FormInput";
import OAuthButtons from "../OAuthButtons";
import { useAuth } from "../../../context/AuthContext";


interface RegisterFormProps {
  onRegister?: () => void;
  onGoogle?: () => void;
  onGithub?: () => void;
  onLogin?: () => void;
}

const RegisterForm = ({
  onRegister,
  onGoogle,
  onGithub,
  onLogin,
}: RegisterFormProps) => {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [isLoading, setIsLoading] = useState(false);
  const [registerError, setRegisterError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const { register } = useAuth();

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setRegisterError("");
    setSuccessMessage("");

    if (!fullName || !email || !password || !confirmPassword) {
      setRegisterError("Please fill in all required fields.");
      return;
    }

    if (password !== confirmPassword) {
      setRegisterError("Passwords do not match.");
      return;
    }

    try {
      setIsLoading(true);

      await register(
      fullName,
        email,
    password
);
      setSuccessMessage(
        "Account created successfully."
      );

      onRegister?.();
    } catch (error: any) {
      console.error("Registration failed:", error);

      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        "Registration failed. Please try again.";

      setRegisterError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">

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

        {/* Full Name */}

        <FormInput
          label="Full Name"
          type="text"
          placeholder="Enter your full name"
          value={fullName}
          onChange={setFullName}
          icon={User}
        />

        {/* Email */}

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
            placeholder="Create a password"
            value={password}
            onChange={setPassword}
            icon={Lock}
          />

          <button
            type="button"
            onClick={() =>
              setShowPassword((previous) => !previous)
            }
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

        {/* Confirm Password */}

        <div className="relative">

          <FormInput
            label="Confirm Password"
            type={
              showConfirmPassword
                ? "text"
                : "password"
            }
            placeholder="Confirm your password"
            value={confirmPassword}
            onChange={setConfirmPassword}
            icon={Lock}
          />

          <button
            type="button"
            onClick={() =>
              setShowConfirmPassword(
                (previous) => !previous
              )
            }
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
              showConfirmPassword
                ? "Hide password"
                : "Show password"
            }
          >
            {showConfirmPassword ? (
              <EyeOff size={18} />
            ) : (
              <Eye size={18} />
            )}
          </button>

        </div>

        {/* Terms */}

        <label className="flex cursor-pointer items-start gap-2">

          <input
            type="checkbox"
            required
            className="
              mt-0.5
              h-4
              w-4
              rounded
              border-slate-300
              text-indigo-600
              focus:ring-indigo-500
            "
          />

          <span className="text-xs leading-5 text-slate-500 dark:text-slate-400">
            I agree to the{" "}
            <button
              type="button"
              className="font-semibold text-indigo-600 hover:text-indigo-700 dark:text-indigo-400"
            >
              Terms of Service
            </button>{" "}
            and{" "}
            <button
              type="button"
              className="font-semibold text-indigo-600 hover:text-indigo-700 dark:text-indigo-400"
            >
              Privacy Policy
            </button>
            .
          </span>

        </label>

        {/* Error */}

        {registerError && (
          <div
            className="
              rounded-xl
              border
              border-red-200
              bg-red-50
              px-4
              py-3
              text-sm
              font-medium
              text-red-600
              dark:border-red-900/50
              dark:bg-red-950/30
              dark:text-red-400
            "
          >
            {registerError}
          </div>
        )}

        {/* Success */}

        {successMessage && (
          <div
            className="
              rounded-xl
              border
              border-emerald-200
              bg-emerald-50
              px-4
              py-3
              text-sm
              font-medium
              text-emerald-600
              dark:border-emerald-900/50
              dark:bg-emerald-950/30
              dark:text-emerald-400
            "
          >
            {successMessage}
          </div>
        )}

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
          {isLoading
            ? "Creating Account..."
            : "Create Account"}

          {!isLoading && (
            <ArrowRight size={17} />
          )}
        </button>

      </form>

      {/* Login */}

      <p className="text-center text-sm text-slate-500 dark:text-slate-400">

        Already have an account?{" "}

        <button
          type="button"
          onClick={onLogin}
          className="
            font-semibold
            text-indigo-600
            hover:text-indigo-700
            dark:text-indigo-400
          "
        >
          Sign In
        </button>

      </p>

    </div>
  );
};

export default RegisterForm;