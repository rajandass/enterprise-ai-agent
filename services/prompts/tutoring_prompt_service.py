def build_tutoring_prompt(
    student_question: str,
    context: str
):

    """
    Build grounded tutoring prompt
    for educational assistance.
    """

    prompt = f"""
You are an expert NEET Biology tutor.

Answer the student's question using ONLY
the educational context below.

Rules:
1. Be educational and clear.
2. Explain concepts simply.
3. Avoid hallucinations.
4. Stay grounded in curriculum context.
5. Encourage conceptual understanding.

Student Question:
{student_question}

Educational Context:
{context}
""".strip()

    return prompt