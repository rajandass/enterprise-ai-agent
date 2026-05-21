import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load concept chunks
with open("concept_chunks.json", "r", encoding="utf-8") as f:
    concept_chunks = json.load(f)

embedded_chunks = []

for chunk in concept_chunks:

    response = client.embeddings.create(
        input=chunk["content"],
        model="text-embedding-3-small"
    )

    embedding = response.data[0].embedding

    chunk["embedding"] = embedding

    embedded_chunks.append(chunk)

print(f"Generated embeddings: {len(embedded_chunks)}")

print("\nEmbedding dimensions:")
print(len(embedded_chunks[0]["embedding"]))

# Save embedded chunks
with open(
    "embedded_concept_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        embedded_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("\nSaved embedded_concept_chunks.json")