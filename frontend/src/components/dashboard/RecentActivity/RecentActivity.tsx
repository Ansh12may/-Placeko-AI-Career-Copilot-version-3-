import { ArrowRight } from "lucide-react";

import ActivityCard from "./ActivityCard";
import { activities } from "./data";

const RecentActivity = () => {
  return (
    <section className="mt-8">

      {/* Header */}

      <div className="mb-6 flex items-center justify-between">

        <div>

          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            Recent Activity
          </h2>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            Keep track of your latest career progress.
          </p>

        </div>

        <button
          className="
            flex
            items-center
            gap-2
            text-sm
            font-semibold
            text-indigo-600
            transition-colors
            hover:text-indigo-700
          "
        >
          View All

          <ArrowRight size={16} />

        </button>

      </div>

      {/* Activity List */}

      <div
        className="
          rounded-2xl
          border
          border-slate-200
          bg-white
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
        "
      >
        {activities.map((activity, index) => (
          <div
            key={activity.id}
            className={
              index !== activities.length - 1
                ? "border-b border-slate-200 dark:border-slate-800"
                : ""
            }
          >
            <ActivityCard activity={activity} />
          </div>
        ))}
      </div>

    </section>
  );
};

export default RecentActivity;