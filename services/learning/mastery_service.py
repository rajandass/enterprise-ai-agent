from collections import defaultdict


def generate_mastery_report(
    quiz_history
):

    """
    Generate concept mastery analytics
    from quiz history.
    """

    concept_stats = defaultdict(
        lambda: {
            "correct": 0,
            "wrong": 0
        }
    )

    # Analyze Quiz History
    for quiz in quiz_history:

        concept = quiz["concept"]

        if quiz["is_correct"]:

            concept_stats[concept][
                "correct"
            ] += 1

        else:

            concept_stats[concept][
                "wrong"
            ] += 1

    # Build Report
    mastery_report = {}

    for concept, stats in (
        concept_stats.items()
    ):

        total_attempts = (
            stats["correct"]
            +
            stats["wrong"]
        )

        accuracy = (
            stats["correct"]
            / total_attempts
        ) * 100

        # Mastery Classification
        if accuracy >= 80:

            mastery = "Strong"

        elif accuracy >= 50:

            mastery = "Moderate"

        else:

            mastery = "Weak"

        mastery_report[concept] = {

            "accuracy": round(
                accuracy,
                2
            ),

            "mastery": mastery,

            "attempts": total_attempts,

            "correct": stats["correct"],

            "wrong": stats["wrong"]
        }

    return mastery_report