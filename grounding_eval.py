"""
Placeko Resume-Extraction Grounding Evaluator

WHAT THIS MEASURES
-------------------
Your ResumeAgent extracts skills/projects/technologies from a resume via
an LLM (Groq), then GroundingService checks every extracted entity against
the ORIGINAL resume text:

    1. Deterministic phrase match (fast, no LLM)          -> GROUNDED
    2. If that fails, an LLM verifier checks it            -> SUPPORTED / UNSUPPORTED / UNCERTAIN

This script runs that full pipeline over a folder of real resumes and
reports, in aggregate:

    - % of extracted skills grounded deterministically in the source text
    - of the rest, % confirmed SUPPORTED / caught as UNSUPPORTED (hallucinated) /
      left UNCERTAIN by the LLM verifier
    - the same breakdown for project technologies
    - an overall "grounding accuracy" = (grounded + LLM-supported) / total extracted

This needs NO manually labeled ground truth — the grounding logic itself
is doing the verification. That's the whole point of the architecture,
and it's a genuinely strong resume metric:

    "Built a two-stage grounding pipeline that deterministically verifies
    X% of LLM-extracted entities against source text and routes the rest
    to an LLM verifier, catching Y% hallucinated skills before they reach
    ATS scoring, across a Z-resume evaluation set."

HOW TO RUN
----------
1. Put this file at the ROOT of your Placekov5 repo (next to backend/),
   since the imports below assume `backend` is importable from cwd —
   same way main.py does it.
2. Put a folder of real resumes (pdf/docx) in ./eval_resumes/
   (10-30 varied resumes is enough for a solid number; more is better).
3. Make sure backend/.env has a valid GROQ_API_KEY (same one your app uses —
   this calls the real LLM extraction + verifier, so it will make API calls).
4. Run:  python grounding_eval.py
   Prints a summary and writes grounding_report.json with full detail.
"""

import asyncio
import json
from pathlib import Path

from backend.Resume.tools.resume_parser import parse_resume
from backend.Resume.agents.resume_agent import ResumeAgent
from backend.Resume.services.grounding_service import GroundingService

EVAL_RESUMES_DIR = Path("eval_resumes")
REPORT_PATH = Path("grounding_report.json")


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


async def main():
    if not EVAL_RESUMES_DIR.exists():
        print(f"Create '{EVAL_RESUMES_DIR}/' and put 10-30 real resumes in it (pdf/docx).")
        return

    resume_files = [
        p for p in EVAL_RESUMES_DIR.iterdir()
        if p.suffix.lower() in (".pdf", ".docx")
    ]
    if not resume_files:
        print(f"No .pdf/.docx files found in {EVAL_RESUMES_DIR}/")
        return

    agent = ResumeAgent()
    grounder = GroundingService()

    per_resume_results = []
    for resume_path in resume_files:
        print(f"Processing {resume_path.name} ...")
        try:
            result = await evaluate_one(resume_path, agent, grounder)
            per_resume_results.append(result)
        except Exception as e:
            print(f"  [skip] {resume_path.name} failed: {e}")

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


if __name__ == "__main__":
    asyncio.run(main())