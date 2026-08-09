import { useState } from "react";
import AuthLayout from "../../components/auth/AuthLayout";
import AuthCard from "../../components/auth/AuthCard";
import LoginForm from "../../components/auth/LoginForm";
import RegisterForm from "../../components/auth/RegisterForm";

type AuthMode = "login" | "register";
const AuthPage = () => {
  const [mode, setMode] = useState<AuthMode>("login");

  const handleBack = () => {
    window.location.href = "/";
  };

  const handleLoginSuccess = () => {
    window.location.href = "/dashboard";
  };

  const handleRegisterSuccess = () => {
    window.location.href = "/dashboard";
  };

  const handleGoogle = () => {
    console.log("Google authentication");
  };

  const handleGithub = () => {
    console.log("GitHub authentication");
  };

  return (
    <AuthLayout onBack={handleBack}>
      <AuthCard
        title={
          mode === "login"
            ? "Welcome back to Placeko"
            : "Create your Placeko account"
        }
        subtitle={
          mode === "login"
            ? "Sign in to continue your career journey."
            : "Start your AI-powered career journey today."
        }
      >
        {mode === "login" ? (
          <LoginForm
            onLogin={handleLoginSuccess}
            onGoogle={handleGoogle}
            onGithub={handleGithub}
            onSignup={() => setMode("register")}
            onForgotPassword={() =>
              console.log("Forgot password")
            }
          />
        ) : (
          <RegisterForm
            onRegister={handleRegisterSuccess}
            onGoogle={handleGoogle}
            onGithub={handleGithub}
            onLogin={() => setMode("login")}
          />
        )}
      </AuthCard>
    </AuthLayout>
  );
};

export default AuthPage;