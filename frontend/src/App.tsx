
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


function App() {
  const navigate = useNavigate();

  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
  document.documentElement.classList.toggle("dark", isDarkMode);
}, [isDarkMode]);

  const handleNavigate = (tab: string) => {
    navigate(tab);
  };

  const handleToggleDarkMode = () => {
    setIsDarkMode((prev) => !prev);
  };

  return (
    <Routes>
      <Route
        path="/"
        element={
          <LandingPage
            onNavigate={handleNavigate}
            isDarkMode={isDarkMode}
            onToggleDarkMode={handleToggleDarkMode}
          />
        }
      />

      <Route
        path="/auth"
        element={<AuthPage />}
      />

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


<Route
  path="/settings"
  element={
    <ProtectedRoute>
      <DashboardLayout>
        <SettingsPage
          isDarkMode={isDarkMode}
          onToggleDarkMode={handleToggleDarkMode}
        />
      </DashboardLayout>
    </ProtectedRoute>
  }

/>

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