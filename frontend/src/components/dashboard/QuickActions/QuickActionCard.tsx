import { ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

import type { QuickAction } from "./types";

interface QuickActionCardProps {
  action: QuickAction;
}

const QuickActionCard = ({
  action,
}: QuickActionCardProps) => {
  const navigate = useNavigate();

  if (!action) {
    console.error("QuickActionCard: action is undefined");
    return null;
  }

  const Icon = action.icon;

  return (
    <button
      type="button"
      onClick={() => navigate(action.route)}
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
        hover:border-indigo-200
        hover:shadow-lg
        dark:border-slate-800
        dark:bg-slate-900
        dark:hover:border-indigo-800
      "
    >
      <div className="flex items-center gap-4">

        <div
          className={`
            ${action.color}
            flex
            h-14
            w-14
            shrink-0
            items-center
            justify-center
            rounded-xl
            shadow-md
            transition-transform
            duration-300
            group-hover:scale-105
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

      <ArrowRight
        size={22}
        className="
          shrink-0
          text-slate-400
          transition-transform
          duration-300
          group-hover:translate-x-1
          group-hover:text-indigo-600
        "
      />
    </button>
  );
};

export default QuickActionCard;