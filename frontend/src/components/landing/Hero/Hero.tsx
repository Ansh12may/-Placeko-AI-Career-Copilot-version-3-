import HeroBackground from "./HeroBackground";
import HeroBadge from "./HeroBadge";
import HeroButtons from "./HeroButtons";
import HeroContent from "./HeroContent";
import HeroStats from "./HeroStats";

interface HeroProps {
  onGetStarted: () => void;
  onExploreDemo: () => void;
}

const Hero = ({
  onGetStarted,
  onExploreDemo,
}: HeroProps) => {
  return (
    <section className="relative overflow-hidden px-6 py-24">

      {/* Existing background */}
      <HeroBackground />

      {/* =====================================================
          Purple Hero Glow
          ===================================================== */}

      <div
        className="
          pointer-events-none
          absolute
          left-1/2
          top-16
          z-0
          h-[520px]
          w-[950px]
          -translate-x-1/2
          rounded-full
          bg-[radial-gradient(ellipse_at_center,rgba(124,58,237,0.18)_0%,rgba(139,92,246,0.09)_38%,transparent_72%)]
          blur-3xl
        "
      />

      {/* =====================================================
          Subtle Dot Texture
          ===================================================== */}

      <div
        className="
          pointer-events-none
          absolute
          left-1/2
          top-10
          z-0
          h-[540px]
          w-[1050px]
          -translate-x-1/2
          opacity-30
          [background-image:radial-gradient(rgba(99,102,241,0.35)_1px,transparent_1px)]
          [background-size:18px_18px]
          [mask-image:radial-gradient(ellipse_at_center,black_15%,transparent_72%)]
        "
      />

      {/* =====================================================
          Hero Content
          ===================================================== */}

      <div className="relative z-10 mx-auto flex max-w-6xl flex-col items-center text-center">

        <HeroBadge />

        <HeroContent />

        <HeroButtons
          onGetStarted={onGetStarted}
          onExploreDemo={onExploreDemo}
        />

        <HeroStats />

      </div>

    </section>
  );
};

export default Hero;