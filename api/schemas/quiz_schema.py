from pydantic import BaseModel


# -----------------------------
# MCQ Generation
# -----------------------------

class MCQGenerationRequest(
    BaseModel
):

    topic: str

    difficulty: str = "beginner"


class MCQGenerationResponse(
    BaseModel
):

    topic: str

    difficulty: str

    mcqs: str

    sources: list


# -----------------------------
# Answer Evaluation
# -----------------------------

class EvaluationRequest(
    BaseModel
):

    question: str

    student_answer: str

    correct_answer: str

    concept: str


class EvaluationResponse(
    BaseModel
):

    concept: str

    question: str

    student_answer: str

    correct_answer: str

    is_correct: bool

    evaluation: str