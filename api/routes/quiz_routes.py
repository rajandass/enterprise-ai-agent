from fastapi import (
    APIRouter,
    Depends
)

from api.dependencies.auth import (
    verify_api_key
)
import logging

logger = logging.getLogger(__name__)

from api.schemas.quiz_schema import (
    MCQGenerationRequest,
    MCQGenerationResponse,
    EvaluationRequest,
    EvaluationResponse
)

from services.tutoring.mcq_service import (
    generate_mcqs
)

from services.tutoring.evaluation_service import (
    evaluate_student_answer
)

router = APIRouter()


# ---------------------------------
# Generate MCQs
# ---------------------------------

@router.post(
    "/quiz/generate",
    response_model=MCQGenerationResponse
)
def generate_quiz(
    request: MCQGenerationRequest,
    api_key: str = Depends(verify_api_key)
):

    """
    Generate adaptive MCQs.
    """

    response = generate_mcqs(
        topic=request.topic,
        difficulty=request.difficulty
    )

    return response


# ---------------------------------
# Evaluate Student Answer
# ---------------------------------

@router.post(
    "/quiz/evaluate",
    response_model=EvaluationResponse
)
def evaluate_answer(
    request: EvaluationRequest,
    api_key: str = Depends(verify_api_key)

):

    """
    Evaluate student answer.
    """

    response = evaluate_student_answer(

        question=request.question,

        student_answer=(
            request.student_answer
        ),

        correct_answer=(
            request.correct_answer
        ),

        concept=request.concept
    )

    return response