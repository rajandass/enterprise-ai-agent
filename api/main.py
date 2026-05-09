import os
import uuid
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from fastapi import Header, HTTPException,Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
import redis
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from services.conversation_service import (
    save_message,
    get_conversation,
    list_conversations,
    create_chat_session,
    generate_title
)



from pipelines.query import (
    ask_question,
    stream_answer
)
from pipelines.ingestion import run_ingestion





connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

if connection_string:
    configure_azure_monitor(
        connection_string=connection_string
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
LoggingInstrumentor().instrument(set_logging_format=True)
logger = logging.getLogger(__name__)
logger.propagate = True


logger.info("application_startup_completed")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Enterprise AI Support Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://enterprise-ai-ui-prod-12345.azurewebsites.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

class QueryRequest(BaseModel):

    query: str
    session_id: str

API_KEY = os.getenv("API_KEY")


@app.on_event("startup")
def startup_event():
    logger.info("running_ingestion")
    run_ingestion()

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/ask")
@limiter.limit("5/minute")
def ask(
    request: Request,
    req: QueryRequest,
    x_api_key: str = Header(
    None,
    alias="X-Api-Key"
            )
):

    if x_api_key != API_KEY:
        raise HTTPException(
        status_code=401,
        detail="Unauthorized"
        )
    request_id = str(uuid.uuid4())
    result = ask_question(req.query)
    session_id = req.session_id

    create_chat_session(
    session_id=session_id,
    title=generate_title(req.query)
    )

    save_message(
        session_id=session_id,
        role="user",
        content=req.query
    )

    save_message(
        session_id=session_id,
        role="assistant",
        content=result["answer"],
        citations=result.get("citations", [])
    )

    logger.info(f"response_type: {type(result)}") 
    return {
        "request_id": request_id,
        **result
    }

@app.post("/ask-stream")
@limiter.limit("5/minute")
def ask_stream(
    request: Request,
    req: QueryRequest,
    x_api_key: str = Header(
    None,
    alias="X-Api-Key"
        )
):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return StreamingResponse(
        stream_answer(req.query),
        media_type="text/plain"
    )


@app.get("/health/live")
def liveness_probe():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness_probe():
    checks = {
        "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
        "api_key": bool(os.getenv("API_KEY")),
        "redis": redis_client.ping()
    }

    all_ready = all(checks.values())

    return {
        "status": "ready" if all_ready else "not_ready",
        "checks": checks
    }

@app.get("/conversations/{session_id}")
def get_conversation_history(
    session_id: str
):
    messages = get_conversation(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }

@app.get("/conversations")
def get_conversations():
    conversations = list_conversations()

    return {
        "conversations": conversations
    }