import { useEffect, useState } from "react";
import { X } from "lucide-react";

import {
  updateApplication,
} from "../../api/application";

import type {
  Application,
  ApplicationStatus,
} from "../../types/application";


// =========================================================
// Props
// =========================================================

interface EditApplicationModalProps {
  isOpen: boolean;

  application: Application | null;

  onClose: () => void;

  onUpdated: (
    application: Application
  ) => void;
}


// =========================================================
// Status Options
// =========================================================

const STATUS_OPTIONS: {
  value: ApplicationStatus;
  label: string;
}[] = [
  {
    value: "saved",
    label: "Saved",
  },
  {
    value: "applied",
    label: "Applied",
  },
  {
    value: "screening",
    label: "Screening",
  },
  {
    value: "interview",
    label: "Interview",
  },
  {
    value: "offer",
    label: "Offer",
  },
  {
    value: "accepted",
    label: "Accepted",
  },
  {
    value: "rejected",
    label: "Rejected",
  },
  {
    value: "withdrawn",
    label: "Withdrawn",
  },
];


// =========================================================
// Component
// =========================================================

const EditApplicationModal = ({
  isOpen,
  application,
  onClose,
  onUpdated,
}: EditApplicationModalProps) => {
  const [jobTitle, setJobTitle] =
    useState("");

  const [company, setCompany] =
    useState("");

  const [location, setLocation] =
    useState("");

  const [applyUrl, setApplyUrl] =
    useState("");

  const [notes, setNotes] =
    useState("");

  const [status, setStatus] =
    useState<ApplicationStatus>("saved");

  const [isSubmitting, setIsSubmitting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  // =========================================================
  // Populate Form
  // =========================================================

  useEffect(() => {
    if (!application || !isOpen) {
      return;
    }

    setJobTitle(
      application.job_title
    );

    setCompany(
      application.company
    );

    setLocation(
      application.location ?? ""
    );

    setApplyUrl(
      application.apply_url ?? ""
    );

    setNotes(
      application.notes ?? ""
    );

    setStatus(
      application.status
    );

    setError(null);

  }, [application, isOpen]);


  // =========================================================
  // Close
  // =========================================================

  const handleClose = () => {
    if (isSubmitting) {
      return;
    }

    setError(null);

    onClose();
  };


  // =========================================================
  // Submit
  // =========================================================

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!application) {
      return;
    }

    if (!jobTitle.trim()) {
      setError(
        "Job title is required."
      );

      return;
    }

    if (!company.trim()) {
      setError(
        "Company is required."
      );

      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      const updatedApplication =
        await updateApplication(
          application.id,
          {
            job_title:
              jobTitle.trim(),

            company:
              company.trim(),

            location:
              location.trim() ||
              null,

            apply_url:
              applyUrl.trim() ||
              null,

            notes:
              notes.trim() ||
              null,

            status,
          }
        );

      onUpdated(
        updatedApplication
      );

      onClose();

    } catch (err) {
      console.error(
        "Failed to update application:",
        err
      );

      setError(
        "Unable to update the application. Please try again."
      );

    } finally {
      setIsSubmitting(false);
    }
  };


  // =========================================================
  // Hidden
  // =========================================================

  if (!isOpen || !application) {
    return null;
  }


  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm">

      <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-2xl bg-white shadow-xl dark:bg-slate-900">

        {/* ===================================================
            Header
            =================================================== */}

        <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4 dark:border-slate-800">

          <div>

            <h2 className="text-lg font-bold text-slate-900 dark:text-white">
              Edit Application
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Update your application details.
            </p>

          </div>

          <button
            type="button"
            onClick={handleClose}
            disabled={isSubmitting}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-50 dark:hover:bg-slate-800 dark:hover:text-white"
          >
            <X size={18} />
          </button>

        </div>


        {/* ===================================================
            Form
            =================================================== */}

        <form
          onSubmit={handleSubmit}
          className="space-y-5 p-6"
        >

          {/* Error */}

          {error && (
            <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-600">
              {error}
            </div>
          )}


          {/* Job Title */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Job Title
            </label>

            <input
              type="text"
              value={jobTitle}
              onChange={(event) =>
                setJobTitle(
                  event.target.value
                )
              }
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              placeholder="e.g. Python AI Engineer"
            />

          </div>


          {/* Company */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Company
            </label>

            <input
              type="text"
              value={company}
              onChange={(event) =>
                setCompany(
                  event.target.value
                )
              }
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              placeholder="e.g. OpenAI"
            />

          </div>


          {/* Location */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Location
            </label>

            <input
              type="text"
              value={location}
              onChange={(event) =>
                setLocation(
                  event.target.value
                )
              }
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              placeholder="e.g. Remote / Bangalore"
            />

          </div>


          {/* Apply URL */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Application URL
            </label>

            <input
              type="url"
              value={applyUrl}
              onChange={(event) =>
                setApplyUrl(
                  event.target.value
                )
              }
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              placeholder="https://..."
            />

          </div>


          {/* Status */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Status
            </label>

            <select
              value={status}
              onChange={(event) =>
                setStatus(
                  event.target
                    .value as ApplicationStatus
                )
              }
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            >
              {STATUS_OPTIONS.map(
                (option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                )
              )}
            </select>

          </div>


          {/* Notes */}

          <div>

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Notes
            </label>

            <textarea
              value={notes}
              onChange={(event) =>
                setNotes(
                  event.target.value
                )
              }
              disabled={isSubmitting}
              rows={4}
              className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
              placeholder="Add notes about this application..."
            />

          </div>


          {/* =================================================
              Actions
              ================================================= */}

          <div className="flex justify-end gap-3 border-t border-slate-100 pt-5 dark:border-slate-800">

            <button
              type="button"
              onClick={handleClose}
              disabled={isSubmitting}
              className="rounded-xl border border-slate-200 px-5 py-2.5 text-sm font-semibold text-slate-600 transition hover:border-slate-300 hover:text-slate-900 disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={
                isSubmitting ||
                !jobTitle.trim() ||
                !company.trim()
              }
              className="rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isSubmitting
                ? "Saving..."
                : "Save Changes"}
            </button>

          </div>

        </form>

      </div>

    </div>
  );
};

export default EditApplicationModal;