interface ATSScoreProps {
  selectedRole: string;
}

const scores: Record<string, number> = {
  "Frontend Engineer": 88,
  "Backend Engineer": 84,
  "AI Engineer": 91,
  "Full Stack Developer": 86,
};

const ATSScore = ({ selectedRole }: ATSScoreProps) => {
  const score = scores[selectedRole];

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">

      <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
        ATS Match Score
      </p>

      <div className="mt-4 flex items-center justify-between">

        <div>
          <h3 className="text-5xl font-black text-indigo-600">
            {score}%
          </h3>

          <p className="mt-2 text-sm text-slate-500">
            {selectedRole}
          </p>
        </div>

        <div
          className="
            flex
            h-20
            w-20
            items-center
            justify-center
            rounded-full
            border-4
            border-indigo-600
            border-t-transparent
            text-xl
            font-bold
            text-indigo-600
          "
        >
          {score}
        </div>

      </div>

    </div>
  );
};

export default ATSScore;