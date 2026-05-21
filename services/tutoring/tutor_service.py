import os

from openai import OpenAI
from dotenv import load_dotenv

from services.retrieval.vector_search_service import (
    search_similar_chunks
)
import logging

from services.cache.cache_service import (
    get_cached_response,
    set_cached_response
)
from services.prompts.tutoring_prompt_service import (
    build_tutoring_prompt
)

logger = logging.getLogger(__name__)
load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME")


def generate_tutor_response(
    student_question: str
):

    """
    Generate grounded educational
    tutoring response.
    """
    cache_key = (
    f"tutor:{student_question.strip().lower()}"
        )
    cached_response = (
        get_cached_response(
                    cache_key
                )
        )

    if cached_response:

        logger.info(
            f"tutor_cache_hit: {student_question}"
        )

        return cached_response

    logger.info(
        f"tutor_cache_miss: {student_question}"
    )
    
    # Retrieve Context
    retrieved_chunks = search_similar_chunks(
        student_question
    )

    # Build Context
    context = ""

    for chunk in retrieved_chunks:

        context += f"""
Concept: {chunk['concept']}
Section: {chunk['section']}

Content:
{chunk['content']}

------------------------
"""

    # Prompt
    prompt = build_tutoring_prompt(
    student_question=student_question,
    context=context
    )

    # Generate Response
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

        temperature=float(os.getenv("TEMPERATURE"))
    )

    tutor_answer = (
        response
        .choices[0]
        .message
        .content
    )

    result = {
        "question": student_question,
        "answer": tutor_answer,
        "sources": retrieved_chunks
    }

    set_cached_response(
        cache_key,
        result,
        ttl=3600
    )

    return result