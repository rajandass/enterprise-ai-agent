from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Cells are the basic structural and functional units of life."
)

embedding = response.data[0].embedding

print(f"Embedding dimensions: {len(embedding)}")