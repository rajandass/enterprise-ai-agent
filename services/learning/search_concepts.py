import requests
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Azure AI Search Config
SEARCH_ENDPOINT = "https://neet-search-12345.search.windows.net"

INDEX_NAME = "neet-biology-rich-index"

API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# User Query
query = "What are lipids?"

# Step 1 — Generate Query Embedding
embedding_response = client.embeddings.create(
    input=query,
    model="text-embedding-3-small"
)

query_vector = embedding_response.data[0].embedding

# Step 2 — Azure Vector Search
url = (
    f"{SEARCH_ENDPOINT}/indexes/"
    f"{INDEX_NAME}/docs/search"
    f"?api-version=2024-07-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

payload = {
    "count": True,

    "select": (
        "chunk_id,"
        "chapter,"
        "section,"
        "concept,"
        "content"
    ),

    "vectorQueries": [
        {
            "kind": "vector",

            "vector": query_vector,

            "fields": "embedding",

            "k": 3
        }
    ]
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

results = response.json()

print("\n--- SEARCH RESULTS ---\n")

for doc in results["value"]:

    print("Concept:", doc.get("concept"))

    print("Section:", doc.get("section"))

    print("\nContent:\n")

    print(doc.get("content"))

    print("\n" + "=" * 80 + "\n")