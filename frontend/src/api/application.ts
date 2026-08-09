import api from "./axios";

import type {
  Application,
  ApplicationStatus,
} from "../types/application";


// =========================================================
// API Response Types
// =========================================================

interface ApplicationResponse {
  success: boolean;
  data: Application;
}

interface ApplicationsResponse {
  success: boolean;
  data: Application[];
}


// =========================================================
// Get Applications
// =========================================================

export const getApplications = async (): Promise<
  Application[]
> => {
  const response =
    await api.get<ApplicationsResponse>(
      "/api/applications"
    );

  return response.data.data;
};


// =========================================================
// Get Single Application
// =========================================================

export const getApplication = async (
  applicationId: string
): Promise<Application> => {
  const response =
    await api.get<ApplicationResponse>(
      `/api/applications/${applicationId}`
    );

  return response.data.data;
};


// =========================================================
// Create Application
// =========================================================

export interface CreateApplicationRequest {
  job_id?: string | null;

  job_title: string;

  company: string;

  location?: string | null;

  apply_url?: string | null;

  status?: ApplicationStatus;

  notes?: string | null;
}

export const createApplication = async (
  request: CreateApplicationRequest
): Promise<Application> => {
  const response =
    await api.post<ApplicationResponse>(
      "/api/applications",
      request
    );

  return response.data.data;
};


// =========================================================
// Update Application
// =========================================================

export interface UpdateApplicationRequest {
  job_title?: string;

  company?: string;

  location?: string | null;

  apply_url?: string | null;

  notes?: string | null;

  status?: ApplicationStatus;
}

export const updateApplication = async (
  applicationId: string,
  request: UpdateApplicationRequest
): Promise<Application> => {
  const response =
    await api.patch<ApplicationResponse>(
      `/api/applications/${applicationId}`,
      request
    );

  return response.data.data;
};


// =========================================================
// Update Application Status
// =========================================================

export const updateApplicationStatus = async (
  applicationId: string,
  status: ApplicationStatus
): Promise<Application> => {
  const response =
    await api.patch<ApplicationResponse>(
      `/api/applications/${applicationId}/status`,
      {
        status,
      }
    );

  return response.data.data;
};


// =========================================================
// Delete Application
// =========================================================

export const deleteApplication = async (
  applicationId: string
): Promise<void> => {
  await api.delete(
    `/api/applications/${applicationId}`
  );
};

