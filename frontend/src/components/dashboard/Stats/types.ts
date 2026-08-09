import type { LucideIcon } from "lucide-react";

export interface Stat {
  id: number;
  title: string;
  value: string | number;
  change: string;
  trend: "up" | "down";
  icon: LucideIcon;
  color: string;
}