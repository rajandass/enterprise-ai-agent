import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load Student Memory
with open("student_progress.json", "r") as f:

    student_memory = json.load(f)

weak_concepts = student_memory["weak_concepts"]

quiz_history = student_memory["quiz_history"]

# Build Weak Concept Summary
weak_summary = ""

for concept, score in weak_concepts.items():

    weak_summary += (
        f"- {concept}: {score} mistakes\n"
    )

# Build Quiz History Summary
history_summary = ""

for quiz in quiz_history[-5:]:

    history_summary += f"""
Concept: {quiz['concept']}
Question: {quiz['question']}
Misconception: {quiz['misconception']}
"""

# Prompt
prompt = f"""
You are an expert NEET Biology study coach.

Analyze the student's weak concepts and
generate a personalized revision plan.

Rules:
1. Prioritize weakest concepts first.
2. Explain WHY revision is needed.
3. Suggest conceptual focus areas.
4. Recommend learning sequence.
5. Keep advice practical for NEET preparation.
6. Encourage conceptual understanding.

Weak Concepts:
{weak_summary}

Recent Mistakes:
{history_summary}
"""

# Generate Revision Plan
response = client.chat.completions.create(
    model="gpt-4.1-mini",

    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert NEET revision coach."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.4
)

plan = response.choices[0].message.content

print("\n--- PERSONALIZED REVISION PLAN ---\n")

print(plan)