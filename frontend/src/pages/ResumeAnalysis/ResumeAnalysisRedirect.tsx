import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { getResumes } from "../../api/resume";

const ResumeAnalysisRedirect = () => {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  useEffect(() => {
    const redirectToLatestResume = async () => {
      try {
        const response = await getResumes();

        if (!response.data || response.data.length === 0) {
          setError("No resume found. Please upload a resume first.");
          return;
        }

        // Backend returns resumes in creation order.
        // Sort explicitly so we always select the newest one.
        const latestResume = [...response.data].sort(
          (a, b) =>
            new Date(b.created_at).getTime() -
            new Date(a.created_at).getTime()
        )[0];

        navigate(`/resume-analysis/${latestResume.id}`, {
          replace: true,
        });
      } catch (error) {
        console.error(
          "Failed to find latest resume:",
          error
        );

        setError("Unable to load your latest resume.");
      }
    };

    redirectToLatestResume();
  }, [navigate]);

  if (error) {
    return (
      <div className="flex min-h-full items-center justify-center bg-slate-50 p-6 dark:bg-slate-950">
        <div className="rounded-2xl border border-red-200 bg-red-50 px-6 py-5 text-center text-sm text-red-600">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-full items-center justify-center bg-slate-50 dark:bg-slate-950">
      <div className="flex items-center gap-3 text-slate-500 dark:text-slate-400">
        <Loader2 className="h-5 w-5 animate-spin" />

        Loading latest resume analysis...
      </div>
    </div>
  );
};

export default ResumeAnalysisRedirect;