from services.learning.mastery_service import (
    generate_mastery_report
)

from services.learning.spaced_repetition_service import (
    generate_revision_queue
)


def generate_student_dashboard(
    student_memory
):

    """
    Generate complete student
    learning dashboard.
    """

    quiz_history = (
        student_memory["quiz_history"]
    )

    # Mastery Analytics
    mastery_report = (
        generate_mastery_report(
            quiz_history
        )
    )

    # Revision Queue
    revision_queue = (
        generate_revision_queue(
            quiz_history
        )
    )

    # Overall Metrics
    total_questions = 0
    total_correct = 0

    for quiz in quiz_history:

        total_questions += 1

        if quiz["is_correct"]:

            total_correct += 1

    # Accuracy
    if total_questions > 0:

        overall_accuracy = (
            total_correct
            /
            total_questions
        ) * 100

    else:

        overall_accuracy = 0

    # Readiness Classification
    if overall_accuracy >= 80:

        readiness = (
            "High NEET Readiness"
        )

    elif overall_accuracy >= 50:

        readiness = (
            "Moderate NEET Readiness"
        )

    else:

        readiness = (
            "Needs Improvement"
        )

    # Weak Concepts
    weak_concepts = []

    for concept, data in (
        mastery_report.items()
    ):

        if data["mastery"] == "Weak":

            weak_concepts.append(
                concept
            )

    return {

        "overall_accuracy": round(
            overall_accuracy,
            2
        ),

        "readiness": readiness,

        "mastery_report":
            mastery_report,

        "revision_queue":
            revision_queue,

        "weak_concepts":
            weak_concepts,

        "total_questions":
            total_questions,

        "total_correct":
            total_correct
    }