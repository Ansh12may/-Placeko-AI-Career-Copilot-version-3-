import React from "react";
import { motion } from "framer-motion";
import type { NavigationTab } from "../../../types/index.ts";

import Logo from "./Logo";
import NavLinks from "./NavLinks";
import ThemeToggle from "./ThemeToggle";
import AuthButtons from "./AuthButtons";

interface LandingNavbarProps {
  onNavigate: (tab: NavigationTab) => void;
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

const LandingNavbar: React.FC<LandingNavbarProps> = ({
  onNavigate,
  isDarkMode,
  onToggleDarkMode,
}) => {
  return (
    <motion.header
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="sticky top-0 z-50 w-full h-16
                 bg-white/80 dark:bg-slate-950/80
                 backdrop-blur-md
                 border-b border-slate-200/80
                 dark:border-slate-800/80"
    >
      <div className="max-w-7xl mx-auto h-full px-6 flex items-center justify-between">

        {/* Left Section */}
        <Logo onNavigate={onNavigate} />

        {/* Center Section */}
        <NavLinks />

        {/* Right Section */}
        <div className="flex items-center gap-3">

          <ThemeToggle
            isDarkMode={isDarkMode}
            onToggleDarkMode={onToggleDarkMode}
          />

          <AuthButtons
            onNavigate={onNavigate}
          />

        </div>

      </div>
    </motion.header>
  );
};

export default LandingNavbar;