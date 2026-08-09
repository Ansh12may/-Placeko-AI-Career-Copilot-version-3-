import {
  FileText,
  Briefcase,
  ClipboardCheck,
  Trophy,
} from "lucide-react";

import type { Stat } from "./types";

export const stats: Stat[] = [
  {
    id: 1,
    title: "Resume Score",
    value: "88",
    change: "+5%",
    trend: "up",
    icon: FileText,
    color: "bg-indigo-600",
  },
  {
    id: 2,
    title: "Job Matches",
    value: "24",
    change: "+12",
    trend: "up",
    icon: Briefcase,
    color: "bg-emerald-500",
  },
  {
    id: 3,
    title: "Applications",
    value: "5",
    change: "+2",
    trend: "up",
    icon: ClipboardCheck,
    color: "bg-orange-500",
  },
  {
    id: 4,
    title: "Interview Readiness",
    value: "92%",
    change: "+8%",
    trend: "up",
    icon: Trophy,
    color: "bg-pink-500",
  },
];