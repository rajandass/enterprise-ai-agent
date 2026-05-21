from pydantic import BaseModel


class TutorRequest(BaseModel):

    question: str


class TutorResponse(BaseModel):

    question: str

    answer: str

    sources: list