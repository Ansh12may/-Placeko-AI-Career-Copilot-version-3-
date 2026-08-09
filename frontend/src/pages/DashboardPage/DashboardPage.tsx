import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatsGrid from "../../components/dashboard/Stats/StatsGrid";
import QuickActions from "../../components/dashboard/QuickActions";
import JobRecommendations from "../../components/dashboard/JobRecommendations";
import RecentActivity from "../../components/dashboard/RecentActivity";

import { getCurrentUser } from "../../api/auth";
import { getResumes } from "../../api/resume";

import type { User } from "../../api/auth";
import type { ResumeLibraryItem } from "../../types/resume";

const DashboardPage = () => {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [activeResume, setActiveResume] =
    useState<ResumeLibraryItem | null>(null);

  useEffect(() => {
    const loadDashboardData = async () => {
      console.log("Dashboard: loading started");

      try {
        console.log("Dashboard: requesting current user...");

        const currentUser = await getCurrentUser();

        console.log(
          "Dashboard: current user received:",
          currentUser
        );

        setUser(currentUser);

        console.log("Dashboard: requesting resumes...");

        const resumeResponse = await getResumes();

        console.log(
          "Dashboard: resume response:",
          resumeResponse
        );

        const active = resumeResponse.data.find(
          (resume) => resume.is_active
        );

        console.log(
          "Dashboard: active resume:",
          active
        );

        setActiveResume(active ?? null);

        console.log("Dashboard: loading finished");

      } catch (error) {
        console.error(
          "Dashboard: failed to load data:",
          error
        );
      }
    };

    loadDashboardData();
  }, []);

  return (
    <>
      <WelcomeBanner
        userName={user?.full_name || "there"}
        resumeName={
          activeResume?.file_name ||
          "No resume uploaded"
        }
        matchedJobs={24}
        improvementAreas={3}
        hasResume={!!activeResume}
        onViewMatches={() => navigate("/jobs")}
        onStartInterview={() => navigate("/interview")}
      />

      <StatsGrid
        resumeScore={
          activeResume?.ats_score ?? null
        }
        jobMatches={24}
      />

      <QuickActions />

      <div className="mt-8 grid grid-cols-6 gap-8 xl:grid-cols-3">

        <div className="xl:col-span-2">
          <JobRecommendations />
        </div>

        <div>
          <RecentActivity />
        </div>

      </div>
    </>
  );
};

export default DashboardPage;