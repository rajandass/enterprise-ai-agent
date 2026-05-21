import json
from collections import defaultdict

# Load Student Memory
with open("student_progress.json", "r") as f:

    student_memory = json.load(f)

quiz_history = student_memory["quiz_history"]

# Statistics
concept_stats = defaultdict(
    lambda: {
        "correct": 0,
        "wrong": 0
    }
)

# Analyze Quiz Data
for quiz in quiz_history:

    concept = quiz["concept"]

    if quiz["is_correct"]:

        concept_stats[concept]["correct"] += 1

    else:

        concept_stats[concept]["wrong"] += 1

# Generate Dashboard
print("\n=== STUDENT PERFORMANCE DASHBOARD ===\n")

total_questions = 0
total_correct = 0

for concept, stats in concept_stats.items():

    attempts = (
        stats["correct"] +
        stats["wrong"]
    )

    accuracy = (
        stats["correct"] / attempts
    ) * 100

    total_questions += attempts
    total_correct += stats["correct"]

    # Mastery Level
    if accuracy >= 80:
        mastery = "Strong"

    elif accuracy >= 50:
        mastery = "Moderate"

    else:
        mastery = "Weak"

    print(f"Concept: {concept}")

    print(f"Attempts: {attempts}")

    print(
        f"Accuracy: "
        f"{round(accuracy, 2)}%"
    )

    print(f"Mastery: {mastery}")

    # Recommendation
    if mastery == "Weak":

        print(
            "Recommendation: "
            "High-priority revision needed."
        )

    elif mastery == "Moderate":

        print(
            "Recommendation: "
            "Continue MCQ practice."
        )

    else:

        print(
            "Recommendation: "
            "Maintain through revision."
        )

    print("-" * 50)

# Overall Performance
overall_accuracy = (
    total_correct / total_questions
) * 100

print("\n=== OVERALL PERFORMANCE ===\n")

print(
    f"Overall Accuracy: "
    f"{round(overall_accuracy, 2)}%"
)

# Readiness Estimation
if overall_accuracy >= 80:

    readiness = "High NEET Readiness"

elif overall_accuracy >= 50:

    readiness = "Moderate NEET Readiness"

else:

    readiness = "Needs Significant Improvement"

print(f"Readiness Level: {readiness}")