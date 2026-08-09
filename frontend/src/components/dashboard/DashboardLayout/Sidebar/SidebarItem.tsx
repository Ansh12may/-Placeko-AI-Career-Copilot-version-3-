import type { LucideIcon } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";

interface SidebarItemProps {
  icon: LucideIcon;
  label: string;
  path: string;
  badge?: number;
}

const SidebarItem = ({
  icon: Icon,
  label,
  path,
  badge,
}: SidebarItemProps) => {
  const navigate = useNavigate();
  const location = useLocation();

  const active =
  path === "/interview"
    ? location.pathname === "/interview" ||
      (
        location.pathname.startsWith("/interview/") &&
        !location.pathname.startsWith("/interview/history")
      )
    : location.pathname === path ||
      (path !== "/dashboard" &&
        location.pathname.startsWith(`${path}/`));

  return (
    <button
      type="button"
      onClick={() => navigate(path)}
      className={`
        flex
        w-full
        items-center
        gap-2.5
        rounded-lg
        px-3
        py-2
        text-left
        text-sm
        transition-all
        duration-200

        ${
          active
            ? "bg-indigo-600 text-white shadow-sm"
            : "text-slate-600 hover:bg-slate-100 hover:text-indigo-600 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-indigo-400"
        }
      `}
    >
      <Icon className="h-4 w-4 shrink-0" />

      <span className="font-medium">
        {label}
      </span>

      {badge !== undefined && (
        <span
          className={`
            ml-auto
            rounded-full
            px-1.5
            py-0.5
            text-[9px]
            font-semibold

            ${
              active
                ? "bg-white/20 text-white"
                : "bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400"
            }
          `}
        >
          {badge}
        </span>
      )}
    </button>
  );
};

export default SidebarItem;