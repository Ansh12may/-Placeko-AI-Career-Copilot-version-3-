"""
Resume Agent

Responsible for:
- Reading the resume path from GraphState
- Parsing the resume
- Invoking the LLM for structured extraction
- Validating the CandidateProfile
- Updating GraphState

This agent performs resume understanding only.

It does NOT:
- Store resumes in MongoDB
- Calculate ATS scores
- Search for jobs
- Perform job ranking
"""

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from backend.utils.base_agent import BaseAgent
from backend.graphs.state import GraphState
from backend.config.settings import settings

from backend.Resume.prompts.resume_prompt import (
    RESUME_SYSTEM_PROMPT,
)

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.Resume.tools.resume_parser import (
    parse_resume,
)


class ResumeAgent(BaseAgent):
    """
    AI Agent responsible for understanding
    a candidate's resume.

    Workflow:

        GraphState
            ↓
        Resume Path
            ↓
        Parse Resume
            ↓
        Extract Resume Text
            ↓
        Invoke LLM
            ↓
        CandidateProfile
            ↓
        Update GraphState
    """

    def __init__(self):
        super().__init__()

        self.llm = settings.llm

        self.system_prompt = RESUME_SYSTEM_PROMPT

    # =========================================================
    # Prepare Input
    # =========================================================

    def prepare_input(
        self,
        state: GraphState,
    ) -> str:
        """
        Extract resume path from GraphState.
        """

        resume_path = state.get("resume_path")

        if not resume_path:
            raise ValueError(
                "Resume path not found in GraphState."
            )

        return resume_path

    # =========================================================
    # Resume Parser
    # =========================================================

    def invoke_tools(
        self,
        resume_path: str,
    ) -> str:
        """
        Parse the resume and extract text.
        """

        resume_text = parse_resume(resume_path)

        if not resume_text:
            raise ValueError(
                "Could not extract text from resume."
            )

        return resume_text

    # =========================================================
    # LLM Extraction
    # =========================================================

    def invoke_llm(
    self,
    resume_text: str,
) -> CandidateProfile:
        """
        Extract candidate information from the resume.

        The LLM returns JSON.
        The result is normalized to the existing
        CandidateProfile schema before Pydantic validation.
        """

        messages = [
            SystemMessage(
                content=self.system_prompt
                + """

    IMPORTANT:

    Return ONLY valid JSON.

    Use EXACTLY these CandidateProfile fields:

    {
        "name": null,
        "email": null,
        "phone": null,
        "summary": null,
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "linkedin": null,
        "github": null
    }

    For every project use EXACTLY:

    {
        "title": "",
        "technologies": [],
        "description": ""
    }

    Do NOT use "name" for a project.

    For certifications use ONLY strings.

    Correct:

    "certifications": [
        "Improving Deep Neural Networks - DeepLearning.AI",
        "Algorithmic Toolbox - Coursera"
    ]

    Incorrect:

    "certifications": [
        {
            "name": "...",
            "issuer": "...",
            "description": "..."
        }
    ]

    IMPORTANT EXPERIENCE RULE:

    Projects are NOT professional experience.

    If the resume contains projects such as Placeko,
    WanderNest, academic projects, personal projects,
    or technical projects, they MUST go into "projects".

    If there is no actual employment/internship experience,
    return:

    "experience": []

    Return JSON only.
    """
            ),
            HumanMessage(
                content=resume_text
            ),
        ]

        # -----------------------------------------------------
        # Ask Groq for JSON
        # -----------------------------------------------------

        response = self.llm.invoke(messages)

        # -----------------------------------------------------
        # Parse JSON
        # -----------------------------------------------------

        import json

        content = response.content

        if not isinstance(content, str):
            raise ValueError(
                "LLM returned non-string content."
            )
        content = content.strip()
        if content.startswith("{") and not content.endswith("}"):
            content += "}"

        try:
            data = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"LLM returned invalid JSON: {error}"
            ) from error

        # -----------------------------------------------------
        # Normalize projects
        # -----------------------------------------------------

        projects = data.get("projects", [])

        normalized_projects = []

        for project in projects:

            if not isinstance(project, dict):
                continue

            title = project.get("title")

            # Handle LLM occasionally returning "name"
            if not title:
                title = project.get("name")

            normalized_projects.append(
                {
                    "title": title or "Untitled Project",
                    "technologies": project.get(
                        "technologies",
                        [],
                    ),
                    "description": project.get(
                        "description"
                    ),
                }
            )

        data["projects"] = normalized_projects

        # -----------------------------------------------------
        # Normalize certifications
        # -----------------------------------------------------

        certifications = data.get(
            "certifications",
            [],
        )

        normalized_certifications = []

        for certification in certifications:

            # Correct format
            if isinstance(
                certification,
                str,
            ):
                normalized_certifications.append(
                    certification
                )
                continue

            # Handle LLM returning certification object
            if isinstance(
                certification,
                dict,
            ):

                name = certification.get(
                    "name",
                    "",
                )

                issuer = certification.get(
                    "issuer",
                    "",
                )

                if name and issuer:
                    normalized_certifications.append(
                        f"{name} - {issuer}"
                    )

                elif name:
                    normalized_certifications.append(
                        name
                    )

        data["certifications"] = (
            normalized_certifications
        )

        # -----------------------------------------------------
        # Normalize education
        # -----------------------------------------------------

        education = data.get(
            "education",
            [],
        )

        normalized_education = []

        for item in education:

            if not isinstance(item, dict):
                continue

            normalized_education.append(
                {
                    "institution": item.get(
                        "institution",
                        "",
                    ),
                    "degree": item.get(
                        "degree",
                        "",
                    ),
                    "year": item.get(
                        "year",
                        item.get("duration"),
                    ),
                }
            )

        data["education"] = normalized_education

        # -----------------------------------------------------
        # Normalize experience
        # -----------------------------------------------------

        experience = data.get(
            "experience",
            [],
        )

        if not isinstance(
            experience,
            list,
        ):
            data["experience"] = []

        # -----------------------------------------------------
        # Final Pydantic validation
        # -----------------------------------------------------

        candidate = CandidateProfile.model_validate(
            data
        )

        return candidate
    # =========================================================
    # Validation
    # =========================================================

    def validate(
        self,
        candidate: CandidateProfile,
    ) -> CandidateProfile:
        """
        CandidateProfile is already validated
        through Pydantic.
        """

        if candidate is None:
            raise ValueError(
                "Resume extraction returned no candidate profile."
            )

        return candidate

    # =========================================================
    # Update Graph State
    # =========================================================

    def update_state(
        self,
        state: GraphState,
        resume_text: str,
        candidate: CandidateProfile,
    ) -> GraphState:
        """
        Store parsed resume text and structured
        candidate profile in GraphState.
        """

        state["resume_text"] = resume_text
        state["candidate_profile"] = candidate

        return state

    # =========================================================
    # Run Agent
    # =========================================================

    def run(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the complete resume analysis step.
        """

        # 1. Get resume path
        resume_path = self.prepare_input(state)

        # 2. Parse resume
        resume_text = self.invoke_tools(resume_path)

        # 3. Extract CandidateProfile
        candidate = self.invoke_llm(resume_text)

        # 4. Validate
        candidate = self.validate(candidate)

        # 5. Update state
        state = self.update_state(
            state,
            resume_text,
            candidate,
        )

        return state