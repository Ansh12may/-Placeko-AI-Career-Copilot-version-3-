const SidebarLogo = () => {
  return (
    <div
      className="
        flex
        items-center
        gap-3
        border-b
        border-slate-200
        px-5
        py-5
        dark:border-slate-800
      "
    >
      {/* Logo */}

      <div
        className="
          flex
          h-10
          w-10
          shrink-0
          items-center
          justify-center
          rounded-lg
          bg-gradient-to-br
          from-indigo-600
          to-violet-600
          text-base
          font-black
          text-white
          shadow-sm
        "
      >
        P
      </div>

      {/* Brand */}

      <div className="min-w-0">
        <h1
          className="
            text-lg
            font-extrabold
            leading-tight
            text-slate-900
            dark:text-white
          "
        >
          Placeko
        </h1>

        <p
          className="
            text-[11px]
            leading-tight
            text-slate-400
            dark:text-slate-500
          "
        >
          AI Career Copilot
        </p>
      </div>
    </div>
  );
};

export default SidebarLogo;