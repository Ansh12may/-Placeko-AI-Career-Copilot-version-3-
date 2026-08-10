import { quickActions } from "./data";
import QuickActionCard from "./QuickActionCard";

const QuickActions = () => {
  return (
    <section className="mt-8">

      <div className="mb-6">
        <h2 className="text-xl font-bold text-slate-900 dark:text-white">
          Quick Actions
        </h2>

        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Jump directly to the tools you use most.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {quickActions.map((action) => (
          <QuickActionCard
            key={action.id}
            action={action}
          />
        ))}
      </div>

    </section>
  );
};

export default QuickActions;