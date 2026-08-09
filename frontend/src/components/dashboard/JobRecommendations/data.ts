import type { JobRecommendation } from "./types";

export const recommendedJobs: JobRecommendation[] = [
  {
    id: 1,
    company: "Google",
    role: "Backend Engineer Intern",
    location: "Bangalore",
    salary: "₹18 LPA",
    match: 94,
    skills: ["Python", "FastAPI", "React"],
  },
  {
    id: 2,
    company: "Microsoft",
    role: "Software Engineer",
    location: "Hyderabad",
    salary: "₹22 LPA",
    match: 91,
    skills: ["C++", "DSA", "Azure"],
  },
  {
    id: 3,
    company: "Amazon",
    role: "SDE Intern",
    location: "Chennai",
    salary: "₹16 LPA",
    match: 89,
    skills: ["Java", "Spring", "AWS"],
  },
];