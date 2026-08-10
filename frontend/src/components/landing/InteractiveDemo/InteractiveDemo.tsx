import { useState } from "react";

import DemoHeader from "./DemoHeader";
import RoleSelector from "./RoleSelector";
import ATSScore from "./ATSScore";
import AnalysisCards from "./AnalysisCards";

const InteractiveDemo = () => {
  const [selectedRole, setSelectedRole] =
    useState("Frontend Engineer");

  return (
    <section
      id="demo"
      className="
        relative
        overflow-hidden
        bg-slate-50
        px-6
        py-24
        dark:bg-slate-950
      "
    >

      {/* Background Glow */}

      <div
        className="
          pointer-events-none
          absolute
          left-1/2
          top-0
          h-[400px]
          w-[700px]
          -translate-x-1/2
          rounded-full
          bg-indigo-500/5
          blur-3xl
        "
      />

      {/* Demo Content */}

      <div className="relative z-10 mx-auto max-w-6xl space-y-10">

        <DemoHeader />

        <RoleSelector
          selectedRole={selectedRole}
          onRoleChange={setSelectedRole}
        />

        <ATSScore
          selectedRole={selectedRole}
        />

        <AnalysisCards
          selectedRole={selectedRole}
        />

      </div>

    </section>
  );
};

export default InteractiveDemo;