import json
from datetime import datetime, timedelta

# Load Student Memory
with open("student_progress.json", "r") as f:

    student_memory = json.load(f)

quiz_history = student_memory["quiz_history"]

# Current Date
today = datetime.now()

# Revision Queue
revision_queue = []

# Analyze Weak Concepts
for quiz in quiz_history:

    concept = quiz["concept"]

    is_correct = quiz["is_correct"]

    timestamp = datetime.strptime(
        quiz["timestamp"],
        "%Y-%m-%d %H:%M:%S.%f"
    )

    # Spaced Repetition Logic
    if is_correct:

        revision_days = 7

    else:

        revision_days = 1

    next_revision = (
        timestamp +
        timedelta(days=revision_days)
    )

    # Add Due Concepts
    if next_revision <= today:

        revision_queue.append({
            "concept": concept,
            "next_revision": str(next_revision),
            "priority": (
                "High"
                if not is_correct
                else "Medium"
            )
        })

# Remove Duplicate Concepts
unique_revisions = {}

for item in revision_queue:

    concept = item["concept"]

    if concept not in unique_revisions:

        unique_revisions[concept] = item

# Print Revision Schedule
print("\n--- SPACED REPETITION QUEUE ---\n")

for concept, item in unique_revisions.items():

    print(f"Concept: {concept}")

    print(
        f"Next Revision: "
        f"{item['next_revision']}"
    )

    print(
        f"Priority: "
        f"{item['priority']}"
    )

    print("-" * 50)