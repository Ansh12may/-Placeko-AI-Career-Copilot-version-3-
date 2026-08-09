import { motion } from "framer-motion";

const DemoHeader = () => {
  return (
    <div className="text-center space-y-4">
      <motion.span
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="
          text-xs
          font-bold
          uppercase
          tracking-[0.3em]
          text-indigo-600
          dark:text-indigo-400
        "
      >
        Interactive Preview
      </motion.span>

      <motion.h2
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="
          text-3xl
          md:text-4xl
          font-extrabold
          tracking-tight
          text-slate-900
          dark:text-white
        "
      >
        See Instant ATS Resume Compatibility
      </motion.h2>

      <motion.p
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="
          mx-auto
          max-w-2xl
          text-slate-600
          dark:text-slate-400
        "
      >
        Select a target role below to see how Placeko evaluates
        your resume, identifies missing skills, and prepares you
        for interviews.
      </motion.p>
    </div>
  );
};

export default DemoHeader;