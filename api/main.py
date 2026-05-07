import os
import uuid
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter

import pipelines.query

from pipelines.query  import ask_question
from pipelines.ingestion import run_ingestion

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    configure_azure_monitor(
        connection_string=connection_string
    )
    logger_provider = LoggerProvider()

    log_exporter = AzureMonitorLogExporter(
        connection_string=connection_string
    )

    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(log_exporter)
    )

    handler = LoggingHandler(
        level=logging.INFO,
        logger_provider=logger_provider
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
LoggingInstrumentor().instrument(set_logging_format=True)
logger = logging.getLogger(__name__)
logger.propagate = True
logger.info(f"query_module_loaded: {pipelines.query.__file__}")
logger.info("application_startup_completed")


app = FastAPI(title="Enterprise AI Support Agent")

class QueryRequest(BaseModel):
    query: str

@app.on_event("startup")
def startup_event():
    logger.info("running_ingestion")
    run_ingestion()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/ask")
def ask(req: QueryRequest):
    request_id = str(uuid.uuid4())  # ✅ HERE
    result = ask_question(req.query)

    logger.info(f"response_type: {type(result)}") 
    return {
        "request_id": request_id,
        **result
    }