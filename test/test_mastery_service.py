import json

from services.learning.mastery_service import (
    generate_mastery_report
)

# Load Student Memory
with open(
    "student_progress.json",
    "r"
) as f:

    student_memory = json.load(f)

quiz_history = (
    student_memory["quiz_history"]
)

# Generate Report
report = generate_mastery_report(
    quiz_history
)

print(
    "\n--- MASTERY REPORT ---\n"
)

for concept, data in report.items():

    print(f"Concept: {concept}")

    print(
        f"Accuracy: "
        f"{data['accuracy']}%"
    )

    print(
        f"Mastery: "
        f"{data['mastery']}"
    )

    print(
        f"Attempts: "
        f"{data['attempts']}"
    )

    print(
        f"Correct: "
        f"{data['correct']}"
    )

    print(
        f"Wrong: "
        f"{data['wrong']}"
    )

    print("-" * 50)