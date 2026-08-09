import type { WorkflowStep as WorkflowStepType } from "./types";

interface WorkflowStepProps {
  step: WorkflowStepType;
}

const WorkflowStep = ({
  step: {
    number,
    title,
    description,
    icon: Icon,
  },
}: WorkflowStepProps) => {
  return (
    <div
      className="
        group
        rounded-2xl
        border
        border-slate-200
        dark:border-slate-800
        bg-white
        dark:bg-slate-900
        p-6
        shadow-sm
        transition-all
        duration-300
        hover:-translate-y-2
        hover:shadow-xl
      "
    >
      {/* Step Number */}

      <div className="flex justify-center">
        <div
          className="
            flex
            h-12
            w-12
            items-center
            justify-center
            rounded-full
            bg-indigo-600
            text-white
            font-bold
          "
        >
          {number}
        </div>
      </div>

      {/* Icon */}

      <div className="mt-5 flex justify-center">
        <div
          className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-xl
            bg-indigo-100
            dark:bg-indigo-950
            text-indigo-600
            dark:text-indigo-400
          "
        >
          <Icon className="h-7 w-7" />
        </div>
      </div>

      {/* Title */}

      <h3
        className="
          mt-6
          text-center
          text-xl
          font-bold
          text-slate-900
          dark:text-white
        "
      >
        {title}
      </h3>

      {/* Description */}

      <p
        className="
          mt-4
          text-center
          leading-7
          text-slate-600
          dark:text-slate-400
        "
      >
        {description}
      </p>
    </div>
  );
};

export default WorkflowStep;