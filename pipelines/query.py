import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import time

load_dotenv()

# ✅ Load once (critical optimization)
embeddings = OpenAIEmbeddings()
# Load vector DB

db = Chroma(
    persist_directory = "models/vector_db",
    embedding_function = embeddings
)

# Retrieve relevant docs
retriever = db.as_retriever(search_kwargs={"k": 1})

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0 , max_tokens=100)
cache = {}

def ask_question(query: str):
    if query in cache:
        print("⚡ Cache hit")
        return cache[query]

    start_time = time.time()
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""
    Answer the question using ONLY the context.

    Context:
    {context}

    Q:{query}
    A:
    """
    response =  llm .invoke(prompt)
    cache[query] = response.content

    latency = time.time() - start_time


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