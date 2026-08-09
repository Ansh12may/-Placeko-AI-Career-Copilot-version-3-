import { useState } from "react";

import DemoHeader from "./DemoHeader";
import RoleSelector from "./RoleSelector";
import ATSScore from "./ATSScore";
import AnalysisCards from "./AnalysisCards";

const InteractiveDemo = () => {
  const [selectedRole, setSelectedRole] =
    useState("Frontend Engineer");

  return (
    <section className="py-24 px-6 bg-slate-100/70 dark:bg-slate-900/40">
      <div className="mx-auto max-w-6xl space-y-10">

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