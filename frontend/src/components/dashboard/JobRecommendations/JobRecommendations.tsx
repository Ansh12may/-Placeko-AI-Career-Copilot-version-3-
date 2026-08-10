import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

import JobCard from "./JobCard";
import type { Job } from "../../../api/job";

interface JobRecommendationsProps {
  jobs: Job[];
}

const JobRecommendations = ({
  jobs,
}: JobRecommendationsProps) => {
  const navigate = useNavigate();

  // Only show the top recommendations on dashboard
  const displayedJobs = jobs.slice(0, 3);

  return (
    <section className="mt-8">

      {/* Header */}

      <div className="mb-6 flex items-center justify-between">

        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Recommended Jobs
          </h2>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            AI-powered opportunities matched to your active resume.
          </p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/jobs")}
          className="
            flex
            items-center
            gap-2
            text-sm
            font-semibold
            text-indigo-600
            transition-colors
            hover:text-indigo-700
          "
        >
          View All
          <ArrowRight size={16} />
        </button>

      </div>

      {/* Empty State */}

      {displayedJobs.length === 0 ? (

        <div
          className="
            rounded-2xl
            border
            border-dashed
            border-slate-300
            bg-white
            p-8
            text-center
            dark:border-slate-700
            dark:bg-slate-900
          "
        >
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">
            No job recommendations yet
          </p>

          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Upload or activate a resume to discover jobs matched to your profile.
          </p>

          <button
            type="button"
            onClick={() => navigate("/resume")}
            className="
              mt-5
              rounded-xl
              bg-indigo-600
              px-4
              py-2.5
              text-sm
              font-semibold
              text-white
              transition
              hover:bg-indigo-700
            "
          >
            Manage Resume
          </button>
        </div>

      ) : (

        /* Job Cards */

        <div className="flex flex-col gap-6">

          {displayedJobs.map((job) => (
            <JobCard
              key={`${job.title}-${job.company}-${job.location}`}
              job={job}
            />
          ))}

        </div>

      )}

    </section>
  );
};

export default JobRecommendations;