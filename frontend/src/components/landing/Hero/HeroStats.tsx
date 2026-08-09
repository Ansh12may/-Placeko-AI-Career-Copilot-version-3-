const HeroStats = () => {
  const stats = [
    {
      value: "12,400+",
      label: "Candidates Placed",
      color: "text-slate-900 dark:text-white",
    },
    {
      value: "94.8%",
      label: "ATS Pass Rate",
      color: "text-indigo-600 dark:text-indigo-400",
    },
    {
      value: "$148k",
      label: "Average Salary",
      color: "text-emerald-600 dark:text-emerald-400",
    },
    {
      value: "3.2x",
      label: "More Interviews",
      color: "text-purple-600 dark:text-purple-400",
    },
  ];

  return (
    <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-5">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="
            rounded-2xl
            border
            border-slate-200
            dark:border-slate-800
            bg-white
            dark:bg-slate-900
            p-5
            text-center
            shadow-sm
            transition-all
            duration-300
            hover:-translate-y-1
            hover:shadow-lg
          "
        >
          <h3
            className={`text-3xl font-extrabold font-mono ${stat.color}`}
          >
            {stat.value}
          </h3>

          <p
            className="
              mt-2
              text-sm
              text-slate-500
              dark:text-slate-400
            "
          >
            {stat.label}
          </p>
        </div>
      ))}
    </div>
  );
};

export default HeroStats;