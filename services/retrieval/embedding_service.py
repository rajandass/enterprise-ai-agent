import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Default Embedding Model
EMBEDDING_MODEL = "text-embedding-3-small"


def generate_embedding(text: str):

    """
    Generate embedding vector
    for input text.
    """

    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL
    )

    embedding = response.data[0].embedding

    return embedding

