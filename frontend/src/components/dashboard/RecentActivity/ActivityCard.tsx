import {
  Briefcase,
  FileText,
  GraduationCap,
  Mic,
} from "lucide-react";

import type { Activity } from "./types";

interface ActivityCardProps {
  activity: Activity;
}

const ActivityCard = ({ activity }: ActivityCardProps) => {
  const getActivityIcon = () => {
    switch (activity.type) {
      case "resume":
        return (
          <div className="rounded-full bg-indigo-100 p-2 dark:bg-indigo-900/30">
            <FileText
              size={18}
              className="text-indigo-600 dark:text-indigo-400"
            />
          </div>
        );

      case "job":
        return (
          <div className="rounded-full bg-emerald-100 p-2 dark:bg-emerald-900/30">
            <Briefcase
              size={18}
              className="text-emerald-600 dark:text-emerald-400"
            />
          </div>
        );

      case "interview":
        return (
          <div className="rounded-full bg-orange-100 p-2 dark:bg-orange-900/30">
            <Mic
              size={18}
              className="text-orange-600 dark:text-orange-400"
            />
          </div>
        );

      case "roadmap":
        return (
          <div className="rounded-full bg-pink-100 p-2 dark:bg-pink-900/30">
            <GraduationCap
              size={18}
              className="text-pink-600 dark:text-pink-400"
            />
          </div>
        );
    }
  };

  return (
    <div
      className="
        flex
        items-start
        gap-4
        rounded-xl
        p-4
        transition-all
        duration-300
        hover:bg-slate-50
        dark:hover:bg-slate-800
      "
    >
      {/* Icon */}

      {getActivityIcon()}

      {/* Content */}

      <div className="flex-1">

        <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
          {activity.title}
        </h3>

        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          {activity.description}
        </p>

        <p className="mt-2 text-xs text-slate-400">
          {activity.time}
        </p>

      </div>
    </div>
  );
};

export default ActivityCard;