import {
  ArrowUpRight,
  MapPin,
  Building2,
  Clock3,
} from "lucide-react";

import type { JobRecommendation } from "./types";

interface JobCardProps {
  job: JobRecommendation;
}

const JobCard = ({ job }: JobCardProps) => {
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
      <div className="flex justify-between gap-8">

        {/* LEFT */}

        <div className="flex flex-1 gap-5">

          {/* Company Logo */}

          <div
            className="
              flex
              h-14
              w-14
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
            {job.company.charAt(0)}
          </div>

          {/* Info */}

          <div className="flex-1">

            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              {job.role}
            </h3>

            <div className="mt-1 flex items-center gap-2 text-slate-600 dark:text-slate-300">

              <Building2 size={16} />

              <span className="font-medium">
                {job.company}
              </span>

            </div>

            <div className="mt-3 flex flex-wrap items-center gap-5 text-sm text-slate-500">

              <div className="flex items-center gap-2">

                <MapPin size={15} />

                {job.location}

              </div>

              <div className="flex items-center gap-2">

                <Clock3 size={15} />

                Posted 2 days ago

              </div>

            </div>

            {/* Skills */}

            <div className="mt-5 flex flex-wrap gap-2">

              {job.skills.map((skill) => (
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

          </div>

        </div>

        {/* RIGHT */}

        <div
          className="
            flex
            min-w-[170px]
            flex-col
            items-end
            justify-between
          "
        >

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
            {job.match}% Match
          </span>

          <p className="mt-6 text-1xl font-bold text-slate-900 dark:text-white">
            {job.salary}
          </p>

          <button
            className="
              mt-8
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