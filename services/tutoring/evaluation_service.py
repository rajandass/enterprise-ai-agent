import os

from openai import OpenAI
from dotenv import load_dotenv
import logging

from services.cache.cache_service import (
    get_cached_response,
    set_cached_response
)
logger = logging.getLogger(__name__)
load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME")

TEMPERATURE = float(
    os.getenv("TEMPERATURE")
)


def evaluate_student_answer(
    question: str,
    student_answer: str,
    correct_answer: str,
    concept: str
):

    """
    Evaluate student answer and
    generate educational feedback.
    """
    cache_key = (
        "evaluation:"
        f"{concept.strip().lower()}:"
        f"{question.strip().lower()}:"
        f"{student_answer.strip().lower()}:"
        f"{correct_answer.strip().lower()}"
    )
    
    cached_response = (
        get_cached_response(
            cache_key
        )
    )

    if cached_response:

        logger.info(
            f"evaluation_cache_hit: {concept}"
        )

        return cached_response

    logger.info(
        f"evaluation_cache_miss: {concept}"
    )

    # Prompt
    prompt = f"""
You are an expert NEET Biology tutor.

Evaluate the student's answer.

Question:
{question}

Student Answer:
{student_answer}

Correct Answer:
{correct_answer}

Concept:
{concept}

Instructions:
1. Determine correctness.
2. Explain WHY the answer is correct or incorrect.
3. Detect misconception if present.
4. Provide remediation guidance.
5. Encourage conceptual understanding.
6. Keep explanation educational and clear.
"""

    # LLM Call
    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert "
                    "NEET Biology tutor."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=TEMPERATURE
    )

    evaluation = (
        response
        .choices[0]
        .message
        .content
    )

    # Correctness Logic
    is_correct = (
        student_answer.strip().upper()
        ==
        correct_answer.strip().upper()
    )

    result = {
        "concept": concept,
        "question": question,
        "student_answer": student_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "evaluation": evaluation
    }

    set_cached_response(
        cache_key,
        result,
        ttl=3600
    )

    return result