import { useEffect, useState } from "react";
import {
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Loader2,
  FileText,
  GraduationCap,
  Briefcase,
  Code2,
  Award,
  UserRound,
} from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";

import { getResumeById } from "../../api/resume";
import type {
  ResumeDetail,
  SectionScore,
} from "../../types/resume";

const ResumeAnalysisPage = () => {
  const navigate = useNavigate();
  const { resumeId } = useParams<{ resumeId: string }>();

  const [resume, setResume] = useState<ResumeDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!resumeId) {
      setError("Resume ID is missing.");
      setLoading(false);
      return;
    }

    const loadResume = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await getResumeById(resumeId);

        setResume(response.data);
      } catch (err) {
        console.error("Failed to load resume:", err);
        setError("Unable to load resume analysis.");
      } finally {
        setLoading(false);
      }
    };

    loadResume();
  }, [resumeId]);

  if (loading) {
    return (
      <div className="flex min-h-full items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="flex items-center gap-3 text-slate-500">
          <Loader2 className="h-5 w-5 animate-spin" />
          Loading resume analysis...
        </div>
      </div>
    );
  }

  if (error || !resume) {
    return (
      <div className="min-h-full bg-slate-50 p-6 dark:bg-slate-950">
        <button
          type="button"
          onClick={() => navigate("/resume")}
          className="mb-6 flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-indigo-600 dark:text-slate-300"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Resume Library
        </button>

        <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-600">
          {error || "Resume not found."}
        </div>
      </div>
    );
  }

  const { candidate_profile, ats_report } = resume;

  const scoreColor =
    ats_report.overall_score >= 80
      ? "text-emerald-600 dark:text-emerald-400"
      : ats_report.overall_score >= 60
        ? "text-amber-600 dark:text-amber-400"
        : "text-red-600 dark:text-red-400";

  return (
    <div className="min-h-full bg-slate-50 p-6 dark:bg-slate-950">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <button
            type="button"
            onClick={() => navigate("/resume")}
            className="mb-3 flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-indigo-600 dark:text-slate-400"
          >
            <ArrowLeft className="h-4 w-4" />
            Resume Library
          </button>

          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400">
              <FileText className="h-5 w-5" />
            </div>

            <div>
              <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
                Resume Analysis
              </h1>

              <p className="text-sm text-slate-500 dark:text-slate-400">
                {resume.file_name}
              </p>
            </div>
          </div>
        </div>

        <div className="rounded-xl bg-indigo-50 px-4 py-3 text-right dark:bg-indigo-950/40">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
            Candidate Level
          </p>

          <p className="mt-1 font-semibold capitalize text-indigo-600 dark:text-indigo-400">
            {ats_report.candidate_level
  ? ats_report.candidate_level.replace("_", " ")
  : "Not available"}
          </p>
        </div>
      </div>

      {/* Score Overview */}
      <div className="mb-6 grid gap-5 lg:grid-cols-3">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            Overall ATS Score
          </p>

          <div className="mt-3 flex items-end gap-2">
            <span className={`text-5xl font-bold ${scoreColor}`}>
              {ats_report.overall_score.toFixed(2)}
            </span>

            <span className="mb-2 text-sm text-slate-400">
              / 100
            </span>
          </div>
        </div>

        <ScoreCard
          title="Projects"
          score={ats_report.projects}
          icon={<Code2 className="h-5 w-5" />}
        />

        <ScoreCard
          title="Skills"
          score={ats_report.skills}
          icon={<Award className="h-5 w-5" />}
        />
      </div>

      {/* Candidate Profile */}
      <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <SectionHeader
          icon={<UserRound className="h-5 w-5" />}
          title="Candidate Profile"
        />

        <div className="mt-5 grid gap-5 md:grid-cols-2">
          <InfoItem
            label="Name"
            value={candidate_profile.name || "Not provided"}
          />

          <InfoItem
            label="Email"
            value={candidate_profile.email || "Not provided"}
          />

          <InfoItem
            label="Phone"
            value={candidate_profile.phone || "Not provided"}
          />

          <InfoItem
            label="LinkedIn"
            value={candidate_profile.linkedin || "Not provided"}
          />

          <InfoItem
            label="GitHub"
            value={candidate_profile.github || "Not provided"}
          />
        </div>

        {candidate_profile.summary && (
          <div className="mt-5">
            <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">
              Summary
            </p>

            <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
              {candidate_profile.summary}
            </p>
          </div>
        )}
      </section>

      {/* Score Breakdown */}
      <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <SectionHeader
          icon={<FileText className="h-5 w-5" />}
          title="ATS Score Breakdown"
        />

        <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <ScoreRow
            label="Contact Information"
            score={ats_report.contact_information}
          />

          <ScoreRow
            label="Education"
            score={ats_report.education}
          />

          <ScoreRow
            label="Projects"
            score={ats_report.projects}
          />

          <ScoreRow
            label="Skills"
            score={ats_report.skills}
          />

          <ScoreRow
            label="Certifications"
            score={ats_report.certifications}
          />

          <ScoreRow
            label="Formatting"
            score={ats_report.formatting}
          />

          <ScoreRow
            label="Summary"
            score={ats_report.summary}
          />

          <ScoreRow
            label="Experience"
            score={ats_report.experience}
          />
        </div>
      </section>

      {/* Strengths + Weaknesses */}
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <FeedbackCard
          title="Strengths"
          icon={<CheckCircle2 className="h-5 w-5" />}
          items={ats_report.strengths}
          type="success"
        />

        <FeedbackCard
          title="Areas to Improve"
          icon={<AlertTriangle className="h-5 w-5" />}
          items={ats_report.weaknesses}
          type="warning"
        />
      </div>

      {/* Missing Keywords */}
      {ats_report.missing_keywords.length > 0 && (
        <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <SectionHeader
            icon={<Code2 className="h-5 w-5" />}
            title="Suggested Keywords"
          />

          <div className="mt-4 flex flex-wrap gap-2">
            {ats_report.missing_keywords.map((keyword) => (
              <span
                key={keyword}
                className="rounded-full bg-slate-100 px-3 py-1.5 text-sm font-medium text-slate-700 dark:bg-slate-800 dark:text-slate-300"
              >
                {keyword}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Detailed Feedback */}
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <FeedbackList
          title="Education Feedback"
          icon={<GraduationCap className="h-5 w-5" />}
          items={ats_report.education_feedback}
        />

        <FeedbackList
          title="Project Feedback"
          icon={<Code2 className="h-5 w-5" />}
          items={ats_report.project_feedback}
        />

        <FeedbackList
          title="Experience Feedback"
          icon={<Briefcase className="h-5 w-5" />}
          items={ats_report.experience_feedback}
        />

        <FeedbackList
          title="Skills Feedback"
          icon={<Award className="h-5 w-5" />}
          items={ats_report.skills_feedback}
        />
      </div>

      {/* Recommendations */}
      <section className="rounded-2xl border border-indigo-100 bg-indigo-50/60 p-6 dark:border-indigo-900/40 dark:bg-indigo-950/20">
        <SectionHeader
          icon={<Lightbulb className="h-5 w-5" />}
          title="Top Recommendations"
        />

        <div className="mt-5 space-y-3">
          {ats_report.recommendations.map((recommendation, index) => (
            <div
              key={`${recommendation}-${index}`}
              className="flex gap-3 rounded-xl bg-white p-4 dark:bg-slate-900"
            >
              <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-600 dark:bg-indigo-900/50 dark:text-indigo-400">
                {index + 1}
              </div>

              <p className="text-sm leading-6 text-slate-600 dark:text-slate-300">
                {recommendation}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

interface ScoreCardProps {
  title: string;
  score: SectionScore;
  icon: React.ReactNode;
}

const ScoreCard = ({
  title,
  score,
  icon,
}: ScoreCardProps) => {
  const percentage =
    score.max_score === 0
      ? 100
      : (score.score / score.max_score) * 100;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center gap-3 text-indigo-600 dark:text-indigo-400">
        {icon}

        <p className="font-medium text-slate-700 dark:text-slate-300">
          {title}
        </p>
      </div>

      <div className="mt-4 flex items-end gap-2">
        <span className="text-3xl font-bold text-slate-900 dark:text-white">
          {score.score}
        </span>

        <span className="mb-1 text-sm text-slate-400">
          / {score.max_score}
        </span>
      </div>

      <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
        <div
          className="h-full rounded-full bg-indigo-600"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

interface ScoreRowProps {
  label: string;
  score: SectionScore;
}

const ScoreRow = ({
  label,
  score,
}: ScoreRowProps) => {
  const isNotApplicable = score.max_score === 0;

  const percentage = isNotApplicable
    ? 100
    : (score.score / score.max_score) * 100;

  return (
    <div className="rounded-xl border border-slate-100 p-4 dark:border-slate-800">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
          {label}
        </p>

        {isNotApplicable ? (
          <span className="text-xs font-semibold text-slate-400">
            N/A
          </span>
        ) : (
          <span className="text-sm font-bold text-slate-900 dark:text-white">
            {score.score}/{score.max_score}
          </span>
        )}
      </div>

      {!isNotApplicable && (
        <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
          <div
            className="h-full rounded-full bg-indigo-600"
            style={{ width: `${percentage}%` }}
          />
        </div>
      )}
    </div>
  );
};

interface SectionHeaderProps {
  icon: React.ReactNode;
  title: string;
}

const SectionHeader = ({
  icon,
  title,
}: SectionHeaderProps) => {
  return (
    <div className="flex items-center gap-3">
      <div className="text-indigo-600 dark:text-indigo-400">
        {icon}
      </div>

      <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
        {title}
      </h2>
    </div>
  );
};

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
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>

      <p className="mt-1 truncate text-sm font-medium text-slate-800 dark:text-slate-200">
        {value}
      </p>
    </div>
  );
};

interface FeedbackCardProps {
  title: string;
  icon: React.ReactNode;
  items: string[];
  type: "success" | "warning";
}

const FeedbackCard = ({
  title,
  icon,
  items,
  type,
}: FeedbackCardProps) => {
  const iconClass =
    type === "success"
      ? "text-emerald-600 dark:text-emerald-400"
      : "text-amber-600 dark:text-amber-400";

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className={`flex items-center gap-3 ${iconClass}`}>
        {icon}

        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          {title}
        </h2>
      </div>

      <ul className="mt-5 space-y-3">
        {items.map((item, index) => (
          <li
            key={`${item}-${index}`}
            className="flex gap-3 text-sm leading-6 text-slate-600 dark:text-slate-400"
          >
            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-current" />
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
};

interface FeedbackListProps {
  title: string;
  icon: React.ReactNode;
  items: string[];
}

const FeedbackList = ({
  title,
  icon,
  items,
}: FeedbackListProps) => {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <SectionHeader
        icon={icon}
        title={title}
      />

      <ul className="mt-5 space-y-3">
        {items.length === 0 ? (
          <li className="text-sm text-slate-400">
            No specific feedback available.
          </li>
        ) : (
          items.map((item, index) => (
            <li
              key={`${item}-${index}`}
              className="flex gap-3 text-sm leading-6 text-slate-600 dark:text-slate-400"
            >
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-500" />
              {item}
            </li>
          ))
        )}
      </ul>
    </section>
  );
};

export default ResumeAnalysisPage;