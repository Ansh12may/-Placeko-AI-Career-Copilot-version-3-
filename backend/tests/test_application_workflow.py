"""
Resume Grounding + ATS Integration Tests

Tests:

1. Normal resume grounding integration
2. False extraction protection
3. Missing grounding failure
4. Empty grounding behavior
5. Full ResumeAnalysisAgent integration
"""

from backend.graphs.state import GraphState
from backend.Resume.schemas.candidate import CandidateProfile
from backend.ATS.agents.resume_analysis_agent import ResumeAnalysisAgent
from backend.Resume.services.grounding_service import GroundingService


# ============================================================
# TEST 1
# Normal Grounding
# ============================================================

def test_normal_grounding():

    print("\n==========================================")
    print("     TEST 1: NORMAL GROUNDING")
    print("==========================================")

    candidate = CandidateProfile(
        name="Ashutosh Kushwaha",
        skills=[
            "Python",
            "FastAPI",
            "React",
            "MongoDB",
        ],
    )

    resume_text = """
    Ashutosh Kushwaha

    Technical Skills:
    Python, FastAPI, React, MongoDB

    Projects:
    Placeko - AI Powered Job Intelligence Platform
    Technologies: Python, FastAPI, React

    TradeNova - Portfolio Risk Engine
    Technologies: Python, React
    """

    grounding_service = GroundingService()

    grounding_result = grounding_service.ground(
        candidate=candidate,
        resume_text=resume_text,
    )

    print("\nGrounded skills:")
    print(
        grounding_result["skills"]["grounded"]
    )

    print("\nUnresolved skills:")
    print(
        grounding_result["skills"]["unresolved"]
    )

    assert set(
        grounding_result["skills"]["grounded"]
    ) == {
        "Python",
        "FastAPI",
        "React",
        "MongoDB",
    }

    assert (
        grounding_result["skills"]["unresolved"]
        == []
    )

    print("\n✅ NORMAL GROUNDING PASSED")


# ============================================================
# TEST 2
# False Extraction Protection
# ============================================================

def test_false_extraction_protection():

    print("\n==========================================")
    print("     TEST 2: FALSE EXTRACTION")
    print("==========================================")

    candidate = CandidateProfile(
        name="Ashutosh Kushwaha",
        skills=[
            "Python",
            "FastAPI",
            "React",
            "Java",
            "Kubernetes",
        ],
    )

    resume_text = """
    Ashutosh Kushwaha

    Technical Skills:
    Python, FastAPI, React

    Projects:
    Placeko
    Technologies: Python, FastAPI, React
    """

    grounding_service = GroundingService()

    grounding_result = grounding_service.ground(
        candidate=candidate,
        resume_text=resume_text,
    )

    grounded_skills = (
        grounding_result["skills"]["grounded"]
    )

    unresolved_skills = (
        grounding_result["skills"]["unresolved"]
    )

    print("\nExtracted skills:")
    print(candidate.skills)

    print("\nGrounded skills:")
    print(grounded_skills)

    print("\nUnresolved skills:")
    print(unresolved_skills)

    assert grounded_skills == [
        "Python",
        "FastAPI",
        "React",
    ]

    assert unresolved_skills == [
        "Java",
        "Kubernetes",
    ]

    # Original profile must remain unchanged.

    assert candidate.skills == [
        "Python",
        "FastAPI",
        "React",
        "Java",
        "Kubernetes",
    ]

    agent = ResumeAnalysisAgent()

    ats_profile = agent.prepare_ats_profile(
        profile=candidate,
        grounding_result=grounding_result,
    )

    print("\nATS scoring skills:")
    print(ats_profile.skills)

    assert ats_profile.skills == [
        "Python",
        "FastAPI",
        "React",
    ]

    assert candidate.skills == [
        "Python",
        "FastAPI",
        "React",
        "Java",
        "Kubernetes",
    ]

    print(
        "\n✅ FALSE EXTRACTION PROTECTION PASSED"
    )


# ============================================================
# TEST 3
# Missing Grounding Must Fail
# ============================================================

def test_missing_grounding():

    print("\n==========================================")
    print("     TEST 3: MISSING GROUNDING")
    print("==========================================")

    candidate = CandidateProfile(
        name="Ashutosh Kushwaha",
        skills=[
            "Python",
            "FastAPI",
        ],
    )

    agent = ResumeAnalysisAgent()

    try:

        agent.prepare_ats_profile(
            profile=candidate,
            grounding_result=None,
        )

    except ValueError as error:

        print("\nExpected error:")
        print(error)

        assert (
            str(error)
            == "Grounding result not found in GraphState. "
               "ATS scoring requires source-grounded extraction."
        )

        print(
            "\n✅ MISSING GROUNDING TEST PASSED"
        )

        return

    raise AssertionError(
        "Expected ValueError when grounding_result is missing."
    )


# ============================================================
# TEST 4
# Empty Grounded Skills Are Valid
# ============================================================

def test_empty_grounding_is_valid():

    print("\n==========================================")
    print("     TEST 4: EMPTY GROUNDING")
    print("==========================================")

    candidate = CandidateProfile(
        name="Ashutosh Kushwaha",
        skills=[
            "Java",
            "Kubernetes",
        ],
    )

    grounding_result = {
        "skills": {
            "grounded": [],
            "unresolved": [
                "Java",
                "Kubernetes",
            ],
        },
        "projects": [],
    }

    agent = ResumeAnalysisAgent()

    ats_profile = agent.prepare_ats_profile(
        profile=candidate,
        grounding_result=grounding_result,
    )

    print("\nOriginal skills:")
    print(candidate.skills)

    print("\nATS scoring skills:")
    print(ats_profile.skills)

    assert ats_profile.skills == []

    assert candidate.skills == [
        "Java",
        "Kubernetes",
    ]

    print(
        "\n✅ EMPTY GROUNDING TEST PASSED"
    )


# ============================================================
# TEST 5
# Full ResumeAnalysisAgent Integration
# ============================================================

def test_resume_analysis_agent_uses_grounded_profile():

    print("\n==========================================")
    print("     TEST 5: FULL ATS INTEGRATION")
    print("==========================================")

    # --------------------------------------------------------
    # Simulate an LLM extraction containing an unsupported
    # skill.
    # --------------------------------------------------------

    candidate = CandidateProfile(
        name="Ashutosh Kushwaha",
        skills=[
            "Python",
            "FastAPI",
            "React",
            "Java",
        ],
    )

    resume_text = """
    Ashutosh Kushwaha

    Technical Skills:
    Python, FastAPI, React

    Projects:
    Placeko
    Technologies: Python, FastAPI, React
    """

    # --------------------------------------------------------
    # Generate grounding result.
    # --------------------------------------------------------

    grounding_service = GroundingService()

    grounding_result = grounding_service.ground(
        candidate=candidate,
        resume_text=resume_text,
    )

    print("\nGrounding result:")
    print(grounding_result)

    assert grounding_result["skills"]["grounded"] == [
        "Python",
        "FastAPI",
        "React",
    ]

    assert grounding_result["skills"]["unresolved"] == [
        "Java",
    ]

    # --------------------------------------------------------
    # Build GraphState.
    # --------------------------------------------------------

    state: GraphState = {
        "messages": [],
        "resume_path": None,
        "resume_text": resume_text,
        "candidate_profile": candidate,

        "grounding_result": grounding_result,

        "jobs": None,
        "ranked_jobs": None,
        "recommended_jobs": None,
        "selected_job": None,

        "interview_session": None,

        "next_node": None,
        "error": None,

        "ats_report": None,

        "application_id": None,
        "application_status": None,
        "application_materials": None,
        "human_approval": None,
        "application_result": None,
        "application_thread_id": None,

        "workflow_type": None,
    }

    # --------------------------------------------------------
    # Create agent.
    # --------------------------------------------------------

    agent = ResumeAnalysisAgent()

    # --------------------------------------------------------
    # Fake ATS scoring service.
    #
    # The fake output MUST match the real ATSScoringService
    # contract expected by ATSReport.
    # --------------------------------------------------------

    captured_profile = {}

    def fake_calculate_scores(
        profile: CandidateProfile,
    ):

        captured_profile["profile"] = profile

        return {
            "candidate_level": "fresher",

            "overall_score": 80,

            "contact_information": {
                "score": 10,
                "max_score": 10,
            },

            "education": {
                "score": 10,
                "max_score": 10,
            },

            "experience": {
                "score": 0,
                "max_score": 0,
            },

            "projects": {
                "score": 10,
                "max_score": 15,
            },

            "skills": {
                "score": 10,
                "max_score": 15,
            },

            "certifications": {
                "score": 10,
                "max_score": 10,
            },

            "formatting": {
                "score": 10,
                "max_score": 10,
            },

            "summary": {
                "score": 10,
                "max_score": 15,
            },
        }

    agent.ats_scoring_service.calculate_scores = (
        fake_calculate_scores
    )

    # --------------------------------------------------------
    # Fake qualitative analysis service.
    #
    # We are testing orchestration, not the LLM.
    # --------------------------------------------------------

    def fake_analyze_resume(
        profile: CandidateProfile,
    ):

        return {
            "strengths": [],
            "weaknesses": [],
            "missing_keywords": [],

            "formatting_feedback": [],
            "education_feedback": [],
            "experience_feedback": [],
            "project_feedback": [],
            "skills_feedback": [],

            "recommendations": [],
        }

    agent.analysis_service.analyze_resume = (
        fake_analyze_resume
    )

    # --------------------------------------------------------
    # Run the ACTUAL ResumeAnalysisAgent pipeline.
    # --------------------------------------------------------

    result_state = agent.run(state)

    # --------------------------------------------------------
    # Verify ATS scoring received grounded profile.
    # --------------------------------------------------------

    scored_profile = captured_profile.get(
        "profile"
    )

    assert scored_profile is not None

    print(
        "\nOriginal CandidateProfile skills:"
    )
    print(candidate.skills)

    print(
        "\nProfile received by ATSScoringService:"
    )
    print(scored_profile.skills)

    # --------------------------------------------------------
    # Java must NOT reach ATS scoring.
    # --------------------------------------------------------

    assert scored_profile.skills == [
        "Python",
        "FastAPI",
        "React",
    ]

    assert "Java" not in scored_profile.skills

    # --------------------------------------------------------
    # Original CandidateProfile must remain untouched.
    # --------------------------------------------------------

    assert candidate.skills == [
        "Python",
        "FastAPI",
        "React",
        "Java",
    ]

    # --------------------------------------------------------
    # Verify ATS report was successfully produced.
    # --------------------------------------------------------

    report = result_state["ats_report"]

    assert report is not None

    print("\nATS report created:")
    print(report)

    # --------------------------------------------------------
    # Verify report values.
    # --------------------------------------------------------

    assert report.candidate_level.value == "fresher"

    assert report.overall_score == 80

    assert report.skills.score == 10
    assert report.skills.max_score == 15

    assert report.projects.score == 10
    assert report.projects.max_score == 15

    print(
        "\n✅ FULL ATS INTEGRATION PASSED"
    )

# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("##########################################")
    print("#     RESUME GROUNDING TEST SUITE       #")
    print("##########################################")

    test_normal_grounding()

    test_false_extraction_protection()

    test_missing_grounding()

    test_empty_grounding_is_valid()

    test_resume_analysis_agent_uses_grounded_profile()

    print("\n")
    print("==========================================")
    print("       ✅ ALL TESTS PASSED")
    print("==========================================")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()