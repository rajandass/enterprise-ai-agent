def build_verification_prompt(
    context: str,
    answer: str
):

    """
    Build grounding verification prompt
    for AI answer validation.
    """

    prompt = f"""
Check if the answer is fully supported by the context.

Context:
{context}

Answer:
{answer}

Respond with ONLY one word:
- SUPPORTED
- PARTIALLY_SUPPORTED
- NOT_SUPPORTED
""".strip()

    return prompt