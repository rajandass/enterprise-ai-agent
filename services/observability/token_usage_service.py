
def calculate_token_usage(
    response,
    cost_per_1k_tokens: float = 0.00015
):

    """
    Extract token usage and
    estimate OpenAI cost.
    """

    usage = (
        response
        .response_metadata
        .get("token_usage", {})
    )

    prompt_tokens = usage.get(
        "prompt_tokens",
        0
    )

    completion_tokens = usage.get(
        "completion_tokens",
        0
    )

    total_tokens = usage.get(
        "total_tokens",
        0
    )

    estimated_cost = (
        total_tokens / 1000
    ) * cost_per_1k_tokens

    estimated_cost = round(
        estimated_cost,
        6
    )

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": estimated_cost
    }