import { ArrowRight } from "lucide-react";

import type { QuickAction } from "./types";

interface QuickActionCardProps {
  action: QuickAction;
}

const QuickActionCard = ({ action }: QuickActionCardProps) => {
  const Icon = action.icon;

  return (
    <button
      className="
        group
        flex
        w-full
        items-center
        justify-between
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        text-left
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-1
        hover:shadow-lg
        dark:border-slate-800
        dark:bg-slate-900
      "
    >
      {/* Left */}

      <div className="flex items-center gap-4">

        <div
          className={`
            ${action.color}
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-xl
            shadow-md
          `}
        >
          <Icon
            size={26}
            className="text-white"
          />
        </div>

        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
            {action.title}
          </h3>

          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            {action.description}
          </p>
        </div>

      </div>

      {/* Right */}

      <ArrowRight
        size={22}
        className="
          text-slate-400
          transition-transform
          duration-300
          group-hover:translate-x-1
        "
      />

    </button>
  );
};

export default QuickActionCard;