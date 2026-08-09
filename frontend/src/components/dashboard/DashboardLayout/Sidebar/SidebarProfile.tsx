import { ChevronRight, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../../../context/AuthContext";

const SidebarProfile = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate("/auth", { replace: true });
  };

  const fullName = user?.full_name || "User";
  const email = user?.email || "";

  const initials = fullName
    .split(" ")
    .map((name) => name.charAt(0))
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div
      className="
        border-t
        border-slate-200
        p-3
        dark:border-slate-800
      "
    >
      {/* Profile */}

      <button
        type="button"
        onClick={() => navigate("/profile")}
        className="
          flex
          w-full
          items-center
          gap-2.5
          rounded-lg
          p-2
          transition
          duration-200
          hover:bg-slate-100
          dark:hover:bg-slate-800
        "
      >
        {/* Avatar */}

        <div
          className="
            flex
            h-9
            w-9
            shrink-0
            items-center
            justify-center
            overflow-hidden
            rounded-full
            bg-gradient-to-br
            from-indigo-500
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
            <span className="text-xs font-bold text-white">
              {initials}
            </span>
          )}
        </div>

        {/* User Info */}

        <div className="min-w-0 flex-1 text-left">
          <h3
            className="
              truncate
              text-sm
              font-semibold
              text-slate-900
              dark:text-white
            "
          >
            {fullName}
          </h3>

          <p
            className="
              truncate
              text-[11px]
              text-slate-400
              dark:text-slate-500
            "
          >
            {email}
          </p>
        </div>

        {/* Arrow */}

        <ChevronRight
          className="
            h-4
            w-4
            shrink-0
            text-slate-400
          "
        />
      </button>

      {/* Logout */}

      <button
        type="button"
        onClick={handleLogout}
        className="
          mt-1
          flex
          w-full
          items-center
          gap-2.5
          rounded-lg
          px-2
          py-2
          text-xs
          font-medium
          text-slate-500
          transition
          duration-200
          hover:bg-red-50
          hover:text-red-600
          dark:text-slate-400
          dark:hover:bg-red-950/30
          dark:hover:text-red-400
        "
      >
        <LogOut className="h-4 w-4" />

        Logout
      </button>
    </div>
  );
};

export default SidebarProfile;