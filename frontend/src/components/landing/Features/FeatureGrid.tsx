import FeatureCard from "./FeatureCard";
import { features } from "./data";

const FeatureGrid = () => {
  return (
    <div
      className="
        mt-16
        grid
        grid-cols-1
        gap-8
        md:grid-cols-2
        lg:grid-cols-4
      "
    >
      {features.map((feature) => (
        <FeatureCard
          key={feature.title}
          feature={feature}
        />
      ))}
    </div>
  );
};

export default FeatureGrid;