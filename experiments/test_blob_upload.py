from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
account_key = os.getenv("AZURE_STORAGE_KEY")
container_name = os.getenv("AZURE_STORAGE_CONTAINER")

connection_string = (
    f"DefaultEndpointsProtocol=https;"
    f"AccountName={account_name};"
    f"AccountKey={account_key};"
    f"EndpointSuffix=core.windows.net"
)

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)

blob_client = container_client.get_blob_client(
    "test-upload.txt"
)

content = b"NEET Biology Learning Assistant Blob Upload Test"

blob_client.upload_blob(content, overwrite=True)

print("Blob upload successful")