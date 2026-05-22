import logging

from db.cosmos_client import (
    check_cosmos_health
)

from services.retrieval.vector_search_service import (
    check_search_health
)

from storage.blob_storage_client import (
    check_blob_storage_health
)

logger = logging.getLogger(__name__)


def validate_dependencies():

    """
    Validate critical application
    dependencies during startup.
    """

    checks = {
        "cosmos": check_cosmos_health,
        "azure_search": check_search_health,
        "blob_storage": check_blob_storage_health
    }

    results = {}

    for name, validator in checks.items():

        try:

            healthy = validator()

            results[name] = healthy

            logger.info(
                f"startup_dependency_check "
                f"{name}="
                f"{'healthy' if healthy else 'failed'}"
            )

        except Exception as ex:

            results[name] = False

            logger.exception(
                f"startup_dependency_exception "
                f"{name}={str(ex)}"
            )

    return results