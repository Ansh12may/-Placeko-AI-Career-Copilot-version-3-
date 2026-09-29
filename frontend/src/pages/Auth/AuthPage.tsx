import { useState } from "react";
import AuthLayout from "../../components/auth/AuthLayout";
import AuthCard from "../../components/auth/AuthCard";
import LoginForm from "../../components/auth/LoginForm";
import RegisterForm from "../../components/auth/RegisterForm";
import { useNavigate } from "react-router-dom";

type AuthMode = "login" | "register";

const AuthPage = () => {

  const [mode, setMode] = useState<AuthMode>("login");
  const navigate = useNavigate();

  const handleBack = () => {
    navigate("/");
  };

  const handleLoginSuccess = () => {
    navigate("/dashboard");

  };

  const handleRegisterSuccess = () => {
    navigate("/dashboard");

  };

  const handleGoogle = () => {
    window.location.href =
      `${import.meta.env.VITE_API_URL}/api/auth/google`;
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
            onSignup={() => setMode("register")}
            onForgotPassword={() =>
              console.log("Forgot password")
            }
          />
        ) : (
          <RegisterForm
            onRegister={handleRegisterSuccess}
            onGoogle={handleGoogle}
            onLogin={() => setMode("login")}
          />
        )}
      </AuthCard>
    </AuthLayout>
  );
};

export default AuthPage;