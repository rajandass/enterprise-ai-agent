from services.retrieval.vector_search_service import (
    search_similar_chunks
)

results = search_similar_chunks(
    "What are lipids?"
)

print("\n--- SEARCH RESULTS ---\n")

for item in results:

    print(
        f"Concept: "
        f"{item['concept']}"
    )

    print(
        f"Section: "
        f"{item['section']}"
    )

    print()

    print(
        f"Content:\n"
        f"{item['content'][:300]}"
    )

    print("\n" + "=" * 80 + "\n")