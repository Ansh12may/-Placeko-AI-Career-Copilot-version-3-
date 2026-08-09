import { motion } from "framer-motion";
import type { NavigationTab } from "../../../types/index.ts";

interface LogoProps {
  onNavigate: (tab: NavigationTab) => void;
}

const Logo =({ onNavigate }:LogoProps) => {
  return (
    <motion.button
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      onClick={() => onNavigate("landing")}
      className="flex items-center gap-3 outline-none"
    >
      {/* Logo Icon */}
      <div
        className="
          h-10
          w-10
          rounded-xl
          bg-gradient-to-br
          from-indigo-600
          to-violet-600
          flex
          items-center
          justify-center
          shadow-lg
          shadow-indigo-500/20
        "
      >
        <span className="text-white text-xl font-black italic">
          P
        </span>
      </div>

      {/* Brand */}
      <div className="flex flex-col items-start">
        <span className="text-xl font-extrabold tracking-normal text-slate-900 dark:text-white">
          Placeko
        </span>

        <span className="text-[10px] uppercase tracking-[0.25em] text-slate-500 dark:text-slate-400">
          AI Career Copilot
        </span>
      </div>
    </motion.button>
  );
};

export default Logo;

