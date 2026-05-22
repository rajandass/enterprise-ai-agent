import os
import requests

from services.retrieval.embedding_service import (
    generate_embedding
)

from core.config import settings

SEARCH_ENDPOINT = (
    settings.AZURE_SEARCH_ENDPOINT
)

SEARCH_KEY = (
    settings.AZURE_SEARCH_API_KEY
)

INDEX_NAME = (
    settings.AZURE_SEARCH_INDEX_NAME
)

API_VERSION = (
    settings.AZURE_SEARCH_API_VERSION
)

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
        json=payload,
        timeout=10
    )
    results = response.json()

    return results.get("value", [])

def check_search_health():

    """
    Lightweight Azure AI Search
    connectivity validation.
    """

    try:

        headers = {
            "api-key": SEARCH_KEY
        }

        response = requests.get(
            (
                f"{SEARCH_ENDPOINT}"
                f"/indexes/{INDEX_NAME}"
                f"?api-version={API_VERSION}"
            ),
            headers=headers,
            timeout=5
        )

        return response.status_code == 200

    except Exception:

        return False