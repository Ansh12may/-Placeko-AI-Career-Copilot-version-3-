import { motion } from "framer-motion";

const HeroContent = () => {
  return (
    <>
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.6 }}
        className="
          mt-6
          max-w-4xl
          text-4xl
          md:text-6xl
          font-extrabold
          tracking-tight
          leading-tight
          text-slate-900
          dark:text-white
        "
      >
        Land Your Dream Tech Role with{" "}
        <span className="text-indigo-600 dark:text-indigo-400">
          AI Precision
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="
          mt-6
          max-w-2xl
          text-lg
          leading-8
          text-slate-600
          dark:text-slate-400
        "
      >
        Placeko optimizes your resume for ATS filters, discovers matching
        opportunities, conducts AI-powered mock interviews, and builds a
        personalized roadmap to help you land your dream role.
      </motion.p>
    </>
  );
};

export default HeroContent;