import api from "./axios";

// ============================================================
// JOB READINESS TYPES
// ============================================================

export interface CandidateEvidence {
  source_type:
    | "skill"
    | "project"
    | "experience"
    | "certification"
    | "candidate_confirmation";

  source: string;

  matched_text?: string | null;
}

export interface JobRequirementEvidence {
  requirement: string;

  status:
    | "proven"
    | "unproven"
    | "resume_gap"
    | "candidate_confirmed";

  evidence: CandidateEvidence[];

  explanation: string;
}

export interface JobReadiness {
  requirements: JobRequirementEvidence[];

  proven_count: number;

  unproven_count: number;

  resume_gap_count: number;

  candidate_confirmed_count: number;
}

// ============================================================
// JOB
// ============================================================

export interface Job {
  job_id?: string | null;

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

  pinecone_score?: number | null;

  reranker_score?: number | null;

  job_readiness?: JobReadiness | null;
}

// ============================================================
// RECOMMENDED JOBS
// ============================================================

export interface RecommendedJobsResponse {
  success: boolean;

  data: Job[];
}

export const getRecommendedJobs =
  async (): Promise<Job[]> => {
    const response =
      await api.get<RecommendedJobsResponse>(
        "/api/jobs/recommended"
      );

    return response.data.data;
  };

// ============================================================
// VERIFY JOB REQUIREMENT
// ============================================================

export const verifyJobRequirement =
  async (
    job: Job,
    requirement: string
  ): Promise<void> => {
    await api.post(
      "/api/jobs/readiness/verify",
      {
        job,
        requirement,
      }
    );
  };

// ============================================================
// MCP JOB RESEARCH
// ============================================================

export interface JobResearchRequest {
  query: string;
}

export interface JobResearchToolUsage {
  tool: string;

  arguments: Record<
    string,
    unknown
  >;
}

export interface JobResearchData {
  resume_id: string;

  report: string;

  tools_used: JobResearchToolUsage[];

  research_rounds: number;
}

export interface JobResearchResponse {
  success: boolean;

  data: JobResearchData;
}

// ============================================================
// RUN JOB RESEARCH AGENT
// ============================================================

export const researchJobs =
  async (
    query: string
  ): Promise<JobResearchData> => {
    const response =
      await api.post<JobResearchResponse>(
        "/api/jobs/research",
        {
          query,
        }
      );

    return response.data.data;
  };