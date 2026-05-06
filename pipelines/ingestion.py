import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def run_ingestion():

    # Load document
    loader = TextLoader("data/company_docs.txt")
    documents = loader.load()

    # Split document
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 300,
        chunk_overlap = 50
    )

    docs = text_splitter.split_documents(documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings()

    # Store in vector DB

    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory = "models/vector_db"
    )

    # db.persist()

    print("✅ Ingestion complete. Vector DB created.")

if __name__ == "__main__":
    run_ingestion()