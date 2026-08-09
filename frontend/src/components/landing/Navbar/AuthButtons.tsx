
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import  type { NavigationTab }  from "../../../types/index.ts";

interface AuthButtonsProps {
  onNavigate: (tab: NavigationTab) => void;
}

const AuthButtons = ({ onNavigate }:AuthButtonsProps) => {
  return (
    <div className="flex items-center gap-3">

      {/* Sign In Button */}
      <motion.button
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.97 }}
        onClick={() => onNavigate("auth")}
        className="
          hidden
          sm:flex
          items-center
          justify-center
          px-4
          py-2
          rounded-lg
          text-sm
          font-semibold
          text-slate-700
          dark:text-slate-300
          hover:text-indigo-600
          dark:hover:text-indigo-400
          transition-colors
        "
      >
        Sign In
      </motion.button>

      {/* Get Started Button */}
      <motion.button
        whileHover={{
          scale: 1.03,
          y: -1,
        }}
        whileTap={{ scale: 0.97 }}
        onClick={() => onNavigate("auth")}
        className="
          flex
          items-center
          gap-2
          px-5
          py-2.5
          rounded-xl
          bg-gradient-to-r
          from-indigo-600
          to-violet-600
          hover:from-indigo-500
          hover:to-violet-500
          text-white
          text-sm
          font-bold
          shadow-lg
          shadow-indigo-600/25
          transition-all
        "
      >
        <span>Get Started</span>

        <ArrowRight
          size={16}
          className="transition-transform group-hover:translate-x-1"
        />
      </motion.button>

    </div>
  );
};

export default AuthButtons;