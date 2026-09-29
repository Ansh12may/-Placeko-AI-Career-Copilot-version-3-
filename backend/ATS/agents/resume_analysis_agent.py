"""
Resume Analysis Agent

Responsible for generating a complete ATS report.

Responsibilities:
- Read CandidateProfile from GraphState
- Read source grounding result from GraphState
- Calculate deterministic ATS scores
- Invoke ResumeAnalysisService for qualitative feedback
- Merge deterministic scores with AI feedback
- Create ATSReport
- Update GraphState

This agent performs orchestration only.

It does NOT:
- Parse resumes
- Perform MongoDB operations
- Search for jobs
- Perform job ranking
"""
from typing import Optional
from backend.graphs.state import GraphState
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.services.resume_analysis_service import (ResumeAnalysisService)
from backend.ATS.services.ats_scoring_service import (ATSScoringService)
from backend.ATS.schemas.ats_report import (ATSReport,SourceVerification)


class ResumeAnalysisAgent:

    def __init__(self):
        self.analysis_service = (ResumeAnalysisService())
        self.ats_scoring_service = (ATSScoringService())

    # Prepare Input
    
    def prepare_input(self,state: GraphState) -> CandidateProfile:
        """
        Extract CandidateProfile from GraphState.
        """

        profile = state.get("candidate_profile")

        if profile is None:
            raise ValueError(
                "Candidate profile not found in GraphState."
            )

        return profile

    # Prepare ATS Profile


    def prepare_ats_profile(self,profile: CandidateProfile,grounding_result: Optional[dict]) -> CandidateProfile:
        """
        Create the CandidateProfile that will be used for ATS scoring.

        Deterministically grounded skills are trusted directly.

        Skills that could not be grounded deterministically are included
        only when the LLM verifier explicitly marks them as SUPPORTED.

        UNSUPPORTED and UNCERTAIN entities are excluded from the
        ATS-scoring profile.

        The original CandidateProfile is never modified.
        """

        # 1. Grounding result is required

        if grounding_result is None:
            raise ValueError(
                "Grounding result not found in GraphState. "
                "ATS scoring requires source-grounded extraction."
            )

        # 2. Read skill grounding

        skill_grounding = grounding_result.get("skills")

        if not isinstance(skill_grounding, dict):
            raise ValueError(
                "Invalid grounding result: "
                "'skills' section is missing or malformed."
            )

        grounded_skills = skill_grounding.get(
            "grounded",
            [],
        )

        unresolved_skills = skill_grounding.get(
            "unresolved",
            [],
        )

        if not isinstance(grounded_skills, list):
            raise ValueError(
                "Invalid grounding result: "
                "'grounded' skills must be a list."
            )

        if not isinstance(unresolved_skills, list):
            raise ValueError(
                "Invalid grounding result: "
                "'unresolved' skills must be a list."
            )

        # 3. Start with deterministically grounded skills

        final_skills = list(grounded_skills)

        # 4. Read LLM verifier results

        verification_results = grounding_result.get(
            "llm_verification",
            [],
        )

        if not isinstance(verification_results, list):
            verification_results = []

        # 5. Add unresolved skills only when verifier
        #    explicitly confirms them as supported

        unresolved_skill_lookup = {
            skill.strip().lower()
            for skill in unresolved_skills
            if isinstance(skill, str) and skill.strip()
        }

        for result in verification_results:

            if not isinstance(result, dict):
                continue

            entity = result.get("entity")
            status = result.get("status")

            if not isinstance(entity, str):
                continue

            normalized_entity = entity.strip().lower()

            # Only process entities that were actually
            # unresolved skills.
            if normalized_entity not in unresolved_skill_lookup:
                continue

            # Only an explicit SUPPORTED verdict can
            # promote an unresolved skill.
            if status == "SUPPORTED":

                # Preserve the original extracted skill
                # spelling/capitalization where possible.
                for original_skill in unresolved_skills:

                    if (
                        isinstance(original_skill, str)
                        and original_skill.strip().lower()
                        == normalized_entity
                    ):
                        if original_skill not in final_skills:
                            final_skills.append(
                                original_skill
                            )
                        break

        # 6. Return a temporary ATS profile.
        #
        # The original CandidateProfile remains unchanged.

        return profile.model_copy(
            update={
                "skills": final_skills
            }
        )

    def build_source_verification(self,grounding_result: dict) -> SourceVerification:
        """
        Convert the internal grounding result into a small,
        user-facing source verification summary.

        The detailed grounding result remains an internal
        implementation detail.
        """

        if grounding_result is None:
            raise ValueError(
                "Grounding result not found in GraphState. "
                "ATS analysis requires source-grounded extraction."
            )

        # Skills

        skills_result = grounding_result.get("skills",{})
        grounded_skills = skills_result.get("grounded",[],)
        unresolved_skills = skills_result.get("unresolved",[])

        # Projects

        projects_result = grounding_result.get("projects",[],)
        grounded_projects = 0
        unresolved_projects = 0

        for project in projects_result:

            if project.get(
                "title_grounded",
                False,
            ):
                grounded_projects += 1
            else:
                unresolved_projects += 1

  
        # Overall verification status
     

        verified = (
            len(unresolved_skills) == 0
            and unresolved_projects == 0
        )

        return SourceVerification(
            verified=verified,
            grounded_skills=len(grounded_skills),
            unresolved_skills=len(unresolved_skills),
            grounded_projects=grounded_projects,
            unresolved_projects=unresolved_projects,
        )

    # Build ATS Report
  

    def build_report(self,scores: dict,analysis: dict, source_verification: SourceVerification) -> ATSReport:
        """
        Merge deterministic ATS scores with
        AI-generated qualitative feedback.
        """

        return ATSReport(
            # Candidate Level
            candidate_level=scores["candidate_level"],
            # Overall Score
            overall_score=scores["overall_score"],

            # Section Scores
            contact_information=scores["contact_information"],
            education=scores["education"],
            experience=scores["experience"],
            projects=scores["projects"],
            skills=scores["skills"],
            certifications=scores["certifications"],
            formatting=scores["formatting"],
            summary=scores["summary"],

            # AI Qualitative Analysis
            
            strengths=analysis.get("strengths",[]),
            weaknesses=analysis.get("weaknesses",[]),
            missing_keywords=analysis.get("missing_keywords",[]),

            # Section Feedback
           
            formatting_feedback=analysis.get("formatting_feedback",[]),
            education_feedback=analysis.get("education_feedback",[]),
            experience_feedback=analysis.get("experience_feedback",[]),
            project_feedback=analysis.get("project_feedback",[]),
            skills_feedback=analysis.get("skills_feedback",[]),


            # Recommendations
           
            recommendations=analysis.get("recommendations",[]),

            source_verification=source_verification
        )

    # Run
    def run( self, state: GraphState) -> GraphState:

        # 1. Get original candidate profile

        profile = self.prepare_input(state)

        # 2. Get grounding result

        grounding_result = state.get("grounding_result")
        if grounding_result is None:
            raise ValueError(
                "Grounding result not found in GraphState. "
                "ATS analysis requires source-grounded extraction."

            )

        # 3. Create temporary profile for ATS scoring

        ats_profile = self.prepare_ats_profile( profile=profile,grounding_result=grounding_result)

        scores = (
            self.ats_scoring_service
            .calculate_scores(
                ats_profile
            )

        )

        analysis = (
            self.analysis_service
            .analyze_resume(
                ats_profile
            )

        )
        source_verification = (
            self.build_source_verification(
            grounding_result)
        )

        # 6. Build final ATS report
        report = self.build_report(scores=scores,analysis=analysis,source_verification=source_verification,)

        # 7. Store report in GraphState
        
        state["ats_report"] = report
        return state