
import { motion } from "framer-motion";
import { Moon, Sun } from "lucide-react";

interface ThemeToggleProps {
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

const ThemeToggle = ({isDarkMode,onToggleDarkMode}:ThemeToggleProps) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onToggleDarkMode}
      title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
      className="
        flex
        items-center
        justify-center
        w-10
        h-10
        rounded-xl
        bg-slate-100
        dark:bg-slate-800
        border
        border-slate-200
        dark:border-slate-700
        text-slate-700
        dark:text-slate-200
        hover:bg-slate-200
        dark:hover:bg-slate-700
        transition-all
        duration-200
      "
    >
      {isDarkMode ? (
        <Sun className="w-5 h-5 text-amber-400" />
      ) : (
        <Moon className="w-5 h-5" />
      )}
    </motion.button>
  );
};

export default ThemeToggle;