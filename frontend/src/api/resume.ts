import api from "./axios";

import type {
  ResumeDetailResponse,
  ResumeListResponse,
  ResumeUploadResponse,
} from "../types/resume";



export const getResumes = async (): Promise<ResumeListResponse> => {
  const response = await api.get<ResumeListResponse>(
    "/api/resume"
  );

  return response.data;
};


export const getResumeById = async (
  resumeId: string
): Promise<ResumeDetailResponse> => {
  const response = await api.get<ResumeDetailResponse>(
    `/api/resume/${resumeId}`
  );

  return response.data;
};


export const uploadResume = async (
  file: File
): Promise<ResumeUploadResponse> => {

  const formData = new FormData();

  formData.append("file", file);

  const response =
    await api.post<ResumeUploadResponse>(
      "/api/resume/upload",
      formData
    );

  return response.data;
};


// =========================================================
// Delete Resume
// =========================================================

export const deleteResume = async (
  resumeId: string
): Promise<void> => {

  await api.delete(
    `/api/resume/${resumeId}`
  );

};