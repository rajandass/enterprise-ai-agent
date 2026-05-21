
import logging
import time
from langchain_core.messages import HumanMessage
from services.observability.token_usage_service import (
    calculate_token_usage
)

from services.cache.cache_service import (
    get_cached_response,
    set_cached_response,
    build_cache_hit_response
)
from services.verification.answer_verification_service import (
    verify_grounded_answer
)

from services.prompts.rag_prompt_service import (
    build_rag_prompt
)

from core.config import settings

from services.llm.llm_service import (
    get_llm,
    get_streaming_llm
)

from services.retrieval.chroma_retriever_service import (
    get_retriever
)

logger = logging.getLogger(__name__)

retriever = get_retriever(k=1)

def ask_question(query: str):

    query = query.strip().lower()
    cache_key = f"query:{query}"

    start_time = time.time()
    cached_response = get_cached_response(
        cache_key
    )
    if cached_response:

        logger.warning(
            f"cache_hit: {query}"
        )

        cache_latency = (
            time.time() - start_time
        )

        return build_cache_hit_response(
            cached_response=cached_response,
            latency=cache_latency
        )

    logger.warning(f"cache_miss: {query}")


    logger.info("ask_question_started")

    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs]) if docs else "No relevant context found."
    prompt = build_rag_prompt(
        query=query,
        context=context
    )

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
    
    llm = get_llm()
    response = llm.invoke(prompt)
    answer = response.content

    verification_result = verify_grounded_answer(context, answer)
    confidence = verification_result.get("confidence")

    token_usage = calculate_token_usage(
    response
    )

    prompt_tokens = (
        token_usage["prompt_tokens"]
    )

    completion_tokens = (
        token_usage["completion_tokens"]
    )

    total_tokens = (
        token_usage["total_tokens"]
    )

    cost = (
        token_usage["estimated_cost"]
    )

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
        "citations": sources,
        "cache_hit": False,
    }

    logger.info("🔥 QUERY FUNCTION EXECUTED")
    logger.info(f"🔥 FINAL RETURN TYPE: {type(result)}")

    set_cached_response(
        cache_key,
        result,
        ttl=3600
    )
    return result


def stream_answer(query: str):

    query = query.strip().lower()

    cache_key = f"stream:{query}"

    cached_response = get_cached_response(
        cache_key
    )

    if cached_response:

        logger.warning(
            f"stream_cache_hit: {query}"
        )

        cached_text = cached_response.get(
            "answer",
            ""
        )

        for word in cached_text.split():

            yield word + " "

        return

    logger.warning(
        f"stream_cache_miss: {query}"
    )

    docs = retriever.invoke(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    ) if docs else "No relevant context found."

    prompt = build_rag_prompt(
        query=query,
        context=context
    )

    stream_llm = get_streaming_llm()

    full_response = ""

    for chunk in stream_llm.stream(
        [HumanMessage(content=prompt)]
    ):

        if chunk.content:

            full_response += chunk.content

            yield chunk.content

    set_cached_response(
        cache_key,
        {
            "answer": full_response
        },
        ttl=3600
    )

if __name__ == "__main__":
    question = "How many leave days do employees get?"
    answer = ask_question(question)
    print("\n🤖 Answer:")
    print(answer)
    