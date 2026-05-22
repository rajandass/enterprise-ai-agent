
import logging
from fastapi import(
    FastAPI
      )
from azure.monitor.opentelemetry import configure_azure_monitor
from fastapi.exceptions import RequestValidationError
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler

import redis
from fastapi.middleware.cors import CORSMiddleware
from pipelines.ingestion import run_ingestion

from api.routes.tutoring_routes import (
    router as tutoring_router
)
from api.routes.quiz_routes import (
    router as quiz_router
)

from api.routes.learning_routes import (
    router as learning_router
)

from api.routes.chat_routes import (
    router as chat_router
)

from api.dependencies.rate_limiter import (
    limiter
)

from core.config import settings

from middleware.exception_handler import (
    global_exception_handler,
    validation_exception_handler
)

from middleware.request_logging_middleware import (
    request_logging_middleware
)

from db.cosmos_client import (
    check_cosmos_health
)
from services.retrieval.vector_search_service import (
    check_search_health
)
from storage.blob_storage_client import (
    check_blob_storage_health
)
from health.startup_validator import (
    validate_dependencies
)

connection_string = (
    settings.APPLICATIONINSIGHTS_CONNECTION_STRING
)

if connection_string:
    configure_azure_monitor(
        connection_string=connection_string
    )

if settings.REDIS_CONNECTION_STRING:
    redis_client = redis.from_url(
        settings.REDIS_CONNECTION_STRING,
        decode_responses=True
    )
else:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
LoggingInstrumentor().instrument(set_logging_format=True)
logger = logging.getLogger(__name__)
logger.propagate = True


logger.info("application_startup_completed")



app = FastAPI(
    title="Enterprise Educational AI Platform",
    version="1.0.0",
    description="Adaptive educational AI platform"
)
app.middleware("http")(request_logging_middleware)
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

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(SlowAPIMiddleware)


# Register Routes
app.include_router(
    tutoring_router,
    prefix="/api/v1",
    tags=["Tutoring"]
)


app.include_router(
    quiz_router,
    prefix="/api/v1",
    tags=["Quiz"]
)

app.include_router(
    learning_router,
    prefix="/api/v1",
    tags=["Learning"]
)

app.include_router(
    chat_router,
    prefix="/api/v1",
    tags=["Enterprise Chat"]
)

ENABLE_INGESTION = (
    settings.ENABLE_INGESTION
)

@app.on_event("startup")
def startup_event():

    logger.info(
        "application_startup"
    )

    dependency_results = (
    validate_dependencies()
    )

    logger.info(
        f"startup_dependency_summary="
        f"{dependency_results}"
    )
    
    if ENABLE_INGESTION:
        logger.info(
            "running_ingestion"
        )
        run_ingestion()

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/health/live")
def liveness_probe():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness_probe():

    checks = {}

    # Redis Check
    try:

        redis_client.ping()

        checks["redis"] = True

    except Exception as ex:

        logger.exception(
            f"redis_readiness_failed: {str(ex)}"
        )

        checks["redis"] = False

    # OpenAI Check
    checks["openai_api_key"] = bool(
        settings.OPENAI_API_KEY
    )

    # Internal API Security
    checks["api_key"] = bool(
        settings.API_KEY
    )

    # Cosmos DB Check
    try:

        checks["cosmos"] = (
            check_cosmos_health()
        )

    except Exception as ex:

        logger.exception(
            f"cosmos_readiness_failed: {str(ex)}"
        )

        checks["cosmos"] = False

    # Azure AI Search Check
    try:

        checks["azure_search"] = (
            check_search_health()
        )

    except Exception as ex:

        logger.exception(
            f"search_readiness_failed: {str(ex)}"
        )

        checks["azure_search"] = False

    # Blob Storage Check
    try:

        checks["storage"] = (
            check_blob_storage_health()
        )

    except Exception as ex:

        logger.exception(
            f"storage_readiness_failed: {str(ex)}"
        )

        checks["storage"] = False


    all_ready = all(
        checks.values()
    )

    return {
        "status": (
            "ready"
            if all_ready
            else "not_ready"
        ),
        "checks": checks
    }

