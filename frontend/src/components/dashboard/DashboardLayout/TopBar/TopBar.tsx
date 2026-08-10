import {
  Bell,
  ChevronDown,
  Moon,
  Search,
  Upload,
  Sun,
  X,
  CheckCircle2,
  User,
  Settings,
  Sparkles,
  LogOut,
} from "lucide-react";

import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  useNavigate,
} from "react-router-dom";

import { useAuth } from "../../../../context/AuthContext";

import {
  getResumes,
  uploadResume,
} from "../../../../api/resume";

import type {
  ResumeLibraryItem,
} from "../../../../types/resume";



// =========================================================
// Props
// =========================================================

interface TopBarProps {
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}


// =========================================================
// Component
// =========================================================

const TopBar = ({
  isDarkMode,
  onToggleDarkMode,
}: TopBarProps) => {

  const {
    user,
    logout,
  } = useAuth();

  const navigate = useNavigate();


  // =========================================================
  // Refs
  // =========================================================

  const fileInputRef =
    useRef<HTMLInputElement | null>(null);

  const searchInputRef =
    useRef<HTMLInputElement | null>(null);

  const profileMenuRef =
    useRef<HTMLDivElement | null>(null);


  // =========================================================
  // State
  // =========================================================

  const [isUploading, setIsUploading] =
    useState(false);

  const [uploadError, setUploadError] =
    useState<string | null>(null);

  const [activeResume, setActiveResume] =
    useState<ResumeLibraryItem | null>(null);

  const [isResumeMenuOpen, setIsResumeMenuOpen] =
    useState(false);

  const [isNotificationsOpen, setIsNotificationsOpen] =
    useState(false);

  const [isProfileMenuOpen, setIsProfileMenuOpen] =
    useState(false);

  const [searchQuery, setSearchQuery] =
    useState("");


  // =========================================================
  // User
  // =========================================================

  const fullName =
    user?.full_name || "User";

  const email =
    user?.email || "";


  const initials =
    fullName
      .split(" ")
      .filter(Boolean)
      .map(
        (name) =>
          name.charAt(0)
      )
      .join("")
      .slice(0, 2)
      .toUpperCase();

  // =========================================================
  // Load Active Resume
  // =========================================================

  const loadActiveResume = async () => {

    try {

      const response =
        await getResumes();

      const active =
        response.data.find(
          (resume) =>
            resume.is_active
        ) ?? null;

      setActiveResume(active);

    } catch (error) {

      console.error(
        "Failed to load active resume:",
        error
      );

    }

  };


  useEffect(() => {

    loadActiveResume();

  }, []);


  // =========================================================
  // Keyboard Shortcuts
  // =========================================================

  useEffect(() => {

    const handleKeyboard = (
      event: KeyboardEvent
    ) => {

      // Cmd + K / Ctrl + K
      if (
        (event.metaKey ||
          event.ctrlKey) &&
        event.key.toLowerCase() === "k"
      ) {

        event.preventDefault();

        searchInputRef.current?.focus();

      }


      // Escape
      if (
        event.key === "Escape"
      ) {

        setIsNotificationsOpen(
          false
        );

        setIsResumeMenuOpen(
          false
        );

        setIsProfileMenuOpen(
          false
        );

      }

    };


    window.addEventListener(
      "keydown",
      handleKeyboard
    );


    return () => {

      window.removeEventListener(
        "keydown",
        handleKeyboard
      );

    };

  }, []);


  // =========================================================
  // Close Profile Menu When Clicking Outside
  // =========================================================

  useEffect(() => {

    const handleClickOutside = (
      event: MouseEvent
    ) => {

      if (
        profileMenuRef.current &&
        !profileMenuRef.current.contains(
          event.target as Node
        )
      ) {

        setIsProfileMenuOpen(
          false
        );

      }

    };


    document.addEventListener(
      "mousedown",
      handleClickOutside
    );


    return () => {

      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );

    };

  }, []);


  // =========================================================
  // Search
  // =========================================================

  const handleSearchKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {

    if (
      event.key !== "Enter"
    ) {

      return;

    }


    const query =
      searchQuery
        .trim()
        .toLowerCase();


    if (!query) {

      return;

    }


    if (
      query.includes("resume") ||
      query.includes("cv")
    ) {

      navigate("/resume");

    } else if (
      query.includes("job")
    ) {

      navigate("/jobs");

    } else if (
      query.includes("application")
    ) {

      navigate("/applications");

    } else if (
      query.includes("interview")
    ) {

      navigate("/interview");

    } else if (
      query.includes("history")
    ) {

      navigate(
        "/interview/history"
      );

    } else if (
      query.includes("profile")
    ) {

      navigate("/profile");

    } else if (
      query.includes("setting")
    ) {

      navigate("/settings");

    } else if (
      query.includes("dashboard")
    ) {

      navigate("/dashboard");

    }


    setSearchQuery("");

  };


  // =========================================================
  // Upload Resume
  // =========================================================

  const handleUploadClick = () => {

    if (isUploading) {

      return;

    }


    setUploadError(null);

    fileInputRef.current?.click();

  };


  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    const file =
      event.target.files?.[0];


    // Allow selecting same file again
    event.target.value = "";


    if (!file) {

      return;

    }


    // -------------------------------------------------------
    // Validate file type
    // -------------------------------------------------------

    if (
      file.type !== "application/pdf" &&
      !file.name
        .toLowerCase()
        .endsWith(".pdf")
    ) {

      setUploadError(
        "Only PDF resumes are supported."
      );

      return;

    }


    // -------------------------------------------------------
    // Validate file size
    // -------------------------------------------------------

    const maxFileSize =
      5 * 1024 * 1024;


    if (
      file.size > maxFileSize
    ) {

      setUploadError(
        "Resume must be smaller than 5 MB."
      );

      return;

    }


    // -------------------------------------------------------
    // Upload
    // -------------------------------------------------------

    try {

      setIsUploading(true);

      setUploadError(null);


      console.log(
        "Uploading resume:",
        file.name
      );


      const response =
        await uploadResume(file);


      console.log(
        "Resume upload response:",
        response
      );


      // Refresh active resume
      await loadActiveResume();


      // -----------------------------------------------------
      // Resolve returned resume ID
      // -----------------------------------------------------

      const responseData =
        response?.data as
          | {
              resume_id?: string;
              id?: string;
            }
          | undefined;


      const resumeId =
        responseData?.resume_id ??
        responseData?.id;


      // -----------------------------------------------------
      // Navigate
      // -----------------------------------------------------

      if (resumeId) {

        navigate(
          `/resume-analysis/${resumeId}`
        );

      } else {

        console.warn(
          "Resume uploaded successfully, but no resume ID was returned."
        );

        navigate("/resume");

      }

    } catch (error) {

      console.error(
        "Resume upload failed:",
        error
      );


      setUploadError(
        error instanceof Error
          ? error.message
          : "Unable to upload your resume. Please try again."
      );

    } finally {

      setIsUploading(false);

    }

  };


  // =========================================================
  // Resume Dropdown
  // =========================================================

  const handleResumeClick = () => {

    setIsResumeMenuOpen(
      (previous) => !previous
    );

    setIsNotificationsOpen(false);

    setIsProfileMenuOpen(false);

  };


  // =========================================================
  // Notification
  // =========================================================

  const handleNotificationClick = () => {

    setIsNotificationsOpen(
      (previous) => !previous
    );

    setIsResumeMenuOpen(false);

    setIsProfileMenuOpen(false);

  };


  // =========================================================
  // Profile Menu
  // =========================================================

  const handleProfileClick = () => {

    setIsProfileMenuOpen(
      (previous) => !previous
    );

    setIsNotificationsOpen(false);

    setIsResumeMenuOpen(false);

  };


  // =========================================================
  // Profile Navigation
  // =========================================================

  const handleProfileNavigation = (
    path: string
  ) => {

    setIsProfileMenuOpen(false);

    navigate(path);

  };


  // =========================================================
  // Logout
  // =========================================================

  const handleLogout = async () => {

    setIsProfileMenuOpen(false);

    await logout();

    navigate("/login");

  };


  // =========================================================
  // Safe ATS Score
  // =========================================================

  const atsScore =
    activeResume?.ats_score;


  const formattedAtsScore =
    typeof atsScore === "number" &&
    Number.isFinite(atsScore)
      ? Math.round(atsScore)
      : null;


  // =========================================================
  // Render
  // =========================================================

  return (

    <header
      className="
        relative
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

      {/* =====================================================
          LEFT SIDE
          ===================================================== */}

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
            ref={searchInputRef}
            type="text"
            value={searchQuery}
            onChange={(event) =>
              setSearchQuery(
                event.target.value
              )
            }
            onKeyDown={
              handleSearchKeyDown
            }
            placeholder="Search or jump to..."
            className="
              h-10
              w-64
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

        <div className="relative hidden md:block">

          <button
            type="button"
            onClick={handleResumeClick}
            className="
              flex
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
              dark:border-indigo-900
              dark:bg-indigo-950
              dark:text-indigo-300
            "
          >

            <span
              className="
                flex
                h-6
                w-6
                items-center
                justify-center
                rounded-md
                bg-white
                text-indigo-600
                dark:bg-indigo-900
              "
            >
              <Search
                className="h-3.5 w-3.5"
              />
            </span>


            <span className="max-w-[200px] truncate">

              {activeResume?.file_name ||
                "No active resume"}

            </span>


            {formattedAtsScore !== null && (

              <span
                className="
                  rounded-full
                  bg-indigo-600
                  px-2
                  py-0.5
                  text-[10px]
                  font-bold
                  text-white
                "
              >
                ATS {formattedAtsScore}
              </span>

            )}


            <ChevronDown
              className="
                h-4
                w-4
                shrink-0
                text-indigo-500
              "
            />

          </button>


          {/* Resume Dropdown */}

          {isResumeMenuOpen && (

            <div
              className="
                absolute
                left-0
                top-12
                z-[100]
                w-72
                rounded-2xl
                border
                border-slate-200
                bg-white
                p-2
                shadow-xl
                dark:border-slate-700
                dark:bg-slate-900
              "
            >

              <button
                type="button"
                onClick={() => {

                  setIsResumeMenuOpen(false);

                  navigate("/resume");

                }}
                className="
                  flex
                  w-full
                  items-center
                  gap-3
                  rounded-xl
                  px-3
                  py-3
                  text-left
                  text-sm
                  font-semibold
                  text-slate-700
                  hover:bg-slate-50
                  dark:text-slate-200
                  dark:hover:bg-slate-800
                "
              >

                <Search
                  className="
                    h-4
                    w-4
                    text-indigo-500
                  "
                />

                Open Resume Library

              </button>


              {activeResume && (

                <button
                  type="button"
                  onClick={() => {

                    setIsResumeMenuOpen(false);

                    navigate(
                      `/resume-analysis/${activeResume.id}`
                    );

                  }}
                  className="
                    flex
                    w-full
                    items-center
                    gap-3
                    rounded-xl
                    px-3
                    py-3
                    text-left
                    text-sm
                    font-semibold
                    text-slate-700
                    hover:bg-slate-50
                    dark:text-slate-200
                    dark:hover:bg-slate-800
                  "
                >

                  <CheckCircle2
                    className="
                      h-4
                      w-4
                      text-emerald-500
                    "
                  />

                  View Active Resume Analysis

                </button>

              )}

            </div>

          )}

        </div>

      </div>


      {/* =====================================================
          RIGHT SIDE
          ===================================================== */}

      <div className="flex items-center gap-3">

        {/* Hidden file input */}

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          className="hidden"
        />


        {/* Upload Resume */}

        <button
          type="button"
          onClick={handleUploadClick}
          disabled={isUploading}
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
            disabled:cursor-not-allowed
            disabled:opacity-60
            sm:flex
            dark:bg-white
            dark:text-slate-900
            dark:hover:bg-slate-200
          "
        >

          <Upload className="h-4 w-4" />

          {isUploading
            ? "Uploading..."
            : "Upload Resume"}

        </button>


        {/* Upload Error */}

        {uploadError && (

          <div
            className="
              fixed
              right-6
              top-20
              z-[200]
              flex
              max-w-sm
              items-start
              gap-3
              rounded-xl
              border
              border-red-200
              bg-red-50
              px-4
              py-3
              text-sm
              font-medium
              text-red-600
              shadow-lg
              dark:border-red-900
              dark:bg-red-950
            "
          >

            <span>
              {uploadError}
            </span>

            <button
              type="button"
              onClick={() =>
                setUploadError(null)
              }
              className="shrink-0"
            >

              <X className="h-4 w-4" />

            </button>

          </div>

        )}


        {/* Notifications */}

        <div className="relative">

          <button
            type="button"
            onClick={
              handleNotificationClick
            }
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


          {isNotificationsOpen && (

            <div
              className="
                absolute
                right-0
                top-12
                z-[100]
                w-80
                rounded-2xl
                border
                border-slate-200
                bg-white
                p-4
                shadow-xl
                dark:border-slate-700
                dark:bg-slate-900
              "
            >

              <div className="flex items-center justify-between">

                <h3
                  className="
                    text-sm
                    font-bold
                    text-slate-900
                    dark:text-white
                  "
                >
                  Notifications
                </h3>

                <button
                  type="button"
                  onClick={() =>
                    setIsNotificationsOpen(false)
                  }
                  className="
                    text-slate-400
                    hover:text-slate-600
                  "
                >

                  <X className="h-4 w-4" />

                </button>

              </div>


              <div
                className="
                  mt-4
                  rounded-xl
                  bg-slate-50
                  p-4
                  dark:bg-slate-800
                "
              >

                <p
                  className="
                    text-sm
                    font-semibold
                    text-slate-700
                    dark:text-slate-200
                  "
                >
                  No new notifications
                </p>

                <p
                  className="
                    mt-1
                    text-xs
                    leading-5
                    text-slate-500
                    dark:text-slate-400
                  "
                >
                  New job matches, resume updates and
                  interview reminders will appear here.
                </p>

              </div>

            </div>

          )}

        </div>


        {/* Theme */}

        <button
          type="button"
          onClick={
            onToggleDarkMode
          }
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

          {isDarkMode ? (
            <Sun className="h-4 w-4" />
          ) : (
            <Moon className="h-4 w-4" />
          )}

          {isDarkMode
            ? "Light"
            : "Dark"}

        </button>


        {/* =================================================
            PROFILE / ACCOUNT DROPDOWN
            ================================================= */}

        <div
          ref={profileMenuRef}
          className="relative"
        >

          {/* Avatar */}

          <button
            type="button"
            onClick={handleProfileClick}
            className="
              flex
              items-center
              rounded-xl
              p-1
              transition
              hover:bg-slate-100
              dark:hover:bg-slate-800
            "
            title="Account"
            aria-label="Open account menu"
            aria-expanded={
              isProfileMenuOpen
            }
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

      referrerPolicy="no-referrer"

      onLoad={() => {

        console.log("Google avatar loaded successfully");

      }}

      onError={(error) => {

        console.error("Google avatar failed to load:", error);

      }}

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


          {/* Account Dropdown */}

          {isProfileMenuOpen && (

            <div
              className="
                absolute
                right-0
                top-12
                z-[200]
                w-72
                overflow-hidden
                rounded-2xl
                border
                border-slate-200
                bg-white
                shadow-2xl
                dark:border-slate-700
                dark:bg-slate-900
              "
            >

              {/* User Header */}

              <div
                className="
                  border-b
                  border-slate-100
                  px-4
                  py-4
                  dark:border-slate-800
                "
              >

                <div className="flex items-center gap-3">

                  <div
                    className="
                      h-10
                      w-10
                      shrink-0
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
                        className="
                          h-full
                          w-full
                          object-cover
                        "
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


                  <div className="min-w-0">

                    <p
                      className="
                        truncate
                        text-sm
                        font-bold
                        text-slate-900
                        dark:text-white
                      "
                    >
                      {fullName}
                    </p>

                    <p
                      className="
                        truncate
                        text-xs
                        text-slate-400
                        dark:text-slate-500
                      "
                    >
                      {email}
                    </p>

                  </div>

                </div>

              </div>


              {/* Navigation */}

              <div className="p-2">

                {/* View Profile */}

                <button
                  type="button"
                  onClick={() =>
                    handleProfileNavigation(
                      "/profile"
                    )
                  }
                  className="
                    flex
                    w-full
                    items-center
                    gap-3
                    rounded-xl
                    px-3
                    py-3
                    text-left
                    text-sm
                    font-medium
                    text-slate-700
                    transition
                    hover:bg-slate-50
                    dark:text-slate-200
                    dark:hover:bg-slate-800
                  "
                >

                  <User
                    className="
                      h-4
                      w-4
                      text-slate-500
                    "
                  />

                  View Profile

                </button>


                {/* Account Settings */}

                <button
                  type="button"
                  onClick={() =>
                    handleProfileNavigation(
                      "/settings"
                    )
                  }
                  className="
                    flex
                    w-full
                    items-center
                    gap-3
                    rounded-xl
                    px-3
                    py-3
                    text-left
                    text-sm
                    font-medium
                    text-slate-700
                    transition
                    hover:bg-slate-50
                    dark:text-slate-200
                    dark:hover:bg-slate-800
                  "
                >

                  <Settings
                    className="
                      h-4
                      w-4
                      text-slate-500
                    "
                  />

                  Account Settings

                </button>


                {/* Visit Landing Page */}

                <button
                  type="button"
                  onClick={() =>
                    handleProfileNavigation(
                      "/"
                    )
                  }
                  className="
                    flex
                    w-full
                    items-center
                    gap-3
                    rounded-xl
                    px-3
                    py-3
                    text-left
                    text-sm
                    font-medium
                    text-slate-700
                    transition
                    hover:bg-slate-50
                    dark:text-slate-200
                    dark:hover:bg-slate-800
                  "
                >

                  <Sparkles
                    className="
                      h-4
                      w-4
                      text-indigo-500
                    "
                  />

                  Visit Landing Page

                </button>

              </div>


              {/* Logout */}

              <div
                className="
                  border-t
                  border-slate-100
                  p-2
                  dark:border-slate-800
                "
              >

                <button
                  type="button"
                  onClick={handleLogout}
                  className="
                    flex
                    w-full
                    items-center
                    gap-3
                    rounded-xl
                    px-3
                    py-3
                    text-left
                    text-sm
                    font-medium
                    text-red-600
                    transition
                    hover:bg-red-50
                    dark:text-red-400
                    dark:hover:bg-red-950
                  "
                >

                  <LogOut
                    className="
                      h-4
                      w-4
                    "
                  />

                  Log Out

                </button>

              </div>

            </div>

          )}

        </div>

      </div>

    </header>

  );
};


export default TopBar;