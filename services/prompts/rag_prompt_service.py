def build_rag_prompt(
    query: str,
    context: str
):

    """
    Build grounded RAG prompt
    for enterprise assistant.
    """

    prompt = f"""
Answer using ONLY the context.

Context:
{context}

Q:
{query}

A:
""".strip()

    return prompt