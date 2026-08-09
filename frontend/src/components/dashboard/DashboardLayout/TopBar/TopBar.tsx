import {
  Bell,
  ChevronDown,
  Moon,
  Search,
  Upload,
} from "lucide-react";

import { useAuth } from "../../../../context/AuthContext";

const TopBar = () => {
  const { user } = useAuth();

  const fullName = user?.full_name || "User";

  const initials = fullName
    .split(" ")
    .map((name) => name.charAt(0))
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <header
      className="
        z-50
        flex
        h-16
        shrink-0
        items-center
        justify-between
        border-b
        border-slate-200
        bg-white
        px-6
        dark:border-slate-800
        dark:bg-slate-900
      "
    >
      {/* LEFT SIDE */}

      <div className="flex items-center gap-3">

        {/* Search */}

        <div className="relative hidden md:block">
          <Search
            className="
              absolute
              left-3
              top-1/2
              h-4
              w-4
              -translate-y-1/2
              text-slate-400
            "
          />

          <input
            type="text"
            placeholder="Search or jump to..."
            className="
              h-10
              w-52
              rounded-xl
              border
              border-slate-200
              bg-slate-50
              pl-9
              pr-12
              text-sm
              text-slate-700
              outline-none
              transition
              focus:border-indigo-500
              focus:ring-2
              focus:ring-indigo-100
              dark:border-slate-700
              dark:bg-slate-800
              dark:text-white
            "
          />

          <span
            className="
              absolute
              right-2
              top-1/2
              -translate-y-1/2
              rounded-md
              border
              border-slate-200
              bg-white
              px-1.5
              py-0.5
              text-[10px]
              font-medium
              text-slate-400
              dark:border-slate-700
              dark:bg-slate-700
            "
          >
            ⌘K
          </span>
        </div>

        {/* Active Resume */}

        <button
          type="button"
          className="
            hidden
            h-10
            max-w-[340px]
            items-center
            gap-2
            rounded-xl
            border
            border-indigo-100
            bg-indigo-50
            px-3
            text-sm
            font-semibold
            text-indigo-900
            transition
            hover:bg-indigo-100
            md:flex
            dark:border-indigo-900
            dark:bg-indigo-950
            dark:text-indigo-300
          "
        >
          <span className="flex h-6 w-6 items-center justify-center rounded-md bg-white text-indigo-600 dark:bg-indigo-900">
            <Search className="h-3.5 w-3.5" />
          </span>

          <span className="truncate">
            Senior Full-Stack Engineer Resume
          </span>

          <span className="rounded-full bg-indigo-600 px-2 py-0.5 text-[10px] font-bold text-white">
            ATS 88
          </span>

          <ChevronDown className="h-4 w-4 shrink-0 text-indigo-500" />
        </button>
      </div>

      {/* RIGHT SIDE */}

      <div className="flex items-center gap-3">

        {/* Upload Resume */}

        <button
          type="button"
          className="
            hidden
            items-center
            gap-2
            rounded-xl
            bg-slate-900
            px-4
            py-2.5
            text-sm
            font-semibold
            text-white
            transition
            hover:bg-slate-800
            sm:flex
            dark:bg-white
            dark:text-slate-900
            dark:hover:bg-slate-200
          "
        >
          <Upload className="h-4 w-4" />
          Upload Resume
        </button>

        {/* Notifications */}

        <button
          type="button"
          className="
            relative
            rounded-xl
            p-2.5
            text-slate-600
            transition
            hover:bg-slate-100
            dark:text-slate-300
            dark:hover:bg-slate-800
          "
        >
          <Bell className="h-5 w-5" />

          <span
            className="
              absolute
              right-1.5
              top-1.5
              h-2
              w-2
              rounded-full
              bg-indigo-500
            "
          />
        </button>

        {/* Theme */}

        <button
          type="button"
          className="
            hidden
            items-center
            gap-2
            rounded-xl
            border
            border-slate-200
            px-3
            py-2
            text-sm
            font-medium
            text-slate-700
            transition
            hover:bg-slate-50
            sm:flex
            dark:border-slate-700
            dark:text-slate-300
            dark:hover:bg-slate-800
          "
        >
          <Moon className="h-4 w-4" />
          Dark
        </button>

        {/* Profile */}

        <button
          type="button"
          className="
            flex
            items-center
            rounded-xl
            p-1
            transition
            hover:bg-slate-100
            dark:hover:bg-slate-800
          "
        >
          <div
            className="
              h-9
              w-9
              overflow-hidden
              rounded-full
              bg-gradient-to-br
              from-indigo-600
              to-violet-600
            "
          >
            {user?.avatar ? (
              <img
                src={user.avatar}
                alt={fullName}
                className="h-full w-full object-cover"
              />
            ) : (
              <div
                className="
                  flex
                  h-full
                  w-full
                  items-center
                  justify-center
                  text-xs
                  font-bold
                  text-white
                "
              >
                {initials}
              </div>
            )}
          </div>
        </button>
      </div>
    </header>
  );
};

export default TopBar;