import api from "./axios";

import type {
  InterviewAnswer,
  InterviewReport,
  InterviewRequest,
  InterviewSession,
} from "../types/interview";


// =========================================================
// API Response Types
// =========================================================

interface InterviewSessionResponse {
  success: boolean;
  data: InterviewSession;
}

interface InterviewReportResponse {
  success: boolean;
  data: InterviewReport;
}


// =========================================================
// Start Interview
// =========================================================

export const startInterview = async (
  request: InterviewRequest
): Promise<InterviewSession> => {
  const response = await api.post<InterviewSessionResponse>(
    "/api/interview/start",
    request
  );

  return response.data.data;
};


// =========================================================
// Submit Answer
// =========================================================

export const submitInterviewAnswer = async (
  sessionId: string,
  answer: InterviewAnswer
): Promise<InterviewSession> => {
  const response = await api.post<InterviewSessionResponse>(
    `/api/interview/answer/${sessionId}`,
    answer
  );

  return response.data.data;
};


// =========================================================
// Get Session
// =========================================================

export const getInterviewSession = async (
  sessionId: string
): Promise<InterviewSession> => {
  const response = await api.get<InterviewSessionResponse>(
    `/api/interview/session/${sessionId}`
  );

  return response.data.data;
};


// =========================================================
// Get Current Question
// =========================================================

export const getCurrentQuestion = async (
  sessionId: string
) => {
  const response = await api.get(
    `/api/interview/question/${sessionId}`
  );

  return response.data.data;
};


// =========================================================
// Finish Interview
// =========================================================

export const finishInterview = async (
  sessionId: string
): Promise<InterviewReport> => {
  const response = await api.post<InterviewReportResponse>(
    `/api/interview/finish/${sessionId}`
  );

  return response.data.data;
};

export const getInterviewHistory = async (): Promise<InterviewSession[]> => {
  const response = await api.get<{
    success: boolean;
    data: InterviewSession[];
  }>("/api/interview/history");

  return response.data.data;

};



export const submitVoiceAnswer = async (
  sessionId: string,
  formData: FormData
): Promise<InterviewSession> => {
  const response = await api.post<InterviewSessionResponse>(
    `/api/interview/voice/${sessionId}`,
    formData
  );

  return response.data.data;
};