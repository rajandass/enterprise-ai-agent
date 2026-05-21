from services.retrieval.embedding_service import (
    generate_embedding
)

vector = generate_embedding("Lipids")

print(len(vector))