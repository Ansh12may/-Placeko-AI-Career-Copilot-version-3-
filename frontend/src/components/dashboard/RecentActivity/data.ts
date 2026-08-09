import type { Activity } from "./types";

export const activities: Activity[] = [
  {
    id: 1,
    title: "Resume Score Updated",
    description: "Your ATS score improved to 88/100.",
    time: "2 hours ago",
    type: "resume",
  },
  {
    id: 2,
    title: "New Job Match",
    description: "Google Backend Engineer matched your profile.",
    time: "5 hours ago",
    type: "job",
  },
  {
    id: 3,
    title: "Mock Interview Completed",
    description: "You scored 91% in your AI interview.",
    time: "Yesterday",
    type: "interview",
  },
  {
    id: 4,
    title: "Roadmap Updated",
    description: "New DSA tasks have been added.",
    time: "2 days ago",
    type: "roadmap",
  },
];