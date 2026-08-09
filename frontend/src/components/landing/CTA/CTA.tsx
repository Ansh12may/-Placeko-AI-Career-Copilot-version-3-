interface CTAProps {
  onGetStarted: () => void;
}
const CTA = ({ onGetStarted }: CTAProps) => {
  return (
    <section className="bg-indigo-600 py-24 px-6">
      <div className="mx-auto max-w-4xl text-center">

        <h2 className="text-4xl font-extrabold text-white">
          Ready to Transform Your Career?
        </h2>

        <p className="mt-6 text-lg text-indigo-100">
          Upload your resume, practice AI mock interviews,
          discover personalized jobs, and prepare for your
          dream placement with Placeko.
        </p>

        <button
          onClick={onGetStarted}
          className="
            mt-10
            rounded-xl
            bg-white
            px-8
            py-4
            text-lg
            font-semibold
            text-indigo-600
            transition
            hover:scale-105
          "
        >
          Get Started Free
        </button>

      </div>
    </section>
  );
};

export default CTA;