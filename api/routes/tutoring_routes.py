from fastapi import (
    APIRouter,
    Depends
)

from api.dependencies.auth import (
    verify_api_key
)
import logging

logger = logging.getLogger(__name__)

from api.schemas.tutoring_schema import (
    TutorRequest,
    TutorResponse
)

from services.tutoring.tutor_service import (
    generate_tutor_response
)

router = APIRouter()


@router.post(
    "/tutor/chat",
    response_model=TutorResponse
)
def tutor_chat(
    request: TutorRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Educational tutoring endpoint.
    """

    response = generate_tutor_response(
        request.question
    )

    return response