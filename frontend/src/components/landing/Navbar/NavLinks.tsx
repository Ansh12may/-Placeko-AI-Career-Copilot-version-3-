import { motion } from "framer-motion";

const NavLinks = () => {
  const navLinks = [
    {
      label: "Features",
      href: "#features",
    },
    {
      label: "How It Works",
      href: "#how-it-works",
    },
    {
      label: "Live Demo",
      href: "#demo",
    },
  ];

  return (
    <nav className="hidden items-center gap-8 lg:flex">
      {navLinks.map((link) => (
        <motion.a
          key={link.label}
          href={link.href}
          whileHover={{ y: -2 }}
          transition={{ duration: 0.2 }}
          className="
            group
            relative
            text-sm
            font-semibold
            text-slate-600
            transition-colors
            duration-200
            hover:text-indigo-600
            dark:text-slate-300
            dark:hover:text-indigo-400
          "
        >
          {link.label}

          {/* Animated Underline */}

          <span
            className="
              absolute
              -bottom-1
              left-0
              h-[2px]
              w-0
              bg-indigo-600
              transition-all
              duration-300
              group-hover:w-full
              dark:bg-indigo-400
            "
          />
        </motion.a>
      ))}
    </nav>
  );
};

export default NavLinks;