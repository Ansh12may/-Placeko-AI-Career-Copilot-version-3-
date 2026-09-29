import "./App.css";
import { Routes, Route, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import LandingPage from "./pages/Landing/landingPage";
import DashboardPage from "./pages/DashboardPage/DashboardPage";
import AuthPage from "./pages/Auth/AuthPage";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import ProfilePage from "./pages/Profile/ProfilePage";
import DashboardLayout from "./components/dashboard/DashboardLayout/DashboardLayout";
import SettingsPage from "./pages/Settings/SettingsPage";
import ResumeLibraryPage from "./pages/Resume/ResumeLibraryPage";
import ResumeAnalysisPage from "./pages/ResumeAnalysis/ResumeAnalysisPage";
import ResumeAnalysisRedirect from "./pages/ResumeAnalysis/ResumeAnalysisRedirect";
import RecommendedJobsPage from "./pages/RecommendedJobsPage/RecommendedJobsPage";
import InterviewSetupPage from "./pages/Interview/InterviewSetupPage";
import InterviewPage from "./pages/Interview/InterviewPage";
import InterviewReportPage from "./pages/Interview/InterviewReportPage";
import InterviewHistoryPage from "./pages/Interview/InterviewHistoryPage";
import ApplicationsPage from "./pages/applications/ApplicationsPage";
import OAuthCallbackPage from "./pages/Auth/OAuthCallbackPage";

// NEW
import JobResearchPage from "./pages/JobResearchPage/JobResearchPage";

function App() {
  const navigate = useNavigate();

  const [isDarkMode, setIsDarkMode] =
    useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle(
      "dark",
      isDarkMode
    );
  }, [isDarkMode]);

  const handleNavigate = (tab: string) => {
    switch (tab) {
      case "landing":
        navigate("/");
        break;

      case "auth":
        navigate("/auth");
        break;

      case "dashboard":
        navigate("/dashboard");
        break;

      case "profile":
        navigate("/profile");
        break;

      case "settings":
        navigate("/settings");
        break;

      case "resumes":
        navigate("/resume");
        break;

      case "resume-details":
        navigate("/resume-analysis");
        break;

      case "job-details":
        navigate("/jobs");
        break;

      // NEW
      case "job-research":
        navigate("/jobs/research");
        break;

      case "applications":
        navigate("/applications");
        break;

      case "mock-interview":
        navigate("/interview");
        break;

      case "interview-report":
        navigate("/interview/history");
        break;

      default:
        console.warn(
          `Unknown navigation tab: ${tab}`
        );
    }
  };

  const handleToggleDarkMode = () => {
    setIsDarkMode(
      (prev) => !prev
    );
  };

  return (
    <Routes>

      {/* =====================================================
          LANDING
          ===================================================== */}

      <Route
        path="/"
        element={
          <LandingPage
            onNavigate={handleNavigate}
            isDarkMode={isDarkMode}
            onToggleDarkMode={
              handleToggleDarkMode
            }
          />
        }
      />

      {/* =====================================================
          OAUTH
          ===================================================== */}

      <Route
        path="/oauth/callback"
        element={
          <OAuthCallbackPage />
        }
      />

      {/* =====================================================
          AUTH
          ===================================================== */}

      <Route
        path="/auth"
        element={
          <AuthPage />
        }
      />

      {/* =====================================================
          DASHBOARD
          ===================================================== */}

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <DashboardPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          PROFILE
          ===================================================== */}

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ProfilePage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          SETTINGS
          ===================================================== */}

      <Route
        path="/settings"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <SettingsPage
                isDarkMode={
                  isDarkMode
                }
                onToggleDarkMode={
                  handleToggleDarkMode
                }
              />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          RESUME LIBRARY
          ===================================================== */}

      <Route
        path="/resume"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ResumeLibraryPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          RESUME ANALYSIS
          ===================================================== */}

      <Route
        path="/resume-analysis/:resumeId"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ResumeAnalysisPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/resume-analysis"
        element={
          <ProtectedRoute>
            <ResumeAnalysisRedirect />
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          RECOMMENDED JOBS
          ===================================================== */}

      <Route
        path="/jobs"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <RecommendedJobsPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          AI JOB RESEARCH
          ===================================================== */}

      <Route
        path="/jobs/research"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <JobResearchPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          INTERVIEW SETUP
          ===================================================== */}

      <Route
        path="/interview"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <InterviewSetupPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          INTERVIEW HISTORY
          ===================================================== */}

      <Route
        path="/interview/history"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <InterviewHistoryPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          INTERVIEW SESSION
          ===================================================== */}

      <Route
        path="/interview/:sessionId"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <InterviewPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          INTERVIEW REPORT
          ===================================================== */}

      <Route
        path="/interview/:sessionId/report"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <InterviewReportPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* =====================================================
          APPLICATIONS
          ===================================================== */}

      <Route
        path="/applications"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ApplicationsPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

export default App;