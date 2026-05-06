from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from pipelines.query  import ask_question

app = FastAPI(title="Enterprise AI Support Agent")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QueryRequest):
    request_id = str(uuid.uuid4())  # ✅ HERE
    result = ask_question(req.question)
    return {
        "request_id": request_id,
        **result
    }