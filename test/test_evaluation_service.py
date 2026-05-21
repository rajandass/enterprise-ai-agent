from services.tutoring.evaluation_service import (
    evaluate_student_answer
)

response = evaluate_student_answer(
    question=(
        "Why are lipids acid insoluble?"
    ),

    student_answer="A",

    correct_answer="B",

    concept="Lipids"
)

print("\n--- ANSWER EVALUATION ---\n")

print(response["evaluation"])