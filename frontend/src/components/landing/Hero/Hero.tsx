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
    <section className="relative overflow-hidden py-24 px-6">
      <HeroBackground />

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