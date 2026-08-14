import { useEffect, useState } from "react";
import {
  FileText,
  Eye,
  Loader2,
  AlertCircle,
  Calendar,
  Trash2,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import {
  getResumes,
  deleteResume,
} from "../../api/resume";

import type {
  ResumeLibraryItem,
} from "../../types/resume";


const ResumeLibraryPage = () => {
  const navigate = useNavigate();

  const [resumes, setResumes] =
    useState<ResumeLibraryItem[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [deletingId, setDeletingId] =
    useState<string | null>(null);

  // Load Resumes

  const loadResumes = async () => {
    try {
      setLoading(true);
      setError("");

      const response =
        await getResumes();

      setResumes(
        response.data
      );

    } catch (err) {

      console.error(
        "Failed to load resumes:",
        err
      );

      setError(
        "Unable to load your resumes."
      );

    } finally {

      setLoading(false);

    }
  };

  // Initial Load
  
  useEffect(() => {
    loadResumes();
  }, []);

  // Format Date


  const formatDate = (
    date: string
  ) => {

    return new Date(
      date
    ).toLocaleDateString(
      "en-IN",
      {
        day: "numeric",
        month: "short",
        year: "numeric",
      }
    );
  };



  // Open Resume
 

  const handleOpenResume = (
    resumeId: string
  ) => {

    if (deletingId) {
      return;
    }

    navigate(
      `/resume-analysis/${resumeId}`
    );
  };



  // Delete Resume


  const handleDeleteResume = async (
    resume: ResumeLibraryItem
  ) => {

    if (deletingId) {
      return;
    }

    const confirmed =
      window.confirm(
        `Are you sure you want to delete "${resume.file_name}"?\n\nThis will permanently remove the resume and its ATS analysis.`
      );

    if (!confirmed) {
      return;
    }


    try {

      setDeletingId(
        resume.id
      );

      setError("");


      await deleteResume(
        resume.id
      );


     
      // Remove from UI immediately
  

      setResumes(
        (currentResumes) =>
          currentResumes.filter(
            (item) =>
              item.id !== resume.id
          )
      );


    } catch (err) {

      console.error(
        "Failed to delete resume:",
        err
      );

      setError(
        "Unable to delete this resume. Please try again."
      );

    } finally {

      setDeletingId(
        null
      );

    }
  };


  
  // Loading
  

  if (loading) {

    return (
      <div className="flex min-h-full items-center justify-center bg-slate-50 p-6 dark:bg-slate-950">

        <div className="flex items-center gap-3 text-slate-500 dark:text-slate-400">

          <Loader2
            className="h-5 w-5 animate-spin"
          />

          Loading resumes...

        </div>

      </div>
    );
  }


  return (
    <div className="min-h-full bg-slate-50 p-6 dark:bg-slate-950">

      {/*
          Header
          */}

      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>

          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
            Resume Library
          </h1>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Manage your resumes and view their ATS analysis.
          </p>

        </div>


        

      </div>


      {/*
          Error
       */}

      {error && (

        <div className="mb-6 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600 dark:border-red-900 dark:bg-red-950/30">

          <AlertCircle
            className="h-5 w-5 shrink-0"
          />

          <span>
            {error}
          </span>

        </div>

      )}


      {/* =====================================================
          Empty State
          ===================================================== */}

      {resumes.length === 0 && (

        <div className="flex min-h-[350px] flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white dark:border-slate-700 dark:bg-slate-900">

          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400">

            <FileText
              className="h-7 w-7"
            />

          </div>


          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
            No resumes yet
          </h2>


          <p className="mt-1 max-w-md text-center text-sm text-slate-500 dark:text-slate-400">
            Upload your resume to generate your candidate profile and ATS analysis.
          </p>

        </div>

      )}

      {/* =====================================================
          Resume Cards
          ===================================================== */}

      {resumes.length > 0 && (

        <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">

          {resumes.map(
            (resume) => {

              const isDeleting =
                deletingId === resume.id;


              return (

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

                  {/* =================================================
                      File Header
                      ================================================= */}

                  <div className="flex items-start justify-between gap-3">

                    <div className="flex min-w-0 items-center gap-3">

                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600 dark:bg-indigo-950/40 dark:text-indigo-400">

                        <FileText
                          className="h-5 w-5"
                        />

                      </div>


                      <div className="min-w-0">

                        <h3 className="max-w-[190px] truncate font-semibold text-slate-900 dark:text-white">
                          {resume.file_name}
                        </h3>

                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          {resume.content_type || "Resume"}
                        </p>

                      </div>

                    </div>


                    {/* ATS */}

                    <div className="shrink-0 rounded-xl bg-indigo-50 px-3 py-2 text-center dark:bg-indigo-950/40">

                      <p className="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                        {resume.ats_score !== null
                          ? Math.round(
                              resume.ats_score
                            )
                          : "—"}
                      </p>

                      <p className="text-[10px] font-medium uppercase tracking-wide text-slate-500">
                        ATS
                      </p>

                    </div>

                  </div>


                  {/* =================================================
                      Active Badge
                      ================================================= */}

                  {resume.is_active && (

                    <div className="mt-4">

                      <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-semibold text-emerald-700 dark:bg-emerald-950/30 dark:text-emerald-400">
                        Active Resume
                      </span>

                    </div>

                  )}


                  {/* =================================================
                      Candidate
                      ================================================= */}

                  <div className="mt-5">

                    <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                      {resume.candidate_name || "Candidate"}
                    </p>


                    <div className="mt-2 flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">

                      <Calendar
                        className="h-3.5 w-3.5"
                      />

                      Uploaded{" "}
                      {formatDate(
                        resume.created_at
                      )}

                    </div>

                  </div>


                  {/* =================================================
                      Actions
                      ================================================= */}

                  <div className="mt-5 grid grid-cols-[1fr_auto] gap-2">

                    {/* View */}

                    <button
                      type="button"
                      disabled={!!deletingId}
                      onClick={() =>
                        handleOpenResume(
                          resume.id
                        )
                      }
                      className="
                        flex
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
                        disabled:cursor-not-allowed
                        disabled:opacity-50
                        dark:border-slate-700
                        dark:text-slate-300
                        dark:hover:border-indigo-800
                        dark:hover:bg-indigo-950/30
                        dark:hover:text-indigo-400
                      "
                    >

                      <Eye
                        className="h-4 w-4"
                      />

                      View Analysis

                    </button>


                    {/* Delete */}

                    <button
                      type="button"
                      disabled={!!deletingId}
                      onClick={() =>
                        handleDeleteResume(
                          resume
                        )
                      }
                      title="Delete resume"
                      className="
                        flex
                        h-11
                        w-11
                        items-center
                        justify-center
                        rounded-xl
                        border
                        border-red-200
                        text-red-500
                        transition
                        hover:bg-red-50
                        hover:text-red-600
                        disabled:cursor-not-allowed
                        disabled:opacity-50
                        dark:border-red-900
                        dark:text-red-400
                        dark:hover:bg-red-950/30
                      "
                    >

                      {isDeleting ? (

                        <Loader2
                          className="h-4 w-4 animate-spin"
                        />

                      ) : (

                        <Trash2
                          className="h-4 w-4"
                        />

                      )}

                    </button>

                  </div>

                </div>

              );
            }
          )}

        </div>

      )}

    </div>
  );
};

export default ResumeLibraryPage;