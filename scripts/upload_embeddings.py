import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Azure AI Search Config
SEARCH_ENDPOINT = "https://neet-search-12345.search.windows.net"
INDEX_NAME = "neet-biology-rich-index"
API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

url = (
    f"{SEARCH_ENDPOINT}/indexes/"
    f"{INDEX_NAME}/docs/index"
    f"?api-version=2024-07-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

# Load embedded chunks
with open(
    "embedded_concept_chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

documents = []

for i, chunk in enumerate(chunks):

    documents.append({
        "@search.action": "upload",

        "chunk_id": f"chunk-{i}",

        "document_id": "biomolecules",

        "subject": "Biology",

        "chapter": "Biomolecules",

        "section": chunk["section"],
        "concept": chunk["concept"],

        "content": chunk["content"],

        "embedding": chunk["embedding"]
    })

payload = {
    "value": documents
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("Status Code:", response.status_code)

print("\nResponse:")

print(response.text)