import {
  Bell,
  Moon,
  Lock,
} from "lucide-react";

interface SettingsPageProps {
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

const SettingsPage = ({
      isDarkMode,
      onToggleDarkMode,
}:SettingsPageProps) => {
  return (
    <div className="space-y-6 pb-16">

      {/* Header */}

      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
          Account & System Preferences
        </h1>

        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Manage theme preferences, AI alerts, and security settings.
        </p>
      </div>

      {/* Appearance & Theme */}

      <section
        className="
          rounded-2xl
          border
          border-slate-200
          bg-white
          p-6
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
        "
      >
        <div className="mb-5 flex items-center gap-3">
          <Moon className="h-5 w-5 text-orange-500" />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Appearance & Theme
          </h2>
        </div>

        <div
          className="
            flex
            items-center
            justify-between
            rounded-xl
            bg-slate-50
            p-4
            dark:bg-slate-800
          "
        >
          <div>
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              Dark Mode Canvas
            </p>

            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              Low-contrast, eye-safe interface theme
            </p>
          </div>

          <button
        type="button"
        onClick={onToggleDarkMode}  
        className="
        rounded-lg
     bg-slate-900
        px-4
        py-2
        text-xs
        font-semibold
         text-white
        transition
         hover:bg-slate-800
         dark:bg-white
         dark:text-slate-900
         dark:hover:bg-slate-200
  "
>
  {isDarkMode ? "Dark Active" : "Light Active"}
</button>
        </div>
      </section>

      {/* AI Notifications */}

      <section
        className="
          rounded-2xl
          border
          border-slate-200
          bg-white
          p-6
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
        "
      >
        <div className="mb-5 flex items-center gap-3">
          <Bell className="h-5 w-5 text-indigo-500" />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            AI Notifications & Alerts
          </h2>
        </div>

        <div className="space-y-3">

          <PreferenceRow
            title="Recommended Job Alerts"
            description="Notify when new 90%+ match roles appear"
          />

          <PreferenceRow
            title="ATS Score Re-evaluation"
            description="Alert when AI keyword suggestions update"
          />

          <PreferenceRow
            title="Interview Reminders"
            description="Alert before scheduled technical mock interviews"
          />

        </div>
      </section>

      {/* Security */}

      <section
        className="
          rounded-2xl
          border
          border-slate-200
          bg-white
          p-6
          shadow-sm
          dark:border-slate-800
          dark:bg-slate-900
        "
      >
        <div className="mb-5 flex items-center gap-3">
          <Lock className="h-5 w-5 text-emerald-500" />

          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            Security
          </h2>
        </div>

        <div
          className="
            flex
            items-center
            justify-between
            rounded-xl
            bg-slate-50
            p-4
            dark:bg-slate-800
          "
        >
          <div>
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              Password
            </p>

            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
              Keep your Placeko account secure.
            </p>
          </div>

          <button
            type="button"
            className="
              rounded-lg
              border
              border-slate-200
              px-4
              py-2
              text-xs
              font-semibold
              text-slate-700
              hover:bg-white
              dark:border-slate-700
              dark:text-slate-200
              dark:hover:bg-slate-700
            "
          >
            Change Password
          </button>
        </div>
      </section>

      {/* Save */}

      <button
        type="button"
        className="
          rounded-xl
          bg-indigo-600
          px-6
          py-3
          text-sm
          font-semibold
          text-white
          shadow-sm
          transition
          hover:bg-indigo-700
        "
      >
        Save Preferences
      </button>
    </div>
  );
};

interface PreferenceRowProps {
  title: string;
  description: string;
}

const PreferenceRow = ({
  title,
  description,
}: PreferenceRowProps) => {
  return (
    <label
      className="
        flex
        cursor-pointer
        items-center
        justify-between
        rounded-xl
        bg-slate-50
        p-4
        dark:bg-slate-800
      "
    >
      <div>
        <p className="text-sm font-semibold text-slate-900 dark:text-white">
          {title}
        </p>

        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
          {description}
        </p>
      </div>

      <input
        type="checkbox"
        defaultChecked
        className="h-4 w-4 accent-indigo-600"
      />
    </label>
  );
};

export default SettingsPage;