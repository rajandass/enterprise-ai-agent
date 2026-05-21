from pydantic import BaseModel


class StudentMemoryRequest(
    BaseModel
):

    student_memory: dict


class DashboardResponse(
    BaseModel
):

    overall_accuracy: float

    readiness: str

    mastery_report: dict

    revision_queue: list

    weak_concepts: list

    total_questions: int

    total_correct: int


class MasteryResponse(
    BaseModel
):

    mastery_report: dict


class RevisionQueueResponse(
    BaseModel
):

    revision_queue: list