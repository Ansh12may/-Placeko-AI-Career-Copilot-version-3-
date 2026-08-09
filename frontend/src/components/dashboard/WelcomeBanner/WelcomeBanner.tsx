import { Mic } from "lucide-react";

interface WelcomeBannerProps {
  userName: string;
  resumeName: string;
  matchedJobs: number;
  improvementAreas: number;
  hasResume: boolean;
  onViewMatches: () => void;
  onStartInterview: () => void;
}

const WelcomeBanner = ({
  userName,
  resumeName,
  matchedJobs,
  improvementAreas,
  hasResume,
  onViewMatches,
  onStartInterview,
}: WelcomeBannerProps) => {
  return (
    <section className="relative overflow-hidden rounded-2xl bg-indigo-700 p-6 text-white shadow-lg shadow-indigo-100 dark:shadow-none">

      <div className="relative z-10 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

        {/* Left */}

        <div className="space-y-2">

          <div className="flex items-center gap-2">

            <span
              className="
                rounded-full
                border
                border-indigo-500
                bg-indigo-600
                px-2.5
                py-0.5
                font-mono
                text-[10px]
                font-bold
                uppercase
                tracking-wider
                text-indigo-100
              "
            >
              Pro Analysis
            </span>

            <span className="text-xs text-indigo-200">
              •{" "}
              {hasResume
                ? `Active Resume: ${resumeName}`
                : "No active resume"}
            </span>

          </div>

          <h1 className="text-3xl font-bold tracking-tight">
            Welcome back, {userName} 👋
          </h1>

          {hasResume ? (
            <p className="max-w-2xl text-sm leading-relaxed text-indigo-100">
              Your resume analysis is complete. We've found{" "}
              <span className="font-bold text-white">
                {matchedJobs} high-match opportunities
              </span>{" "}
              and identified{" "}
              <span className="font-bold text-white">
                {improvementAreas} key areas
              </span>{" "}
              to improve before your next interview.
            </p>
          ) : (
            <p className="max-w-2xl text-sm leading-relaxed text-indigo-100">
              Upload your resume to get personalized job
              recommendations and AI-powered resume analysis.
            </p>
          )}

        </div>

        {/* Right */}

        <div className="flex items-center gap-3">

          <button
            onClick={onViewMatches}
            className="
              rounded-lg
              bg-white
              px-4
              py-2.5
              text-xs
              font-bold
              text-indigo-700
              transition-colors
              hover:bg-slate-100
            "
          >
            {hasResume
              ? "View My Matches"
              : "Upload Resume"}
          </button>

          <button
            onClick={onStartInterview}
            className="
              flex
              items-center
              gap-2
              rounded-lg
              border
              border-indigo-500
              bg-indigo-600
              px-4
              py-2.5
              text-xs
              font-bold
              transition-colors
              hover:bg-indigo-500
            "
          >
            <Mic size={15} />
            Start Mock Prep
          </button>

        </div>

      </div>

    </section>
  );
};

export default WelcomeBanner;