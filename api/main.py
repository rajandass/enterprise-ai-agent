import os
import uuid
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from azure.monitor.opentelemetry import configure_azure_monitor

import pipelines.query
print("🔥 IMPORTED FROM:", pipelines.query.__file__)
from pipelines.query  import ask_question
from pipelines.ingestion import run_ingestion

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    configure_azure_monitor(
        connection_string=connection_string
    )
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
app = FastAPI(title="Enterprise AI Support Agent")

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
def startup_event():
    print("🚀 Running ingestion...")
    run_ingestion()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QueryRequest):
    request_id = str(uuid.uuid4())  # ✅ HERE
    result = ask_question(req.query)

    print("DEBUG TYPE:", type(result))  # 🔥 ADD THIS
    return {
        "request_id": request_id,
        **result
    }