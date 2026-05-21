import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Azure Search Config
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

difficulty = "advanced"

# Topic
topic = "Lipids"

# STEP 1 — Generate Topic Embedding
embedding_response = client.embeddings.create(
    input=topic,
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
    "top": 5,

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

            "k": 5
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

# STEP 4 — MCQ Prompt
prompt = f"""
You are an expert NEET Biology examiner.

Using ONLY the educational context below:

Generate 5 {difficulty}-level NEET Biology MCQs.

Rules:
1. Each question must have 4 options.
2. Mark the correct answer.
3. Keep questions aligned to {difficulty} difficulty.
4. Do NOT hallucinate outside textbook content.
5. Use conceptually accurate biology.

Difficulty Guidelines:

- beginner:
  direct factual questions

- intermediate:
  conceptual understanding questions

- advanced:
  application, reasoning, comparison,
  and tricky NEET-style questions

Educational Context:
{context}
"""

# STEP 5 — Generate MCQs
chat_response = client.chat.completions.create(
    model="gpt-4.1-mini",

    messages=[
        {
            "role": "system",
            "content": (
                "You are a NEET Biology MCQ generator."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.4
)

mcqs = chat_response.choices[0].message.content

# STEP 6 — Output
print("\n--- GENERATED MCQs ---\n")

print(mcqs)