import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Bot,
  CheckCircle2,
  Loader2,
  Search,
  Sparkles,
  Wrench,
  XCircle,
} from "lucide-react";

import {
  researchJobs,
  type JobResearchData,
} from "../../api/job";

const DEFAULT_QUERY =
  "Find relevant AI/ML and backend jobs in India that match my resume.";

const JobResearchPage = () => {
  const [query, setQuery] =
    useState<string>(DEFAULT_QUERY);

  const [result, setResult] =
    useState<JobResearchData | null>(null);

  const [isLoading, setIsLoading] =
    useState<boolean>(false);

  const [error, setError] =
    useState<string | null>(null);

  // ============================================================
  // RUN JOB RESEARCH
  // ============================================================

  const handleResearch = async () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      setError("Please enter a research request.");
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setResult(null);

      const researchResult =
        await researchJobs(trimmedQuery);

      setResult(researchResult);
    } catch (err) {
      console.error(
        "Job research failed:",
        err
      );

      setError(
        "Unable to complete job research. Please try again."
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-6">

      {/* ========================================================
          PAGE HEADER
          ======================================================== */}

      <div>
        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-100 text-violet-600 dark:bg-violet-500/10 dark:text-violet-400">
            <Bot size={22} />
          </div>

          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              AI Job Research
            </h1>

            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              Ask Placeko to research jobs using your resume,
              job-market data, and grounded candidate evidence.
            </p>
          </div>

        </div>
      </div>

      {/* ========================================================
          RESEARCH INPUT
          ======================================================== */}

      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">

        <div className="mb-4 flex items-center gap-2">

          <Sparkles
            size={17}
            className="text-violet-500"
          />

          <h2 className="text-sm font-bold text-slate-900 dark:text-white">
            What do you want to research?
          </h2>

        </div>

        <div className="flex flex-col gap-3">

          <textarea
            value={query}
            onChange={(event) =>
              setQuery(event.target.value)
            }
            rows={4}
            maxLength={500}
            disabled={isLoading}
            placeholder="Example: Find backend AI jobs in India that match my Python, FastAPI, LangGraph and RAG experience."
            className="
              w-full
              resize-none
              rounded-xl
              border
              border-slate-200
              bg-slate-50
              px-4
              py-3
              text-sm
              text-slate-800
              outline-none
              transition
              placeholder:text-slate-400
              focus:border-violet-400
              focus:ring-2
              focus:ring-violet-100
              disabled:cursor-not-allowed
              disabled:opacity-60
              dark:border-slate-700
              dark:bg-slate-950
              dark:text-slate-100
              dark:focus:ring-violet-500/10
            "
          />

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

            <span className="text-xs text-slate-400">
              {query.length}/500 characters
            </span>

            <button
              type="button"
              onClick={handleResearch}
              disabled={
                isLoading ||
                !query.trim()
              }
              className="
                inline-flex
                items-center
                justify-center
                gap-2
                rounded-xl
                bg-violet-600
                px-5
                py-2.5
                text-sm
                font-semibold
                text-white
                shadow-sm
                transition
                hover:bg-violet-700
                disabled:cursor-not-allowed
                disabled:opacity-50
              "
            >

              {isLoading ? (
                <>
                  <Loader2
                    size={17}
                    className="animate-spin"
                  />

                  Researching...
                </>
              ) : (
                <>
                  <Search size={17} />

                  Research Jobs
                </>
              )}

            </button>

          </div>

        </div>

      </section>

      {/* ========================================================
          ERROR
          ======================================================== */}

      {error && (
        <div className="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4 dark:border-red-900/50 dark:bg-red-950/20">

          <XCircle
            size={18}
            className="mt-0.5 shrink-0 text-red-500"
          />

          <div>

            <p className="text-sm font-semibold text-red-700 dark:text-red-400">
              Research failed
            </p>

            <p className="mt-1 text-xs text-red-600 dark:text-red-400/80">
              {error}
            </p>

          </div>

        </div>
      )}

      {/* ========================================================
          LOADING
          ======================================================== */}

      {isLoading && (
        <section className="rounded-2xl border border-violet-200 bg-violet-50/50 p-6 dark:border-violet-900/40 dark:bg-violet-950/10">

          <div className="flex items-center gap-4">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-100 dark:bg-violet-500/10">

              <Loader2
                size={20}
                className="animate-spin text-violet-600"
              />

            </div>

            <div>

              <p className="text-sm font-bold text-slate-900 dark:text-white">
                Placeko is researching...
              </p>

              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                The agent is searching jobs and checking them
                against your grounded resume evidence.
              </p>

            </div>

          </div>

        </section>
      )}

      {/* ========================================================
          RESULT
          ======================================================== */}

      {result && !isLoading && (
        <>
          {/* ====================================================
              RESEARCH STATS
              ==================================================== */}

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">

            <ResearchStat
              label="Research rounds"
              value={result.research_rounds}
            />

            <ResearchStat
              label="Tools used"
              value={result.tools_used.length}
            />

            <ResearchStat
              label="Resume"
              value={
                result.resume_id
                  ? "Active resume"
                  : "Not found"
              }
            />

          </div>

          {/* ====================================================
              REPORT
              ==================================================== */}

          <section className="rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">

            <div className="flex items-center gap-2 border-b border-slate-200 px-5 py-4 dark:border-slate-800">

              <CheckCircle2
                size={18}
                className="text-emerald-500"
              />

              <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                Job Research Report
              </h2>

            </div>

            {/* ==================================================
                MARKDOWN REPORT
                ================================================== */}

            <div className="px-5 py-6">

              <div className="
                max-w-none
                text-sm
                leading-7
                text-slate-700
                dark:text-slate-300
              ">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{

                    h1: ({ children }) => (
                      <h1 className="
                        mb-4
                        mt-1
                        text-2xl
                        font-bold
                        text-slate-900
                        dark:text-white
                      ">
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2 className="
                        mb-3
                        mt-7
                        text-xl
                        font-bold
                        text-slate-900
                        dark:text-white
                      ">
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3 className="
                        mb-2
                        mt-5
                        text-lg
                        font-semibold
                        text-slate-900
                        dark:text-white
                      ">
                        {children}
                      </h3>
                    ),

                    p: ({ children }) => (
                      <p className="mb-4">
                        {children}
                      </p>
                    ),

                    ul: ({ children }) => (
                      <ul className="
                        mb-4
                        list-disc
                        space-y-1
                        pl-6
                      ">
                        {children}
                      </ul>
                    ),

                    ol: ({ children }) => (
                      <ol className="
                        mb-4
                        list-decimal
                        space-y-1
                        pl-6
                      ">
                        {children}
                      </ol>
                    ),

                    li: ({ children }) => (
                      <li className="pl-1">
                        {children}
                      </li>
                    ),

                    strong: ({ children }) => (
                      <strong className="
                        font-semibold
                        text-slate-900
                        dark:text-white
                      ">
                        {children}
                      </strong>
                    ),

                    em: ({ children }) => (
                      <em className="italic">
                        {children}
                      </em>
                    ),

                    blockquote: ({ children }) => (
                      <blockquote className="
                        my-4
                        border-l-4
                        border-violet-300
                        pl-4
                        italic
                        text-slate-500
                        dark:border-violet-700
                        dark:text-slate-400
                      ">
                        {children}
                      </blockquote>
                    ),

                    table: ({ children }) => (
                      <div className="
                        my-5
                        overflow-x-auto
                        rounded-xl
                        border
                        border-slate-200
                        dark:border-slate-700
                      ">
                        <table className="
                          w-full
                          border-collapse
                          text-sm
                        ">
                          {children}
                        </table>
                      </div>
                    ),

                    thead: ({ children }) => (
                      <thead className="
                        bg-slate-100
                        dark:bg-slate-800
                      ">
                        {children}
                      </thead>
                    ),

                    tbody: ({ children }) => (
                      <tbody>
                        {children}
                      </tbody>
                    ),

                    tr: ({ children }) => (
                      <tr className="
                        border-b
                        border-slate-100
                        last:border-b-0
                        dark:border-slate-800
                      ">
                        {children}
                      </tr>
                    ),

                    th: ({ children }) => (
                      <th className="
                        border-b
                        border-slate-200
                        px-4
                        py-3
                        text-left
                        font-semibold
                        text-slate-900
                        dark:border-slate-700
                        dark:text-white
                      ">
                        {children}
                      </th>
                    ),

                    td: ({ children }) => (
                      <td className="
                        px-4
                        py-3
                        align-top
                        text-slate-700
                        dark:text-slate-300
                      ">
                        {children}
                      </td>
                    ),

                    hr: () => (
                      <hr className="
                        my-7
                        border-slate-200
                        dark:border-slate-700
                      " />
                    ),

                    code: ({ children }) => (
                      <code className="
                        rounded-md
                        bg-slate-100
                        px-1.5
                        py-0.5
                        text-xs
                        text-violet-700
                        dark:bg-slate-800
                        dark:text-violet-300
                      ">
                        {children}
                      </code>
                    ),

                    a: ({ href, children }) => (
                      <a
                        href={href}
                        target="_blank"
                        rel="noreferrer"
                        className="
                          font-medium
                          text-violet-600
                          underline
                          decoration-violet-300
                          underline-offset-2
                          hover:text-violet-700
                          dark:text-violet-400
                          dark:hover:text-violet-300
                        "
                      >
                        {children}
                      </a>
                    ),
                  }}
                >
                  {result.report.replace(
                    /<br\s*\/?>/gi,
                    "\n"
                  )}
                </ReactMarkdown>

              </div>

            </div>

          </section>

          {/* ====================================================
              MCP TOOLS
              ==================================================== */}

          <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">

            <div className="mb-4 flex items-center gap-2">

              <Wrench
                size={17}
                className="text-violet-500"
              />

              <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                MCP Tools Used
              </h2>

            </div>

            {result.tools_used.length === 0 ? (
              <p className="text-xs text-slate-400">
                No MCP tools were recorded.
              </p>
            ) : (
              <div className="flex flex-wrap gap-2">

                {result.tools_used.map(
                  (item, index) => (
                    <span
                      key={`${item.tool}-${index}`}
                      className="
                        rounded-lg
                        border
                        border-slate-200
                        bg-slate-50
                        px-3
                        py-2
                        text-xs
                        font-medium
                        text-slate-600
                        dark:border-slate-700
                        dark:bg-slate-950
                        dark:text-slate-300
                      "
                    >
                      {item.tool}
                    </span>
                  )
                )}

              </div>
            )}

          </section>
        </>
      )}

    </div>
  );
};

// ============================================================
// RESEARCH STAT
// ============================================================

interface ResearchStatProps {
  label: string;
  value: string | number;
}

const ResearchStat = ({
  label,
  value,
}: ResearchStatProps) => {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">

      <p className="text-xs font-medium text-slate-400">
        {label}
      </p>

      <p className="mt-2 text-xl font-bold text-slate-900 dark:text-white">
        {value}
      </p>

    </div>
  );
};

export default JobResearchPage;