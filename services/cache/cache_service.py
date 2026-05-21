import os
import json
import redis

from typing import Optional
from dotenv import load_dotenv
import copy

load_dotenv()


redis_connection_string = os.getenv(
    "REDIS_CONNECTION_STRING"
)

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


def get_cached_response(
    cache_key: str
) -> Optional[dict]:

    """
    Retrieve cached response.
    """

    cached_data = redis_client.get(
        cache_key
    )

    if cached_data:

        return json.loads(
            cached_data
        )

    return None


def set_cached_response(
    cache_key: str,
    response: dict,
    ttl: int = 3600
):

    """
    Store response in cache.
    """

    redis_client.setex(
        cache_key,
        ttl,
        json.dumps(response)
    )

def build_cache_hit_response(
    cached_response: dict,
    latency: float
):

    """
    Build standardized cache hit response
    with correct observability metadata.
    """

    response = copy.deepcopy(
        cached_response
    )

    response["tokens"] = 0
    response["cost"] = 0
    response["latency"] = round(
        latency,
        4
    )
    response["cache_hit"] = True

    return response   