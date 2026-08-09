export interface Activity {
  id: number;
  title: string;
  description: string;
  time: string;
  type: "resume" | "job" | "interview" | "roadmap";

}