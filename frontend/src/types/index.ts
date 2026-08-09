export type NavigationTab = 
  | 'landing'
  | 'auth'
  | 'dashboard'
  | 'resumes'
  | 'resume-details'
  | 'job-details'
  | 'applications'
  | 'mock-interview'
  | 'interview-report'
  | 'learning-roadmap'
  | 'profile'
  | 'settings';

export type ResumeDetailTab = 
  | 'overview'
  | 'profile'
  | 'ats'
  | 'jobs'
  | 'interviews'
  | 'roadmap';

export interface Resume {
  id: string;
  name: string;
  uploadDate: string;
  atsScore: number;
  jobsCount: number;
  interviewsCount: number;
  status: 'Active' | 'Saved' | 'Draft';
  fileSize: string;
  parsedProfile: CandidateProfile;
  atsBreakdown: ATSBreakdown;
  learningRoadmap: LearningModule[];
}

export interface CandidateProfile {
  fullName: string;
  email: string;
  phone: string;
  location: string;
  linkedin: string;
  github: string;
  summary: string;
  skills: { name: string; category: string; level: 'Expert' | 'Advanced' | 'Intermediate' }[];
  experience: {
    company: string;
    role: string;
    period: string;
    location: string;
    highlights: string[];
  }[];
  projects: {
    title: string;
    description: string;
    tags: string[];
    link?: string;
  }[];
  education: {
    institution: string;
    degree: string;
    period: string;
    gpa?: string;
  }[];
  certifications: string[];
}

export interface ATSBreakdown {
  overallScore: number;
  sectionScores: {
    content: number;
    keywords: number;
    grammar: number;
    formatting: number;
    skillsMatch: number;
  };
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  missingSkills: string[];
  keywords: { text: string; value: number }[];
  timeline: { date: string; score: number; note: string }[];
}

export interface Job {
  id: string;
  title: string;
  company: string;
  logo: string;
  location: string;
  salary: string;
  experience: string;
  type: 'Full-time' | 'Remote' | 'Hybrid' | 'Contract';
  matchScore: number;
  skills: string[];
  matchedSkills: string[];
  missingSkills: string[];
  postedDate: string;
  status: 'Saved' | 'Applied' | 'Interviewing' | 'Offer' | 'Rejected' | 'None';
  description: string;
  responsibilities: string[];
  requirements: string[];
  benefits: string[];
}

export interface ApplicationItem {
  id: string;
  jobId: string;
  jobTitle: string;
  company: string;
  logo: string;
  stage: 'Saved' | 'Applied' | 'OA' | 'Technical' | 'HR' | 'Offer' | 'Rejected';
  appliedDate: string;
  salary: string;
  nextStep?: string;
}

export interface MockInterviewSession {
  id: string;
  resumeId: string;
  jobTitle: string;
  company: string;
  date: string;
  overallScore: number;
  technicalScore: number;
  communicationScore: number;
  confidenceScore: number;
  completenessScore: number;
  recommendation: 'Strong Hire' | 'Hire' | 'Needs Improvement' | 'Not Recommended';
  strengths: string[];
  weaknesses: string[];
  knowledgeGaps: string[];
  questions: {
    id: number;
    question: string;
    category: string;
    userAnswer?: string;
    feedback: string;
    idealAnswer: string;
    score: number;
  }[];
}

export interface LearningModule {
  id: string;
  week: number;
  topic: string;
  priority: 'High' | 'Medium' | 'Low';
  estimatedHours: number;
  completed: boolean;
  resources: { name: string; url: string; type: 'Video' | 'Article' | 'Interactive' }[];
  practiceTasks: string[];
}

export interface UserProfile {
  name: string;
  email: string;
  avatar: string;
  title: string;
  bio: string;
  resumesCount: number;
  applicationsCount: number;
  interviewsCount: number;
  avgScore: number;
  achievements: { title: string; date: string; icon: string }[];
}
