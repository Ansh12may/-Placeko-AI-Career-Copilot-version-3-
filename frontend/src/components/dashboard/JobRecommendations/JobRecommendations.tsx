import { ArrowRight } from "lucide-react";

import JobCard from "./JobCard";
import { recommendedJobs } from "./data";

const JobRecommendations = () => {
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

      {/* Job Cards */}

      <div className="flex flex-col gap-6">

        {recommendedJobs.map((job) => (
          <JobCard
            key={job.id}
            job={job}
          />
        ))}

      </div>

    </section>
  );
};

export default JobRecommendations;