const HeroStats = () => {
  const capabilities = [
    {
      value: "AI",
      label: "Resume Intelligence",
      description: "Understand your career profile",
      color: "text-slate-900 dark:text-white",
    },
    {
      value: "NLP",
      label: "Semantic Job Matching",
      description: "Match skills beyond keywords",
      color: "text-indigo-600 dark:text-indigo-400",
    },
    {
      value: "LLM",
      label: "Personalized Interviews",
      description: "Questions built around your profile",
      color: "text-purple-600 dark:text-purple-400",
    },
    {
      value: "DB",
      label: "Application Pipeline",
      description: "Track applications persistently",
      color: "text-emerald-600 dark:text-emerald-400",
    },
  ];

  return (
    <div className="mt-20 grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-4">
      {capabilities.map((capability) => (
        <div
          key={capability.label}
          className="
            rounded-2xl
            border
            border-slate-200
            bg-white
            p-5
            text-center
            shadow-sm
            transition-all
            duration-300
            hover:-translate-y-1
            hover:border-indigo-200
            hover:shadow-lg
            dark:border-slate-800
            dark:bg-slate-900
            dark:hover:border-indigo-900
          "
        >
          <h3
            className={`text-2xl font-extrabold tracking-tight ${capability.color}`}
          >
            {capability.value}
          </h3>

          <p
            className="
              mt-2
              text-sm
              font-bold
              text-slate-800
              dark:text-white
            "
          >
            {capability.label}
          </p>

          <p
            className="
              mt-1
              text-xs
              leading-5
              text-slate-500
              dark:text-slate-400
            "
          >
            {capability.description}
          </p>
        </div>
      ))}
    </div>
  );
};

export default HeroStats;