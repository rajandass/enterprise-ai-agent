import os
import logging
import time
import redis
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma

redis_connection_string = os.getenv("REDIS_CONNECTION_STRING")

if redis_connection_string:
    redis_client = redis.from_url(
        redis_connection_string,
        decode_responses=True
    )
else:
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )

logger = logging.getLogger(__name__)

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



def ask_question(query: str):

    query = query.strip().lower()
    cache_key = f"query:{query}"

    cached_response = redis_client.get(cache_key)

    if cached_response:
        logger.warning(f"cache_hit: {query}")

        return {
            "answer": cached_response,
            "source": "redis_cache"
        }

    logger.warning(f"cache_miss: {query}")


    logger.info("ask_question_started")

    start_time = time.time()
    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs]) if docs else "No relevant context found."
    prompt = f"""
    Answer using ONLY the context.

    Context:{context}

    Q:{query}
    A:""".strip()

    if not docs:

        result = {
        "answer": "⚠️ No relevant information found in knowledge base.",
        "confidence": "LOW",
        "tokens": 0,
        "cost": 0.0,
        "latency": 0,
        "citations": []
        }

        return result
    
    response = llm.invoke(prompt)
    answer = response.content

    verification_prompt = f"""
    Check if the answer is fully supported by the context.

    Context:
    {context}

    Answer:
    {answer}

    Respond with ONLY one word:
    - SUPPORTED
    - PARTIALLY_SUPPORTED
    - NOT_SUPPORTED
    """
    verification_response = llm.invoke(verification_prompt).content.strip()

    usage = response.response_metadata.get("token_usage", {})

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    # Approx pricing (gpt-4o-mini)
    cost_per_1k_tokens = 0.00015
    cost = (total_tokens / 1000) * cost_per_1k_tokens
    cost = round(cost, 6)

    if verification_response == "SUPPORTED":
        confidence = "HIGH"
    elif verification_response == "PARTIALLY_SUPPORTED":
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    latency = time.time() - start_time


    logger.info("debug_info_started")
    logger.info(f"Cache MISS")
    logger.warning(f"query_received: {query}")
    logger.info(f"query_latency_seconds: {latency}")
    logger.info(f"Context length: {len(context)} chars")
    logger.info(f"Prompt hash: {hash(prompt)}")

    logger.info("\n💰 TOKEN USAGE")
    logger.info(f"Prompt tokens: {prompt_tokens}")
    logger.info(f"Completion tokens: {completion_tokens}")
    logger.info(f"total_tokens_used: {total_tokens}")
    logger.info(f"Estimated cost: ${cost:.6f}")

    # ✅ Store result
    result = {
        "answer": answer,
        "confidence": confidence,
        "tokens": total_tokens,
        "cost": cost,
        "latency": round(latency, 2),
        "citations": sources
    }

    logger.info("🔥 QUERY FUNCTION EXECUTED")
    logger.info(f"🔥 FINAL RETURN TYPE: {type(result)}")

    redis_client.setex(
    cache_key,
    3600,
    answer
        )
    return result

if __name__ == "__main__":
    question = "How many leave days do employees get?"
    answer = ask_question(question)
    print("\n🤖 Answer:")
    print(answer)