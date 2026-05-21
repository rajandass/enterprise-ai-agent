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

from services.prompts.mcq_prompt_service import (
    build_mcq_prompt
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


def generate_mcqs(
    topic: str,
    difficulty: str = "beginner"
):

    """
    Generate curriculum-grounded MCQs.
    """
    cache_key = (
    f"mcq:{topic.strip().lower()}:{difficulty}"
        )
    cached_response = (
        get_cached_response(
            cache_key
        )
    )

    if cached_response:

        logger.info(
            f"mcq_cache_hit: {topic}"
        )

        return cached_response

    logger.info(
        f"mcq_cache_miss: {topic}"
    )

    # Retrieve Educational Context
    retrieved_chunks = search_similar_chunks(
        topic
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

    # Difficulty Instructions
    if difficulty == "beginner":

        difficulty_instruction = """
Generate simple conceptual MCQs.
Focus on definitions and fundamentals.
"""

    elif difficulty == "advanced":

        difficulty_instruction = """
Generate challenging NEET-style MCQs.
Focus on reasoning and application.
"""

    else:

        difficulty_instruction = """
Generate moderate conceptual MCQs.
"""

    # Prompt
    prompt = build_mcq_prompt(
    topic=topic,
        context=context,
        difficulty_instruction=(
            difficulty_instruction
        )
    )

    # LLM Call
    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert "
                    "NEET Biology examiner."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=TEMPERATURE
    )

    mcqs = (
        response
        .choices[0]
        .message
        .content
    )

    result = {
        "topic": topic,
        "difficulty": difficulty,
        "mcqs": mcqs,
        "sources": retrieved_chunks
    }

    set_cached_response(
        cache_key,
        result,
        ttl=3600
    )

    return result