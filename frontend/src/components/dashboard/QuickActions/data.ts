import {
  BookOpen,
  Briefcase,
  FileText,
  Mic,
} from "lucide-react";

import type { QuickAction } from "./types";

export const quickActions: QuickAction[] = [
  {
    id: 1,
    title: "Resume Library",
    description: "Manage all your resumes",
    icon: FileText,
    color: "bg-indigo-600",
    route: "/resume",
  },
  {
    id: 2,
    title: "Find Jobs",
    description: "Discover AI matched jobs",
    icon: Briefcase,
    color: "bg-emerald-500",
    route: "/jobs",
  },
  {
    id: 3,
    title: "Mock Interview",
    description: "Practice with AI interviewer",
    icon: Mic,
    color: "bg-orange-500",
    route: "/interview",
  },
  {
    id: 4,
    title: "Application Roadmap",
    description: "Track your preparation",
    icon: BookOpen,
    color: "bg-pink-500",
    route: "/learning-roadmap",
  },
];