"""
Interview Controller

Exposes REST endpoints for the Interview module.

Responsibilities
----------------
- Authenticate the current user
- Validate incoming requests
- Invoke InterviewService
- Return structured responses

Contains NO business logic.
"""

from fastapi import (

    APIRouter,

    Depends,

    HTTPException,

    status,

    UploadFile,

    File,

    Form,

)

from backend.auth.dependency.auth_dependency import (
    get_current_user,
)

from backend.Interview.services.interview_service import (
    InterviewService,
)

from backend.Interview.schemas.interview_request import (
    InterviewRequest,
)

from backend.Interview.schemas.interview_answer import (
    InterviewAnswer,
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/interview",
    tags=["Interview"],
)

interview_service = InterviewService()


# =========================================================
# START INTERVIEW
# =========================================================

@router.post("/start")
async def start_interview(
    request: InterviewRequest,
    current_user=Depends(get_current_user),
):
    """
    Start a new personalized interview.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        session = await interview_service.start_interview(
            request=request,
            user_id=user_id,
        )

        return {
            "success": True,
            "data": session,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# SUBMIT ANSWER
# =========================================================

@router.post("/answer/{session_id}")
async def submit_answer(
    session_id: str,
    answer: InterviewAnswer,
    current_user=Depends(get_current_user),
):
    """
    Submit an answer for the current question.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        session = await interview_service.submit_answer(
            session_id=session_id,
            answer=answer,
            user_id=user_id,
        )

        return {
            "success": True,
            "data": session,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# FINISH INTERVIEW
# =========================================================

@router.post("/finish/{session_id}")
async def finish_interview(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Finish an interview and generate the final report.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        report = await interview_service.finish_interview(
            session_id=session_id,
            user_id=user_id,
        )

        return {
            "success": True,
            "data": report,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# GET SESSION
# =========================================================

@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Retrieve an interview session belonging
    to the authenticated user.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        session = await interview_service.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        return {
            "success": True,
            "data": session,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# CURRENT QUESTION
# =========================================================

@router.get("/question/{session_id}")
async def current_question(
    session_id: str,
    current_user=Depends(get_current_user),
):
    """
    Retrieve the current interview question.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        question = await interview_service.get_current_question(
            session_id=session_id,
            user_id=user_id,
        )

        return {
            "success": True,
            "data": question,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# =========================================================
# INTERVIEW HISTORY
# =========================================================

@router.get("/history")
async def get_interview_history(
    current_user=Depends(get_current_user),
):
    """
    Retrieve all interview sessions belonging
    to the authenticated user.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        sessions = await interview_service.get_interview_history(
            user_id=user_id,
        )

        return {
            "success": True,
            "data": sessions,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )





# =========================================================
# SUBMIT VOICE ANSWER
# =========================================================

@router.post("/voice/{session_id}")
async def submit_voice_answer(
    session_id: str,
    question_id: int = Form(...),
    audio: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    """
    Submit a voice answer for the current interview question.
    """

    try:

        user_id = str(
            current_user["_id"]
        )

        audio_bytes = await audio.read()

        if not audio_bytes:
            raise ValueError(
                "Audio file is empty."
            )

        session = await interview_service.submit_voice_answer(
            session_id=session_id,
            question_id=question_id,
            audio_bytes=audio_bytes,
            filename=audio.filename or "answer.webm",
            user_id=user_id,
        )

        return {
            "success": True,
            "data": session,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )