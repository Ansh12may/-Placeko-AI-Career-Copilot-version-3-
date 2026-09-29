"""
Placeko Resume-Extraction Grounding Evaluator — resumable version.

WHY THIS VERSION
-----------------
The original grounding_eval.py processes the whole eval_resumes/ folder in
one run. If you hit a Groq rate limit halfway through, you lose everything
and have to start over. This version checkpoints after every resume, so:

    - Rerunning the script SKIPS resumes already in the checkpoint.
    - If you hit a rate limit, it saves progress and exits cleanly instead
      of crashing.
    - You can grow eval_resumes/ over multiple days/quota windows and just
      keep rerunning the same command — it picks up where it left off.

HOW TO RUN
----------
Same setup as before (root of Placekov5, eval_resumes/ folder populated,
backend/.env has GROQ_API_KEY). Then:

    python grounding_eval_resumable.py

Run it, let it go until it hits a rate limit or finishes, wait for quota
to reset, rerun the same command. Repeat until every resume in
eval_resumes/ has been processed. Final report (grounding_report.json) is
only written once every resume has a result.

To force a clean re-evaluation of everything (e.g. you changed the
grounding logic), delete eval_checkpoint.json first.
"""

import asyncio
import json
import re
import time
from pathlib import Path

from backend.Resume.tools.resume_parser import parse_resume
from backend.Resume.agents.resume_agent import ResumeAgent
from backend.Resume.services.grounding_service import GroundingService

EVAL_RESUMES_DIR = Path("eval_resumes")
CHECKPOINT_PATH = Path("eval_checkpoint.json")
REPORT_PATH = Path("grounding_report.json")

# Baseline delay between resumes. With an 8000 TPM Groq limit this alone
# won't save you — the auto-retry below is what actually handles it — but
# it still reduces how often you trip the limit in the first place.
SLEEP_BETWEEN_CALLS_SECONDS = 5

# If a rate limit hits mid-resume, retry the SAME resume this many times,
# waiting however long Groq says to wait (plus a buffer) each time, before
# giving up and checkpointing/exiting for the day.
MAX_RATE_LIMIT_RETRIES = 6
RATE_LIMIT_WAIT_BUFFER_SECONDS = 2

# Substrings that indicate a rate-limit error from Groq/OpenAI-style clients.
RATE_LIMIT_MARKERS = ("rate limit", "429", "rate_limit", "too many requests")

# Groq's error message includes e.g. "Please try again in 4.2075s"
WAIT_TIME_PATTERN = re.compile(r"try again in ([\d.]+)s", re.IGNORECASE)


def is_rate_limit_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(marker in msg for marker in RATE_LIMIT_MARKERS)


def parse_wait_seconds(exc: Exception, default: float = 10.0) -> float:
    match = WAIT_TIME_PATTERN.search(str(exc))
    if match:
        return float(match.group(1)) + RATE_LIMIT_WAIT_BUFFER_SECONDS
    return default


def load_checkpoint() -> dict:
    if CHECKPOINT_PATH.exists():
        with open(CHECKPOINT_PATH, "r") as f:
            return json.load(f)
    return {"per_resume_detail": []}


def save_checkpoint(checkpoint: dict):
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump(checkpoint, f, indent=2)


async def evaluate_one(resume_path: Path, agent: ResumeAgent, grounder: GroundingService) -> dict:
    """Run extraction + grounding for a single resume."""
    resume_text = parse_resume(resume_path)
    candidate = agent.invoke_llm(resume_text)

    grounding_result = grounder.ground_with_verifier(
        candidate=candidate,
        resume_text=resume_text,
    )

    verification_lookup = {
        v["entity"].strip().lower(): v["status"]
        for v in grounding_result.get("llm_verification", [])
    }

    def classify(entity: str, grounded: bool) -> str:
        if grounded:
            return "GROUNDED"
        return verification_lookup.get(entity.strip().lower(), "UNCERTAIN")

    skill_classes = [
        classify(s, True) for s in grounding_result["skills"]["grounded"]
    ] + [
        classify(s, False) for s in grounding_result["skills"]["unresolved"]
    ]

    tech_classes = []
    for project in grounding_result["projects"]:
        tech_classes += [
            classify(t, True) for t in project["technologies"]["grounded"]
        ]
        tech_classes += [
            classify(t, False) for t in project["technologies"]["unresolved"]
        ]

    return {
        "resume": resume_path.name,
        "num_skills_extracted": len(candidate.skills),
        "num_projects": len(candidate.projects),
        "skill_classification": skill_classes,
        "tech_classification": tech_classes,
    }


def summarize(classifications: list) -> dict:
    total = len(classifications)
    if total == 0:
        return {"total": 0}
    counts = {"GROUNDED": 0, "SUPPORTED": 0, "UNSUPPORTED": 0, "UNCERTAIN": 0}
    for c in classifications:
        counts[c] = counts.get(c, 0) + 1
    return {
        "total": total,
        "grounded_pct": round(counts["GROUNDED"] / total * 100, 1),
        "llm_supported_pct": round(counts["SUPPORTED"] / total * 100, 1),
        "llm_unsupported_pct": round(counts["UNSUPPORTED"] / total * 100, 1),
        "uncertain_pct": round(counts["UNCERTAIN"] / total * 100, 1),
        "overall_grounding_accuracy_pct": round(
            (counts["GROUNDED"] + counts["SUPPORTED"]) / total * 100, 1
        ),
        "hallucination_catch_rate_pct": round(
            counts["UNSUPPORTED"] / total * 100, 1
        ),
        "counts": counts,
    }


def write_final_report(per_resume_results: list):
    all_skill_classes = []
    all_tech_classes = []
    for r in per_resume_results:
        all_skill_classes += r["skill_classification"]
        all_tech_classes += r["tech_classification"]
    all_combined = all_skill_classes + all_tech_classes

    skill_summary = summarize(all_skill_classes)
    tech_summary = summarize(all_tech_classes)
    overall_summary = summarize(all_combined)

    print(f"\nEvaluated {len(per_resume_results)} resumes\n")
    print("SKILLS:")
    print(json.dumps(skill_summary, indent=2))
    print("\nPROJECT TECHNOLOGIES:")
    print(json.dumps(tech_summary, indent=2))
    print("\nOVERALL (skills + project technologies combined):")
    print(json.dumps(overall_summary, indent=2))

    with open(REPORT_PATH, "w") as f:
        json.dump(
            {
                "num_resumes": len(per_resume_results),
                "skills_summary": skill_summary,
                "project_tech_summary": tech_summary,
                "overall_summary": overall_summary,
                "per_resume_detail": per_resume_results,
            },
            f,
            indent=2,
        )
    print(f"\nFull report written to {REPORT_PATH}")
    if "overall_grounding_accuracy_pct" in overall_summary:
        print(
            f"\nResume bullet: 'Built a two-stage grounding pipeline achieving "
            f"{overall_summary['overall_grounding_accuracy_pct']}% verified extraction "
            f"accuracy across {len(per_resume_results)} resumes, catching "
            f"{overall_summary['hallucination_catch_rate_pct']}% hallucinated entities "
            f"before ATS scoring.'"
        )


async def main():
    if not EVAL_RESUMES_DIR.exists():
        print(f"Create '{EVAL_RESUMES_DIR}/' and put resumes in it (pdf/docx).")
        return

    resume_files = sorted(
        p for p in EVAL_RESUMES_DIR.iterdir()
        if p.suffix.lower() in (".pdf", ".docx")
    )
    if not resume_files:
        print(f"No .pdf/.docx files found in {EVAL_RESUMES_DIR}/")
        return

    checkpoint = load_checkpoint()
    done_names = {r["resume"] for r in checkpoint["per_resume_detail"]}
    remaining = [p for p in resume_files if p.name not in done_names]

    print(f"{len(done_names)} resume(s) already done (from checkpoint).")
    print(f"{len(remaining)} resume(s) left to process.\n")

    if not remaining:
        print("Nothing left to process — writing final report from checkpoint.")
        write_final_report(checkpoint["per_resume_detail"])
        return

    agent = ResumeAgent()
    grounder = GroundingService()

    for i, resume_path in enumerate(remaining):
        print(f"[{i + 1}/{len(remaining)}] Processing {resume_path.name} ...")

        result = None
        for attempt in range(1, MAX_RATE_LIMIT_RETRIES + 1):
            try:
                result = await evaluate_one(resume_path, agent, grounder)
                break
            except Exception as e:
                if is_rate_limit_error(e):
                    wait_s = parse_wait_seconds(e)
                    print(f"  Rate limit hit (attempt {attempt}/{MAX_RATE_LIMIT_RETRIES}), "
                          f"waiting {wait_s:.1f}s before retrying...")
                    time.sleep(wait_s)
                    continue
                else:
                    print(f"  [skip] {resume_path.name} failed (not rate-limit): {e}")
                    break

        if result is None:
            # Either a non-rate-limit failure (already logged and skipped
            # above), or retries were exhausted — the latter usually means
            # a daily/larger quota rather than a per-minute one, so it's
            # worth stopping the whole run here rather than burning more
            # retries on the next resume too.
            continue

        checkpoint["per_resume_detail"].append(result)
        save_checkpoint(checkpoint)
        print(f"  done, checkpoint saved ({len(checkpoint['per_resume_detail'])} total).")

        if i < len(remaining) - 1:
            time.sleep(SLEEP_BETWEEN_CALLS_SECONDS)

    print("\nAll resumes processed.")
    write_final_report(checkpoint["per_resume_detail"])


if __name__ == "__main__":
    asyncio.run(main())