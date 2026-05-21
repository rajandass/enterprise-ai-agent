import requests
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

SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# Student Question
question = "Explain lipids in simple words"

# STEP 1 — Generate Query Embedding
embedding_response = client.embeddings.create(
    input=question,
    model="text-embedding-3-small"
)

query_vector = embedding_response.data[0].embedding

# STEP 2 — Retrieve Relevant Chunks
search_url = (
    f"{SEARCH_ENDPOINT}/indexes/"
    f"{INDEX_NAME}/docs/search"
    f"?api-version=2024-07-01"
)

headers = {
    "Content-Type": "application/json",
    "api-key": SEARCH_API_KEY
}

payload = {
    "top": 3,

    "select": (
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

search_response = requests.post(
    search_url,
    headers=headers,
    json=payload
)

results = search_response.json()

# STEP 3 — Build Context
context = ""

for doc in results["value"]:

    context += f"""
Concept: {doc['concept']}
Section: {doc['section']}

Content:
{doc['content']}

------------------------
"""

# STEP 4 — Grounded Tutoring Prompt
prompt = f"""
You are an expert NEET Biology tutor.

Answer ONLY using the provided educational context.

Rules:
1. Explain clearly for NEET students.
2. Use simple educational language.
3. Include section references when explaining.
4. Do NOT hallucinate information.
5. If answer is missing from context, say:
   'I could not find this in the textbook context.'

Educational Context:
{context}

Student Question:
{question}
"""

# STEP 5 — Generate Tutoring Response
chat_response = client.chat.completions.create(
    model="gpt-4.1-mini",

    messages=[
        {
            "role": "system",
            "content": "You are a helpful NEET Biology tutor."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.3
)

answer = chat_response.choices[0].message.content

# STEP 6 — Output
print("\n--- RETRIEVED CONTEXT ---\n")

print(context)

print("\n--- TUTOR ANSWER ---\n")

print(answer)