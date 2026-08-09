"""
Interview Report Agent

Responsible for generating the final interview report
after the interview has been completed.

Responsibilities
----------------
- Validate interview completion
- Invoke InterviewReportService
- Attach the generated report to the InterviewSession
- Return the updated InterviewSession

This agent contains NO business logic.
"""

from backend.Interview.schemas.interview_session import (
    InterviewSession,
    InterviewStatus,
)

from backend.Interview.services.interview_report_service import (
    InterviewReportService,
)


class InterviewReportAgent:
    """
    Generates and attaches the final interview report.
    """

    def __init__(self):
        self.report_service = InterviewReportService()

    # ---------------------------------------------------------

    def run(
        self,
        session: InterviewSession,
    ) -> InterviewSession:
        """
        Generate and attach the final interview report.
        """

        if session.status != InterviewStatus.COMPLETED:
            raise ValueError(
                "Interview must be completed before generating a report."
            )

        report = self.report_service.generate_report(
            session=session
        )

        if report is None:
            raise ValueError(
                "Failed to generate interview report."
            )

        session.report = report

        return session