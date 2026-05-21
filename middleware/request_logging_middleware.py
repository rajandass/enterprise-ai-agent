import time
import uuid
import logging

from fastapi import Request


logger = logging.getLogger(__name__)


async def request_logging_middleware(
    request: Request,
    call_next
):

    """
    Middleware for request tracing
    and latency logging.
    """

    request_id = str(uuid.uuid4())

    start_time = time.time()

    logger.info(
        f"request_started "
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path}"
    )

    response = await call_next(request)

    latency = round(
        time.time() - start_time,
        4
    )

    logger.info(
        f"request_completed "
        f"request_id={request_id} "
        f"status_code={response.status_code} "
        f"latency={latency}s"
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response