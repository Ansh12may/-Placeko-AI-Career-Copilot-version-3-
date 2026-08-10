import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

import ActivityCard from "./ActivityCard";
import type { Activity } from "./types";

interface RecentActivityProps {
  activities: Activity[];
}

const RecentActivity = ({
  activities=[],
}: RecentActivityProps) => {
  const navigate = useNavigate();

  const displayedActivities =
    activities.slice(0, 5);

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
          type="button"
          onClick={() => navigate("/applications")}
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

        {displayedActivities.length === 0 ? (

          <div className="p-8 text-center">

            <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">
              No recent activity
            </p>

            <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
              Your resume, applications, and interviews will appear here.
            </p>

          </div>

        ) : (

          displayedActivities.map(
            (activity, index) => (

              <div
                key={activity.id}
                className={
                  index !==
                  displayedActivities.length - 1
                    ? "border-b border-slate-200 dark:border-slate-800"
                    : ""
                }
              >

                <ActivityCard
                  activity={activity}
                />

              </div>

            )
          )

        )}

      </div>

    </section>
  );
};

export default RecentActivity;