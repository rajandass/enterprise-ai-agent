import json

from services.learning.dashboard_service import (
    generate_student_dashboard
)

# Load Student Memory
with open(
    "student_progress.json",
    "r"
) as f:

    student_memory = json.load(f)

# Generate Dashboard
dashboard = (
    generate_student_dashboard(
        student_memory
    )
)

print(
    "\n--- STUDENT DASHBOARD ---\n"
)

print(
    f"Overall Accuracy: "
    f"{dashboard['overall_accuracy']}%"
)

print(
    f"Readiness: "
    f"{dashboard['readiness']}"
)

print(
    f"Weak Concepts: "
    f"{dashboard['weak_concepts']}"
)

print()

print(
    "--- REVISION QUEUE ---"
)

for item in (
    dashboard["revision_queue"]
):

    print()

    print(
        f"Concept: "
        f"{item['concept']}"
    )

    print(
        f"Priority: "
        f"{item['priority']}"
    )