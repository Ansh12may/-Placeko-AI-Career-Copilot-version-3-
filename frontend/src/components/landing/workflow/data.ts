import {
  Upload,
  FileSearch,
  ScanSearch,
  Briefcase,
  Mic,
  BarChart3,
} from "lucide-react";

import type { WorkflowStep } from "./types";

export const workflowSteps: WorkflowStep[] = [
  {
    number: 1,
    title: "Upload Resume",
    description:
      "Upload your PDF or DOCX resume securely to begin your career analysis.",
    icon: Upload,
  },

  {
    number: 2,
    title: "AI Resume Analysis",
    description:
      "Placeko extracts skills, projects, education, and experience using AI.",
    icon: FileSearch,
  },

  {
    number: 3,
    title: "ATS Optimization",
    description:
      "Receive keyword suggestions and improve your ATS compatibility score.",
    icon: ScanSearch,
  },

  {
    number: 4,
    title: "AI Job Matching",
    description:
      "Find jobs semantically matched to your profile and career goals.",
    icon: Briefcase,
  },

  {
    number: 5,
    title: "Mock Interview",
    description:
      "Practice technical interviews with AI-powered voice evaluation.",
    icon: Mic,
  },

  {
    number: 6,
    title: "Track Applications",
    description:
      "Manage your applications, interviews, and offers from one dashboard.",
    icon: BarChart3,
  },
];