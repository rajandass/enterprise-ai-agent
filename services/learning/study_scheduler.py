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

# Student Constraints
daily_study_hours = 3

exam_goal = "NEET Biology Preparation"

# Build Weak Concept Summary
weak_summary = ""

for concept, score in weak_concepts.items():

    weak_summary += (
        f"- {concept}: {score} mistakes\n"
    )

# Build Recent Mistakes
history_summary = ""

for quiz in quiz_history[-5:]:

    history_summary += f"""
Concept: {quiz['concept']}
Misconception: {quiz['misconception']}
"""

# Prompt
prompt = f"""
You are an expert NEET study planner.

Create a personalized DAILY study schedule.

Rules:
1. Prioritize weak concepts first.
2. Allocate study time intelligently.
3. Include:
   - concept revision
   - MCQ practice
   - recap/revision
4. Focus on conceptual understanding.
5. Make plan realistic for NEET students.
6. Include motivation and study tips.

Student Goal:
{exam_goal}

Daily Study Hours:
{daily_study_hours}

Weak Concepts:
{weak_summary}

Recent Mistakes:
{history_summary}
"""

# Generate Schedule
response = client.chat.completions.create(
    model="gpt-4.1-mini",

    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert NEET study coach."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ],

    temperature=0.4
)

schedule = response.choices[0].message.content

print("\n--- PERSONALIZED STUDY SCHEDULE ---\n")

print(schedule)