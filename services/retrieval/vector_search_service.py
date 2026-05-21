import os
import requests
from dotenv import load_dotenv

from services.retrieval.embedding_service import (
    generate_embedding
)

load_dotenv()

# Azure AI Search Config
SEARCH_ENDPOINT = os.getenv(
    "AZURE_SEARCH_ENDPOINT"
)
SEARCH_KEY = os.getenv(
    "AZURE_SEARCH_API_KEY"
)
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION")

# Search URL
SEARCH_URL = (
    f"{SEARCH_ENDPOINT}"
    f"/indexes/{INDEX_NAME}"
    f"/docs/search"
    f"?api-version={API_VERSION}"
)


def search_similar_chunks(
    query: str,
    top_k: int = 3
):

    """
    Perform semantic vector search
    against Azure AI Search.
    """

    query_vector = generate_embedding(query)

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    payload = {
        "count": True,

        "select": (
            "concept,section,content"
        ),

        "vectorQueries": [
            {
                "kind": "vector",

                "vector": query_vector,

                "fields": "embedding",

                "k": top_k
            }
        ]
    }

    response = requests.post(
        SEARCH_URL,
        headers=headers,
        json=payload
    )

    print("\n--- STATUS CODE ---\n")
    print(response.status_code)

    print("\n--- RAW RESPONSE ---\n")
    print(response.text)

    results = response.json()

    return results.get("value", [])