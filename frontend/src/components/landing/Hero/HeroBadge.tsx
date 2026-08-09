import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

const HeroBadge = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="
        inline-flex
        items-center
        gap-2
        px-4
        py-2
        rounded-full
        bg-indigo-50
        dark:bg-indigo-950/70
        border
        border-indigo-200
        dark:border-indigo-800
      "
    >
      <Sparkles className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />

      <span
        className="
          text-xs
          font-bold
          uppercase
          tracking-widest
          text-indigo-700
          dark:text-indigo-300
        "
      >
        AI Career Copilot
      </span>
    </motion.div>
  );
};

export default HeroBadge;