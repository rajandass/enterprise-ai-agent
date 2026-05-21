from langchain_openai import (
    OpenAIEmbeddings
)

from langchain_chroma import Chroma


# Load embeddings once
embeddings = OpenAIEmbeddings()


# Shared vector DB
db = Chroma(
    persist_directory="models/vector_db",
    embedding_function=embeddings
)


def get_retriever(
    k: int = 1
):

    """
    Return shared retriever instance.
    """

    return db.as_retriever(
        search_kwargs={"k": k}
    )