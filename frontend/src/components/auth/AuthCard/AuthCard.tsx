import type { ReactNode } from "react";

interface AuthCardProps {
  children: ReactNode;
  title: string;
  subtitle: string;
}

const AuthCard = ({
  children,
  title,
  subtitle,
}: AuthCardProps) => {
  return (
    <section
      className="
        w-full
        max-w-md
        rounded-2xl
        border
        border-slate-200
        bg-white
        px-8
        py-9
        shadow-xl
        shadow-slate-200/60
        dark:border-slate-800
        dark:bg-slate-900
        dark:shadow-none
      "
    >
      {/* Logo */}

      <div className="flex justify-center">
        <div
          className="
            flex
            h-12
            w-12
            items-center
            justify-center
            rounded-xl
            bg-indigo-600
            text-2xl
            font-bold
            italic
            text-white
            shadow-lg
            shadow-indigo-200
            dark:shadow-none
          "
        >
          P
        </div>
      </div>

      {/* Header */}

      <div className="mt-4 text-center">

        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          {title}
        </h1>

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          {subtitle}
        </p>

      </div>

      {/* Content */}

      <div className="mt-7">
        {children}
      </div>

    </section>
  );
};

export default AuthCard;