import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
import time
from functools import lru_cache

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
    query = query.strip().lower()
    if query in cache:
        print("⚡ Cache HIT")
        print(f"Cache size: {len(cache)}")
        return cache[query]


    start_time = time.time()
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs]) if docs else "No relevant context found."
    prompt = f"""
    Answer using ONLY the context.

    Context:{context}

    Q:{query}
    A:""".strip()

    if not docs:
          return "⚠️ No relevant information found in knowledge base."
    
    response = llm.invoke(prompt)
    answer = response.content


    usage = response.response_metadata.get("token_usage", {})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    # Approx pricing (gpt-4o-mini)
    cost_per_1k_tokens = 0.00015
    cost = (total_tokens / 1000) * cost_per_1k_tokens
    cost = round(cost, 6)

    confidence = "HIGH"
    if not docs:
        confidence = "LOW"
    elif total_tokens < 30:
        confidence = "MEDIUM"
    elif "no relevant" in context.lower():
        confidence = "LOW"

    sources = [doc.metadata.get("source", "unknown") for doc in docs]
    
    latency = time.time() - start_time


    print("\n📊 DEBUG INFO")
    print(f"Cache MISS")
    print(f"Query: {query}")
    print(f"Latency: {latency:.2f} sec")
    print(f"Context length: {len(context)} chars")
    print(f"Prompt hash: {hash(prompt)}")

    print("\n💰 TOKEN USAGE")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Estimated cost: ${cost:.6f}")

    # ✅ Store result
    result = {
        "answer": answer,
        "confidence": confidence,
        "tokens": total_tokens,
        "cost": cost,
        "latency": round(latency, 2),
        "sources": sources
    }

    cache[query] = result
    return result

if __name__ == "__main__":
    question = "How many leave days do employees get?"
    answer = ask_question(question)
    print("\n🤖 Answer:")
    print(answer)