import { useEffect, useMemo, useState } from "react";
import {
  Edit3,
  Plus,
  RefreshCw,
  Trash2,
} from "lucide-react";

import AddApplicationModal from "../applications/AddApplicationModal";
import EditApplicationModal from "../applications/EditApplicationModal";

import {
  getApplications,
  updateApplicationStatus,
  deleteApplication,
} from "../../api/application";

import type {
  Application,
  ApplicationStatus,
} from "../../types/application";


// =========================================================
// Kanban Configuration
// =========================================================

interface KanbanColumn {
  status: ApplicationStatus;
  title: string;
  description: string;
}

const KANBAN_COLUMNS: KanbanColumn[] = [
  {
    status: "saved",
    title: "Saved",
    description: "Jobs you want to consider",
  },
  {
    status: "applied",
    title: "Applied",
    description: "Applications you've submitted",
  },
  {
    status: "screening",
    title: "Screening",
    description: "Initial recruiter screening",
  },
  {
    status: "interview",
    title: "Interview",
    description: "Interviews in progress",
  },
  {
    status: "offer",
    title: "Offer",
    description: "Offers received",
  },
  {
    status: "accepted",
    title: "Accepted",
    description: "Offers you've accepted",
  },
  {
    status: "rejected",
    title: "Rejected",
    description: "Applications that ended",
  },
  {
    status: "withdrawn",
    title: "Withdrawn",
    description: "Applications you withdrew",
  },
];


// =========================================================
// Status Colors
// =========================================================

const getStatusClasses = (
  status: ApplicationStatus
) => {
  switch (status) {
    case "saved":
      return "bg-slate-100 text-slate-600";

    case "applied":
      return "bg-blue-100 text-blue-600";

    case "screening":
      return "bg-amber-100 text-amber-700";

    case "interview":
      return "bg-indigo-100 text-indigo-600";

    case "offer":
      return "bg-emerald-100 text-emerald-600";

    case "accepted":
      return "bg-green-100 text-green-700";

    case "rejected":
      return "bg-red-100 text-red-600";

    case "withdrawn":
      return "bg-gray-100 text-gray-600";

    default:
      return "bg-slate-100 text-slate-600";
  }
};


// =========================================================
// Application Card
// =========================================================

interface ApplicationCardProps {
  application: Application;

  onStatusChange: (
    applicationId: string,
    status: ApplicationStatus
  ) => void;

  onEdit: (
    application: Application
  ) => void;

  onDelete: (
    applicationId: string
  ) => void;

  isUpdating: boolean;

  isDeleting: boolean;
}

const ApplicationCard = ({
  application,
  onStatusChange,
  onEdit,
  onDelete,
  isUpdating,
  isDeleting,
}: ApplicationCardProps) => {
  const currentIndex =
    KANBAN_COLUMNS.findIndex(
      (column) =>
        column.status === application.status
    );

  const nextColumn =
    currentIndex >= 0 &&
    currentIndex <
      KANBAN_COLUMNS.length - 1
      ? KANBAN_COLUMNS[
          currentIndex + 1
        ]
      : null;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-indigo-300 hover:shadow-md dark:border-slate-800 dark:bg-slate-900">

      {/* =====================================================
          Company / Job
          ===================================================== */}

      <div className="flex items-start justify-between gap-3">

        <div className="min-w-0">

          <h3 className="truncate text-sm font-bold text-slate-900 dark:text-white">
            {application.job_title}
          </h3>

          <p className="mt-1 truncate text-xs font-medium text-slate-500">
            {application.company}
          </p>

        </div>

        <span
          className={`shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold capitalize ${getStatusClasses(
            application.status
          )}`}
        >
          {application.status}
        </span>

      </div>


      {/* =====================================================
          Location
          ===================================================== */}

      {application.location && (
        <p className="mt-3 text-xs text-slate-500">
          {application.location}
        </p>
      )}


      {/* =====================================================
          Notes
          ===================================================== */}

      {application.notes && (
        <p className="mt-3 line-clamp-2 text-xs leading-5 text-slate-500">
          {application.notes}
        </p>
      )}


      {/* =====================================================
          Edit / Delete
          ===================================================== */}

      <div className="mt-4 flex gap-2 border-t border-slate-100 pt-3 dark:border-slate-800">

        {/* Edit */}

        <button
          type="button"
          onClick={() =>
            onEdit(application)
          }
          disabled={
            isUpdating ||
            isDeleting
          }
          className="flex flex-1 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 transition hover:border-indigo-300 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
        >
          <Edit3 size={13} />

          Edit
        </button>


        {/* Delete */}

        <button
          type="button"
          onClick={() =>
            onDelete(application.id)
          }
          disabled={
            isUpdating ||
            isDeleting
          }
          className="flex items-center justify-center rounded-lg border border-red-200 px-3 py-2 text-red-500 transition hover:border-red-300 hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-red-900/50 dark:hover:bg-red-950/30"
          title="Delete application"
        >
          <Trash2 size={13} />
        </button>

      </div>


      {/* =====================================================
          Move Status
          ===================================================== */}

      <div className="mt-2">

        {nextColumn ? (
          <button
            type="button"
            disabled={
              isUpdating ||
              isDeleting
            }
            onClick={() =>
              onStatusChange(
                application.id,
                nextColumn.status
              )
            }
            className="w-full rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 transition hover:border-indigo-300 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300"
          >
            {isUpdating
              ? "Updating..."
              : `Move to ${nextColumn.title}`}
          </button>
        ) : (
          <div className="text-center text-[11px] font-medium text-slate-400">
            Current stage
          </div>
        )}

      </div>

    </div>
  );
};


// =========================================================
// Applications Page
// =========================================================

const ApplicationsPage = () => {

  const [applications, setApplications] =
    useState<Application[]>([]);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [updatingId, setUpdatingId] =
    useState<string | null>(null);

  const [deletingId, setDeletingId] =
    useState<string | null>(null);

  const [isAddModalOpen, setIsAddModalOpen] =
    useState(false);

  const [isEditModalOpen, setIsEditModalOpen] =
    useState(false);

  const [selectedApplication, setSelectedApplication] =
    useState<Application | null>(null);


  // =========================================================
  // Load Applications
  // =========================================================

  const loadApplications = async () => {
    try {

      setIsLoading(true);

      setError(null);

      const data =
        await getApplications();

      setApplications(data);

    } catch (err) {

      console.error(
        "Failed to load applications:",
        err
      );

      setError(
        "Unable to load your applications."
      );

    } finally {

      setIsLoading(false);

    }
  };


  // =========================================================
  // Initial Load
  // =========================================================

  useEffect(() => {
    loadApplications();
  }, []);


  // =========================================================
  // Group Applications
  // =========================================================

  const applicationsByStatus =
    useMemo(() => {

      const grouped: Record<
        ApplicationStatus,
        Application[]
      > = {

        saved: [],
        applied: [],
        screening: [],
        interview: [],
        offer: [],
        accepted: [],
        rejected: [],
        withdrawn: [],

      };

      applications.forEach(
        (application) => {

          grouped[
            application.status
          ].push(application);

        }
      );

      return grouped;

    }, [applications]);


  // =========================================================
  // Update Status
  // =========================================================

  const handleStatusChange = async (
    applicationId: string,
    status: ApplicationStatus
  ) => {

    try {

      setUpdatingId(
        applicationId
      );

      setError(null);

      const updatedApplication =
        await updateApplicationStatus(
          applicationId,
          status
        );

      setApplications(
        (currentApplications) =>
          currentApplications.map(
            (application) =>
              application.id ===
              updatedApplication.id
                ? updatedApplication
                : application
          )
      );

    } catch (err) {

      console.error(
        "Failed to update application status:",
        err
      );

      setError(
        "Unable to update application status."
      );

    } finally {

      setUpdatingId(null);

    }
  };


  // =========================================================
  // Delete Application
  // =========================================================

  const handleDeleteApplication = async (
    applicationId: string
  ) => {

    const confirmed =
      window.confirm(
        "Are you sure you want to delete this application?"
      );

    if (!confirmed) {
      return;
    }

    try {

      setDeletingId(
        applicationId
      );

      setError(null);

      await deleteApplication(
        applicationId
      );

      setApplications(
        (currentApplications) =>
          currentApplications.filter(
            (application) =>
              application.id !==
              applicationId
          )
      );

    } catch (err) {

      console.error(
        "Failed to delete application:",
        err
      );

      setError(
        "Unable to delete application."
      );

    } finally {

      setDeletingId(null);

    }
  };


  // =========================================================
  // Application Created
  // =========================================================

  const handleApplicationCreated = (
    application: Application
  ) => {

    setApplications(
      (currentApplications) => [
        application,
        ...currentApplications,
      ]
    );

  };


  // =========================================================
  // Open Edit Modal
  // =========================================================

  const handleEditApplication = (
    application: Application
  ) => {

    setSelectedApplication(
      application
    );

    setIsEditModalOpen(true);

    setError(null);
  };


  // =========================================================
  // Close Edit Modal
  // =========================================================

  const handleCloseEditModal = () => {

    setIsEditModalOpen(false);

    setSelectedApplication(null);

  };


  // =========================================================
  // Application Updated
  // =========================================================

  const handleApplicationUpdated = (
    updatedApplication: Application
  ) => {

    setApplications(
      (currentApplications) =>
        currentApplications.map(
          (application) =>
            application.id ===
            updatedApplication.id
              ? updatedApplication
              : application
        )
    );

  };


  // =========================================================
  // Loading
  // =========================================================

  if (isLoading) {

    return (
      <div className="flex min-h-[600px] items-center justify-center">

        <div className="flex items-center gap-2 text-sm font-medium text-slate-500">

          <RefreshCw
            size={16}
            className="animate-spin"
          />

          Loading applications...

        </div>

      </div>
    );

  }


  // =========================================================
  // Main UI
  // =========================================================

  return (
    <div className="mx-auto w-full max-w-[1600px]">

      {/* =====================================================
          Header
          ===================================================== */}

      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">

        <div>

          <p className="text-xs font-bold uppercase tracking-wider text-indigo-600">
            Career Tracker
          </p>

          <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 dark:text-white">
            Applications
          </h1>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">
            Track your job applications from saved
            opportunities to accepted offers.
          </p>

        </div>


        {/* Add Button */}

        <button
          type="button"
          onClick={() =>
            setIsAddModalOpen(true)
          }
          className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-indigo-700"
        >

          <Plus size={17} />

          Add Application

        </button>

      </div>


      {/* =====================================================
          Error
          ===================================================== */}

      {error && (
        <div className="mb-6 flex items-center justify-between gap-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3">

          <p className="text-sm font-medium text-red-600">
            {error}
          </p>

          <button
            type="button"
            onClick={loadApplications}
            className="text-xs font-bold text-red-600 underline"
          >
            Retry
          </button>

        </div>
      )}


      {/* =====================================================
          Empty State
          ===================================================== */}

      {!applications.length ? (

        <div className="flex min-h-[400px] items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 dark:border-slate-700 dark:bg-slate-900/50">

          <div className="max-w-md px-6 text-center">

            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-100 text-indigo-600">
              <Plus size={24} />
            </div>

            <h2 className="mt-5 text-lg font-bold text-slate-900 dark:text-white">
              No applications yet
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              Start tracking your job search by
              adding your first application.
            </p>

            <button
              type="button"
              onClick={() =>
                setIsAddModalOpen(true)
              }
              className="mt-5 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-indigo-700"
            >
              Add Application
            </button>

          </div>

        </div>

      ) : (

        /* ===================================================
           Kanban
           =================================================== */

        <div className="overflow-x-auto pb-6">

          <div className="grid min-w-[1800px] grid-cols-8 gap-4">

            {KANBAN_COLUMNS.map(
              (column) => {

                const columnApplications =
                  applicationsByStatus[
                    column.status
                  ];

                return (

                  <div
                    key={column.status}
                    className="flex min-h-[500px] flex-col rounded-2xl bg-slate-50 p-3 dark:bg-slate-900/60"
                  >

                    {/* Column Header */}

                    <div className="mb-3">

                      <div className="flex items-center justify-between">

                        <h2 className="text-sm font-bold text-slate-800 dark:text-white">
                          {column.title}
                        </h2>

                        <span className="flex h-6 min-w-6 items-center justify-center rounded-full bg-white px-2 text-[11px] font-bold text-slate-500 shadow-sm dark:bg-slate-800">
                          {
                            columnApplications.length
                          }
                        </span>

                      </div>

                      <p className="mt-1 text-[10px] leading-4 text-slate-400">
                        {column.description}
                      </p>

                    </div>


                    {/* Cards */}

                    <div className="flex flex-1 flex-col gap-3">

                      {columnApplications.length > 0 ? (

                        columnApplications.map(
                          (application) => (

                            <ApplicationCard
                              key={
                                application.id
                              }

                              application={
                                application
                              }

                              onStatusChange={
                                handleStatusChange
                              }

                              onEdit={
                                handleEditApplication
                              }

                              onDelete={
                                handleDeleteApplication
                              }

                              isUpdating={
                                updatingId ===
                                application.id
                              }

                              isDeleting={
                                deletingId ===
                                application.id
                              }
                            />

                          )
                        )

                      ) : (

                        <div className="flex flex-1 items-center justify-center rounded-xl border border-dashed border-slate-200 bg-white/50 px-3 py-8 dark:border-slate-800 dark:bg-slate-900/30">

                          <p className="text-center text-[11px] text-slate-400">
                            No applications
                          </p>

                        </div>

                      )}

                    </div>

                  </div>

                );

              }
            )}

          </div>

        </div>

      )}


      {/* =====================================================
          Add Application Modal
          ===================================================== */}

      <AddApplicationModal
        isOpen={
          isAddModalOpen
        }

        onClose={() =>
          setIsAddModalOpen(false)
        }

        onCreated={
          handleApplicationCreated
        }
      />


      {/* =====================================================
          Edit Application Modal
          ===================================================== */}

      <EditApplicationModal
        isOpen={
          isEditModalOpen
        }

        application={
          selectedApplication
        }

        onClose={
          handleCloseEditModal
        }

        onUpdated={
          handleApplicationUpdated
        }
      />

    </div>
  );
};

export default ApplicationsPage;