import { TrendingDown, TrendingUp } from "lucide-react";

import type { Stat } from "./types";

interface StatCardProps {
  stat: Stat;
}

const StatCard = ({ stat }: StatCardProps) => {
  const Icon = stat.icon;

  return (
    <div
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-lg
        dark:border-slate-800
        dark:bg-slate-900
      "
    >
      {/* Header */}

      <div className="flex items-start justify-between">

        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            {stat.title}
          </p>

          <h2 className="mt-2 text-3xl font-bold text-slate-900 dark:text-white">
            {stat.value}
          </h2>
        </div>

        <div
          className={`
            ${stat.color}
            flex
            h-12
            w-12
            items-center
            justify-center
            rounded-xl
          `}
        >
          <Icon
            size={22}
            className="text-white"
          />
        </div>

      </div>

      {/* Footer */}

      <div className="mt-6 flex items-center justify-between">

        <span className="text-sm text-slate-500 dark:text-slate-400">
          Last 7 days
        </span>

        <div
          className={`
            flex
            items-center
            gap-1
            rounded-full
            px-2.5
            py-1
            text-sm
            font-semibold
            ${
              stat.trend === "up"
                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
                : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
            }
          `}
        >
          {stat.trend === "up" ? (
            <TrendingUp size={15} />
          ) : (
            <TrendingDown size={15} />
          )}

          {stat.change}
        </div>

      </div>

    </div>
  );
};

export default StatCard;