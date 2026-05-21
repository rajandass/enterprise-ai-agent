import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

SEARCH_ENDPOINT = "https://neet-search-12345.search.windows.net"

INDEX_NAME = "neet-biology-rich-index"

API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

url = (
    f"{SEARCH_ENDPOINT}/indexes/"
    f"{INDEX_NAME}"
    f"?api-version=2024-07-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

index_schema = {
    "name": INDEX_NAME,

    "fields": [

        {
            "name": "chunk_id",
            "type": "Edm.String",
            "key": True,
            "searchable": False
        },

        {
            "name": "document_id",
            "type": "Edm.String",
            "searchable": False,
            "filterable": True
        },

        {
            "name": "subject",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True
        },

        {
            "name": "chapter",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True
        },

        {
            "name": "section",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True
        },

        {
            "name": "concept",
            "type": "Edm.String",
            "searchable": True,
            "filterable": True
        },

        {
            "name": "content",
            "type": "Edm.String",
            "searchable": True
        },

        {
            "name": "embedding",
            "type": "Collection(Edm.Single)",
            "searchable": True,
            "dimensions": 1536,
            "vectorSearchProfile": "vector-profile"
        }
    ],

    "vectorSearch": {
        "algorithms": [
            {
                "name": "hnsw-config",
                "kind": "hnsw"
            }
        ],

        "profiles": [
            {
                "name": "vector-profile",
                "algorithm": "hnsw-config"
            }
        ]
    }
}

response = requests.put(
    url,
    headers=headers,
    data=json.dumps(index_schema)
)

print("Status Code:", response.status_code)

print("\nResponse:")

print(response.text)