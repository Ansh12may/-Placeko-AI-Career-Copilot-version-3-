import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import WelcomeBanner from "../../components/dashboard/WelcomeBanner";
import StatsGrid from "../../components/dashboard/Stats/StatsGrid";
import QuickActions from "../../components/dashboard/QuickActions";
import JobRecommendations from "../../components/dashboard/JobRecommendations";
import RecentActivity from "../../components/dashboard/RecentActivity";

import { getCurrentUser } from "../../api/auth";
import { getResumes,getResumeById, } from "../../api/resume";
import { getApplications } from "../../api/application";
import {
  getRecommendedJobs,
  type Job,
} from "../../api/job";

import type { User } from "../../api/auth";
import type { ResumeLibraryItem,ResumeDetail } from "../../types/resume";
import type { Application } from "../../types/application";

import { getInterviewHistory } from "../../api/interview";
import type { InterviewSession } from "../../types/interview";

import type { Activity } from "../../components/dashboard/RecentActivity/types";


// =========================================================
// Dashboard Page
// =========================================================

const DashboardPage = () => {
  const navigate = useNavigate();

  // =========================================================
  // State
  // =========================================================

  const [user, setUser] =
    useState<User | null>(null);

  const [activeResume, setActiveResume] =
    useState<ResumeLibraryItem | null>(null);

  const [activeResumeDetail, setActiveResumeDetail] =
  useState<ResumeDetail | null>(null);

  const [applications, setApplications] =
    useState<Application[]>([]);

  const [jobMatches, setJobMatches] =
    useState(0);

  const [recommendedJobs, setRecommendedJobs] =
    useState<Job[]>([]);

  const [interviews, setInterviews] =
    useState<InterviewSession[]>([]);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  // =========================================================
  // Load Dashboard Data
  // =========================================================

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // -----------------------------------------------------
        // Load all dashboard data in parallel
        // -----------------------------------------------------

        const [
  currentUser,
  resumeResponse,
  applicationData,
  recommendedJobData,
  interviewHistory,
] = await Promise.all([
  getCurrentUser(),
  getResumes(),
  getApplications(),
  getRecommendedJobs().catch((error) => {
    console.error(
      "Dashboard: failed to load recommended jobs:",
      error
    );

    return [];
  }),
  getInterviewHistory(),
]);

        // -----------------------------------------------------
        // User
        // -----------------------------------------------------

        setUser(currentUser);


        // -----------------------------------------------------
        // Active Resume
        // -----------------------------------------------------

        const activeResume =
  resumeResponse.data.find(
    (resume) => resume.is_active
  ) ?? null;

setActiveResume(activeResume);

if (activeResume) {
  const resumeDetailResponse =
    await getResumeById(activeResume.id);

  setActiveResumeDetail(
    resumeDetailResponse.data
  );
} else {
  setActiveResumeDetail(null);
}


        // -----------------------------------------------------
        // Applications
        // -----------------------------------------------------

        setApplications(
          applicationData
        );


        // -----------------------------------------------------
        // Interviews
        // -----------------------------------------------------

        setInterviews(
          interviewHistory
        );


        // -----------------------------------------------------
        // Recommended Jobs
        // -----------------------------------------------------

        setRecommendedJobs(
          recommendedJobData
        );

        setJobMatches(
          recommendedJobData.length
        );

      } catch (error) {

        console.error(
          "Dashboard: failed to load data:",
          error
        );

        setError(
          "Unable to load your dashboard data."
        );

      } finally {

        setIsLoading(false);

      }
    };

    loadDashboardData();
  }, []);


  // =========================================================
  // Interview Readiness
  // =========================================================

  const completedInterviews =
    interviews.filter(
      (interview) =>
        interview.status === "Completed" &&
        interview.report
    );


  const interviewReadiness =
    completedInterviews.length > 0
      ? Math.round(
          (
            completedInterviews.reduce(
              (total, interview) =>
                total +
                interview.report!.overall_score.score,
              0
            ) /
            completedInterviews.length
          ) * 10
        )
      : null;


  // =========================================================
  // Improvement Areas
  // =========================================================

  const improvementAreas =
    activeResumeDetail
      ? new Set([
          ...activeResumeDetail.ats_report.weaknesses,
          ...activeResumeDetail.ats_report.missing_keywords,
        ]).size
      : 0;


  // =========================================================
  // Recent Activity
  // =========================================================

  const activities: Activity[] = [

    // -------------------------------------------------------
    // Resume Activity
    // -------------------------------------------------------

    ...(activeResume
      ? [
          {
            id: 1,

            title: "Resume analyzed",

            description:

  `Your resume received an ATS score of ${

    activeResumeDetail

      ? Math.round(

          activeResumeDetail.ats_report.overall_score

        )

      : activeResume.ats_score !== null

        ? Math.round(activeResume.ats_score)

        : "N/A"

  }.`,

            time:
              formatRelativeTime(
                activeResume.updated_at
              ),

            type: "resume" as const,

            timestamp:
              new Date(
                activeResume.updated_at
              ).getTime(),
          },
        ]
      : []),


    // -------------------------------------------------------
    // Interview Activity
    // -------------------------------------------------------

    ...interviews
      .filter(
        (interview) =>
          interview.status === "Completed"
      )
      .map(
        (interview, index) => {

         const timestamp = interview.started_at

  ? new Date(interview.started_at).getTime()

  : 0;

          return {
            id: 100 + index,

            title:
              "Interview completed",

            description:
              interview.report
                ? `You scored ${interview.report.overall_score.score.toFixed(
                    1
                  )}/10 in your AI mock interview.`
                : "Your AI mock interview was completed.",

            time:

  interview.started_at

    ? formatRelativeTime(interview.started_at)

    : "Recently",
            type: "interview" as const,

            timestamp,
          };
        }
      ),


    // -------------------------------------------------------
    // Application Activity
    //
    // We only use the confirmed `status` field here.
    // Until we have the exact application timestamp field,
    // these activities are placed after timestamped events.
    // -------------------------------------------------------

    ...applications.map(
      (application, index) => ({
        id: 200 + index,

        title:
          "Application activity",

        description:
          `Application status: ${formatApplicationStatus(
            application.status
          )}`,

        time:
          "Recently",

        type: "job" as const,

        timestamp:
          0,
      })
    ),

  ]
    // -------------------------------------------------------
    // Sort newest first
    // -------------------------------------------------------

    .sort(
      (a, b) =>
        b.timestamp - a.timestamp
    )

    // -------------------------------------------------------
    // Keep latest five
    // -------------------------------------------------------

    .slice(0, 5)

    // -------------------------------------------------------
    // Remove internal timestamp before passing to UI
    // -------------------------------------------------------

    .map(
      ({
        timestamp,
        ...activity
      }) => activity
    );


  // =========================================================
  // Loading State
  // =========================================================

  if (isLoading) {
    return (
      <div className="flex min-h-[500px] items-center justify-center">

        <div className="text-sm font-medium text-slate-500">
          Loading your career dashboard...
        </div>

      </div>
    );
  }


  // =========================================================
  // Error State
  // =========================================================

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-5">

        <p className="text-sm font-semibold text-red-600">
          {error}
        </p>

      </div>
    );
  }


  // =========================================================
  // Dashboard
  // =========================================================

  return (
    <>

      {/* =====================================================
          Welcome Banner
          ===================================================== */}

      <WelcomeBanner
        userName={
          user?.full_name || "there"
        }

        resumeName={
          activeResume?.file_name ||
          "No resume uploaded"
        }

        matchedJobs={
          jobMatches
        }

        improvementAreas={
          improvementAreas
        }

        hasResume={
          !!activeResume
        }

        onViewMatches={() =>
          navigate("/jobs")
        }

        onStartInterview={() =>
          navigate("/interview")
        }
      />


      {/* =====================================================
          Statistics
          ===================================================== */}

      <StatsGrid
        resumeScore={
      activeResumeDetail?.ats_report.overall_score ??
      activeResume?.ats_score ??
      null

}

        jobMatches={
          jobMatches
        }

        applications={
          applications.length
        }

        interviewReadiness={
          interviewReadiness
        }
      />


      {/* =====================================================
          Quick Actions
          ===================================================== */}

      <QuickActions />


      {/* =====================================================
          Jobs + Recent Activity
          ===================================================== */}

      <div className="mt-8 grid grid-cols-1 gap-8 xl:grid-cols-3">

        {/* ---------------------------------------------------
            Recommended Jobs
            --------------------------------------------------- */}

        <div className="xl:col-span-2">

          <JobRecommendations
            jobs={recommendedJobs}
          />

        </div>


        {/* ---------------------------------------------------
            Recent Activity
            --------------------------------------------------- */}

        <div>

          <RecentActivity
            activities={activities}
          />

        </div>

      </div>

    </>
  );
};


// =========================================================
// Relative Time
// =========================================================

const formatRelativeTime = (
  date: string
): string => {

  const timestamp =
    new Date(date).getTime();

  if (Number.isNaN(timestamp)) {
    return "Recently";
  }

  const difference =
    Date.now() - timestamp;

  const minutes =
    Math.floor(
      difference / (1000 * 60)
    );

  if (minutes < 1) {
    return "Just now";
  }

  if (minutes < 60) {
    return `${minutes} min ago`;
  }

  const hours =
    Math.floor(
      minutes / 60
    );

  if (hours < 24) {
    return `${hours} hr ago`;
  }

  const days =
    Math.floor(
      hours / 24
    );

  if (days === 1) {
    return "Yesterday";
  }

  if (days < 7) {
    return `${days} days ago`;
  }

  return new Date(
    date
  ).toLocaleDateString(
    "en-IN",
    {
      day: "numeric",
      month: "short",
    }
  );
};


// =========================================================
// Application Status Formatting
// =========================================================

const formatApplicationStatus = (
  status: string
): string => {

  if (!status) {
    return "Unknown";
  }

  return status
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) =>
      char.toUpperCase()
    );
};


export default DashboardPage;