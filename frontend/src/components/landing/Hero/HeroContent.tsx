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
          max-w-5xl
          text-4xl
          md:text-6xl
          lg:text-7xl
          font-extrabold
          tracking-tight
          leading-[1.05]
          text-slate-900
          dark:text-white
        "
      >
       From Resume to Interview
        <br />
        <span className="text-indigo-600 dark:text-indigo-400">
        Powered by AI
        </span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="
          mt-6
          max-w-3xl
          text-lg
          md:text-xl
          leading-8
          text-slate-600
          dark:text-slate-400
        "
      >
        Placeko turns your resume into career intelligence —
        combining AI-powered resume analysis, semantic job matching,
        personalized interview preparation, and application tracking
        in one platform.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        className="
          mt-6
          flex
          flex-wrap
          items-center
          justify-center
          gap-3
          text-sm
          font-medium
          text-slate-500
          dark:text-slate-400
        "
      >
        <span>Resume Intelligence</span>

        <span className="text-indigo-400">•</span>

        <span>Semantic Job Matching</span>

        <span className="text-indigo-400">•</span>

        <span>Interview AI</span>

        <span className="text-indigo-400">•</span>

        <span>Application Tracking</span>
      </motion.div>
    </>
  );
};

export default HeroContent;