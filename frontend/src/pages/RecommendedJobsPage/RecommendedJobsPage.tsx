import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Bookmark,
  BriefcaseBusiness,
  Building2,
  MapPin,
  Search,
  Send,
  Mic,
} from "lucide-react";

import {
  getRecommendedJobs,
  type Job,
} from "../../api/job";


const RecommendedJobsPage = () => {
  const navigate = useNavigate();

  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [filter, setFilter] = useState<
    "all" | "full-time" | "remote" | "hybrid"
  >("all");

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // =========================================================
  // Load Recommended Jobs
  // =========================================================

  useEffect(() => {
    const loadJobs = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const recommendedJobs =
          await getRecommendedJobs();

        setJobs(recommendedJobs);

        if (recommendedJobs.length > 0) {
          setSelectedJob(recommendedJobs[0]);
        }
      } catch (err) {
        console.error(
          "Failed to load recommended jobs:",
          err
        );

        setError(
          "Unable to load recommended jobs."
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadJobs();
  }, []);

  // =========================================================
  // Search + Filter
  // =========================================================

  const filteredJobs = useMemo(() => {
    const query = searchQuery
      .trim()
      .toLowerCase();

    return jobs.filter((job) => {
      const matchesSearch =
        !query ||
        job.title.toLowerCase().includes(query) ||
        job.company.toLowerCase().includes(query) ||
        job.location.toLowerCase().includes(query) ||
        job.skills.some((skill) =>
          skill.toLowerCase().includes(query)
        );

      const employmentType =
        job.employment_type?.toLowerCase() ?? "";

      const location =
        job.location.toLowerCase();

      let matchesFilter = true;

      if (filter === "full-time") {
        matchesFilter =
          employmentType.includes("full");
      }

      if (filter === "remote") {
        matchesFilter =
          location.includes("remote");
      }

      if (filter === "hybrid") {
        matchesFilter =
          location.includes("hybrid");
      }

      return (
        matchesSearch &&
        matchesFilter
      );
    });
  }, [jobs, searchQuery, filter]);

  // =========================================================
  // Loading State
  // =========================================================

  if (isLoading) {
    return (
      <div className="flex min-h-[500px] items-center justify-center">
        <div className="text-sm font-medium text-slate-500">
          Finding the best jobs for you...
        </div>
      </div>
    );
  }

  // =========================================================
  // Error State
  // =========================================================

  if (error) {
    return (
      <div className="flex min-h-[500px] items-center justify-center">
        <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-sm font-medium text-red-600">
          {error}
        </div>
      </div>
    );
  }

  // =========================================================
  // Main Page
  // =========================================================

  return (
    <div className="flex h-full min-h-0 flex-col gap-5">

      {/* =====================================================
          Search + Filters
          ===================================================== */}

      <div className="flex flex-col gap-3 xl:flex-row xl:items-center xl:justify-between">

        <div className="relative flex-1">
          <Search
            size={18}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            type="text"
            value={searchQuery}
            onChange={(event) =>
              setSearchQuery(event.target.value)
            }
            placeholder="Search openings by role, technology, or company name..."
            className="h-12 w-full rounded-xl border border-slate-200 bg-white pl-11 pr-4 text-sm text-slate-700 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-100"
          />
        </div>

        <div className="flex items-center gap-2">
          {[
            {
              label: "All",
              value: "all" as const,
            },
            {
              label: "Full-time",
              value: "full-time" as const,
            },
            {
              label: "Remote",
              value: "remote" as const,
            },
            {
              label: "Hybrid",
              value: "hybrid" as const,
            },
          ].map((item) => (
            <button
              key={item.value}
              type="button"
              onClick={() =>
                setFilter(item.value)
              }
              className={`rounded-full px-4 py-2 text-xs font-semibold transition ${
                filter === item.value
                  ? "bg-slate-950 text-white"
                  : "border border-slate-200 bg-white text-slate-600 hover:border-violet-300 hover:text-violet-600"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* =====================================================
          Content
          ===================================================== */}

      <div className="grid min-h-0 flex-1 grid-cols-1 gap-5 xl:grid-cols-[minmax(380px,0.85fr)_minmax(600px,1.15fr)]">

        {/* ===================================================
            Job List
            =================================================== */}

        <div className="min-h-0 overflow-y-auto pr-1">
          <div className="flex flex-col gap-3">

            {filteredJobs.length === 0 ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center">
                <BriefcaseBusiness
                  size={30}
                  className="mx-auto mb-3 text-slate-300"
                />

                <p className="text-sm font-semibold text-slate-700">
                  No matching jobs found
                </p>

                <p className="mt-1 text-xs text-slate-400">
                  Try changing your search or filters.
                </p>
              </div>
            ) : (
              filteredJobs.map((job) => {
                const isSelected =
                  selectedJob === job;

                return (
                  <button
                    key={`${job.title}-${job.company}-${job.location}`}
                    type="button"
                    onClick={() =>
                      setSelectedJob(job)
                    }
                    className={`w-full rounded-2xl border bg-white p-4 text-left transition ${
                      isSelected
                        ? "border-violet-400 bg-violet-50/40 shadow-sm"
                        : "border-slate-200 hover:border-violet-200 hover:shadow-sm"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">

                      <div className="flex min-w-0 gap-3">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-xs font-bold text-slate-600">
                          {getCompanyInitials(
                            job.company
                          )}
                        </div>

                        <div className="min-w-0">
                          <h3 className="truncate text-sm font-bold text-slate-900">
                            {job.title}
                          </h3>

                          <p className="mt-1 truncate text-xs text-slate-500">
                            {job.company}
                            {" · "}
                            {job.location}
                          </p>
                        </div>

                      </div>

                      {job.match_score !==
                        null &&
                        job.match_score !==
                          undefined && (
                          <span className="shrink-0 rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-bold text-emerald-600">
                            {formatMatchScore(
                              job.match_score
                            )}
                          </span>
                        )}
                    </div>

                    <div className="mt-4 flex items-center justify-between text-xs">

                      <span className="font-medium text-slate-500">
                        {job.salary ||
                          "Salary not specified"}
                      </span>

                      <span className="font-semibold text-violet-600">
                        {job.employment_type ||
                          "Not specified"}
                      </span>

                    </div>
                  </button>
                );
              })
            )}

          </div>
        </div>

        {/* ===================================================
            Job Details
            =================================================== */}

        <div className="min-h-0 overflow-y-auto">

          {selectedJob ? (
            <JobDetails
          job={selectedJob}
        onPracticeInterview={(job) => {
        navigate("/interview", {
      state: {
        job,
      },
    });
  }}
/>
          ) : (
            <div className="flex h-full min-h-[500px] items-center justify-center rounded-2xl border border-slate-200 bg-white">
              <p className="text-sm text-slate-400">
                Select a job to view details.
              </p>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};


// =========================================================
// Job Details
// =========================================================

interface JobDetailsProps {
  job: Job;
  onPracticeInterview: (job: Job) => void;
}

const JobDetails = ({
  job,
  onPracticeInterview,
}: JobDetailsProps) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">

      {/* Header */}

      <div className="flex flex-col gap-5 border-b border-slate-100 pb-6 lg:flex-row lg:items-start lg:justify-between">

        <div className="flex min-w-0 gap-4">

          <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-violet-50 text-sm font-bold text-violet-600">
            {getCompanyInitials(
              job.company
            )}
          </div>

          <div className="min-w-0">

            <div className="flex flex-wrap items-center gap-2">

              {job.match_score !==
                null &&
                job.match_score !==
                  undefined && (
                  <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-bold text-emerald-600">
                    {formatMatchScore(
                      job.match_score
                    )}{" "}
                    Resume Match
                  </span>
                )}

            </div>

            <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-950">
              {job.title}
            </h1>

            <div className="mt-2 flex flex-wrap items-center gap-3 text-sm text-slate-500">

              <span className="flex items-center gap-1.5">
                <Building2 size={15} />
                {job.company}
              </span>

              <span className="flex items-center gap-1.5">
                <MapPin size={15} />
                {job.location}
              </span>

            </div>
          </div>
        </div>

       <div className="flex flex-wrap items-center gap-2">

  <button

    type="button"

    className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 text-slate-500 transition hover:border-violet-200 hover:text-violet-600"

    title="Save job"

  >

    <Bookmark size={17} />

  </button>

  <button

    type="button"

    onClick={() => onPracticeInterview(job)}

    className="flex items-center gap-2 rounded-xl border border-indigo-200 bg-indigo-50 px-4 py-2.5 text-sm font-semibold text-indigo-600 transition hover:bg-indigo-100"

  >

    <Mic size={15} />

    Practice Interview

  </button>

  {job.apply_url && (

    <a

      href={job.apply_url}

      target="_blank"

      rel="noopener noreferrer"

      className="flex items-center gap-2 rounded-xl bg-violet-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-violet-700"

    >

      <Send size={15} />

      Apply Now

    </a>

  )}

</div>
      </div>

      {/* Job Metadata */}

      <div className="my-6 grid grid-cols-1 gap-3 rounded-2xl bg-slate-50 p-4 sm:grid-cols-3">

        <InfoItem
          label="Compensation"
          value={
            job.salary ||
            "Not specified"
          }
        />

        <InfoItem
          label="Experience"
          value={
            job.experience ||
            "Not specified"
          }
        />

        <InfoItem
          label="Employment Type"
          value={
            job.employment_type ||
            "Not specified"
          }
        />

      </div>

      {/* Skills */}

      {job.skills.length > 0 && (
        <section className="mb-7 rounded-2xl border border-violet-100 bg-violet-50/50 p-5">

          <h2 className="text-sm font-bold uppercase tracking-wide text-slate-800">
            Skills
          </h2>

          <div className="mt-3 flex flex-wrap gap-2">
            {job.skills.map((skill) => (
              <span
                key={skill}
                className="rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700"
              >
                {skill}
              </span>
            ))}
          </div>

        </section>
      )}

      {/* Description */}

      <section>
        <h2 className="text-base font-bold text-slate-900">
          Role Description
        </h2>

        <div className="mt-3 whitespace-pre-line text-sm leading-7 text-slate-600">
          {job.description}
        </div>
      </section>

      {/* Source */}

      <div className="mt-7 border-t border-slate-100 pt-4 text-xs text-slate-400">
        Source: {job.source}
      </div>

    </div>
  );
};


// =========================================================
// Info Item
// =========================================================

interface InfoItemProps {
  label: string;
  value: string;
}

const InfoItem = ({
  label,
  value,
}: InfoItemProps) => {
  return (
    <div>
      <p className="text-[11px] font-medium text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-bold text-slate-900">
        {value}
      </p>
    </div>
  );
};


// =========================================================
// Helpers
// =========================================================

const getCompanyInitials = (
  company: string
): string => {
  if (!company.trim()) {
    return "CO";
  }

  const words = company
    .trim()
    .split(/\s+/);

  if (words.length === 1) {
    return words[0]
      .slice(0, 2)
      .toUpperCase();
  }

  return words
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase();
};


const formatMatchScore = (
  score: number
): string => {
  /*
   * CrossEncoder/Pinecone scores are not inherently
   * percentages. For now, display the raw relevance
   * score rather than falsely presenting it as a percentage.
   */
  return score.toFixed(2);
};


export default RecommendedJobsPage;