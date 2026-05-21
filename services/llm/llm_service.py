from langchain_openai import ChatOpenAI

from core.config import settings


def get_llm():

    """
    Return standard synchronous LLM.
    """

    return ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=500
    )


def get_streaming_llm():

    """
    Return streaming-enabled LLM.
    """

    return ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        streaming=True
    )