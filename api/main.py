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


import pipelines.query
from pipelines.query  import ask_question
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

logger.info(f"query_module_loaded: {pipelines.query.__file__}")
logger.info("application_startup_completed")

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Enterprise AI Support Agent")

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

class QueryRequest(BaseModel):

    query: str
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
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(
        status_code=401,
        detail="Unauthorized"
        )
    request_id = str(uuid.uuid4())  # ✅ HERE
    result = ask_question(req.query)

    logger.info(f"response_type: {type(result)}") 
    return {
        "request_id": request_id,
        **result
    }

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