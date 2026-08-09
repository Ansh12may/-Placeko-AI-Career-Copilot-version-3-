import WorkflowStep from "./WorkflowStep";
import { workflowSteps } from "./data";

const WorkflowTimeline = () => {
  return (
    <div className="relative mt-20">

      {/* Desktop Timeline Line */}
      <div
        className="
          absolute
          left-1/2
          top-0
          hidden
          h-full
          w-1
          -translate-x-1/2
          rounded-full
          bg-gradient-to-b
          from-indigo-500
          via-indigo-300
          to-indigo-500
          lg:block
        "
      />

      {/* Timeline Steps */}
      <div className="space-y-12">
        {workflowSteps.map((step, index) => {
          const isLeft = index % 2 === 0;

          return (
            <div
              key={step.number}
              className="
                grid
                grid-cols-1
                items-center
                gap-8
                lg:grid-cols-[1fr_auto_1fr]
              "
            >
              {/* Left Side */}

              <div className={isLeft ? "lg:block" : "hidden lg:block"}>
                {isLeft && <WorkflowStep step={step} />}
              </div>

              {/* Timeline Dot */}

              <div className="relative flex justify-center">

  {/* Outer Glow */}

  <div

    className="

      absolute

      h-8

      w-8

      rounded-full

      bg-indigo-500/20

      blur-sm

    "

  />

  {/* Outer Ring */}

  <div

    className="

      absolute

      flex

      h-8

      w-8

      items-center

      justify-center

      rounded-full

      border-2

      border-indigo-400

      bg-white

      dark:bg-slate-950

    "

  >

    {/* Inner Circle */}

    <div

      className="

        h-3

        w-3

        rounded-full

        bg-indigo-600

      "

    />

  </div>

</div>
              {/* Right Side */}

              <div className={!isLeft ? "lg:block" : "hidden lg:block"}>
                {!isLeft && <WorkflowStep step={step} />}
              </div>

              {/* Mobile Layout */}

              <div className="lg:hidden">
                <WorkflowStep step={step} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default WorkflowTimeline;