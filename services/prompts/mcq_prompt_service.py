def build_mcq_prompt(
    topic: str,
    context: str,
    difficulty_instruction: str
):

    """
    Build curriculum-grounded MCQ prompt
    for educational assessment generation.
    """

    prompt = f"""
You are an expert NEET Biology examiner.

Generate 5 multiple-choice questions
using ONLY the educational context below.

Rules:
1. Each question must have 4 options.
2. Include correct answer.
3. Keep questions curriculum grounded.
4. Avoid hallucinations.
5. Ensure conceptual clarity.
6. {difficulty_instruction}

Topic:
{topic}

Educational Context:
{context}
""".strip()

    return prompt