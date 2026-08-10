import WorkflowHeader from "./WorkflowHeader";
import WorkflowTimeline from "./WorkflowTimeline";

const Workflow = () => {
  return (
    <section
      id="how-it-works"
      className="
        py-24
        px-6
        bg-slate-50
        dark:bg-slate-900/40
      "
    >
      <div className="mx-auto max-w-6xl">
        <WorkflowHeader />

        <WorkflowTimeline />
      </div>
    </section>
  );
};

export default Workflow;