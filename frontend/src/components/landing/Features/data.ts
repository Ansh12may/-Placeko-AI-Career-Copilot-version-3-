import {
  FileText,
  Briefcase,
  Mic,
  BarChart3,
} from "lucide-react";

import type { Feature } from "./type.ts";

export const features: Feature[] = [
  {
    icon: FileText,
    title: "Resume Intelligence",
    description:
      "ATS optimization, resume parsing, keyword analysis and AI-powered resume improvements.",
  },

  {
    icon: Briefcase,
    title: "AI Job Matching",
    description:
      "Semantic job recommendations based on your skills, experience and career goals.",
  },

  {
    icon: Mic,
    title: "AI Mock Interview",
    description:
      "Practice technical interviews with AI voice evaluation and detailed feedback.",
  },

  {
    icon: BarChart3,
    title: "Career Dashboard",
    description:
      "Track applications, monitor progress and receive personalized learning roadmaps.",
  },
];