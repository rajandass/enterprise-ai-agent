from azure.storage.blob import (
    BlobServiceClient
)

from core.config import settings


connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={settings.AZURE_STORAGE_ACCOUNT};"
    f"AccountKey={settings.AZURE_STORAGE_KEY};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = (
    BlobServiceClient.from_connection_string(
        connection_string
    )
)

container_client = (
    blob_service_client.get_container_client(
        settings.AZURE_STORAGE_CONTAINER
    )
)


def check_blob_storage_health():

    """
    Lightweight Blob Storage
    readiness validation.
    """

    try:

        container_client.get_container_properties()

        return True

    except Exception:

        return False