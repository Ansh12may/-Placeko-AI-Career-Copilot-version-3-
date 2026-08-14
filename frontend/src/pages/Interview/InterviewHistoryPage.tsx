import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";



import {
  Clock,
  ChevronRight,
  CheckCircle2,
  PlayCircle,
  Mic,
  FileText,
} from "lucide-react";
import { getInterviewHistory } from "../../api/interview";
import type { InterviewSession } from "../../types/interview";


const InterviewHistoryPage = () => {
  const navigate = useNavigate();

  const [interviews, setInterviews] = useState<InterviewSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        setLoading(true);
        setError("");

        const data = await getInterviewHistory();

        setInterviews(data);
      } catch (err) {
        console.error("Failed to load interview history:", err);

        setError(
          "Failed to load interview history. Please try again."
        );
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  const formatDate = (date: string | null) => {
    if (!date) return "Date unavailable";

    return new Date(date).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const getAnsweredCount = (session: InterviewSession) => {
    return session.history.filter(
      (item) => item.answer !== null
    ).length;
  };

  const getScore = (session: InterviewSession) => {
    if (!session.report) return null;

    return session.report.overall_score.score;
  };

  if (loading) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-4 border-slate-300 border-t-slate-800" />

          <p className="text-sm text-slate-500">
            Loading interview history...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-[70vh] items-center justify-center">
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-sm text-red-600">
            {error}
          </p>

          <button
            onClick={() => window.location.reload()}
            className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-6 py-8">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="mb-8">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-slate-900 text-white">
            <Mic size={22} />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Interview History
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Review your previous AI mock interviews and performance.
            </p>
          </div>
        </div>
      </div>

      {/* =====================================================
          EMPTY STATE
      ===================================================== */}

      {interviews.length === 0 ? (
        <div className="flex min-h-[400px] items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white dark:border-slate-700 dark:bg-slate-900">
          <div className="text-center">

            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800">
              <FileText
                size={26}
                className="text-slate-500"
              />
            </div>

            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
              No interviews yet
            </h2>

            <p className="mt-2 max-w-md text-sm text-slate-500">
              Start your first AI mock interview to see your
              interview history here.
            </p>

            <button
              onClick={() => navigate("/interview")}
              className="mt-5 rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-slate-700"
            >
              Start Interview
            </button>

          </div>
        </div>
      ) : (

        /* ===================================================
           INTERVIEW LIST
        =================================================== */

        <div className="space-y-4">

          {interviews.map((session) => {

            const answeredCount =
              getAnsweredCount(session);

            const totalQuestions =
              session.interview_plan.technical_questions +
              session.interview_plan.behavioral_questions +
              session.interview_plan.project_questions;

            const score = getScore(session);

            const isCompleted =
              session.status === "Completed";

            const isInProgress =
              session.status === "In Progress";

            return (
              <div
                key={session.session_id}
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md dark:border-slate-700 dark:bg-slate-900"
              >

                <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">

                  {/* LEFT */}
                  <div className="flex items-start gap-4">

                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-slate-100 dark:bg-slate-800">
                      {isCompleted ? (
                        <CheckCircle2
                          size={23}
                          className="text-green-600"
                        />
                      ) : (
                        <PlayCircle
                          size={23}
                          className="text-blue-600"
                        />
                      )}
                    </div>

                    <div>

                      <h2 className="font-semibold text-slate-900 dark:text-white">
                        {session.interview_plan.interview_mode} Interview
                      </h2>

                      <div className="mt-2 flex flex-wrap items-center gap-3 text-sm text-slate-500">

                        <span>
                          {session.interview_plan.difficulty}
                        </span>

                        <span>•</span>

                        <span>
                          {answeredCount}/{totalQuestions} questions
                        </span>

                        <span>•</span>

                        <span className="flex items-center gap-1">
                          <Clock size={14} />
                          {formatDate(session.started_at)}
                        </span>

                      </div>

                    </div>
                  </div>


                  {/* RIGHT */}
                  <div className="flex items-center gap-4">

                    {/* SCORE */}
                    {score !== null && (
                      <div className="text-right">

                        <p className="text-xs text-slate-500">
                          Score
                        </p>

                        <p className="text-xl font-bold text-slate-900 dark:text-white">
                          {score.toFixed(1)}
                          <span className="text-sm font-normal text-slate-400">
                            /10
                          </span>
                        </p>

                      </div>
                    )}

                    {/* STATUS */}
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-medium ${
                        isCompleted
                          ? "bg-green-100 text-green-700"
                          : isInProgress
                            ? "bg-blue-100 text-blue-700"
                            : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {session.status}
                    </span>

                    {/* ACTION */}
                    {isCompleted ? (
                      <button
                        onClick={() =>
                          navigate(
                            `/interview/${session.session_id}/report`
                          )
                        }
                        className="flex items-center gap-1 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
                      >
                        View Report
                        <ChevronRight size={16} />
                      </button>
                    ) : isInProgress ? (
                      <button
                        onClick={() =>
                          navigate(
                            `/interview/${session.session_id}`
                          )
                        }
                        className="flex items-center gap-1 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-700"
                      >
                        Resume
                        <ChevronRight size={16} />
                      </button>
                    ) : null}

                  </div>

                </div>

              </div>
            );
          })}

        </div>
      )}

    </div>
  );
};

export default InterviewHistoryPage;