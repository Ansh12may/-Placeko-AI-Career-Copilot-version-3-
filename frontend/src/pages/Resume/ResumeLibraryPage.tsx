import { useEffect, useState } from "react";
import {
  FileText,
  Upload,
  Eye,
  Loader2,
  AlertCircle,
  Calendar,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getResumes } from "../../api/resume";
import type { ResumeLibraryItem } from "../../types/resume";

const ResumeLibraryPage = () => {
  const navigate = useNavigate();

  const [resumes, setResumes] = useState<ResumeLibraryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadResumes = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await getResumes();

        setResumes(response.data);
      } catch (err) {
        console.error("Failed to load resumes:", err);
        setError("Unable to load your resumes.");
      } finally {
        setLoading(false);
      }
    };

    loadResumes();
  }, []);

  const formatDate = (date: string) => {
    return new Date(date).toLocaleDateString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const handleOpenResume = (resumeId: string) => {
    navigate(`/resume-analysis/${resumeId}`);
  };

  return (
    <div className="min-h-full bg-slate-50 p-6 dark:bg-slate-950">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Resume Library
          </h1>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Manage your resumes and view their ATS analysis.
          </p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/resume/upload")}
          className="
            flex
            items-center
            gap-2
            rounded-xl
            bg-indigo-600
            px-4
            py-2.5
            text-sm
            font-semibold
            text-white
            shadow-sm
            transition
            hover:bg-indigo-700
          "
        >
          <Upload className="h-4 w-4" />
          Upload Resume
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex min-h-[300px] items-center justify-center">
          <div className="flex items-center gap-3 text-slate-500">
            <Loader2 className="h-5 w-5 animate-spin" />
            Loading resumes...
          </div>
        </div>
      )}

      {/* Error */}
      {!loading && error && (
        <div className="flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
          <AlertCircle className="h-5 w-5 shrink-0" />
          {error}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && resumes.length === 0 && (
        <div className="flex min-h-[350px] flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white dark:border-slate-700 dark:bg-slate-900">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400">
            <FileText className="h-7 w-7" />
          </div>

          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
            No resumes yet
          </h2>

          <p className="mt-1 max-w-md text-center text-sm text-slate-500 dark:text-slate-400">
            Upload your resume to generate your candidate profile and ATS
            analysis.
          </p>

          <button
            type="button"
            onClick={() => navigate("/resume/upload")}
            className="mt-5 flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700"
          >
            <Upload className="h-4 w-4" />
            Upload Resume
          </button>
        </div>
      )}

      {/* Resume Cards */}
      {!loading && !error && resumes.length > 0 && (
        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {resumes.map((resume) => (
            <div
              key={resume.id}
              className="
                rounded-2xl
                border
                border-slate-200
                bg-white
                p-5
                shadow-sm
                transition
                hover:-translate-y-0.5
                hover:shadow-md
                dark:border-slate-800
                dark:bg-slate-900
              "
            >
              {/* File */}
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400">
                    <FileText className="h-5 w-5" />
                  </div>

                  <div className="min-w-0">
                    <h3 className="max-w-[190px] truncate font-semibold text-slate-900 dark:text-white">
                      {resume.file_name}
                    </h3>

                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      {resume.content_type}
                    </p>
                  </div>
                </div>

                {/* ATS Score */}
                <div className="rounded-xl bg-indigo-50 px-3 py-2 text-center dark:bg-indigo-950/40">
                  <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                    {resume.ats_score}
                  </p>

                  <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500">
                    ATS
                  </p>
                </div>
              </div>

              {/* Candidate */}
              <div className="mt-5">
                <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  {resume.candidate_name || "Candidate"}
                </p>

                <div className="mt-2 flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                  <Calendar className="h-3.5 w-3.5" />
                  Uploaded {formatDate(resume.created_at)}
                </div>
              </div>

              {/* Action */}
              <button
                type="button"
                onClick={() => handleOpenResume(resume.id)}
                className="
                  mt-5
                  flex
                  w-full
                  items-center
                  justify-center
                  gap-2
                  rounded-xl
                  border
                  border-slate-200
                  px-4
                  py-2.5
                  text-sm
                  font-semibold
                  text-slate-700
                  transition
                  hover:border-indigo-200
                  hover:bg-indigo-50
                  hover:text-indigo-600
                  dark:border-slate-700
                  dark:text-slate-300
                  dark:hover:border-indigo-800
                  dark:hover:bg-indigo-950/30
                  dark:hover:text-indigo-400
                "
              >
                <Eye className="h-4 w-4" />
                View Analysis
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ResumeLibraryPage;