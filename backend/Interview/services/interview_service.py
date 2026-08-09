"""
Interview Service

Application service responsible for orchestrating the
complete interview lifecycle.

Responsibilities
----------------
- Start interviews
- Load candidate resume
- Manage interview sessions
- Generate questions
- Retrieve current question
- Submit and evaluate answers
- Finish interviews
- Generate final interview reports

This service coordinates repositories, agents, and
domain services.

It contains NO LLM reasoning.
"""

from datetime import datetime
from typing import Optional

from backend.Resume.schemas.candidate import (
    CandidateProfile,
)

from backend.Resume.repositories.resume_repository import (
    ResumeRepository,
)

from backend.Jobs.schemas.job import Job

from backend.Interview.schemas.interview_request import (
    InterviewRequest,
)

from backend.Interview.schemas.interview_plan import (
    InterviewMode,
    DifficultyLevel,
    InterviewPlan,
)

from backend.Interview.schemas.interview_question import (
    InterviewQuestion,
)

from backend.Interview.schemas.interview_session import (
    InterviewSession,
    InterviewStatus,
)

from backend.Interview.schemas.interview_answer import (
    InterviewAnswer,
)

from backend.Interview.schemas.interview_report import (
    InterviewReport,
)

from backend.Interview.schemas.question_answer_pair import (
    QuestionAnswerPair,
)

from backend.Interview.agents.interview_planner_agent import (
    InterviewPlannerAgent,
)

from backend.Interview.agents.question_generator_agent import (
    QuestionGeneratorAgent,
)

from backend.Interview.agents.answer_evaluation_agent import (
    AnswerEvaluationAgent,
)

from backend.Interview.agents.interview_report_agent import (
    InterviewReportAgent,
)

from backend.Interview.services.interview_flow_service import (
    InterviewFlowService,
)

from backend.Interview.session.session_manager import (
    InterviewSessionManager,
)
from backend.Interview.services.voice_service import (
    VoiceService,

)


class InterviewService:
    """
    Application service responsible for coordinating
    the interview workflow.
    """

    def __init__(self):

        self.resume_repository = ResumeRepository()

        self.planner_agent = InterviewPlannerAgent()

        self.question_agent = QuestionGeneratorAgent()

        self.evaluation_agent = AnswerEvaluationAgent()

        self.report_agent = InterviewReportAgent()

        self.flow_service = InterviewFlowService()

        self.session_manager = InterviewSessionManager()

        self.voice_service = VoiceService()

    # =========================================================
    # START INTERVIEW
    # =========================================================

    async def start_interview(
        self,
        request: InterviewRequest,
        user_id: str,
    ) -> InterviewSession:
        """
        Create a new personalized interview session.
        """

        # -----------------------------------------------------
        # 1. Load requested resume
        # -----------------------------------------------------

        resume = (
            await self.resume_repository.get_resume_by_id(
                resume_id=request.resume_id,
                user_id=user_id,
            )
        )

        if not resume:
            raise ValueError(
                "Resume not found."
            )

        # -----------------------------------------------------
        # 2. Extract candidate profile
        # -----------------------------------------------------

        candidate_profile_data = resume.get(
            "candidate_profile"
        )

        if not candidate_profile_data:
            raise ValueError(
                "Candidate profile not found for this resume."
            )

        candidate_profile = (
            CandidateProfile.model_validate(
                candidate_profile_data
            )
        )

        # -----------------------------------------------------
        # 3. Convert interview configuration
        # -----------------------------------------------------

        interview_mode = InterviewMode(
            request.interview_type.value.capitalize()
        )

        difficulty = DifficultyLevel(
            request.difficulty.value.capitalize()
        )

        # -----------------------------------------------------
        # 4. Build optional target job
        # -----------------------------------------------------

        job: Optional[Job] = None

        if request.job_description:

            job = Job(
                title="Target Role",
                company="Target Company",
                location="Not specified",
                description=request.job_description,
                source="user-provided",
            )

        elif request.job_id:

            raise ValueError(
                "job_id is not supported yet because jobs are "
                "not currently persisted in a repository. "
                "Please provide job_description instead."
            )

        # -----------------------------------------------------
        # 5. Generate Interview Plan
        # -----------------------------------------------------

        planner_state = {
            "candidate_profile": candidate_profile,
            "selected_job": job,
            "interview_mode": interview_mode,
            "difficulty": difficulty,
        }

        planner_state = self.planner_agent.run(
            planner_state
        )

        interview_plan = planner_state.get(
            "interview_plan"
        )

        if interview_plan is None:
            raise ValueError(
                "Failed to generate interview plan."
            )

        # -----------------------------------------------------
        # 6. Normalize question count
        # -----------------------------------------------------

        interview_plan = self._normalize_question_count(
            plan=interview_plan,
            num_questions=request.num_questions,
            interview_mode=interview_mode,
            include_projects=request.include_projects,
            include_behavioral=request.include_behavioral,
        )

        # -----------------------------------------------------
        # 7. Create Interview Session
        # -----------------------------------------------------

        session = InterviewSession(
            user_id=user_id,
            resume_id=request.resume_id,
            candidate=candidate_profile,
            target_job=job,
            interview_plan=interview_plan,
            status=InterviewStatus.IN_PROGRESS,
            started_at=datetime.utcnow(),
        )

        # -----------------------------------------------------
        # 8. Generate First Question
        # -----------------------------------------------------

        category = self.flow_service.next_category(
            session
        )

        question_state = {
            "candidate_profile": candidate_profile,
            "selected_job": job,
            "interview_plan": interview_plan,
            "question_number": 1,
            "current_category": category,
            "previous_questions": [],
        }

        question_state = self.question_agent.run(
            question_state
        )

        current_question = question_state.get(
            "current_question"
        )

        if current_question is None:
            raise ValueError(
                "Failed to generate the first interview question."
            )

        session.history.append(
            QuestionAnswerPair(
                question=current_question
            )
        )

        session.current_question_index = 0

        # -----------------------------------------------------
        # 9. Persist Session
        # -----------------------------------------------------

        await self.session_manager.create_session(
            session
        )

        return session

    # =========================================================
    # NORMALIZE QUESTION COUNT
    # =========================================================

    def _normalize_question_count(
        self,
        plan: InterviewPlan,
        num_questions: int,
        interview_mode: InterviewMode,
        include_projects: bool,
        include_behavioral: bool,
    ) -> InterviewPlan:

        if interview_mode == InterviewMode.TECHNICAL:

            return plan.model_copy(
                update={
                    "technical_questions": num_questions,
                    "project_questions": 0,
                    "behavioral_questions": 0,
                }
            )

        if interview_mode == InterviewMode.BEHAVIORAL:

            return plan.model_copy(
                update={
                    "technical_questions": 0,
                    "project_questions": 0,
                    "behavioral_questions": num_questions,
                }
            )

        if interview_mode == InterviewMode.PROJECT:

            return plan.model_copy(
                update={
                    "technical_questions": 0,
                    "project_questions": num_questions,
                    "behavioral_questions": 0,
                }
            )

        if not include_projects and not include_behavioral:

            return plan.model_copy(
                update={
                    "technical_questions": num_questions,
                    "project_questions": 0,
                    "behavioral_questions": 0,
                }
            )

        if not include_projects:

            behavioral_questions = num_questions // 3

            technical_questions = (
                num_questions - behavioral_questions
            )

            return plan.model_copy(
                update={
                    "technical_questions": technical_questions,
                    "project_questions": 0,
                    "behavioral_questions": behavioral_questions,
                }
            )

        if not include_behavioral:

            project_questions = num_questions // 3

            technical_questions = (
                num_questions - project_questions
            )

            return plan.model_copy(
                update={
                    "technical_questions": technical_questions,
                    "project_questions": project_questions,
                    "behavioral_questions": 0,
                }
            )

        technical_questions = num_questions // 2

        project_questions = num_questions // 4

        behavioral_questions = (
            num_questions
            - technical_questions
            - project_questions
        )

        return plan.model_copy(
            update={
                "technical_questions": technical_questions,
                "project_questions": project_questions,
                "behavioral_questions": behavioral_questions,
            }
        )

    # =========================================================
    # GET SESSION
    # =========================================================

    async def get_session(
        self,
        session_id: str,
        user_id: str,
    ) -> InterviewSession:
        """
        Retrieve an interview session belonging
        to the authenticated user.
        """

        return await self.session_manager.get_session(
            session_id=session_id,
            user_id=user_id,
        )

    # =========================================================
    # CURRENT QUESTION
    # =========================================================

    async def get_current_question(
        self,
        session_id: str,
        user_id: str,
    ) -> InterviewQuestion:
        """
        Return the current interview question.
        """

        session = await self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        if not session.history:
            raise ValueError(
                "Interview session contains no questions."
            )

        return session.history[
            session.current_question_index
        ].question

# =========================================================

# INTERVIEW HISTORY

# =========================================================

    async def get_interview_history(

        self,

        user_id: str,

    ) -> list[InterviewSession]:

        """

        Retrieve all interview sessions belonging

        to the authenticated user.

        """

        return await self.session_manager.list_sessions(

            user_id=user_id,

        )

    # =========================================================
    # SUBMIT ANSWER
    # =========================================================

    async def submit_answer(
            self,
            session_id: str,
            answer: InterviewAnswer,
            user_id: str,
        ) -> InterviewSession:
            """
            Store the candidate's answer, evaluate it,
            and generate the next question if required.
            """

        # -----------------------------------------------------
        # 1. Retrieve Session
        # -----------------------------------------------------

            session = await self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        # -----------------------------------------------------
        # 2. Validate Interview Status
        # -----------------------------------------------------

            if session.status != InterviewStatus.IN_PROGRESS:
                raise ValueError(
                "Interview is not currently in progress."
            )

        # -----------------------------------------------------
        # 3. Validate Current Question
        # -----------------------------------------------------

            if not session.history:
                raise ValueError(
                    "Interview session contains no questions."
                )

            pair = session.history[
                session.current_question_index
            ]

            if answer.question_id != pair.question.question_id:
                raise ValueError(
                    "Answer does not belong to the current question."
                )

            # -----------------------------------------------------
            # 4. Prevent Duplicate Answer
            # -----------------------------------------------------

            if pair.answer is not None:
                raise ValueError(
                    "The current question has already been answered."
                )

            # -----------------------------------------------------
            # 5. Store Candidate Answer
            # -----------------------------------------------------

            pair.answer = answer

            # -----------------------------------------------------
            # 6. Evaluate Answer
            # -----------------------------------------------------

            session = self.evaluation_agent.run(
                session
            )




            

            # -----------------------------------------------------
            # 7. Check Interview Completion
            # -----------------------------------------------------

            if self.flow_service.is_interview_complete(
                session
            ):

                session.status = (
                    InterviewStatus.COMPLETED
                )

                session.ended_at = datetime.utcnow()

                await self.session_manager.update_session(
                    session
                )

                return session

            # -----------------------------------------------------
            # 8. Determine Next Question Category
            # -----------------------------------------------------

            category = self.flow_service.next_category(
                session
            )

            # -----------------------------------------------------
            # 9. Generate Next Question
            # -----------------------------------------------------

            question_state = {
                "candidate_profile": session.candidate,
                "selected_job": session.target_job,
                "interview_plan": session.interview_plan,
                "question_number": len(session.history) + 1,
                "current_category": category,
                "previous_questions": [
                    pair.question.question
                    for pair in session.history
                ],
            }

            question_state = self.question_agent.run(
                question_state
            )

            next_question = question_state.get(
                "current_question"
            )

            if next_question is None:
                raise ValueError(
                    "Failed to generate the next interview question."
                )

            # -----------------------------------------------------
            # 10. Append Next Question
            # -----------------------------------------------------

            session.history.append(
                QuestionAnswerPair(
                    question=next_question
                )
            )

            session.current_question_index = (
                len(session.history) - 1
            )

            # -----------------------------------------------------
            # 11. Persist Updated Session
            # -----------------------------------------------------

            await self.session_manager.update_session(
                session
            )

            return session


    # =========================================================
    # SUBMIT VOICE ANSWER
    # =========================================================
    async def submit_voice_answer(
        self,
        session_id: str,
        question_id: int,
        audio_bytes: bytes,
        filename: str,
        user_id: str,
    ) -> InterviewSession:
        """
        Process a voice answer.

        Flow:

        Audio
            ↓
        VoiceService
            ↓
        Transcript + Voice Metadata
            ↓
        InterviewAnswer
            ↓
        Existing submit_answer()
            ↓
        Answer Evaluation
            ↓
        Next Question / Completion
        """

        # -----------------------------------------------------
        # 1. Retrieve current session
        # -----------------------------------------------------

        session = await self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        # -----------------------------------------------------
        # 2. Validate interview status
        # -----------------------------------------------------

        if session.status != InterviewStatus.IN_PROGRESS:
            raise ValueError(
                "Interview is not currently in progress."
            )

        # -----------------------------------------------------
        # 3. Validate current question
        # -----------------------------------------------------

        if not session.history:
            raise ValueError(
                "Interview session contains no questions."
            )

        pair = session.history[
            session.current_question_index
        ]

        if question_id != pair.question.question_id:
            raise ValueError(
                "Answer does not belong to the current question."
            )

        # -----------------------------------------------------
        # 4. Prevent duplicate answer
        # -----------------------------------------------------

        if pair.answer is not None:
            raise ValueError(
                "The current question has already been answered."
            )

        # -----------------------------------------------------
        # 5. Process audio
        # -----------------------------------------------------

        voice_result = await self.voice_service.process_audio(
            audio_bytes=audio_bytes,
            filename=filename,
        )

        transcript = voice_result.get(
            "transcript",
            "",
        ).strip()

        if not transcript:
            raise ValueError(
                "Could not extract speech from the audio."
            )

        # -----------------------------------------------------
        # 6. Convert voice result into InterviewAnswer
        # -----------------------------------------------------

        answer = InterviewAnswer(
            question_id=question_id,

            transcript=transcript,

            source="Voice",

            duration_seconds=voice_result[
                "audio_duration"
            ],

            metadata={
                "audio_duration": voice_result[
                    "audio_duration"
                ],

                "word_count": voice_result[
                    "word_count"
                ],

                "speech_rate": voice_result[
                    "speech_rate"
                ],
            },
        )

        # -----------------------------------------------------
        # 7. Reuse existing answer pipeline
        # -----------------------------------------------------

        return await self.submit_answer(
            session_id=session_id,
            answer=answer,
            user_id=user_id,
        )









    

        # =========================================================
        # FINISH INTERVIEW
        # =========================================================

    async def finish_interview(
            self,
            session_id: str,
            user_id: str,
        ) -> InterviewReport:
            """
            Generate and persist the final interview report.
            """

            # -----------------------------------------------------
            # 1. Retrieve Session
            # -----------------------------------------------------

            session = await self.get_session(
                session_id=session_id,
                user_id=user_id,
            )

            # -----------------------------------------------------
            # 2. Validate Interview Status
            # -----------------------------------------------------

            if session.status != InterviewStatus.COMPLETED:
                raise ValueError(
                    "Interview has not been completed yet."
                )

            # -----------------------------------------------------
            # 3. Generate Report
            # -----------------------------------------------------

            session = self.report_agent.run(
                session
            )

            # -----------------------------------------------------
            # 4. Persist Updated Session + Report
            # -----------------------------------------------------

            await self.session_manager.update_session(
                session
            )

            # -----------------------------------------------------
            # 5. Validate Report
            # -----------------------------------------------------

            if session.report is None:
                raise ValueError(
                    "Failed to generate interview report."
                )

            return session.report



    

