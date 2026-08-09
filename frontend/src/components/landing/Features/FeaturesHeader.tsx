import { motion } from "framer-motion";

const FeaturesHeader = () => {
  return (
    <div className="mx-auto max-w-3xl text-center">
      {/* Small Badge */}
      <motion.span
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.4 }}
        className="
          text-xs
          font-bold
          uppercase
          tracking-[0.3em]
          text-indigo-600
          dark:text-indigo-400
        "
      >
        Core Features
      </motion.span>

      {/* Heading */}
      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1, duration: 0.4 }}
        className="
          mt-4
          text-4xl
          font-extrabold
          tracking-tight
          text-slate-900
          dark:text-white
        "
      >
        Everything You Need to Land Your Dream Job
      </motion.h2>

      {/* Description */}
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2, duration: 0.4 }}
        className="
          mt-6
          text-lg
          leading-8
          text-slate-600
          dark:text-slate-400
        "
      >
        From AI-powered resume optimization and semantic job matching
        to voice-based mock interviews and career analytics,
        Placeko supports every step of your placement journey.
      </motion.p>
    </div>
  );
};

export default FeaturesHeader;