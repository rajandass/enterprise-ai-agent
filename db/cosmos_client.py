import os

from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER")
COSMOS_SESSION_CONTAINER =os.getenv("COSMOS_SESSION_CONTAINER")

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
