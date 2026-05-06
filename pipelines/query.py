import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import time

load_dotenv()

def ask_question(query: str):
    start_time = time.time()
    # Load vector DB
    embeddings = OpenAIEmbeddings()
    db = Chroma(
        persist_directory = "models/vector_db",
        embedding_function = embeddings
    )

    # Retrieve relevant docs
    retriever = db.as_retriever(search_kwargs={"k": 2})
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    # LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = f"""
    You are an enterprise assistant.
    Answer ONLY from the context below.

    Context:
    {context}

    Question:
    {query}
    """
    response =  llm .invoke(prompt)
    end_time = time.time()
    latency = end_time - start_time
    
    print("\n📊 DEBUG INFO")
    print(f"Query: {query}")
    print(f"Latency: {latency:.2f} sec")
    print(f"Context length: {len(context)} chars")


    return response.content

if __name__ == "__main__":
    question = "How many leave days do employees get?"
    answer = ask_question(question)
    print("\n🤖 Answer:")
    print(answer)