from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SEARCH_SERVICE = "neet-search-12345"
INDEX_NAME = "neet-biology-index"
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

text = "Cells are the basic structural and functional units of life."

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

embedding = response.data[0].embedding

document = {
    "value": [
        {
            "@search.action": "upload",
            "chunk_id": "real-test-chunk-001",
            "document_id": "real-test-doc-001",
            "subject": "Biology",
            "chapter": "Cell: The Unit of Life",
            "topic": "Introduction",
            "source_document": "NCERT Biology",
            "page_number": 1,
            "content": text,
            "embedding": embedding
        }
    ]
}

url = (
    f"https://{SEARCH_SERVICE}.search.windows.net/"
    f"indexes/{INDEX_NAME}/docs/index"
    f"?api-version=2024-07-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": SEARCH_API_KEY
}

result = requests.post(
    url,
    headers=headers,
    json=document
)

print(result.status_code)
print(result.text)