import { useState } from "react";
import type { SyntheticEvent } from "react";
import { X } from "lucide-react";

import {
  createApplication,
} from "../../api/application";

import type {
  Application,
  ApplicationStatus,
} from "../../types/application";


// =========================================================
// Props
// =========================================================

interface AddApplicationModalProps {
  isOpen: boolean;

  onClose: () => void;

  onCreated: (
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
];


// =========================================================
// Component
// =========================================================

const AddApplicationModal = ({
  isOpen,
  onClose,
  onCreated,
}: AddApplicationModalProps) => {
  const [jobTitle, setJobTitle] =
    useState("");

  const [company, setCompany] =
    useState("");

  const [location, setLocation] =
    useState("");

  const [applyUrl, setApplyUrl] =
    useState("");

  const [status, setStatus] =
    useState<ApplicationStatus>("saved");

  const [notes, setNotes] =
    useState("");

  const [isSubmitting, setIsSubmitting] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  // =======================================================
  // Reset Form
  // =======================================================

  const resetForm = () => {
    setJobTitle("");
    setCompany("");
    setLocation("");
    setApplyUrl("");
    setStatus("saved");
    setNotes("");
    setError(null);
  };


  // =======================================================
  // Close Modal
  // =======================================================

  const handleClose = () => {
    if (isSubmitting) {
      return;
    }

    resetForm();
    onClose();
  };


  // =======================================================
  // Submit
  // =======================================================

  const handleSubmit = async (
    event: SyntheticEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!jobTitle.trim()) {
      setError(
        "Please enter the job title."
      );
      return;
    }

    if (!company.trim()) {
      setError(
        "Please enter the company name."
      );
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);

      const application =
        await createApplication({
          job_title: jobTitle.trim(),

          company: company.trim(),

          location:
            location.trim() || null,

          apply_url:
            applyUrl.trim() || null,

          status,

          notes:
            notes.trim() || null,
        });

      onCreated(application);

      resetForm();

      onClose();

    } catch (err) {
      console.error(
        "Failed to create application:",
        err
      );

      setError(
        "Unable to create the application. Please try again."
      );

    } finally {
      setIsSubmitting(false);
    }
  };


  // =======================================================
  // Hidden
  // =======================================================

  if (!isOpen) {
    return null;
  }


  // =======================================================
  // UI
  // =======================================================

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 px-4 backdrop-blur-sm"
      onMouseDown={(event) => {
        if (
          event.target === event.currentTarget &&
          !isSubmitting
        ) {
          handleClose();
        }
      }}
    >

      <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">

        {/* =================================================
            Header
            ================================================= */}

        <div className="flex items-center justify-between border-b border-slate-100 px-6 py-5 dark:border-slate-800">

          <div>

            <h2 className="text-lg font-bold text-slate-900 dark:text-white">
              Add Application
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Add a job to your application pipeline.
            </p>

          </div>

          <button
            type="button"
            onClick={handleClose}
            disabled={isSubmitting}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:opacity-50 dark:hover:bg-slate-800"
          >
            <X size={18} />
          </button>

        </div>


        {/* =================================================
            Form
            ================================================= */}

        <form
          onSubmit={handleSubmit}
          className="p-6"
        >

          {/* Error */}

          {error && (
            <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-xs font-medium text-red-600">
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
              placeholder="e.g. Python AI Engineer"
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />

          </div>


          {/* Company */}

          <div className="mt-4">

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
              placeholder="e.g. OpenAI"
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />

          </div>


          {/* Location */}

          <div className="mt-4">

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Location
              <span className="ml-1 font-normal text-slate-400">
                (optional)
              </span>
            </label>

            <input
              type="text"
              value={location}
              onChange={(event) =>
                setLocation(
                  event.target.value
                )
              }
              placeholder="e.g. Remote / Bangalore"
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />

          </div>


          {/* Apply URL */}

          <div className="mt-4">

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Application URL
              <span className="ml-1 font-normal text-slate-400">
                (optional)
              </span>
            </label>

            <input
              type="url"
              value={applyUrl}
              onChange={(event) =>
                setApplyUrl(
                  event.target.value
                )
              }
              placeholder="https://..."
              disabled={isSubmitting}
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />

          </div>


          {/* Status */}

          <div className="mt-4">

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
              className="mt-2 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700 outline-none transition focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
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

          <div className="mt-4">

            <label className="text-xs font-bold text-slate-700 dark:text-slate-300">
              Notes
              <span className="ml-1 font-normal text-slate-400">
                (optional)
              </span>
            </label>

            <textarea
              value={notes}
              onChange={(event) =>
                setNotes(
                  event.target.value
                )
              }
              placeholder="Add notes about this application..."
              rows={3}
              disabled={isSubmitting}
              className="mt-2 w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white focus:ring-2 focus:ring-indigo-100 disabled:opacity-60 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
            />

          </div>


          {/* Actions */}

          <div className="mt-6 flex justify-end gap-3">

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
                ? "Adding..."
                : "Add Application"}
            </button>

          </div>

        </form>

      </div>

    </div>
  );
};

export default AddApplicationModal;