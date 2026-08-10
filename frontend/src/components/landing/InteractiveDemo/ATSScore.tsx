import { Sparkles } from "lucide-react";

interface ATSScoreProps {
  selectedRole: string;
}

interface RoleAnalysis {
  score: number;
  summary: string;
  focus: string[];
}

const roleAnalysis: Record<string, RoleAnalysis> = {
  "Frontend Engineer": {
    score: 88,
    summary:
      "Strong alignment with the core frontend requirements. Your React and TypeScript experience gives you a solid foundation for this role.",
    focus: ["GraphQL", "Docker", "Cypress"],
  },

  "Backend Engineer": {
    score: 84,
    summary:
      "Good backend alignment with strong Node.js and API experience. Strengthening infrastructure and distributed-system skills would improve your profile.",
    focus: ["Redis", "Kubernetes", "Kafka"],
  },

  "AI Engineer": {
    score: 91,
    summary:
      "Strong alignment with modern AI engineering requirements through Python, Transformers, LangChain, and vector databases.",
    focus: ["LoRA", "RLHF", "Distributed Training"],
  },

  "Full Stack Developer": {
    score: 87,
    summary:
      "Strong full-stack foundation across React, Node.js, MongoDB, and TypeScript. Cloud and production architecture are the main areas to strengthen.",
    focus: ["AWS", "CI/CD", "Microservices"],
  },
};

const ATSScore = ({
  selectedRole,
}: ATSScoreProps) => {
  const analysis =
    roleAnalysis[selectedRole] ??
    roleAnalysis["Frontend Engineer"];

  return (
    <div
      className="
        rounded-2xl
        border
        border-slate-200
        bg-white
        p-6
        shadow-sm
        dark:border-slate-800
        dark:bg-slate-900
      "
    >
      <div className="grid items-center gap-8 lg:grid-cols-[0.8fr_1.2fr]">

        {/* =================================================
            ATS SCORE
            ================================================= */}

        <div className="flex items-center gap-6">

          {/* Score Circle */}

          <div
            className="
              relative
              flex
              h-28
              w-28
              shrink-0
              items-center
              justify-center
              rounded-full
              border-[6px]
              border-indigo-100
              dark:border-indigo-950
            "
          >

            <div
              className="
                absolute
                inset-[-6px]
                rounded-full
                border-[6px]
                border-transparent
                border-t-indigo-600
                border-r-indigo-600
                -rotate-45
              "
            />

            <div className="text-center">

              <p className="text-2xl font-extrabold text-indigo-600 dark:text-indigo-400">
                {analysis.score}%
              </p>

              <p className="text-[9px] font-bold uppercase tracking-wider text-slate-400">
                Match
              </p>

            </div>

          </div>

          {/* Score Information */}

          <div>

            <p className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
              ATS Match Score
            </p>

            <h3 className="mt-1 text-xl font-bold text-slate-900 dark:text-white">
              {selectedRole}
            </h3>

            <p className="mt-2 max-w-sm text-xs leading-5 text-slate-500 dark:text-slate-400">
              Semantic alignment between your profile
              and the selected role.
            </p>

          </div>

        </div>


        {/* =================================================
            AI CAREER INSIGHT
            ================================================= */}

        <div
          className="
            rounded-xl
            border
            border-indigo-100
            bg-gradient-to-br
            from-indigo-50
            via-white
            to-violet-50
            p-5
            dark:border-indigo-900
            dark:from-indigo-950/50
            dark:via-slate-900
            dark:to-violet-950/30
          "
        >

          {/* Header */}

          <div className="flex items-center gap-2">

            <div
              className="
                flex
                h-8
                w-8
                items-center
                justify-center
                rounded-lg
                bg-indigo-600
                text-white
              "
            >
              <Sparkles size={15} />
            </div>

            <div>

              <p className="text-xs font-bold text-indigo-700 dark:text-indigo-300">
                AI Career Insight
              </p>

              <p className="text-[10px] text-slate-400">
                Profile analysis
              </p>

            </div>

          </div>


          {/* Summary */}

          <p className="mt-4 text-xs leading-5 text-slate-600 dark:text-slate-300">
            {analysis.summary}
          </p>


          {/* Focus Areas */}

          <div className="mt-4">

            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Recommended focus
            </p>

            <div className="mt-2 flex flex-wrap gap-2">

              {analysis.focus.map((skill) => (
                <span
                  key={skill}
                  className="
                    rounded-full
                    border
                    border-indigo-100
                    bg-white
                    px-2.5
                    py-1
                    text-[10px]
                    font-semibold
                    text-indigo-600
                    dark:border-indigo-900
                    dark:bg-indigo-950/40
                    dark:text-indigo-300
                  "
                >
                  {skill}
                </span>
              ))}

            </div>

          </div>

        </div>

      </div>
    </div>
  );
};

export default ATSScore;