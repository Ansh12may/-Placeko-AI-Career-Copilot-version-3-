export interface SectionScore {
  score: number;
  max_score: number;
}

export type CandidateLevel =
  | "fresher"
  | "early_career"
  | "experienced"
  | "senior";

export interface ResumeExperience {
  company: string;
  role: string;
  duration: string | null;
  description: string | null;
}

export interface ResumeProject {
  title: string;
  technologies: string[];
  description: string | null;
}

export interface ResumeEducation {
  institution: string;
  degree: string;
  year: string | null;
}

export interface CandidateProfile {
  name: string | null;
  email: string | null;
  phone: string | null;
  summary: string | null;
  skills: string[];
  education: ResumeEducation[];
  experience: ResumeExperience[];
  projects: ResumeProject[];
  certifications: string[];
  linkedin: string | null;
  github: string | null;
}

export interface ATSReport {
  candidate_level: CandidateLevel;

  overall_score: number;

  contact_information: SectionScore;
  education: SectionScore;
  experience: SectionScore;
  projects: SectionScore;
  skills: SectionScore;
  certifications: SectionScore;
  formatting: SectionScore;
  summary: SectionScore;

  strengths: string[];
  weaknesses: string[];
  missing_keywords: string[];

  formatting_feedback: string[];
  education_feedback: string[];
  experience_feedback: string[];
  project_feedback: string[];
  skills_feedback: string[];

  recommendations: string[];
}

export interface ResumeDetail {
  id: string;
  user_id: string;

  file_name: string;
  file_size: number;
  content_type: string;

  candidate_profile: CandidateProfile;
  ats_report: ATSReport;

  is_active: boolean;

  created_at: string;
  updated_at: string;
}

export interface ResumeLibraryItem {

  id: string;
  user_id: string;
  file_name: string;
  file_size: number;
  content_type: string;
  candidate_profile: CandidateProfile;
  ats_report: ATSReport;
  is_active: boolean;
  created_at: string;
  updated_at: string;

}

export interface ResumeListResponse {
  success: boolean;
  data: ResumeLibraryItem[];
}

export interface ResumeDetailResponse {
  success: boolean;
  data: ResumeDetail;
}

export interface ResumeUploadResponse {
  success: boolean;
  message: string;
  data: ResumeDetail;
}