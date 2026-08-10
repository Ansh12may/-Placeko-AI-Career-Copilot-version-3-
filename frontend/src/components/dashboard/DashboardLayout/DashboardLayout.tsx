import {
  useEffect,
  useState,
  type ReactNode,
} from "react";

import Sidebar from "./Sidebar/Sidebar";
import TopBar from "./TopBar";

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout = ({
  children,
}: DashboardLayoutProps) => {

  // =========================================================
  // Dark Mode
  // =========================================================

  const [isDarkMode, setIsDarkMode] =
    useState(() => {
      const savedTheme =
        localStorage.getItem("theme");

      if (savedTheme === "dark") {
        return true;
      }

      if (savedTheme === "light") {
        return false;
      }

      return document.documentElement.classList.contains(
        "dark"
      );
    });


  // =========================================================
  // Apply Theme
  // =========================================================

  useEffect(() => {

    const root =
      document.documentElement;

    root.classList.toggle(
      "dark",
      isDarkMode
    );

    localStorage.setItem(
      "theme",
      isDarkMode
        ? "dark"
        : "light"
    );

  }, [isDarkMode]);


  // =========================================================
  // Toggle Theme
  // =========================================================

  const handleToggleDarkMode = () => {
    setIsDarkMode(
      (previous) => !previous
    );
  };


  // =========================================================
  // Layout
  // =========================================================

  return (
    <div
      className="
        flex
        h-screen
        flex-col
        overflow-hidden
        bg-slate-50
        dark:bg-slate-950
      "
    >

      {/* =====================================================
          Global Top Bar
          ===================================================== */}

      <TopBar
        isDarkMode={isDarkMode}
        onToggleDarkMode={
          handleToggleDarkMode
        }
      />


      {/* =====================================================
          Application Body
          ===================================================== */}

      <div className="flex min-h-0 flex-1">

        {/* ===================================================
            Sidebar
            =================================================== */}

        <Sidebar />


        {/* ===================================================
            Main Content
            =================================================== */}

        <main
          className="
            min-w-0
            flex-1
            overflow-y-auto
            bg-slate-50
            p-8
            dark:bg-slate-950
          "
        >

          {children}

        </main>

      </div>

    </div>
  );
};

export default DashboardLayout;