// =========================================================
// Interview Enums
// =========================================================

export type InterviewType =
  | "technical"
  | "behavioral"
  | "mixed";

export type Difficulty =
  | "easy"
  | "medium"
  | "hard";

export type InterviewMode =
  | "Mixed"
  | "Technical"
  | "Behavioral"
  | "Project"
  | "HR";

export type DifficultyLevel =
  | "Easy"
  | "Medium"
  | "Hard";

export type InterviewStatus =
  | "Not Started"
  | "In Progress"
  | "Paused"
  | "Completed"
  | "Terminated";

export type QuestionCategory =
  | "Technical"
  | "Behavioral"
  | "Project"
  | "HR"
  | "System Design";

export type AnswerSource =
  | "Text"
  | "Voice";

export type HiringRecommendation =
  | "Strong Hire"
  | "Hire"
  | "Borderline"
  | "No Hire";


// =========================================================
// Interview Request
// =========================================================

export interface InterviewRequest {
  resume_id: string;

  job_id?: string | null;

  job_description?: string | null;

  interview_type: InterviewType;

  difficulty: Difficulty;

  num_questions: number;

  include_projects: boolean;

  include_experience: boolean;

  include_behavioral: boolean;

  include_voice_analysis: boolean;
}


// =========================================================
// Interview Question
// =========================================================

export interface InterviewQuestion {
  question_id: number;

  category: QuestionCategory;

  difficulty: DifficultyLevel;

  question: string;

  focus_topic: string;

  expected_topics: string[];

  followup_allowed: boolean;

  estimated_time_seconds: number;

  interviewer_notes: string;

  prerequisite_question_id: number | null;
}


// =========================================================
// Answer Metadata
// =========================================================

export interface AnswerMetadata {
  audio_duration: number;

  word_count: number;

  speech_rate: number;
}


// =========================================================
// Interview Answer
// =========================================================

export interface InterviewAnswer {
  question_id: number;

  transcript: string;

  source: AnswerSource;

  duration_seconds: number;

  answered_at?: string;

  metadata?: AnswerMetadata | null;
}


// =========================================================
// Score Breakdown
// =========================================================

export interface ScoreBreakdown {
  score: number;

  max_score: number;

  feedback: string;
}


// =========================================================
// Interview Feedback
// =========================================================

export interface InterviewFeedback {
  technical: ScoreBreakdown;

  communication: ScoreBreakdown;

  completeness: ScoreBreakdown;

  confidence: ScoreBreakdown;

  overall: ScoreBreakdown;

  strengths: string[];

  weaknesses: string[];

  missing_topics: string[];

  suggestions: string[];

  followup_recommended: boolean;

  interviewer_notes: string;
}


// =========================================================
// Question Answer Pair
// =========================================================

export interface QuestionAnswerPair {
  question: InterviewQuestion;

  answer: InterviewAnswer | null;

  feedback: InterviewFeedback | null;

  interaction_completed: boolean;
}


// =========================================================
// Interview Plan
// =========================================================

export interface InterviewPlan {
  interview_mode: InterviewMode;

  difficulty: DifficultyLevel;

  duration_minutes: number;

  technical_questions: number;

  behavioral_questions: number;

  project_questions: number;

  followup_questions: number;

  focus_topics: string[];

  evaluation_criteria: string[];

  interviewer_notes: string;
}


// =========================================================
// Interview Session
// =========================================================

export interface InterviewSession {
  session_id: string;
  user_id: string;
  resume_id: string;
  candidate: {
    name: string | null;
    email: string | null;
    phone: string | null;
    summary: string | null;
    skills: string[];
    education: unknown[];
    experience: unknown[];
    projects: unknown[];
    certifications: string[];
    linkedin: string | null;
    github: string | null;
  };

  target_job: unknown | null;

  interview_plan: InterviewPlan;

  history: QuestionAnswerPair[];

  current_question_index: number;

  status: InterviewStatus;

  started_at: string | null;

  ended_at: string | null;

  report: InterviewReport | null;
}

// =========================================================
// Interview Score
// =========================================================

export interface InterviewScore {
  score: number;

  max_score: number;
}


// =========================================================
// Question Summary
// =========================================================

export interface QuestionSummary {
  question: string;

  score: number;

  strengths: string[];

  weaknesses: string[];
}


// =========================================================
// Interview Report
// =========================================================

export interface InterviewReport {
  overall_score: InterviewScore;

  technical_score: InterviewScore;

  communication_score: InterviewScore;

  confidence_score: InterviewScore;

  completeness_score: InterviewScore;

  strengths: string[];

  weaknesses: string[];

  knowledge_gaps: string[];

  recommendations: string[];

  learning_roadmap: string[];

  question_summaries: QuestionSummary[];

  final_feedback: string;

  hiring_recommendation: HiringRecommendation;
}

export interface InterviewTargetJob {
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