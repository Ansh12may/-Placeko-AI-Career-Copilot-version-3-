// =========================================================
// Application Status
// =========================================================

export type ApplicationStatus =
  | "saved"
  | "applied"
  | "screening"
  | "interview"
  | "offer"
  | "accepted"
  | "rejected"
  | "withdrawn";


// =========================================================
// Application
// =========================================================

export interface Application {
  id: string;

  user_id: string;

  // -------------------------------------------------------
  // Job information
  // -------------------------------------------------------

  job_id: string | null;

  job_title: string;

  company: string;

  location: string | null;

  apply_url: string | null;

  // -------------------------------------------------------
  // Application state
  // -------------------------------------------------------

  status: ApplicationStatus;

  // -------------------------------------------------------
  // User notes
  // -------------------------------------------------------

  notes: string | null;

  // -------------------------------------------------------
  // Dates
  // -------------------------------------------------------

  applied_at: string | null;

  created_at: string;

  updated_at: string;
}