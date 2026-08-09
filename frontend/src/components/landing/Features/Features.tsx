import FeaturesHeader from "./FeaturesHeader";
import FeatureGrid from "./FeatureGrid";

const Features = () => {
  return (
    <section
      id="features"
      className="
        py-24
        px-6
        bg-white
        dark:bg-slate-950
      "
    >
      <div className="mx-auto max-w-7xl">
        <FeaturesHeader />

        <FeatureGrid />
      </div>
    </section>
  );
};

export default Features;