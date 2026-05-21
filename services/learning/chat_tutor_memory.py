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
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

# Conversation Memory
conversation_history = []

print("\nNEET Biology Tutor Started")
print("Type 'exit' to stop.\n")

while True:

    # Student Question
    question = input("Student: ")

    if question.lower() == "exit":
        break

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

    # STEP 4 — Build Conversation Messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert NEET Biology tutor. "
                "Answer only from provided textbook context. "
                "Use simple educational explanations. "
                "Include section references when possible."
            )
        }
    ]

    # Add Previous Conversation
    messages.extend(conversation_history)

    # Add Current Question + Context
    messages.append({
        "role": "user",
        "content": f"""
Educational Context:
{context}

Student Question:
{question}
"""
    })

    # STEP 5 — Generate Tutor Response
    chat_response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=messages,

        temperature=0.3
    )

    answer = chat_response.choices[0].message.content

    # STEP 6 — Print Answer
    print("\nTutor:\n")

    print(answer)

    print("\n" + "=" * 80 + "\n")

    # STEP 7 — Save Memory
    conversation_history.append({
        "role": "user",
        "content": question
    })

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    # Optional Memory Limit
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]