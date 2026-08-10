import {
  ArrowUpRight,
  MapPin,
  Building2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import type { Job } from "../../../api/job";

interface JobCardProps {
  job: Job;
}

const JobCard = ({ job }: JobCardProps) => {
  const navigate = useNavigate();

  const matchPercentage =
    job.match_score !== null &&
    job.match_score !== undefined
      ? Math.round(job.match_score * 100)
      : null;

  const companyInitial =
    job.company?.trim().charAt(0).toUpperCase() || "C";

  const handleViewJob = () => {
    navigate("/jobs", {
      state: {
        selectedJob: job,
      },
    });
  };

  return (
    <div
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-lg
        dark:border-slate-800
        dark:bg-slate-900
      "
    >
      <div className="flex flex-col gap-6 md:flex-row md:justify-between">

        {/* LEFT */}

        <div className="flex flex-1 gap-5">

          {/* Company Initial */}

          <div
            className="
              flex
              h-14
              w-14
              shrink-0
              items-center
              justify-center
              rounded-xl
              bg-slate-100
              text-xl
              font-bold
              text-slate-700
              dark:bg-slate-800
              dark:text-white
            "
          >
            {companyInitial}
          </div>

          {/* Job Information */}

          <div className="min-w-0 flex-1">

            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              {job.title}
            </h3>

            <div className="mt-1 flex items-center gap-2 text-slate-600 dark:text-slate-300">

              <Building2 size={16} />

              <span className="font-medium">
                {job.company}
              </span>

            </div>

            <div className="mt-3 flex flex-wrap items-center gap-5 text-sm text-slate-500 dark:text-slate-400">

              <div className="flex items-center gap-2">

                <MapPin size={15} />

                {job.location || "Location not specified"}

              </div>

              {job.employment_type && (
                <span>
                  {job.employment_type}
                </span>
              )}

              {job.experience && (
                <span>
                  {job.experience}
                </span>
              )}

            </div>

            {/* Skills */}

            {job.skills.length > 0 && (
              <div className="mt-5 flex flex-wrap gap-2">

                {job.skills.slice(0, 6).map((skill) => (
                  <span
                    key={skill}
                    className="
                      rounded-full
                      bg-slate-100
                      px-3
                      py-1
                      text-xs
                      font-medium
                      text-slate-700
                      dark:bg-slate-800
                      dark:text-slate-300
                    "
                  >
                    {skill}
                  </span>
                ))}

              </div>
            )}

          </div>

        </div>

        {/* RIGHT */}

        <div
          className="
            flex
            min-w-[170px]
            flex-col
            items-start
            justify-between
            md:items-end
          "
        >

          {/* Match */}

          {matchPercentage !== null ? (
            <span
              className="
                rounded-full
                bg-emerald-100
                px-4
                py-1
                text-sm
                font-semibold
                text-emerald-700
                dark:bg-emerald-900/30
                dark:text-emerald-400
              "
            >
              {matchPercentage}% Match
            </span>
          ) : (
            <span
              className="
                rounded-full
                bg-slate-100
                px-4
                py-1
                text-sm
                font-semibold
                text-slate-500
                dark:bg-slate-800
                dark:text-slate-400
              "
            >
              Match unavailable
            </span>
          )}

          {/* Salary */}

          <p className="mt-4 text-lg font-bold text-slate-900 dark:text-white">
            {job.salary || "Salary not specified"}
          </p>

          {/* View Job */}

          <button
            type="button"
            onClick={handleViewJob}
            className="
              mt-6
              flex
              items-center
              gap-2
              rounded-xl
              bg-indigo-600
              px-5
              py-2.5
              text-sm
              font-semibold
              text-white
              transition
              hover:bg-indigo-700
            "
          >
            View Job

            <ArrowUpRight size={16} />

          </button>

        </div>

      </div>
    </div>
  );
};

export default JobCard;