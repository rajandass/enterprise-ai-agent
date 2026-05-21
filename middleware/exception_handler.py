import uuid
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import (
    RequestValidationError
)

logger = logging.getLogger(__name__)


async def global_exception_handler(
    request: Request,
    exc: Exception
):

    """
    Global exception handler for
    standardized API errors.
    """

    request_id = str(uuid.uuid4())

    logger.exception(
        f"Unhandled exception "
        f"request_id={request_id}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "type": "internal_server_error",
                "message": (
                    "An unexpected error occurred."
                ),
                "request_id": request_id
            }
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    """
    Standardized validation
    error response handler.
    """

    request_id = str(uuid.uuid4())

    errors = []

    for error in exc.errors():

        errors.append({
            "field": ".".join(
                map(str, error["loc"])
            ),
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "request_id": request_id,
            "error": {
                "type": "validation_error",
                "message": (
                    "Request validation failed."
                ),
                "details": errors
            }
        }
    )