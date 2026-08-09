import { ArrowRight, ChevronRight } from "lucide-react";

interface HeroButtonsProps {
  onGetStarted: () => void;
  onExploreDemo: () => void;
}

const HeroButtons = ({
  onGetStarted,
  onExploreDemo,
}: HeroButtonsProps) => {
  return (
    <div className="mt-10 flex flex-col sm:flex-row items-center gap-4">
      {/* Primary Button */}
      <button
        onClick={onGetStarted}
        className="
          group
          flex
          items-center
          justify-center
          gap-2
          rounded-xl
          bg-indigo-600
          px-7
          py-3.5
          text-sm
          font-bold
          text-white
          shadow-lg
          shadow-indigo-600/30
          transition-all
          duration-300
          hover:bg-indigo-500
          hover:scale-105
        "
      >
        <span>Create Account & Upload Resume</span>

        <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
      </button>

      {/* Secondary Button */}
      <button
        onClick={onExploreDemo}
        className="
          flex
          items-center
          justify-center
          gap-2
          rounded-xl
          border
          border-slate-200
          dark:border-slate-700
          bg-white
          dark:bg-slate-900
          px-7
          py-3.5
          text-sm
          font-semibold
          text-slate-800
          dark:text-slate-200
          transition-all
          duration-300
          hover:bg-slate-100
          dark:hover:bg-slate-800
        "
      >
        <span>Explore Live Dashboard</span>

        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  );
};

export default HeroButtons;