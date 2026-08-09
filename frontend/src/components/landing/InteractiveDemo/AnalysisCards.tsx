import {
  ArrowRight,
  CheckCircle2,
  Mic,
  Zap,
} from "lucide-react";

interface AnalysisCardsProps {
  selectedRole: string;
}

const analysisData: Record<
  string,
  {
    matched: string;
    missing: string;
  }
> = {
  "Frontend Engineer": {
    matched:
      "React, TypeScript, Vite, Redux, Tailwind CSS",
    missing:
      "GraphQL, Docker, Cypress",
  },

  "Backend Engineer": {
    matched:
      "Node.js, Express, PostgreSQL, REST APIs",
    missing:
      "Redis, Kubernetes, Kafka",
  },

  "AI Engineer": {
    matched:
      "Python, Transformers, LangChain, Vector DBs",
    missing:
      "LoRA, RLHF, Distributed Training",
  },

  "Full Stack Developer": {
    matched:
      "React, Node.js, MongoDB, TypeScript",
    missing:
      "AWS, CI/CD, Microservices",
  },
};

const AnalysisCards = ({
  selectedRole,
}: AnalysisCardsProps) => {
  const data = analysisData[selectedRole];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

      {/* Matched Skills */}

      <div className="rounded-2xl border border-emerald-200 dark:border-emerald-900 bg-emerald-50 dark:bg-emerald-950/30 p-5">

        <div className="flex items-center gap-2">

          <CheckCircle2 className="w-5 h-5 text-emerald-600" />

          <h3 className="font-bold text-emerald-700 dark:text-emerald-300">
            Matched Skills
          </h3>

        </div>

        <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">
          {data.matched}
        </p>

      </div>

      {/* Missing Skills */}

      <div className="rounded-2xl border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950/30 p-5">

        <div className="flex items-center gap-2">

          <Zap className="w-5 h-5 text-amber-600" />

          <h3 className="font-bold text-amber-700 dark:text-amber-300">
            Missing Skills
          </h3>

        </div>

        <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">
          {data.missing}
        </p>

      </div>

      {/* Interview */}

      <div className="rounded-2xl border border-indigo-200 dark:border-indigo-900 bg-indigo-50 dark:bg-indigo-950/30 p-5">

        <div className="flex items-center gap-2">

          <Mic className="w-5 h-5 text-indigo-600" />

          <h3 className="font-bold text-indigo-700 dark:text-indigo-300">
            AI Interview Ready
          </h3>

        </div>

        <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">
          Practice interview questions for{" "}
          <strong>{selectedRole}</strong>.
        </p>

        <button className="group mt-5 flex items-center gap-2 font-semibold text-indigo-600">

          Start Practice

          <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />

        </button>

      </div>

    </div>
  );
};

export default AnalysisCards;