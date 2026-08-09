
const HeroBackground = () => {
  return (
    <>
      {/* Main Gradient Glow */}
      <div
        className="
          absolute
          -top-32
          left-1/2
          -translate-x-1/2
          w-175
          h-87.5
          rounded-full
          bg-linear-to-r
          from-indigo-500/20
          via-purple-500/15
          to-violet-500/20
          blur-[120px]
          pointer-events-none
          -z-10
        "
      />

      {/* Left Decorative Circle */}
      <div
        className="
          absolute
          top-40
          left-10
          w-32
          h-32
          rounded-full
          bg-indigo-500/10
          blur-3xl
          pointer-events-none
          -z-10
        "
      />

      {/* Right Decorative Circle */}
      <div
        className="
          absolute
          bottom-10
          right-10
          w-40
          h-40
          rounded-full
          bg-purple-500/10
          blur-3xl
          pointer-events-none
          -z-10
        "
      />
    </>
  );
};

export default HeroBackground;