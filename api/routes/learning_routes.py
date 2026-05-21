from fastapi import (
    APIRouter,
    Depends
)

from api.dependencies.auth import (
    verify_api_key
)

import logging

logger = logging.getLogger(__name__)

from api.schemas.learning_schema import (
    StudentMemoryRequest,
    DashboardResponse,
    MasteryResponse,
    RevisionQueueResponse
)

from services.learning.dashboard_service import (
    generate_student_dashboard
)

from services.learning.mastery_service import (
    generate_mastery_report
)

from services.learning.spaced_repetition_service import (
    generate_revision_queue
)

router = APIRouter()


# ---------------------------------
# Student Dashboard
# ---------------------------------

@router.post(
    "/student/dashboard",
    response_model=DashboardResponse
)
def student_dashboard(
    request: StudentMemoryRequest,
    api_key: str = Depends(verify_api_key)
):

    """
    Generate student dashboard.
    """

    response = (
        generate_student_dashboard(
            request.student_memory
        )
    )

    return response


# ---------------------------------
# Mastery Analytics
# ---------------------------------

@router.post(
    "/student/mastery",
    response_model=MasteryResponse
)
def mastery_report(
    request: StudentMemoryRequest,
    api_key: str = Depends(verify_api_key)
):

    """
    Generate mastery report.
    """

    quiz_history = (
        request
        .student_memory[
            "quiz_history"
        ]
    )

    mastery = (
        generate_mastery_report(
            quiz_history
        )
    )

    return {
        "mastery_report":
            mastery
    }


# ---------------------------------
# Revision Queue
# ---------------------------------

@router.post(
    "/student/revision-queue",
    response_model=RevisionQueueResponse
)
def revision_queue(
    request: StudentMemoryRequest,
    api_key: str = Depends(verify_api_key)
):

    """
    Generate revision queue.
    """

    quiz_history = (
        request
        .student_memory[
            "quiz_history"
        ]
    )

    queue = (
        generate_revision_queue(
            quiz_history
        )
    )

    return {
        "revision_queue":
            queue
    }