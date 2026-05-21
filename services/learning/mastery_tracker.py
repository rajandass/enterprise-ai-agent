import json
from collections import defaultdict

# Load Student Memory
with open("student_progress.json", "r") as f:

    student_memory = json.load(f)

quiz_history = student_memory["quiz_history"]

# Concept Statistics
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

        concept_stats[concept]["correct"] += 1

    else:

        concept_stats[concept]["wrong"] += 1

# Compute Mastery Scores
mastery_report = {}

for concept, stats in concept_stats.items():

    total = (
        stats["correct"] +
        stats["wrong"]
    )

    accuracy = (
        stats["correct"] / total
    ) * 100

    # Mastery Classification
    if accuracy >= 80:
        level = "Strong"

    elif accuracy >= 50:
        level = "Moderate"

    else:
        level = "Weak"

    mastery_report[concept] = {
        "accuracy": round(accuracy, 2),
        "level": level,
        "attempts": total
    }

# Print Report
print("\n--- STUDENT MASTERY REPORT ---\n")

for concept, report in mastery_report.items():

    print(f"Concept: {concept}")

    print(
        f"Accuracy: "
        f"{report['accuracy']}%"
    )

    print(
        f"Mastery Level: "
        f"{report['level']}"
    )

    print(
        f"Attempts: "
        f"{report['attempts']}"
    )

    print("-" * 50)