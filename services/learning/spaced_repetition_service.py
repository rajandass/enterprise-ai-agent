from datetime import (
    datetime,
    timedelta
)


def generate_revision_queue(
    quiz_history
):

    """
    Generate spaced repetition
    revision queue.
    """

    today = datetime.now()

    revision_queue = []

    # Analyze Quiz History
    for quiz in quiz_history:

        concept = quiz["concept"]

        is_correct = (
            quiz["is_correct"]
        )

        timestamp = datetime.strptime(
            quiz["timestamp"],
            "%Y-%m-%d %H:%M:%S.%f"
        )

        # Revision Logic
        if is_correct:

            revision_days = 7

            priority = "Medium"

        else:

            revision_days = 1

            priority = "High"

        next_revision = (
            timestamp
            +
            timedelta(days=revision_days)
        )

        # Add Due Revisions
        if next_revision <= today:

            revision_queue.append({

                "concept": concept,

                "next_revision":
                    str(next_revision),

                "priority": priority,

                "is_correct":
                    is_correct
            })

    # Remove Duplicates
    unique_revisions = {}

    for item in revision_queue:

        concept = item["concept"]

        if concept not in (
            unique_revisions
        ):

            unique_revisions[
                concept
            ] = item

    return list(
        unique_revisions.values()
    )