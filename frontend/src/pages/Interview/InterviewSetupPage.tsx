import { useEffect, useState } from "react";
import { useLocation,useNavigate } from "react-router-dom";
import type { Job } from "../../api/job";

import {
  BriefcaseBusiness,
  FileText,
  Mic,
  Play,
} from "lucide-react";

import { getResumes } from "../../api/resume";
import { startInterview } from "../../api/interview";

import type { ResumeLibraryItem } from "../../types/resume";
import type {
  Difficulty,
  InterviewType,
} from "../../types/interview";

const InterviewSetupPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const selectedJob =
    (location.state as {
      job?: Job;
    } | null)?.job ?? null;


  const [resumes, setResumes] = useState<ResumeLibraryItem[]>([]);
  const [selectedResumeId, setSelectedResumeId] =
    useState("");

  const [interviewType, setInterviewType] =
    useState<InterviewType>("technical");

  const [difficulty, setDifficulty] =
    useState<Difficulty>("medium");

  const [numQuestions, setNumQuestions] =
    useState(5);

  const [includeProjects, setIncludeProjects] =
    useState(true);

  const [includeExperience, setIncludeExperience] =
    useState(true);

  const [includeBehavioral, setIncludeBehavioral] =
    useState(true);

  const [isLoading, setIsLoading] =
    useState(true);

  const [isStarting, setIsStarting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  // =========================================================
  // Load Resumes
  // =========================================================

  useEffect(() => {
    const loadResumes = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const response = await getResumes();

        setResumes(response.data);

        const activeResume = response.data.find(
          (resume) => resume.is_active
        );

        if (activeResume) {
          setSelectedResumeId(activeResume.id);
        } else if (response.data.length > 0) {
          setSelectedResumeId(
            response.data[0].id
          );
        }
      } catch (err) {
        console.error(
          "Failed to load resumes:",
          err
        );

        setError(
          "Unable to load your resumes."
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadResumes();
  }, []);

  // =========================================================
  // Start Interview
  // =========================================================

  const handleStartInterview = async () => {
    if (!selectedResumeId) {
      setError(
        "Please select a resume before starting."
      );

      return;
    }

    try {
      setIsStarting(true);
      setError(null);

      const session = await startInterview({
        resume_id: selectedResumeId,
        job_id: null,
        job_description:selectedJob?.description ?? null,
        interview_type: interviewType,
        difficulty,
        num_questions: numQuestions,
        include_projects: includeProjects,
        include_experience: includeExperience,
        include_behavioral: includeBehavioral,
        include_voice_analysis: false,
      });

      navigate(
        `/interview/${session.session_id}`
      );
    } catch (err) {
      console.error(
        "Failed to start interview:",
        err
      );

      setError(
        "Unable to start the interview. Please try again."
      );
    } finally {
      setIsStarting(false);
    }
  };

  // =========================================================
  // Loading
  // =========================================================

  if (isLoading) {
    return (
      <div className="flex min-h-[500px] items-center justify-center">
        <p className="text-sm font-medium text-slate-500">
          Loading interview setup...
        </p>
      </div>
    );
  }

  // =========================================================
  // No Resumes
  // =========================================================

  if (!resumes.length) {
    return (
      <div className="flex min-h-[500px] items-center justify-center">
        <div className="max-w-md rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm">

          <FileText
            size={36}
            className="mx-auto mb-4 text-slate-300"
          />

          <h2 className="text-lg font-bold text-slate-900">
            Resume Required
          </h2>

          <p className="mt-2 text-sm leading-6 text-slate-500">
            Upload a resume before starting an
            AI-powered mock interview.
          </p>

          <button
            type="button"
            onClick={() =>
              navigate("/resume")
            }
            className="mt-6 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-indigo-700"
          >
            Upload Resume
          </button>

        </div>
      </div>
    );
  }

  // =========================================================
  // Main UI
  // =========================================================

  return (
    <div className="mx-auto w-full max-w-5xl">

      {/* Header */}

      <div className="mb-8">

        <div className="mb-3 flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
            <Mic size={20} />
          </div>

          <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
            AI Interview Coach
          </span>
        </div>

        <h1 className="text-3xl font-bold tracking-tight text-slate-950 dark:text-white">
          Prepare for your next interview
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">
  {selectedJob
    ? "Configure your interview and let AI generate questions based on your resume and the selected job."
    : "Configure your interview and let AI generate personalized questions based on your resume."}
</p>

      </div>

      {/* Error */}

      {error && (
  <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
    {error}
  </div>
)}

{selectedJob && (
  <div className="mb-6 rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5">
    <div className="flex items-start gap-4">

      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
        <BriefcaseBusiness size={20} />
      </div>

      <div className="min-w-0">
        <p className="text-[11px] font-bold uppercase tracking-wide text-indigo-600">
          Target Job
        </p>

        <h2 className="mt-1 text-base font-bold text-slate-900">
          {selectedJob.title}
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          {selectedJob.company}
          {" · "}
          {selectedJob.location}
        </p>

        {selectedJob.skills.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {selectedJob.skills.slice(0, 8).map((skill) => (
              <span
                key={skill}
                className="rounded-full bg-white px-2.5 py-1 text-[11px] font-semibold text-slate-600"
              >
                {skill}
              </span>
            ))}
          </div>
        )}
      </div>

    </div>
  </div>
)}

<div className="grid grid-cols-1 gap-6 lg:grid-cols-3">

        {/* Configuration */}

        <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">

          {/* Resume */}

          <section>

            <h2 className="text-sm font-bold text-slate-900 dark:text-white">
              Select Resume
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Questions will be personalized using this resume.
            </p>

            <div className="mt-4 grid gap-3">

              {resumes.map((resume) => (
                <button
                  key={resume.id}
                  type="button"
                  onClick={() =>
                    setSelectedResumeId(
                      resume.id
                    )
                  }
                  className={`flex items-center gap-3 rounded-xl border p-4 text-left transition ${
                    selectedResumeId === resume.id
                      ? "border-indigo-500 bg-indigo-50"
                      : "border-slate-200 hover:border-indigo-300"
                  }`}
                >

                  <FileText
                    size={20}
                    className={
                      selectedResumeId ===
                      resume.id
                        ? "text-indigo-600"
                        : "text-slate-400"
                    }
                  />

                  <div className="min-w-0">

                    <p className="truncate text-sm font-semibold text-slate-900">
                      {resume.file_name}
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      {resume.is_active
                        ? "Active resume"
                        : "Resume"}
                    </p>

                  </div>

                </button>
              ))}

            </div>

          </section>

          {/* Interview Type */}

          <section className="mt-8">

            <h2 className="text-sm font-bold text-slate-900">
              Interview Type
            </h2>

            <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-3">

              {[
                {
                  value: "technical" as const,
                  title: "Technical",
                  description:
                    "Technical knowledge and problem solving.",
                },
                {
                  value: "behavioral" as const,
                  title: "Behavioral",
                  description:
                    "Communication and behavioral questions.",
                },
                {
                  value: "mixed" as const,
                  title: "Mixed",
                  description:
                    "Technical, project and behavioral.",
                },
              ].map((item) => (
                <button
                  key={item.value}
                  type="button"
                  onClick={() =>
                    setInterviewType(
                      item.value
                    )
                  }
                  className={`rounded-xl border p-4 text-left transition ${
                    interviewType ===
                    item.value
                      ? "border-indigo-500 bg-indigo-50"
                      : "border-slate-200 hover:border-indigo-300"
                  }`}
                >

                  <p className="text-sm font-bold text-slate-900">
                    {item.title}
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {item.description}
                  </p>

                </button>
              ))}

            </div>

          </section>

          {/* Difficulty */}

          <section className="mt-8">

            <h2 className="text-sm font-bold text-slate-900">
              Difficulty
            </h2>

            <div className="mt-4 flex flex-wrap gap-3">

              {[
                "easy",
                "medium",
                "hard",
              ].map((level) => (
                <button
                  key={level}
                  type="button"
                  onClick={() =>
                    setDifficulty(
                      level as Difficulty
                    )
                  }
                  className={`rounded-full px-5 py-2 text-xs font-semibold capitalize transition ${
                    difficulty === level
                      ? "bg-slate-950 text-white"
                      : "border border-slate-200 bg-white text-slate-600 hover:border-indigo-300"
                  }`}
                >
                  {level}
                </button>
              ))}

            </div>

          </section>

          {/* Number of Questions */}

          <section className="mt-8">

            <h2 className="text-sm font-bold text-slate-900">
              Number of Questions
            </h2>

            <div className="mt-4 flex gap-3">

              {[5, 10, 15, 20].map(
                (count) => (
                  <button
                    key={count}
                    type="button"
                    onClick={() =>
                      setNumQuestions(
                        count
                      )
                    }
                    className={`flex h-10 w-12 items-center justify-center rounded-xl text-sm font-bold transition ${
                      numQuestions === count
                        ? "bg-indigo-600 text-white"
                        : "border border-slate-200 bg-white text-slate-600 hover:border-indigo-300"
                    }`}
                  >
                    {count}
                  </button>
                )
              )}

            </div>

          </section>

          {/* Personalization */}

          <section className="mt-8">

            <h2 className="text-sm font-bold text-slate-900">
              Personalization
            </h2>

            <div className="mt-4 space-y-3">

              <ToggleOption
                label="Include projects"
                description="Ask questions based on your resume projects."
                checked={includeProjects}
                onChange={setIncludeProjects}
              />

              <ToggleOption
                label="Include experience"
                description="Ask questions about your work experience."
                checked={includeExperience}
                onChange={setIncludeExperience}
              />

              <ToggleOption
                label="Include behavioral questions"
                description="Add behavioral questions to the interview."
                checked={includeBehavioral}
                onChange={setIncludeBehavioral}
              />

            </div>

          </section>

        </div>

        {/* Summary */}

        <div className="h-fit rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">

          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 text-indigo-600">
            <BriefcaseBusiness size={22} />
          </div>

          <h2 className="mt-5 text-lg font-bold text-slate-900 dark:text-white">
            Interview Summary
          </h2>

          <div className="mt-5 space-y-4">

            {selectedJob && (
            <SummaryRow
            label="Target Role"
            value={selectedJob.title}/>

            )}

            <SummaryRow
              label="Type"
              value={interviewType}
            />

            <SummaryRow
              label="Difficulty"
              value={difficulty}
            />

            <SummaryRow
              label="Questions"
              value={String(numQuestions)}
            />

            <SummaryRow
              label="Projects"
              value={
                includeProjects
                  ? "Included"
                  : "Excluded"
              }
            />

            <SummaryRow
              label="Experience"
              value={
                includeExperience
                  ? "Included"
                  : "Excluded"
              }
            />

          </div>

          <button
            type="button"
            disabled={isStarting}
            onClick={
              handleStartInterview
            }
            className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Play size={16} />

            {isStarting
              ? "Starting..."
              : "Start Interview"}
          </button>

          <p className="mt-3 text-center text-[11px] leading-5 text-slate-400">
  {selectedJob
    ? "Questions will be generated from your resume and the selected job."
    : "Your questions are generated dynamically from your selected resume."}
</p>

        </div>

      </div>

    </div>
  );
};


// =========================================================
// Toggle
// =========================================================

interface ToggleOptionProps {
  label: string;
  description: string;
  checked: boolean;
  onChange: (
    value: boolean
  ) => void;
}

const ToggleOption = ({
  label,
  description,
  checked,
  onChange,
}: ToggleOptionProps) => {
  return (
    <button
      type="button"
      onClick={() =>
        onChange(!checked)
      }
      className="flex w-full items-center justify-between rounded-xl border border-slate-200 p-4 text-left transition hover:border-indigo-300"
    >

      <div>

        <p className="text-sm font-semibold text-slate-800">
          {label}
        </p>

        <p className="mt-1 text-xs text-slate-500">
          {description}
        </p>

      </div>

      <div
        className={`relative h-6 w-11 rounded-full transition ${
          checked
            ? "bg-indigo-600"
            : "bg-slate-300"
        }`}
      >

        <div
          className={`absolute top-1 h-4 w-4 rounded-full bg-white transition ${
            checked
              ? "left-6"
              : "left-1"
          }`}
        />

      </div>

    </button>
  );
};


// =========================================================
// Summary Row
// =========================================================

interface SummaryRowProps {
  label: string;
  value: string;
}

const SummaryRow = ({
  label,
  value,
}: SummaryRowProps) => {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 pb-3">

      <span className="text-xs text-slate-500">
        {label}
      </span>

      <span className="text-xs font-bold capitalize text-slate-900">
        {value}
      </span>

    </div>
  );
};

export default InterviewSetupPage;