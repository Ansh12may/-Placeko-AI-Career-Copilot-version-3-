import { Award, Briefcase, FileText, Mic } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const ProfilePage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const fullName = user?.full_name || "User";

  const initials = fullName
    .split(" ")
    .map((name) => name.charAt(0))
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="space-y-6 pb-16">

      {/* Profile Hero */}

      <section
        className="
          flex
          flex-col
          gap-6
          rounded-2xl
          border
          border-slate-200
          bg-white
          p-6
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
          md:flex-row
          md:items-center
          md:justify-between
          md:p-8
        "
      >
        <div className="flex flex-col items-center gap-5 text-center sm:flex-row sm:text-left">

          {/* Avatar */}

          <div
            className="
              h-20
              w-20
              shrink-0
              overflow-hidden
              rounded-full
              bg-gradient-to-br
              from-indigo-500
              to-violet-600
              ring-4
              ring-indigo-500/20
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
                  text-2xl
                  font-bold
                  text-white
                "
              >
                {initials}
              </div>
            )}
          </div>

          {/* User Information */}

          <div className="space-y-1">

            <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">
              {fullName}
            </h1>

            <p className="text-sm font-semibold text-indigo-600 dark:text-indigo-400">
              {user?.provider === "email"
                ? "Placeko Candidate"
                : `${user?.provider} Account`}
            </p>

            <p className="text-sm text-slate-500 dark:text-slate-400">
              {user?.email}
            </p>

          </div>
        </div>

        {/* Edit */}

        <button
          type="button"
          onClick={() => navigate("/settings")}
          className="
            shrink-0
            rounded-xl
            bg-slate-900
            px-5
            py-3
            text-sm
            font-semibold
            text-white
            transition
            hover:bg-slate-800
            dark:bg-slate-100
            dark:text-slate-900
            dark:hover:bg-white
          "
        >
          Edit Profile Settings
        </button>

      </section>

      {/* Metrics */}

      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">

        <div className="rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <FileText className="mx-auto mb-2 h-5 w-5 text-indigo-500" />

          <p className="text-xs font-medium text-slate-400">
            Uploaded Resumes
          </p>

          <p className="mt-1 text-2xl font-black text-indigo-600 dark:text-indigo-400">
            0
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <Briefcase className="mx-auto mb-2 h-5 w-5 text-slate-500" />

          <p className="text-xs font-medium text-slate-400">
            Active Applications
          </p>

          <p className="mt-1 text-2xl font-black text-slate-900 dark:text-slate-100">
            0
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <Mic className="mx-auto mb-2 h-5 w-5 text-emerald-500" />

          <p className="text-xs font-medium text-slate-400">
            Mock Interviews
          </p>

          <p className="mt-1 text-2xl font-black text-emerald-600 dark:text-emerald-400">
            0
          </p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <Award className="mx-auto mb-2 h-5 w-5 text-purple-500" />

          <p className="text-xs font-medium text-slate-400">
            Average Performance
          </p>

          <p className="mt-1 text-2xl font-black text-purple-600 dark:text-purple-400">
            0%
          </p>
        </div>

      </section>

      {/* Achievements */}

      <section
        className="
          rounded-2xl
          border
          border-slate-200
          bg-white
          p-5
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
        "
      >

        <h2 className="text-sm font-bold text-slate-900 dark:text-slate-100">
          Career Milestone Achievements
        </h2>

        <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">

          <AchievementCard
            title="Resume Analysis Complete"
            date="Getting Started"
          />

          <AchievementCard
            title="First Mock Interview"
            date="Keep practicing"
          />

          <AchievementCard
            title="Career Roadmap Started"
            date="Keep learning"
          />

          <AchievementCard
            title="First Job Application"
            date="Start applying"
          />

        </div>

      </section>

    </div>
  );
};

interface AchievementCardProps {
  title: string;
  date: string;
}

const AchievementCard = ({
  title,
  date,
}: AchievementCardProps) => {
  return (
    <div
      className="
        rounded-xl
        border
        border-slate-100
        bg-slate-50
        p-4
        dark:border-slate-800
        dark:bg-slate-950/60
      "
    >
      <div
        className="
          mb-2
          flex
          h-9
          w-9
          items-center
          justify-center
          rounded-lg
          bg-indigo-50
          text-indigo-600
          dark:bg-indigo-950
          dark:text-indigo-400
        "
      >
        <Award className="h-4 w-4" />
      </div>

      <p className="text-xs font-bold text-slate-900 dark:text-slate-100">
        {title}
      </p>

      <p className="mt-1 text-[10px] text-slate-400">
        {date}
      </p>
    </div>
  );
};

export default ProfilePage;