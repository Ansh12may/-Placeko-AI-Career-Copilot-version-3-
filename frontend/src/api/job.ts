import api from "./axios";

export interface Job {
  title: string;
  company: string;
  location: string;
  employment_type?: string | null;
  experience?: string | null;
  salary?: string | null;
  skills: string[];
  description: string;
  apply_url?: string | null;
  source: string;
  match_score?: number | null;
}

export interface RecommendedJobsResponse {
  success: boolean;
  data: Job[];
}

export const getRecommendedJobs = async (): Promise<Job[]> => {
  const response = await api.get<RecommendedJobsResponse>(
    "/api/jobs/recommended"
  );

  return response.data.data;
};