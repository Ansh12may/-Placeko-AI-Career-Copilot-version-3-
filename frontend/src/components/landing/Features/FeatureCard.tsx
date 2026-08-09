import type { Feature } from "./type.ts";

interface FeatureCardProps {
  feature: Feature;
}

const FeatureCard = ({
  feature: {
    icon: Icon,
    title,
    description,
  },
}: FeatureCardProps) => {
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
      <div
        className="
          mb-5
          flex
          h-14
          w-14
          items-center
          justify-center
          rounded-xl
          bg-indigo-50
          dark:bg-indigo-950
          text-indigo-600
          dark:text-indigo-400
        "
      >
        <Icon className="h-7 w-7" />
      </div>

      <h3
        className="
          text-xl
          font-bold
          text-slate-900
          dark:text-white
        "
      >
        {title}
      </h3>

      <p
        className="
          mt-3
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

export default FeatureCard;