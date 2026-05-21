
import os

from openai import OpenAI
from dotenv import load_dotenv
from services.prompts.verification_prompt_service import (
    build_verification_prompt
)

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME")

TEMPERATURE = float(
    os.getenv("TEMPERATURE")
)


def verify_grounded_answer(
    context: str,
    answer: str
):

    """
    Verify whether generated answer
    is grounded in retrieved context.
    """
    verification_prompt = (
    build_verification_prompt(
        context=context,
        answer=answer
        )
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You verify whether AI answers "
                    "are grounded in provided context."
                )
            },
            {
                "role": "user",
                "content": verification_prompt
            }
        ],

        temperature=TEMPERATURE
    )

    verification_result = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    if verification_result == "SUPPORTED":

        confidence = "HIGH"

    elif verification_result == (
        "PARTIALLY_SUPPORTED"
    ):

        confidence = "MEDIUM"

    else:

        confidence = "LOW"

    return {
        "verification": verification_result,
        "confidence": confidence
    }

