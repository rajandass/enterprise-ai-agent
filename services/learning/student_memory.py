import json
import os
from datetime import datetime

MEMORY_FILE = "student_progress.json"

# Load Existing Memory
if os.path.exists(MEMORY_FILE):

    with open(MEMORY_FILE, "r") as f:
        student_memory = json.load(f)

else:

    student_memory = {
        "student_name": "Demo Student",
        "weak_concepts": {},
        "quiz_history": []
    }

# Example Quiz Result
quiz_result = {
    "timestamp": str(datetime.now()),

    "concept": "Lipids",

    "question": (
        "Why are lipids acid insoluble?"
    ),

    "student_answer": "A",

    "correct_answer": "B",

    "is_correct": False,

    "misconception": (
        "Confused aggregation with polymerization"
    )
}

# Save Quiz History
student_memory["quiz_history"].append(
    quiz_result
)

# Update Weak Concepts
concept = quiz_result["concept"]

if not quiz_result["is_correct"]:

    if concept not in student_memory["weak_concepts"]:

        student_memory["weak_concepts"][concept] = 0

    student_memory["weak_concepts"][concept] += 1

# Save Memory
with open(MEMORY_FILE, "w") as f:

    json.dump(
        student_memory,
        f,
        indent=2
    )

print("\n--- STUDENT MEMORY UPDATED ---\n")

print(json.dumps(student_memory, indent=2))