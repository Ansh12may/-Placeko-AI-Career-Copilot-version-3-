import { motion } from "framer-motion";
import type { NavigationTab } from "../../../types/index.ts";

interface LogoProps {
  onNavigate: (tab: NavigationTab) => void;
}

const Logo = ({ onNavigate }: LogoProps) => {
  const handleLogoClick = () => {
    onNavigate("landing");

    // Return to the top of the landing page
    window.history.replaceState(null, "", "/");
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  return (
    <motion.button
      type="button"
      whileHover={{ scale: 1.03 }}
      whileTap={{ scale: 0.97 }}
      onClick={handleLogoClick}
      className="flex items-center gap-3 outline-none"
    >
      {/* Logo Icon */}

      <div
        className="
          flex
          h-10
          w-10
          items-center
          justify-center
          rounded-xl
          bg-gradient-to-br
          from-indigo-600
          to-violet-600
          shadow-lg
          shadow-indigo-500/20
        "
      >
        <span className="text-xl font-black italic text-white">
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