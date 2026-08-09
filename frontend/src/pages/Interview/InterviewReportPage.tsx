import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  CircleAlert,
  Lightbulb,
  MessageSquare,
  Map,
  Target,
  Trophy,
} from "lucide-react";

import { getInterviewSession } from "../../api/interview";

import type {
  InterviewSession,
  InterviewReport,
} from "../../types/interview";


// =========================================================
// Component
// =========================================================

const InterviewReportPage = () => {
  const navigate = useNavigate();

  const { sessionId } = useParams<{
    sessionId: string;
  }>();

  const [session, setSession] =
    useState<InterviewSession | null>(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  // =========================================================
  // Load Session
  // =========================================================

  useEffect(() => {
    if (!sessionId) {
      setError("Interview session not found.");
      setIsLoading(false);
      return;
    }

    const loadSession = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const data =
          await getInterviewSession(sessionId);

        setSession(data);
      } catch (err) {
        console.error(
          "Failed to load interview report:",
          err
        );

        setError(
          "Unable to load the interview report."
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadSession();
  }, [sessionId]);


  // =========================================================
  // Loading
  // =========================================================

  if (isLoading) {
    return (
      <div className="flex min-h-[600px] items-center justify-center">
        <p className="text-sm font-medium text-slate-500">
          Preparing your interview report...
        </p>
      </div>
    );
  }


  // =========================================================
  // Error
  // =========================================================

  if (error || !session) {
    return (
      <div className="flex min-h-[600px] items-center justify-center">
        <div className="max-w-md rounded-2xl border border-red-200 bg-red-50 p-6 text-center">

          <p className="text-sm font-semibold text-red-600">
            {error || "Interview report not found."}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate("/interview")
            }
            className="mt-5 rounded-xl bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white"
          >
            Start New Interview
          </button>

        </div>
      </div>
    );
  }


  // =========================================================
  // Report
  // =========================================================

  const report = session.report;


  if (!report) {
    return (
      <div className="mx-auto max-w-2xl py-20 text-center">

        <CircleAlert
          size={40}
          className="mx-auto text-amber-500"
        />

        <h1 className="mt-5 text-xl font-bold text-slate-900">
          Report Not Available
        </h1>

        <p className="mt-2 text-sm text-slate-500">
          The interview has not generated a report yet.
        </p>

        <button
          type="button"
          onClick={() =>
            navigate(
              `/interview/${session.session_id}`
            )
          }
          className="mt-6 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white"
        >
          Back to Interview
        </button>

      </div>
    );
  }


  // =========================================================
  // Main UI
  // =========================================================

  return (
    <div className="mx-auto w-full max-w-6xl">

      {/* =====================================================
          Header
          ===================================================== */}

      <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

        <div>

          <button
            type="button"
            onClick={() =>
              navigate("/interview")
            }
            className="mb-4 flex items-center gap-2 text-xs font-semibold text-slate-500 transition hover:text-indigo-600"
          >
            <ArrowLeft size={14} />
            Interview Setup
          </button>

          <div className="flex items-center gap-3">

            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-amber-600">
              <Trophy size={23} />
            </div>

            <div>

              <p className="text-xs font-bold uppercase tracking-wider text-indigo-600">
                Interview Complete
              </p>

              <h1 className="mt-1 text-2xl font-bold tracking-tight text-slate-950 dark:text-white sm:text-3xl">
                Your Interview Report
              </h1>

            </div>

          </div>

        </div>

        <button
          type="button"
          onClick={() =>
            navigate("/interview")
          }
          className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-indigo-700"
        >
          New Interview
        </button>

      </div>


      {/* =====================================================
          Overall Performance
          ===================================================== */}

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-[0.8fr_1.2fr]">

        <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

          <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Overall Performance
          </p>

          <div className="mt-6 flex items-center gap-6">

            <ScoreCircle
              score={report.overall_score.score}
            />

            <div>

              <p className="text-lg font-bold text-slate-900 dark:text-white">
                {getPerformanceLabel(
                  report.overall_score.score
                )}
              </p>

              <p className="mt-2 max-w-xs text-xs leading-5 text-slate-500">
                Your overall score reflects your
                technical knowledge, communication,
                confidence and completeness.
              </p>

            </div>

          </div>

          <div className="mt-7 border-t border-slate-100 pt-5">

            <div className="flex justify-between text-xs">

              <span className="text-slate-500">
                Questions answered
              </span>

              <span className="font-bold text-slate-800">
                {session.history.filter(
                  (item) => item.answer !== null
                ).length}
              </span>

            </div>

          </div>

        </div>


        {/* Hiring Recommendation */}

        <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

          <div className="flex items-center gap-2">

            <Target
              size={18}
              className="text-indigo-600"
            />

            <h2 className="text-base font-bold text-slate-900 dark:text-white">
              Interview Assessment
            </h2>

          </div>

          <div className="mt-5 rounded-2xl bg-indigo-50 p-5">

            <p className="text-xs font-bold uppercase tracking-wider text-indigo-500">
              Hiring Recommendation
            </p>

            <p className="mt-2 text-2xl font-black text-indigo-700">
              {report.hiring_recommendation}
            </p>

          </div>

          <div className="mt-6">

            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
              Final Feedback
            </p>

            <p className="mt-2 text-sm leading-7 text-slate-600">
              {report.final_feedback}
            </p>

          </div>

        </div>

      </div>


      {/* =====================================================
          Score Breakdown
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

        <div className="flex items-center gap-2">

          <Target
            size={18}
            className="text-indigo-600"
          />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Score Breakdown
          </h2>

        </div>

        <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">

          <ScoreItem
            label="Technical"
            score={report.technical_score}
          />

          <ScoreItem
            label="Communication"
            score={report.communication_score}
          />

          <ScoreItem
            label="Completeness"
            score={report.completeness_score}
          />

          <ScoreItem
            label="Confidence"
            score={report.confidence_score}
          />

        </div>

      </div>


      {/* =====================================================
          Strengths / Weaknesses
          ===================================================== */}

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">

        <InsightCard
          title="Strengths"
          icon={
            <CheckCircle2
              size={19}
              className="text-emerald-600"
            />
          }
          items={report.strengths}
          emptyMessage="No strengths were recorded."
        />

        <InsightCard
          title="Areas to Improve"
          icon={
            <CircleAlert
              size={19}
              className="text-amber-600"
            />
          }
          items={report.weaknesses}
          emptyMessage="No major weaknesses were recorded."
        />

      </div>


      {/* =====================================================
          Knowledge Gaps
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

        <div className="flex items-center gap-2">

          <MessageSquare
            size={19}
            className="text-indigo-600"
          />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Knowledge Gaps
          </h2>

        </div>

        {report.knowledge_gaps.length > 0 ? (

          <div className="mt-5 flex flex-wrap gap-2">

            {report.knowledge_gaps.map(
              (topic) => (
                <span
                  key={topic}
                  className="rounded-full border border-amber-100 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-700"
                >
                  {topic}
                </span>
              )
            )}

          </div>

        ) : (

          <p className="mt-4 text-sm text-slate-500">
            No major knowledge gaps were identified.
          </p>

        )}

      </div>


      {/* =====================================================
          Recommendations
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-indigo-100 bg-indigo-50/60 p-7">

        <div className="flex items-center gap-2">

          <Lightbulb
            size={19}
            className="text-indigo-600"
          />

          <h2 className="text-base font-bold text-slate-900">
            AI Recommendations
          </h2>

        </div>

        <div className="mt-5 space-y-3">

          {report.recommendations.length > 0 ? (

            report.recommendations.map(
              (recommendation, index) => (
                <div
                  key={`${recommendation}-${index}`}
                  className="flex gap-3 rounded-xl bg-white p-4"
                >

                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-600">
                    {index + 1}
                  </span>

                  <p className="text-sm leading-6 text-slate-600">
                    {recommendation}
                  </p>

                </div>
              )
            )

          ) : (

            <p className="text-sm text-slate-500">
              No recommendations were generated.
            </p>

          )}

        </div>

      </div>


      {/* =====================================================
          Learning Roadmap
          ===================================================== */}

      <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

        <div className="flex items-center gap-2">

          <Map
            size={19}
            className="text-indigo-600"
          />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Learning Roadmap
          </h2>

        </div>

        <div className="mt-5 space-y-3">

          {report.learning_roadmap.length > 0 ? (

            report.learning_roadmap.map(
              (item, index) => (
                <div
                  key={`${item}-${index}`}
                  className="flex gap-3 rounded-xl border border-slate-100 p-4"
                >

                  <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-600">
                    {index + 1}
                  </span>

                  <p className="text-sm leading-6 text-slate-600">
                    {item}
                  </p>

                </div>
              )
            )

          ) : (

            <p className="text-sm text-slate-500">
              No learning roadmap was generated.
            </p>

          )}

        </div>

      </div>


      {/* =====================================================
          Question Review
          ===================================================== */}

      <div className="mt-8">

        <h2 className="text-lg font-bold text-slate-900 dark:text-white">
          Question Review
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Review how you performed on each question.
        </p>

        <div className="mt-5 space-y-4">

          {report.question_summaries.map(
            (summary, index) => (
              <QuestionReview
                key={`${summary.question}-${index}`}
                index={index}
                summary={summary}
              />
            )
          )}

        </div>

      </div>


      {/* =====================================================
          Bottom CTA
          ===================================================== */}

      <div className="my-10 flex flex-col items-center rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">

        <Trophy
          size={28}
          className="text-amber-500"
        />

        <h2 className="mt-4 text-lg font-bold text-slate-900 dark:text-white">
          Ready for another round?
        </h2>

        <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
          Practice again to improve your weak areas
          and become more confident before your real
          interview.
        </p>

        <button
          type="button"
          onClick={() =>
            navigate("/interview")
          }
          className="mt-5 rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-indigo-700"
        >
          Start Another Interview
        </button>

      </div>

    </div>
  );
};


// =========================================================
// Score Circle
// =========================================================

interface ScoreCircleProps {
  score: number;
}

const ScoreCircle = ({
  score,
}: ScoreCircleProps) => {
  return (
    <div className="flex h-32 w-32 shrink-0 items-center justify-center rounded-full border-[10px] border-indigo-100 bg-indigo-50">

      <div className="text-center">

        <p className="text-3xl font-black text-indigo-600">
          {score.toFixed(1)}
        </p>

        <p className="text-[10px] font-bold uppercase tracking-wide text-slate-400">
          / 10
        </p>

      </div>

    </div>
  );
};


// =========================================================
// Score Item
// =========================================================

interface ScoreItemProps {
  label: string;
  score: InterviewScoreLike;
}

interface InterviewScoreLike {
  score: number;
  max_score: number;
}

const ScoreItem = ({
  label,
  score,
}: ScoreItemProps) => {
  const percentage =
    score.max_score > 0
      ? (score.score /
          score.max_score) *
        100
      : 0;

  return (
    <div>

      <div className="mb-2 flex items-center justify-between">

        <span className="text-xs font-semibold text-slate-600">
          {label}
        </span>

        <span className="text-xs font-bold text-slate-900">
          {score.score.toFixed(1)}
          /
          {score.max_score}
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-indigo-600"
          style={{
            width: `${Math.min(
              percentage,
              100
            )}%`,
          }}
        />

      </div>

    </div>
  );
};


// =========================================================
// Insight Card
// =========================================================

interface InsightCardProps {
  title: string;
  icon: React.ReactNode;
  items: string[];
  emptyMessage: string;
}

const InsightCard = ({
  title,
  icon,
  items,
  emptyMessage,
}: InsightCardProps) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm dark:border-slate-800 dark:bg-slate-900">

      <div className="flex items-center gap-2">

        {icon}

        <h2 className="text-base font-bold text-slate-900 dark:text-white">
          {title}
        </h2>

      </div>

      <div className="mt-5 space-y-3">

        {items.length > 0 ? (

          items.map(
            (item, index) => (
              <div
                key={`${item}-${index}`}
                className="flex gap-3"
              >

                <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-500" />

                <p className="text-sm leading-6 text-slate-600">
                  {item}
                </p>

              </div>
            )
          )

        ) : (

          <p className="text-sm text-slate-500">
            {emptyMessage}
          </p>

        )}

      </div>

    </div>
  );
};


// =========================================================
// Question Review
// =========================================================

interface QuestionReviewProps {
  index: number;
  summary: InterviewReport["question_summaries"][number];
}

const QuestionReview = ({
  index,
  summary,
}: QuestionReviewProps) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">

      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">

        <div className="flex gap-3">

          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-100 text-xs font-bold text-indigo-600">
            {index + 1}
          </div>

          <div>

            <h3 className="text-sm font-bold leading-6 text-slate-900 dark:text-white">
              {summary.question}
            </h3>

          </div>

        </div>

        <span className="shrink-0 rounded-full bg-indigo-50 px-3 py-1 text-xs font-bold text-indigo-600">
          {summary.score.toFixed(1)}
          /10
        </span>

      </div>


      <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">

        {/* Strengths */}

        <div className="rounded-xl bg-emerald-50 p-4">

          <p className="text-[10px] font-bold uppercase tracking-wide text-emerald-600">
            Strengths
          </p>

          {summary.strengths.length > 0 ? (

            <ul className="mt-2 space-y-2">

              {summary.strengths.map(
                (item, itemIndex) => (
                  <li
                    key={`${item}-${itemIndex}`}
                    className="text-sm leading-6 text-slate-600"
                  >
                    • {item}
                  </li>
                )
              )}

            </ul>

          ) : (

            <p className="mt-2 text-sm text-slate-500">
              No strengths recorded.
            </p>

          )}

        </div>


        {/* Weaknesses */}

        <div className="rounded-xl bg-amber-50 p-4">

          <p className="text-[10px] font-bold uppercase tracking-wide text-amber-600">
            Weaknesses
          </p>

          {summary.weaknesses.length > 0 ? (

            <ul className="mt-2 space-y-2">

              {summary.weaknesses.map(
                (item, itemIndex) => (
                  <li
                    key={`${item}-${itemIndex}`}
                    className="text-sm leading-6 text-slate-600"
                  >
                    • {item}
                  </li>
                )
              )}

            </ul>

          ) : (

            <p className="mt-2 text-sm text-slate-500">
              No weaknesses recorded.
            </p>

          )}

        </div>

      </div>

    </div>
  );
};


// =========================================================
// Helpers
// =========================================================

const getPerformanceLabel = (
  score: number
): string => {
  if (score >= 8.5) {
    return "Excellent performance";
  }

  if (score >= 7) {
    return "Strong performance";
  }

  if (score >= 5) {
    return "Good foundation";
  }

  return "Needs improvement";
};


export default InterviewReportPage;