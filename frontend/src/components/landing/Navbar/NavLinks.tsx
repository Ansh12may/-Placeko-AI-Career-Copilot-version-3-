import React from "react";
import { motion } from "framer-motion";

const NavLinks: React.FC = () => {
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
      href: "#preview",
    },
    {
      label: "Pricing",
      href: "#pricing",
    },
    {
      label: "FAQ",
      href: "#faq",
    },
  ];

  return (
    <nav className="hidden lg:flex items-center gap-8">
      {navLinks.map((link) => (
        <motion.a
          key={link.label}
          href={link.href}
          whileHover={{ y: -2 }}
          transition={{ duration: 0.2 }}
          className="relative group text-sm font-semibold text-slate-600 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors duration-200"
        >
          {link.label}

          {/* Animated Underline */}
          <span className="absolute left-0 -bottom-1 h-[2px] w-0 bg-indigo-600 dark:bg-indigo-400 transition-all duration-300 group-hover:w-full"></span>
        </motion.a>
      ))}
    </nav>
  );
};

export default NavLinks;