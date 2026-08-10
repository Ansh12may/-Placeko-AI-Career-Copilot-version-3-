import StatCard from "./StatCard";
import { stats } from "./data";

interface StatsGridProps {
  resumeScore: number | null;
  jobMatches: number;
  applications: number;
  interviewReadiness: number | null;
}

const StatsGrid = ({
  resumeScore,
  jobMatches,
  applications,
  interviewReadiness,
}: StatsGridProps) => {
    

  const dynamicStats = stats.map((stat) => {

    if (stat.title === "Resume Score") {
      return {
        ...stat,
        value:
          resumeScore !== null
            ? String(Math.round(resumeScore))
            : "—",
      };
    }

    if (stat.title === "Job Matches") {
      return {
        ...stat,
        value: String(jobMatches),
      };
    }

    if (stat.title === "Applications") {
      return {
        ...stat,
        value: String(applications),
      };
    }

    if (stat.title === "Interview Readiness") {
      return {
        ...stat,
        value:
          interviewReadiness !== null
            ? `${interviewReadiness}%`
            : "Not assessed",
      };
    }
    return stat;
  });

  return (
    <section className="mt-8">

      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">
          Overview
        </h2>

        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Track your career progress at a glance.
        </p>
      </div>

      <div
        className="
          grid
          grid-cols-1
          gap-6
          sm:grid-cols-2
          xl:grid-cols-4
        "
      >
        {dynamicStats.map((stat) => (
          <StatCard
            key={stat.id}
            stat={stat}
          />
        ))}
      </div>

    </section>
  );
};

export default StatsGrid;