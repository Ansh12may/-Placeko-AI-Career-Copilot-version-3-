import { motion } from "framer-motion";

const WorkflowHeader = () => {
  return (
    <div className="mx-auto max-w-3xl text-center">
      <motion.span
        initial={{ opacity: 0, y: 15 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="
          text-xs
          font-bold
          uppercase
          tracking-[0.3em]
          text-indigo-600
          dark:text-indigo-400
        "
      >
        Platform Workflow
      </motion.span>

      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.1 }}
        className="
          mt-4
          text-4xl
          font-extrabold
          tracking-tight
          text-slate-900
          dark:text-white
        "
      >
        Your Journey from Resume to Offer Letter
      </motion.h2>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ delay: 0.2 }}
        className="
          mt-6
          text-lg
          leading-8
          text-slate-600
          dark:text-slate-400
        "
      >
        Placeko guides you through every stage of your placement
        journey—from resume analysis to interview preparation and
        application tracking.
      </motion.p>
    </div>
  );
};

export default WorkflowHeader;