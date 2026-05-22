import os

from azure.cosmos import CosmosClient
from core.config import settings

COSMOS_ENDPOINT = settings.COSMOS_ENDPOINT
COSMOS_KEY = settings.COSMOS_KEY
COSMOS_DATABASE = settings.COSMOS_DATABASE
COSMOS_CONTAINER = settings.COSMOS_CONTAINER
COSMOS_SESSION_CONTAINER = (
    settings.COSMOS_SESSION_CONTAINER
)

client = CosmosClient(
    COSMOS_ENDPOINT,
    credential=COSMOS_KEY
)

database = client.get_database_client(
    COSMOS_DATABASE
)

container = database.get_container_client(
    COSMOS_CONTAINER
)

session_container = database.get_container_client(
    COSMOS_SESSION_CONTAINER
)

def check_cosmos_health():

    """
    Lightweight Cosmos DB
    connectivity validation.
    """

    try:

        database.read()

        return True

    except Exception:

        return False