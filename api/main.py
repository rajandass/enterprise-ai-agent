from fastapi import FastAPI
from pydantic import BaseModel

from pipelines.query  import ask_question

app = FastAPI(title="Enterprise AI Support Agent")

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(req: QueryRequest):
    answer = ask_question(req.question)
    return {
        "question": req.question,
        "answer": answer
    }