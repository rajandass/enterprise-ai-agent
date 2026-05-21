import json

from services.learning.spaced_repetition_service import (
    generate_revision_queue
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

# Generate Revision Queue
queue = generate_revision_queue(
    quiz_history
)

print(
    "\n--- REVISION QUEUE ---\n"
)

for item in queue:

    print(
        f"Concept: "
        f"{item['concept']}"
    )

    print(
        f"Next Revision: "
        f"{item['next_revision']}"
    )

    print(
        f"Priority: "
        f"{item['priority']}"
    )

    print("-" * 50)